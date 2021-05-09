import json
import os
import sys
import time
import uuid
from datetime import datetime

import boto3
import FanTaskStatus
from DynamoDB import DynamoDB
from FanEvent import *
from FanEventPublisher import FanEventPublisher
from TaskRecord import TaskRecord
from NamedTupleBase import FanJob

db_table = os.environ.get("TABLE_NAME", "")
if db_table == "":
    raise ValueError(f"Missing env variable for TABLE_NAME")
dynamodb = DynamoDB(db_table, "pk")
seconds_in_24_hours = 60 * 60 * 24
dynamodb.set_ttl_seconds(seconds_in_24_hours)

EVENT_SOUCRE = os.environ.get("AWS_LAMBDA_FUNCTION_NAME", "lambda")

handler_sns_topic_arn = os.environ.get("HANDLER_SNS_TOPIC_ARN", "")
if handler_sns_topic_arn == "":
    raise ValueError(f"Missing env variable for HANDLER_SNS_TOPIC_ARN")
publisher = FanEventPublisher(EVENT_SOUCRE, handler_sns_topic_arn)


def lambda_handler(event, context):
    print(f"Started at {datetime.now()}")

    results = {}
    results["table_name"] = db_table
    fan_out_list = []
    task_started = []

    print(json.dumps(event, indent=3, default=str))
    for count, record in enumerate(event["Records"]):
        event_name = record["Sns"]["MessageAttributes"]["event_name"]["Value"]
        print(f"Record #{count}: {event_name}")
        if event_name == FAN_OUT:
            created_job = process_fan_out(record["Sns"]["Message"])
            fan_out_list.append(created_job.json())
        if event_name == TASK_STARTED:
            raise (ValueError("Haven't implemented process_task_started yet"))
            created_job = process_task_started(record["Sns"]["Message"])
            fan_out_list.append(created_job.json())
        else:
            print(f"Skipping event_name: {event_name}")

    results["fan_out"] = fan_out_list

    print(json.dumps(results, indent=3, default=str))

    print(f"Finished at {datetime.now()}")

    return results


def process_fan_out(sns_message_json):
    fan_event = FanEvent(record_string=sns_message_json)
    task_json = fan_event.message
    task = TaskRecord(
        process_id=task_json["process_id"],
        process_name=task_json["process_name"],
        task_name=task_json["task_name"],
        task_message=task_json["task_message"],
    )
    task.timestamp = datetime.now().isoformat()
    task.pk = f"PROCESS#{task.process_id}"
    task.status = FanTaskStatus.TASK_CREATED
    assert (
        type(task.task_message) == dict
    ), f"expected task_message {task.task_message} to be a dict"
    # task.task_message = json.dumps(task.task_message, indent=3, default=str)
    task.status_change_timestamp = datetime.now().isoformat()
    put_db_task(task)
    publish_next_event(EVENT_SOUCRE, TASK_CREATED, task.json())
    print(f"Added: {task}")
    return task


def put_db_task(task):
    task_dict = task.json()
    call_dynamodb(task_dict)
    return task


def publish_next_event(event_source, event_name, message_json):
    publisher.publish_event(event_name, message_json)


def call_dynamodb(dict):
    dynamodb.put_item(dict)
