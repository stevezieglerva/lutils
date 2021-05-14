import glob
import json
import os
import sys
import time
import uuid
from datetime import datetime

import boto3
from DynamoDB import DynamoDB
from TaskRecord import TaskRecord


def lambda_handler(event, context):
    print(f"Started at {datetime.now()}")
    iterations = event.get("iterations", 20)
    max_delay = event.get("max_delay", 180)
    process_name = event.get("process_name", "e2e tests")
    process_id = str(ulid.ULID())
    db = DynamoDB(os.environ["TABLE_NAME"])

    # Create a group of fan out events for the "e2e tests" process
    for i in range(iterations):
        value = i * 33
        task = TaskRecord(
            process_id=process_id,
            process_name=process_name,
            task_name=f"task-{i}",
            task_message=event,
            db=db,
        )
        task.fan_out()

    print(f"Finished at {datetime.now()}")

    return {}
