import boto3
import time
from datetime import datetime

import os
import json
import sys

from FanIn import FanIn


def lambda_handler(event, context):
    print(f"Started at {datetime.now()}")

    handler_sns_topic_arn = os.environ.get("HANDLER_SNS_TOPIC_ARN", "")
    if handler_sns_topic_arn == "":
        raise ValueError(f"Missing env variable for HANDLER_SNS_TOPIC_ARN")

    results = {}
    inserted = {}

    # Just print the event for now
    print(json.dumps(event, indent=3, default=str))
    for count, record in enumerate(event["Records"]):
        event_name = record["eventName"]
        print(f"Record #{count}: {event_name}")
        fan_in = FanIn(stream_record=record)
        print(f"table: {fan_in.table_name}")
        print(fan_in.created_fan_job)
        if fan_in.event_name == "INSERT":
            process_insert(fan_in, inserted, handler_sns_topic_arn)

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
