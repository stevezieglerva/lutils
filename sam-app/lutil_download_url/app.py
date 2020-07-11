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
            url_parts = urlparse(url)
            domain = re.sub(r"[^a-zA-Z0-9-_.]", "_", url_parts.netloc)
            filename = re.sub(r"[^a-zA-Z0-9-_.]", "_", url)
            s3_key = f"lutil-download-url/latest/{domain}/{filename}"
            create_s3_text_file(
                bucket, s3_key, res.text,
            )
            print(f"File saved to: {s3_key}")
            timestamp = datetime.now().isoformat()
            s3_key = f"lutil-download-url/{domain}/{filename}.{timestamp}"
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


def get_s3_latest_filename(url, source):
    return ""
