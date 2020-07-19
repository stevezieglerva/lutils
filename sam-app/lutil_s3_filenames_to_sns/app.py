import boto3
import time
from datetime import datetime
import logging
import os
import json
import sys
from S3TextFromLambdaEvent import *


def lambda_handler(event, context):

    print(f"Started at {datetime.now()}")
    print(json.dumps(event, indent=3, default=str))

    files = get_files_from_s3_lambda_event(event)
    s3 = boto3.resource("s3")
    text_data = get_file_text_from_s3_file_urls(files, s3)

    messages = format_messages(text_data)
    count = 0
    count = send_messages(messages)

    print(f"Finished at {datetime.now()}")

    return {"msg": "Success", "lines_processed": count}


def format_messages(text_data):
    message_list = []
    for key, value in text_data.items():
        lines = value.split("\n")
        count = 0
        print("line count: {}".format(len(lines)))
        for line in lines:
            count = count + 1
            message = {
                "line_number": count,
                "line": line.strip(),
                "source": key,
                "date": str(datetime.now()),
            }
            message_list.append(message)
    return message_list


def send_messages(message_list):
    sns = boto3.client("sns")
    for message in message_list:
        source = message["source"]
        source_key_parts = source.split("/")
        print(source_key_parts)
        assert (
            len(source_key_parts) >= 6
        ), "Expect input S3 key to have at least three parts"
        POSITION_OF_SNS_TOPIC_NAME = 5
        sns_topic_name = source_key_parts[POSITION_OF_SNS_TOPIC_NAME]
        region = os.environ["region"]
        accountid = os.environ["accountid"]
        sns_arn = f"arn:aws:sns:{region}:{accountid}:{sns_topic_name}"
        print(f"Sending message to {sns_arn}: {message}")
        result = sns.publish(TopicArn=sns_arn, Message=json.dumps(message))
        print(result)
    return len(message_list)
