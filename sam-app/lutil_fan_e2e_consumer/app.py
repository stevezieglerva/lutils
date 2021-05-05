import boto3
import time
from datetime import datetime

import os
import json
import sys
import glob
import time
import random

from NamedTupleBase import *
from FanEvent import FanEvent, get_fanevent_from_string
from FanEventPublisher import FanEventPublisher
import FanEventOptions


def lambda_handler(event, context):
    print(f"Started at {datetime.now()}")
    print(json.dumps(event, indent=3, default=str))
    publisher = FanEventPublisher(os.environ["HANDLER_SNS_TOPIC_ARN"])

    for count, record in enumerate(event["Records"]):
        message = record["Sns"]["Message"]
        event = get_fanevent_from_string(message)
        print(event)
        publisher.task_started(event.event_source, event.job)
        time.sleep(count)

    print(f"Finished at {datetime.now()}")

    return {}
