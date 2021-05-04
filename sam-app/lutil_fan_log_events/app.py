import boto3
import time
from datetime import datetime

import os
import json
import sys
import glob

from NamedTupleBase import FanEvent


from aws_lambda_powertools import Metrics
from aws_lambda_powertools.metrics import MetricUnit


def lambda_handler(event, context):
    print(f"Started at {datetime.now()}")

    for record in event["Records"]:
        message = record["Sns"]["Message"]
        fan_event = get_fanevent_from_string(message)
        metrics.add_metric(name=fan_event.event, unit=MetricUnit.Count, value=1)

    print(f"Finished at {datetime.now()}")

    return {}
