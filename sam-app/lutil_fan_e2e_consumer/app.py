import boto3
import time
from datetime import datetime

import os
import json
import sys
import glob
import time
import random

from FanIn import FanIn
import FanTaskStatus


def lambda_handler(event, context):
    print(f"Started at {datetime.now()}")
    print(json.dumps(event, indent=3, default=str))

    for record in event["Records"]:
        message = record["Sns"]["Message"]
        fan_job = FanIn(event_string=message)
        fan_job.update_task(FanTaskStatus.TASK_CREATED)
        sleep_duration = random.randint(0, 3)
        time.sleep(sleep_duration)
        fan_job.update_task(FanTaskStatus.TASK_COMPLETED)

    print(f"Finished at {datetime.now()}")

    return {}
