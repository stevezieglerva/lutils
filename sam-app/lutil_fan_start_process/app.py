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

    print(f"Finished at {datetime.now()}")

    return {}


def convert_process_from_event(event: dict) -> ProcessDTO:
    return convert_json_to_process(event["process"])


def convert_tasks_from_event(event: dict) -> list:
    json_task_list = event["tasks"]
    task_list = [convert_json_to_task(t) for t in json_task_list]
    return task_list


def start_process(event_data, db: IRepository, notifier: INotifier):
    pass
