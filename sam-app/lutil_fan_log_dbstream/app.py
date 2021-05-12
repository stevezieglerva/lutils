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
    print(f"Started at {datetime.now()}")

    print(json.dumps(event, indent=3, default=str))

    print(f"Finished at {datetime.now()}")

    return {}
