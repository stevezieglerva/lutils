import boto3
import time
from datetime import datetime

import os
import json
import sys
import glob
import time
import random

from NamedTupleBase import *
from FanEvent import *
from TaskRecord import TaskRecord
from FanEventPublisher import FanEventPublisher
import FanEventOptions


def lambda_handler(event, context):
    print(f"Started at {datetime.now()}")
    max_delay = event.get("max_delay", 5)

    print(json.dumps(event, indent=3, default=str))
    publisher = FanEventPublisher(os.environ["HANDLER_SNS_TOPIC_ARN"])

    for count, record in enumerate(event["Records"]):
        print(f"Record #{count}")
        message = record["Sns"]["Message"]
        event = FanEvent(record_string=message)
        print("Received task event:")
        print(event)

        task = TaskRecord(record_string=json.dumps(event.message, default=str))
        publisher.publish_event(event.event_source, TASK_STARTED, task.json())

        print(f"task_message: {task.task_message}")
        max_delay = task.task_message["max_delay"]

        time.sleep(random.randint(0, max_delay))

        publisher.publish_event(event.event_source, TASK_COMPLETED, task.json())
    print(f"Finished at {datetime.now()}")

    return {}
