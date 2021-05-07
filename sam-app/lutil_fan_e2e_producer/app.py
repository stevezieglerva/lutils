import glob
import json
import os
import sys
import time
import uuid
from datetime import datetime

import boto3
from FanEventPublisher import FanEventPublisher
from TaskRecord import TaskRecord


def lambda_handler(event, context):
    print(f"Started at {datetime.now()}")

    publisher = FanEventPublisher(os.environ["HANDLER_SNS_TOPIC_ARN"])
    process_id = publisher.generate_process_id()

    # Create a group of fan out events for the "e2e test" process
    for i in range(10):
        value = i * 33
        task = TaskRecord(
            process_id=process_id,
            process_name="e2e tests",
            task_name=f"task-{i}",
            task_message={"hello": "world"},
        )
        publisher.fan_out(process_id, "e2e tests", f"task-{i}", task.json())

    print(f"Finished at {datetime.now()}")

    return {}
