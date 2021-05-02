import boto3
import time
from datetime import datetime

import os
import json
import sys

from FanIn import FanIn


def lambda_handler(event, context):
    print(f"Started at {datetime.now()}")

    # Just print the event for now
    print(json.dumps(event, indent=3, default=str))

    print(f"Finished at {datetime.now()}")

    return {}
