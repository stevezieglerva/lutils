import boto3
import time
from datetime import datetime

import os
import json
import sys
import glob
import time
import random

from FanIn import FanIn


def lambda_handler(event, context):
    print(f"Started at {datetime.now()}")
    print(json.dumps(event, indent=3, default=str))

    sleep_duration = random.randint(0, 3)
    time.sleep(sleep_duration)

    print(f"Finished at {datetime.now()}")

    return {}
