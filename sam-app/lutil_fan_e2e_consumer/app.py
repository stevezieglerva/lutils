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
from DynamoDB import DynamoDB


def lambda_handler(event, context):
    print(f"Started at {datetime.now()}")
    max_delay = event.get("max_delay", 5)

    print(json.dumps(event, indent=3, default=str))

    db = DynamoDB(os.environ["TABLE_NAME"])

    for count, record in enumerate(event["Records"]):
        print(f"Record #{count}")
        message = record["Sns"]["Message"]
        event = FanEvent(record_string=message)
        print("Received task event:")
        print(event)

        task = TaskRecord(record_string=json.dumps(event.message, default=str), db=db)
        task.start()

        print(f"task_message: {task.task_message}")
        max_delay = task.task_message["max_delay"]
        time.sleep(random.randint(0, max_delay))
        task.complete()

    print(f"Finished at {datetime.now()}")

    return {}
