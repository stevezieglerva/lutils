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

    # Just print the event for now
    print(json.dumps(event, indent=3, default=str))
    for count, record in enumerate(event["Records"]):
        event_name = record["eventName"]
        print(f"Record #{count}: {event_name}")

    print(f"Finished at {datetime.now()}")

    return {"msg": "success"}
