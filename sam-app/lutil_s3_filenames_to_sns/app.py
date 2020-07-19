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

    bucket = event["bucket"]
    prefix = event["prefix"]
    sns_topic = event["sns_arn"]
    print("Getting files")
    files = get_s3_files(bucket, prefix)
    print(files[0])

    messages = format_messages(bucket, files)
    count = send_messages(sns_topic, messages)

    print(f"Finished at {datetime.now()}")

    return {"msg": "Success", "files_processed": count}


def get_s3_files(bucket, prefix):
    s3 = boto3.client("s3")
    files = []
    batch = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    files.extend(batch["Contents"])
    print(f'Received {len(batch["Contents"])} files')
    ##print(json.dumps(files, indent=3, default=str))
    while batch.get("ContinuationToken", "") != "":
        attempt = 0
        while attempt < 10:
            try:
                attempt = attempt + 1
                batch = s3.list_objects_v2(
                    Bucket=bucket,
                    Prefix=prefix,
                    ContinuationToken=batch["ContinuationToken"],
                )
                files.extend(batch["Contents"])
                print(f'Received {len(batch["Contents"])} files')
                break
            except Exception as e:
                print(f"Exception: {e}")
                time.sleep(1)
    return files


def format_messages(bucket, files):
    message_list = []
    count = 0
    for file in files:
        s3_key = file["Key"]
        count = count + 1
        message = {
            "filenumber": count,
            "key": s3_key,
            "bucket": bucket,
            "date": str(datetime.now()),
        }
        message_list.append(message)
    return message_list


def send_messages(topic, message_list):
    sns = boto3.client("sns")
    for message in message_list:
        region = os.environ["region"]
        accountid = os.environ["accountid"]
        sns_arn = topic
        print(f"Sending message to {sns_arn}: {message}")
        result = sns.publish(TopicArn=sns_arn, Message=json.dumps(message))
        print(result)
    return len(message_list)
