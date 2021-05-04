import boto3
import time
from datetime import datetime

import os
import json
import sys
import glob

from FanEventPublisher import FanEventPublisher


def lambda_handler(event, context):
    print(f"Started at {datetime.now()}")

    publisher = FanEventPublisher(os.environ["HANDLER_SNS_TOPIC_ARN"])

    # Create a group of fan out events for the "e2e test" process
    for i in range(10):
        value = i * 33
        publisher.fan_out("e2e tests", f"task-{i}", {"var_1": value})

    print(f"Finished at {datetime.now()}")

    return {}
