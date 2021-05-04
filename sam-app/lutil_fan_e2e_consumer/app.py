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
import FanEventOptions


def lambda_handler(event, context):
    print(f"Started at {datetime.now()}")
    print(json.dumps(event, indent=3, default=str))

    for record in event["Records"]:
        message = record["Sns"]["Message"]
        fan_job = FanIn(os.environ["HANDLER_SNS_TOPIC_ARN"], event_string=message)
        fan_job.update_task(FanEventOptions.TASK_STARTED)

        message_str = fan_job.created_fan_job.message
        message_json = json.loads(message_str)
        sleep_duration = message_json["number"]
        time.sleep(sleep_duration)
        fan_job.update_task(FanEventOptions.TASK_COMPLETED)

    print(f"Finished at {datetime.now()}")

    return {}
