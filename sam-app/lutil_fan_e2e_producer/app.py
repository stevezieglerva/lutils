import boto3
import time
from datetime import datetime

import os
import json
import sys
import glob

from FanOut import FanOut


def lambda_handler(event, context):
    print(f"Started at {datetime.now()}")

    fan = FanOut("e2e test", "sns-done", "lutils-FanProcessingTableTest-X541MIGMFYBW")
    # Create a group of fan out events for the "e2e test" process
    for i in range(10):
        new_job = fan.fan_out(
            f"task #{i}", {"number": i, "parameters": f"38jdjsls-{i}"}
        )

    print(f"Finished at {datetime.now()}")

    return {}
