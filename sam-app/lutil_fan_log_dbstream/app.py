import boto3
import time
from datetime import datetime

import os
import json
import sys
import glob


from aws_lambda_powertools import Metrics
from aws_lambda_powertools.metrics import MetricUnit
from FanEvent import FanEvent
from DynamoDBStream import DynamoDBStream

metrics = Metrics()


@metrics.log_metrics
def lambda_handler(event, context):
    print(event)

    return {}
