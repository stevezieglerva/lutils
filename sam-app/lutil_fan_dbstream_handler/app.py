import boto3
import time
from datetime import datetime

import os
import json
import sys
import glob


from aws_lambda_powertools import Metrics
from aws_lambda_powertools.metrics import MetricUnit
from DynamoDBRepository import DynamoDBRepository
from SNSNotifier import SNSNotifier
from DBStreamAdapter import DBStreamAdapter


metrics = Metrics()


@metrics.log_metrics
def lambda_handler(event, context):
    print(event)

    db_table = os.environ.get("TABLE_NAME", "")
    if db_table == "":
        raise ValueError(f"Missing env variable for TABLE_NAME")
    repo = DynamoDBRepository(db_table)

    handler_sns_topic_arn = os.environ.get("HANDLER_SNS_TOPIC_ARN", "")
    if handler_sns_topic_arn == "":
        raise ValueError(f"Missing env variable for HANDLER_SNS_TOPIC_ARN")
    notifier = SNSNotifier(handler_sns_topic_arn)

    adapter = DBStreamAdapter(repo, notifier)

    processed_count = 0
    for record in event["Records"]:
        results = adapter.process_single_event(record)
        processed_count = processed_count + 1

    return {"processed": processed_count}
