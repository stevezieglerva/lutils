import boto3
import time
import datetime
import logging
import os
import json
import sys
from S3TextFromLambdaEvent import *


def lambda_handler(event, context):
    try:
        aws_request_id = ""
        aws_request_id = ""
        if context is not None:
            aws_request_id = context.aws_request_id

        print("Started")
        sns_arn = os.environ.get("sns_arn", "")
        if sns_arn == "":
            raise (
                ValueError(
                    "Environment variable sns_arn must be set to a valid SNS topic."
                )
            )

        files = get_files_from_s3_lambda_event(event)
        s3 = boto3.resource("s3")
        sns = boto3.client("sns")
        text_data = get_file_text_from_s3_file_urls(files, s3)

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
                    "date": str(datetime.datetime.now()),
                }
                print("Sending message: {}".format(message))
                sns.publish(TopicArn=sns_arn, Message=json.dumps(message))

        print("Finished")

    except Exception as e:
        print("Exception: " + str(e))
        return {"msg": "Exception", "lines_processed": 0, "source": key}

    return {"msg": "Success", "lines_processed": count, "source": key}

