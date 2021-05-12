import boto3
import time
from datetime import datetime

import os
import json
import sys
import glob

from FanEvent import *


from aws_lambda_powertools import Metrics
from aws_lambda_powertools.metrics import MetricUnit
from FanEvent import FanEvent

metrics = Metrics()


@metrics.log_metrics
def lambda_handler(event, context):

    for record in event["Records"]:
        old_image = record["dynamodb"].get("OldImage", None)
        if old_image != None:
            line = "old "
            for k, dynamodb_v in old_image.items():
                value = list(dynamodb_v.values())[0]
                field = f" {value:<50}"
                line = line + field
            print(line)
        new_image = record["dynamodb"].get("NewImage", None)
        if new_image != None:
            line = "new "
            for k, dynamodb_v in new_image.items():
                value = list(dynamodb_v.values())[0]
                field = f" {value:<50}"
                line = line + field
            print(line)
        print("\n")

    return {}
