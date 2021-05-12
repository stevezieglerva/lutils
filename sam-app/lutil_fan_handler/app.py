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
from ProcessRecord import ProcessRecord
from TaskRecord import TaskRecord
from NamedTupleBase import FanJob

db_table = os.environ.get("TABLE_NAME", "")
if db_table == "":
    raise ValueError(f"Missing env variable for TABLE_NAME")
dynamodb = DynamoDB(db_table)
seconds_in_24_hours = 60 * 60 * 24
dynamodb.set_ttl_seconds(seconds_in_24_hours)

EVENT_SOURCE = os.environ.get("AWS_LAMBDA_FUNCTION_NAME", "lambda")

handler_sns_topic_arn = os.environ.get("HANDLER_SNS_TOPIC_ARN", "")
if handler_sns_topic_arn == "":
    raise ValueError(f"Missing env variable for HANDLER_SNS_TOPIC_ARN")
publisher = FanEventPublisher(EVENT_SOURCE, handler_sns_topic_arn)


def lambda_handler(event, context):
    print(f"Started at {datetime.now()}")

    results = {}
    results["table_name"] = db_table
    fan_out_list = []
    task_started_list = []
    task_completed_list = []

    print(json.dumps(event, indent=3, default=str))
    for count, record in enumerate(event["Records"]):
        event_name = record["Sns"]["MessageAttributes"]["event_name"]["Value"]
        print(f"Record #{count}: {event_name}")
        if event_name == FAN_OUT:
            created_job = process_fan_out(record["Sns"]["Message"])
            fan_out_list.append(created_job.json())
        elif event_name == TASK_STARTED:
            updated_job = process_task_started(record["Sns"]["Message"])
            task_started_list.append(updated_job.json())
        elif event_name == TASK_COMPLETED:
            updated_job = process_task_completed(record["Sns"]["Message"])
            task_completed_list.append(updated_job.json())
        else:
            raise ValueError(f"Unexpected event_name: {event_name}")

    results["fan_out"] = fan_out_list
    results["task_started"] = task_started_list
    results["task_completed"] = task_completed_list

    print(json.dumps(results, indent=3, default=str))

    print(f"Finished at {datetime.now()}")

    return results


def process_fan_out(sns_message_json):
    fan_event = FanEvent(record_string=sns_message_json)
    task_json = fan_event.message

    # Add process record
    print("*** putting initial process record in")
    process = ProcessRecord(
        process_id=task_json["process_id"], process_name=task_json["process_name"]
    )
    put_db_task(process)

    # Add task record
    task = TaskRecord(
        process_id=task_json["process_id"],
        process_name=task_json["process_name"],
        task_name=task_json["task_name"],
        task_message=task_json["task_message"],
    )
    task.created = datetime.now().isoformat()
    task.pk = f"PROCESS#{task.process_id}"
    task.status = FanTaskStatus.TASK_CREATED
    assert (
        type(task.task_message) == dict
    ), f"expected task_message {task.task_message} to be a dict"
    task.status_changed_timestamp = datetime.now().isoformat()
    put_db_task(task)

    publish_next_event(EVENT_SOURCE, TASK_CREATED, task.json())
    print(f"Added: {task}")
    return task


def process_task_started(sns_message_json):
    fan_event = FanEvent(record_string=sns_message_json)
    task_json = fan_event.message
    task = TaskRecord(record_string=json.dumps(task_json, indent=3, default=str))
    task.status = TASK_STARTED
    task.status_changed_timestamp = datetime.now().isoformat()
    put_db_task(task)
    print(f"Updated: {task}")
    return task


def process_task_completed(sns_message_json):
    fan_event = FanEvent(record_string=sns_message_json)
    task_json = fan_event.message
    task = TaskRecord(record_string=json.dumps(task_json, indent=3, default=str))
    task.status = TASK_COMPLETED
    task.status_changed_timestamp = datetime.now().isoformat()
    put_db_task(task)
    print(f"Updated: {task}")

    update_process_record_based_on_completions(task.pk)

    return task


def update_process_record_based_on_completions(pk):
    # check if all tasks completed
    process_tasks_list = get_all_tasks_for_process(pk)
    print("all tasks:")
    print(json.dumps(process_tasks_list, indent=3, default=str))
    progress = calculate_progress(process_tasks_list)
    print(f"Progress: {progress}")

    # Get the process record to update it
    print("Get the parent process record")
    get_key = {"pk": pk, "sk": pk}
    print(f"get_key: {get_key}")

    process_record_json = dynamodb.get_item(get_key)
    print(process_record_json)
    process_record = ProcessRecord(
        record_string=json.dumps(process_record_json, indent=3, default=str)
    )
    process_record.progress = progress
    if progress == 1.0:
        process_record.ended = datetime.now().isoformat()
    dynamodb.put_item(process_record.json())

    if progress == 1.0:
        print("Sending event of process completion")
        publish_next_event(EVENT_SOURCE, PROCESS_COMPLETED, process_record.json())


def calculate_progress(process_task_list):
    total_tasks = len(process_task_list)
    completed_tasks = [t for t in process_task_list if t["status"] == TASK_COMPLETED]
    completed_count = len(completed_tasks)
    return float(completed_count / total_tasks)


def get_all_tasks_for_process(pk):
    return dynamodb.query_table_begins({"pk": pk, "sk": "TASK"})


def put_db_task(task):
    task_dict = task.json()
    call_dynamodb(task_dict)
    return task


def publish_next_event(event_source, event_name, message_json):
    publisher.publish_event(event_name, message_json)


def call_dynamodb(dict):
    dynamodb.put_item(dict)
