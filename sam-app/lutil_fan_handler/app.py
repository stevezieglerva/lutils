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


handler_sns_topic_arn = os.environ.get("HANDLER_SNS_TOPIC_ARN", "")
if handler_sns_topic_arn == "":
    raise ValueError(f"Missing env variable for HANDLER_SNS_TOPIC_ARN")
publisher = FanEventPublisher(handler_sns_topic_arn)


def lambda_handler(event, context):
    print(f"Started at {datetime.now()}")

    results = {}
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
            created_job = process_task_started(record["Sns"]["Message"])
            fan_out_list.append(created_job.json())
        else:
            print(f"Skipping event_name: {event_name}")

    results["fan_out"] = fan_out_list

    print(json.dumps(results, indent=3, default=str))

    print(f"Finished at {datetime.now()}")

    return results


def process_fan_out(sns_message_json):
    print("\n\n\n*********")
    print(sns_message_json)
    fan_event = FanEvent(record_string=sns_message_json)
    print(fan_event)
    task_json = fan_event.message
    task = TaskRecord(
        process_id=task_json["process_id"],
        process_name=task_json["process_name"],
        task_name=task_json["task_name"],
    )
    print(task)
    created_job = create_db_task(task)
    publisher.task_created(fan_event.event_source, created_job)
    return created_job


def create_db_task(task):
    task.timestamp = datetime.now().isoformat()
    task.pk = f"PROCESS#{task.process_id}"

    job_dict = task.json()
    job_dict["timestamp"] = datetime.now().isoformat()
    job_dict["pk"] = "FAN-OUT-JOB#" + task.process_id + "-TASK#" + task.task_name
    job_dict["status"] = FanTaskStatus.TASK_CREATED
    job_dict["message"] = json.dumps(task.message, indent=3, default=str)
    job_dict["status_change_timestamp"] = datetime.now().isoformat()
    print(json.dumps(job_dict, indent=3, default=str))
    call_dynamodb(job_dict)
    fan_job_created = job.create_job(
        job_dict["pk"],
        job_dict["timestamp"],
        job_dict["status"],
        job_dict["status_change_timestamp"],
    )
    return fan_job_created


def call_dynamodb(job_dict):
    dynamodb.put_item(job_dict)
