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
            # line = "old "
            for k, dynamodb_v in old_image.items():
                value = list(dynamodb_v.values())[0]
                field = f" {value:<50}"
            # print(line)
        new_image = record["dynamodb"].get("NewImage", None)
        if new_image != None:
            pks = (
                list(old_image["pk"].values())[0]
                + " / "
                + list(old_image["sk"].values())[0]
            )
            print(pks)
            for k, dynamodb_v in new_image.items():
                new_value = list(dynamodb_v.values())[0]
                old_value = ""
                if old_image != None:
                    old_value = list(old_image[k].values())[0]

                if old_value != new_value:
                    field = f"   {k}: {old_value} -> {new_value}"
                    print(field)
        print("\n")

    return {}
