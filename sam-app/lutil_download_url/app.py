import hashlib
import json
import logging
import os
import random
import re
import sys
import time
from datetime import datetime
from typing import List
from urllib.parse import urlparse

import boto3
import requests

from S3TextFromLambdaEvent import *


def lambda_handler(event, context):
    result = {}
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
            use_guid_for_filename_var = os.environ.get("use_guids_for_filenames", "no")
            use_guid_for_filename = False
            if use_guid_for_filename_var == "yes":
                use_guid_for_filename = True
            s3_key = get_s3_key_for_latest(url, source, use_guid_for_filename)
            create_s3_text_file(
                bucket,
                s3_key,
                res.text,
            )
            print(f"File saved to: {s3_key}")
            timestamp = datetime.now().isoformat()
            s3_key_historical = s3_key.replace("latest/", "")
            s3_key = f"{s3_key_historical}.{timestamp}"
            create_s3_text_file(
                bucket,
                s3_key,
                res.text,
            )
            print(f"File saved to: {s3_key}")
            print(f"Finished at {datetime.now()}")

    except Exception as e:
        print("Exception: " + str(e))
        raise (e)
        return {"msg": "Exception"}

    return result


def download_page(url):
    random_secs_delay_for_brownlisting = random.randint(1, 3)
    time.sleep(random_secs_delay_for_brownlisting)
    res = requests.get(url, allow_redirects=True, timeout=30)
    return res


def get_s3_key_for_latest(url, source, use_guid=False):
    url_parts = urlparse(url)
    domain = re.sub(r"[^a-zA-Z0-9-_.]", "_", url_parts.netloc)
    filename = re.sub(r"[^a-zA-Z0-9-_.]", "_", url)
    if use_guid:
        m = hashlib.md5()
        m.update(bytes(filename, "utf-8"))
        hash_val = int.from_bytes(m.digest(), "big")
        filename = str(hash_val)

    source_url_parts = urlparse(source)
    source_key_parts = source_url_parts.path.split("/")
    required_first_parts = 4
    array_index = -1 * (len(source_key_parts) - required_first_parts)
    source_key_parts_without_bucket_through_sns_topic = source_key_parts[array_index:]
    source_prefix = ""
    if len(source_key_parts_without_bucket_through_sns_topic) > 1:
        source_prefix_without_last = source_key_parts_without_bucket_through_sns_topic[
            :-1
        ]
        source_prefix = "/".join(source_prefix_without_last)
        domain = f"{source_prefix}/{domain}"

    s3_key = f"lutil-download-url/latest/{domain}/{filename}"
    return s3_key


def get_random_user_agent_header_set() -> List[str]:
    options = []
    options.append([
        "ACCEPT:text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "ACCEPT-ENCODING:gzip, deflate, br",
        "ACCEPT-LANGUAGE:en-US,en;q=0.9",
        "HOST:www.whatismybrowser.com",
        "REFERER:https://www.google.com/",
        'SEC-CH-UA:"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
        "SEC-CH-UA-MOBILE:?0",
        'SEC-CH-UA-PLATFORM:"macOS"',
        "SEC-FETCH-DEST:document",
        "SEC-FETCH-MODE:navigate",
        "SEC-FETCH-SITE:cross-site",
        "SEC-FETCH-USER:?1",
        "UPGRADE-INSECURE-REQUESTS:1",
        "USER-AGENT:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    ])
    random_index = random.randint(0, len(options) - 1)
    return options[random_index]
