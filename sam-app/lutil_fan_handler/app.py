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

    print(json.dumps(event, indent=3, default=str))
    for count, record in enumerate(event["Records"]):
        event_name = record["Sns"]["MessageAttributes"]["event_name"]["Value"]
        print(f"Record #{count}: {event_name}")
        print(f"'{event_name}' '{FAN_OUT}'")
        if event_name == FAN_OUT:
            created_job = process_fan_out(record["Sns"]["Message"])
            fan_out_list.append(created_job.json())
        else:
            print(f"Skipping event_name: {event_name}")

    results["fan_out"] = fan_out_list

    print(json.dumps(results, indent=3, default=str))

    print(f"Finished at {datetime.now()}")

    return results


def process_fan_out(message_str):
    fan_event = get_fanevent_from_string(message_str)
    created_job = put_to_db(fan_event.job)
    publisher.task_created(fan_event.event_source, created_job)

    return created_job


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
