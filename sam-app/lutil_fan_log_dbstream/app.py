import glob
import json
import os
import sys
import time
from datetime import datetime

import boto3
from aws_lambda_powertools import Metrics
from aws_lambda_powertools.metrics import MetricUnit
from DynamoDBStream import DynamoDBStream
from FanEvent import FanEvent

metrics = Metrics()


@metrics.log_metrics
def lambda_handler(event, context):
    print(json.dumps(event, indent=3, default=str))

    return {}
