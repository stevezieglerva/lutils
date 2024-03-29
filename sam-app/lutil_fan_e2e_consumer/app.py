import boto3
import time
from datetime import datetime

import os
import json
import sys
import glob
import time
import random

from domain.TaskDTO import *


def lambda_handler(event, context):
    print(f"Started at {datetime.now()}")
    complete_task_lambda = os.environ["COMPLETE_TASK_LAMBDA_NAME"]
    max_delay = event.get("max_delay", 5)
    print(json.dumps(event, indent=3, default=str))

    for count, record in enumerate(event["Records"]):
        print(f"Record #{count}")
        message = record["Sns"]["Message"]
        print(f"Received message: {message}")
        message = message.replace("'", '"')
        task_json = json.loads(message)["event_message"]
        task = TaskDTO.create_from_dict(task_json)
        print(f"task_message: {task.task_message}")

        # Random wait to simulate tasks of different lengths
        max_delay = task.task_message["max_delay"]
        time.sleep(random.randint(0, max_delay))

        number_1 = task.task_message["number_1"]
        number_2 = task.task_message["number_2"]
        sum = number_1 + number_2

        info = task.task_message["info"]

        print(f"Info: {info:<25}| Sum: {number_1} + {number_2} = {sum}")

        results = complete_task(complete_task_lambda, task.process_id, task.task_name)

    print(f"Finished at {datetime.now()}")

    return {}


def complete_task(complete_task_lambda: str, process_id: str, task_name: str):
    lam = boto3.client("lambda")
    start_event = {}
    start_event["process_id"] = process_id
    start_event["task_name"] = task_name
    print(f"Calling: {complete_task_lambda} with: {start_event}")
    response = lam.invoke(
        FunctionName=complete_task_lambda,
        InvocationType="RequestResponse",
        Payload=json.dumps(start_event, indent=3, default=str),
    )
    return response