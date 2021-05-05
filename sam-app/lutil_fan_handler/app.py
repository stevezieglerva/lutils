import json
import os
import sys
import time
import uuid
from datetime import datetime

import boto3
from DynamoDB import DynamoDB
from FanEvent import *
from NamedTupleBase import FanJob
import FanTaskStatus


db_table = os.environ.get("TABLE_NAME", "")
if db_table == "":
    raise ValueError(f"Missing env variable for TABLE_NAME")
dynamodb = DynamoDB(db_table, "pk")


def lambda_handler(event, context):
    print(f"Started at {datetime.now()}")

    handler_sns_topic_arn = os.environ.get("HANDLER_SNS_TOPIC_ARN", "")
    if handler_sns_topic_arn == "":
        raise ValueError(f"Missing env variable for HANDLER_SNS_TOPIC_ARN")

    results = {}
    inserted = {}

    print(json.dumps(event, indent=3, default=str))
    for count, record in enumerate(event["Records"]):
        event_name = record["Sns"]["MessageAttributes"]["event_name"]["Value"]
        print(f"Record #{count}: {event_name}")
        print(f"'{event_name}' '{FAN_OUT}'")
        if event_name == FAN_OUT:
            process_fan_out(record["Sns"]["Message"])
        else:
            print("not processed")

    results["inserted"] = inserted

    print(json.dumps(results, indent=3, default=str))

    print(f"Finished at {datetime.now()}")

    return results


def send_start_sns_message(sns_arn, process_name, message):
    print(f"Sending message to {sns_arn}: {message}")
    sns = boto3.client("sns")
    result = sns.publish(
        TopicArn=sns_arn,
        Message=message,
        MessageAttributes={
            "event_name": {"DataType": "String", "StringValue": "start_job"},
            "process_name": {"DataType": "String", "StringValue": process_name},
        },
    )
    print("Sent!")


def process_fan_out(message_str):
    fan_event = get_fanevent_from_string(message_str)

    print(fan_event)
    created_job = put_to_db(fan_event.job)
    print(created_job)
    pass


def process_insert(fan_in, inserted, handler_sns_topic_arn):
    sns_message_json = fan_in.created_fan_job.json()
    process_name = fan_in.created_fan_job.process_name
    send_start_sns_message(
        handler_sns_topic_arn,
        process_name,
        json.dumps(sns_message_json, indent=3, default=str),
    )

    current_topic_count = inserted.get(process_name, 0)
    current_topic_count = current_topic_count + 1
    inserted[process_name] = current_topic_count
    return inserted


def put_to_db(job):
    job_dict = job.json()
    job_dict["timestamp"] = datetime.now().isoformat()
    job_dict["pk"] = "FAN-OUT-JOB#" + job.process_id + "-TASK#" + job.task_name
    job_dict["status"] = FanTaskStatus.TASK_CREATED
    job_dict["message"] = json.dumps(job.message, indent=3, default=str)
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
