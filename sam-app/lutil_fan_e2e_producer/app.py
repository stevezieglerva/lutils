import glob
import json
import os
import sys
import time
from botocore.parsers import PROTOCOL_PARSERS
from botocore.session import SubsetChainConfigFactory
import ulid
from datetime import datetime

import boto3


def lambda_handler(event, context):
    print(f"Started at {datetime.now()}")
    start_process_lambda = os.environ["START_PROCESS_LAMBDA_NAME"]
    iterations = event.get("iterations", 20)
    process_name = event.get("process_name", "e2e tests")

    task_list = []
    for i in range(iterations):
        new_task = {}
        new_task["task_name"] = f"task-{i}"
        new_task["task_message"] = event
        task_list.append(new_task)

    results = start_process(start_process_lambda, process_name, task_list)
    print(results)

    print(f"Finished at {datetime.now()}")

    return {}


def start_process(start_process_lambda, process_name, task_list):
    lam = boto3.client("lambda")

    start_event = {}
    start_event["process_name"] = process_name
    start_event["tasks"] = task_list
    print(f"Calling: {start_process_lambda} with: {start_event}")
    response = lam.invoke(
        FunctionName=start_process_lambda,
        InvocationType="RequestResponse",
        Payload=json.dumps(start_event, indent=3, default=str),
    )
    return response
