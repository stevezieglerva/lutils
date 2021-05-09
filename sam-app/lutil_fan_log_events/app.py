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

metrics = Metrics(service=f"fan-out-{fan_event.event_source}")


@metrics.log_metrics
def lambda_handler(event, context):
    print(f"Started at {datetime.now()}")

    for record in event["Records"]:
        print(record)
        message = record["Sns"]["Message"]
        fan_event = FanEvent(record_string=message)
        print("_event_ " + fan_event.get_formatted_line())
        metrics.add_metric(
            name=f"{fan_event.event_name}",
            unit=MetricUnit.Count,
            value=1,
        )

    print(f"Finished at {datetime.now()}")

    return {}
