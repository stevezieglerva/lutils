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

    db_table = os.environ.get("TABLE_NAME", "")
    if db_table == "":
        raise ValueError(f"Missing env variable for TABLE_NAME")
    dynamodb = DynamoDB(db_table)
    seconds_in_24_hours = 60 * 60 * 24
    dynamodb.set_ttl_seconds(seconds_in_24_hours)

    EVENT_SOURCE = os.environ.get("AWS_LAMBDA_FUNCTION_NAME", "lambda")

    handler_sns_topic_arn = os.environ.get("HANDLER_SNS_TOPIC_ARN", "")
    if handler_sns_topic_arn == "":
        raise ValueError(f"Missing env variable for HANDLER_SNS_TOPIC_ARN")
    publisher = FanEventPublisher(EVENT_SOURCE, handler_sns_topic_arn)



    stream_data = DynamoDBStream(event)
    print("Changes:")
    print(stream_data)
    # stream_data.save_to_table(os.environ["TABLE_NAME"])

    return {}
