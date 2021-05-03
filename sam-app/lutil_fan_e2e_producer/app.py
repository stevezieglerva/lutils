import boto3
import time
from datetime import datetime

import os
import json
import sys
import glob

# from FanIn import FanIn


def lambda_handler(event, context):
    print(f"Started at {datetime.now()}")

    # Just print the event for now
    print(json.dumps(event, indent=3, default=str))

    fan = FanOut("processA", "sns-done", "lutils-FanProcessingTableTest-X541MIGMFYBW")
    new_job = fan.fan_out("task #1", {"parameters": "38jdjsls"})

    print(f"Finished at {datetime.now()}")

    return {}
