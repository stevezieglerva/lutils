import glob
import json
import os
import sys
import time
from datetime import datetime

import boto3
from FanManager import FanManager
from IRepository import IRepository
from INotifier import INotifier
from DynamoDBRepository import DynamoDBRepository
from TestNotifier import TestNotifier
from ProcessDTO import *
from TaskDTO import *


def lambda_handler(event, context):
    print(f"Started at {datetime.now()}")

    print(json.dumps(event, indent=3, default=str))
    db = DynamoDBRepository(os.environ["TABLE_NAME"])
    notifier = TestNotifier(os.environ["HANDLER_SNS_TOPIC_ARN"])
    start_process(event, db, notifier)

    print(f"Finished at {datetime.now()}")

    return {}


def convert_process_from_event(event: dict) -> ProcessDTO:
    return convert_json_to_process(event["process"])


def convert_tasks_from_event(event: dict) -> list:
    json_task_list = event["tasks"]
    task_list = [convert_json_to_task(t) for t in json_task_list]
    return task_list


def start_process(event, db: IRepository, notifier: INotifier) -> dict:
    process = convert_process_from_event(event)
    tasks = convert_tasks_from_event(event)
    fan_manager = FanManager(db, notifier)
    return fan_manager.start_process(process, tasks)
