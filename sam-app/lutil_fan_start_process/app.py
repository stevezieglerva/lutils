import glob
import json
import os
import sys
import time
from datetime import datetime

import boto3
from FanEvent import *


def lambda_handler(event, context):
    print(f"Started at {datetime.now()}")

    print(json.dumps(event, indent=3, default=str))

    print(f"Finished at {datetime.now()}")

    return {}
