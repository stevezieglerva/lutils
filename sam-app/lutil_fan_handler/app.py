import boto3
import time
from datetime import datetime

import os
import json
import sys

from FanIn import FanIn


def lambda_handler(event, context):

    print(f"Started at {datetime.now()}")
    results = {}
    inserted = {}

    # Just print the event for now
    print(json.dumps(event, indent=3, default=str))
    for count, record in enumerate(event["Records"]):
        event_name = record["eventName"]
        print(f"Record #{count}: {event_name}")
        fan_in = FanIn(record)
        print(fan_in.created_fan_job)
        if fan_in.event_name == "INSERT":
            process_insert(fan_in, inserted)

    results["inserted"] = inserted
    print(json.dumps(results, indent=3, default=str))

    print(f"Finished at {datetime.now()}")

    return results


def send_sns_message(sns_topic_arn, message):
    print("Sent!")


def process_insert(fan_in, inserted):
    print("Here!")
    sns_message_json = fan_in.created_fan_job.json()
    sns_arn = fan_in.created_fan_job.completion_sns_arn
    send_sns_message(sns_arn, json.dumps(sns_message_json, indent=3, default=str))
    current_topic_count = inserted.get(sns_arn, 0)
    current_topic_count = current_topic_count + 1
    inserted[sns_arn] = current_topic_count
    return inserted
