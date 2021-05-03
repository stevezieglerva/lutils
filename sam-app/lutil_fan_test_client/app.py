import boto3
import time
from datetime import datetime

import os
import json
import sys
import glob

# from common_layer.FanIn import FanIn


def lambda_handler(event, context):
    print(f"Started at {datetime.now()}")

    # Just print the event for now
    print(json.dumps(event, indent=3, default=str))

    for file in glob.glob("**/*.*", recursive=True):
        print(file)

    print(f"Finished at {datetime.now()}")

    return {}
