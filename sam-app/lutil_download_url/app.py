import boto3
import time
from datetime import datetime
import logging
import os
import json
import sys
import requests
import re
import random
import time
from urllib.parse import urlparse
from S3TextFromLambdaEvent import *


def lambda_handler(event, context):
    try:
        print(f"Started at {datetime.now()}")

        bucket = os.environ["s3_bucket"]
        for records in event["Records"]:
            message = json.loads(records["Sns"]["Message"])
            print(message)
            url = message["line"]
            source = message["source"]
            res = download_page(url)
            status_code = res.status_code
            print(str(res.status_code) + "-" + url)
            result = {
                "processing_type": "async download urls",
                "url": url,
                "status_code": res.status_code,
                "length": len(res.text),
            }
            print(f"processed url: {result}")
            s3_key = get_s3_key_for_latest(url, source)
            create_s3_text_file(
                bucket, s3_key, res.text,
            )
            print(f"File saved to: {s3_key}")
            timestamp = datetime.now().isoformat()
            s3_key_historical = s3_key.replace("latest/", "")
            s3_key = f"{s3_key}.{timestamp}"
            create_s3_text_file(
                bucket, s3_key, res.text,
            )
            print(f"File saved to: {s3_key}")
            print(f"Finished at {datetime.now()}")

    except Exception as e:
        print("Exception: " + str(e))
        raise (e)
        return {"msg": "Exception"}

    return {"msg": "Success"}


def download_page(url):
    random_secs_delay_for_brownlisting = random.randint(1, 3)
    time.sleep(random_secs_delay_for_brownlisting)
    res = requests.get(url, allow_redirects=True, timeout=30)
    return res


def get_s3_key_for_latest(url, source):
    url_parts = urlparse(url)
    domain = re.sub(r"[^a-zA-Z0-9-_.]", "_", url_parts.netloc)
    filename = re.sub(r"[^a-zA-Z0-9-_.]", "_", url)

    source_url_parts = urlparse(source)
    source_key_parts = source_url_parts.path.split("/")
    #    print(source_key_parts)
    required_first_parts = 4
    array_index = -1 * (len(source_key_parts) - required_first_parts)
    source_key_parts_without_bucket_through_sns_topic = source_key_parts[array_index:]
    #   print(
    #        f"source_key_parts_without_bucket_through_sns_topic: {source_key_parts_without_bucket_through_sns_topic}"
    #    )
    source_prefix = ""
    if len(source_key_parts_without_bucket_through_sns_topic) > 1:
        source_prefix_without_last = source_key_parts_without_bucket_through_sns_topic[
            :-1
        ]
        source_prefix = "/".join(source_prefix_without_last)
        #        print(f"source_prefix: {source_prefix}")
        domain = f"{source_prefix}/{domain}"

    s3_key = f"lutil-download-url/latest/{domain}/{filename}"
    return s3_key
