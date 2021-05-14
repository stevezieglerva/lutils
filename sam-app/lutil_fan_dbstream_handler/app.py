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
from DynamoDB import DynamoDB
from TaskUpdateProcessor import TaskUpdateProcessor

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
    # for record in event

    test = {
        "Records": [
            {
                "eventID": "60cf2da2849f89d17f53dcba7a658a8c",
                "eventName": "MODIFY",
                "eventVersion": "1.1",
                "eventSource": "aws:dynamodb",
                "awsRegion": "us-east-1",
                "dynamodb": {
                    "ApproximateCreationDateTime": 1621027471.0,
                    "Keys": {"sk": {"S": "PROCESS#888"}, "pk": {"S": "PROCESS#888"}},
                    "NewImage": {
                        "process_id": {"S": "888"},
                        "process_name": {"S": "keyword blast"},
                        "ended": {"S": ""},
                        "sk": {"S": "PROCESS#888"},
                        "progress": {"N": "0"},
                        "gs1_pk": {"S": "-"},
                        "started": {"S": "2021-05-14T17:24:31.327510"},
                        "pk": {"S": "PROCESS#888"},
                        "gs1_sk": {"S": "-"},
                    },
                    "OldImage": {
                        "process_id": {"S": "888"},
                        "process_name": {"S": "keyword blast"},
                        "ended": {"S": ""},
                        "sk": {"S": "PROCESS#888"},
                        "progress": {"N": "0"},
                        "gs1_pk": {"S": "-"},
                        "started": {"S": "2021-05-14T17:22:46.570132"},
                        "pk": {"S": "PROCESS#888"},
                        "gs1_sk": {"S": "-"},
                    },
                    "SequenceNumber": "1548700000000040486740729",
                    "SizeBytes": 276,
                    "StreamViewType": "NEW_AND_OLD_IMAGES",
                },
                "eventSourceARN": "arn:aws:dynamodb:us-east-1:112280397275:table/lutils2-FanProcessingPartTestTable-Q3PVEB6MO2AJ/stream/2021-05-14T13:21:33.706",
            }
        ]
    }

    return {}
