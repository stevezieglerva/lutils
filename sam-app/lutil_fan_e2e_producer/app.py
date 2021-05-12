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
    iterations = event.get("iterations", 20)
    max_delay = event.get("max_delay", 180)
    process_name = event.get("process_name", "e2e tests")

    event_source = os.environ.get("AWS_LAMBDA_FUNCTION_NAME", "lambda_producer")
    publisher = FanEventPublisher(event_source, os.environ["HANDLER_SNS_TOPIC_ARN"])
    process_id = publisher.generate_process_id()

    # Create a group of fan out events for the "e2e tests" process
    for i in range(iterations):
        value = i * 33
        task = TaskRecord(
            process_id=process_id,
            process_name=process_name,
            task_name=f"task-{i}",
            task_message=event,
        )
        publisher.fan_out(task)

    print(f"Finished at {datetime.now()}")

    return {}
