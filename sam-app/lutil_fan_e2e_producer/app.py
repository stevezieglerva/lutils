import glob
import json
import os
import sys
import time
from botocore.parsers import PROTOCOL_PARSERS
from botocore.session import SubsetChainConfigFactory
import ulid
from datetime import datetime
import random

import boto3


def lambda_handler(event, context):
    print(f"Started at {datetime.now()}")
    start_process_lambda = os.environ["START_PROCESS_LAMBDA_NAME"]
    # Get info from the lambda event
    iterations = event.get("iterations", 20)
    process_name = event.get("process_name", "e2e tests")
    process_information = event.get(
        "process_information", f"general info for '{process_name}'"
    )
    task_prefix = event.get("task_prefix", "task")

    task_list = []
    for i in range(iterations):
        task_message = event.copy()
        new_task = {}
        number_1 = random.randint(0, 100)
        number_2 = random.randint(0, 100)
        task_message["number_1"] = number_1
        task_message["number_2"] = number_2
        new_task["task_name"] = f"{task_prefix}-{i}"
        new_task["task_message"] = task_message
        task_list.append(new_task)

    results = start_process(
        start_process_lambda, process_name, process_information, task_list
    )
    print(results)

    print(f"Finished at {datetime.now()}")

    return {}


def start_process(start_process_lambda, process_name, process_information, task_list):
    lam = boto3.client("lambda")

    start_event = {}
    start_event["process"] = {
        "process_name": process_name,
        "information": process_information,
    }
    start_event["tasks"] = task_list
    print(f"Calling: {start_process_lambda} with: {start_event}")
    response = lam.invoke(
        FunctionName=start_process_lambda,
        InvocationType="RequestResponse",
        Payload=json.dumps(start_event, indent=3, default=str),
    )
    return response
