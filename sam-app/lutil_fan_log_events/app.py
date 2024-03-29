import boto3
import time
from datetime import datetime

import os
import json
import sys
import glob

from domain.FanEventDTO import *


from aws_lambda_powertools import Metrics
from aws_lambda_powertools.metrics import MetricUnit


metrics = Metrics()


@metrics.log_metrics
def lambda_handler(event, context):
    print(f"Started at {datetime.now()}")

    for record in event["Records"]:
        print(record)
        message = record["Sns"]["Message"]
        message = message.replace("'", '"')
        fan_event = FanEventDTO.create_from_dict(json.loads(message))
        print("_event_ " + fan_event.get_formatted_line())
    ##        metrics.add_metric(
    ##            name=f"Source-{fan_event.event_source}", unit=MetricUnit.Count, value=1
    ##        )
    ##        metrics.add_metric(
    ##            name=f"Event-{fan_event.event_name}", unit=MetricUnit.Count, value=1
    ##        )

    print(f"Finished at {datetime.now()}")

    return {}
