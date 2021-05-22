import glob
import json
import os
import sys
import time
from datetime import datetime

import boto3
from FanManager import FanManager
from IRepository import IRepository
from INotifier import INotifier
from DynamoDBRepository import DynamoDBRepository
from SNSNotifier import *
from ProcessDTO import *
from TaskDTO import *
from CompleteTaskAdapter import *


def lambda_handler(event, context):
    print(f"Started at {datetime.now()}")

    print(json.dumps(event, indent=3, default=str))
    db = DynamoDBRepository(os.environ["TABLE_NAME"])
    notifier = SNSNotifier(os.environ["HANDLER_SNS_TOPIC_ARN"])
    adapter = CompleteTaskAdapter(db, notifier)
    results = adapter.complete_task(event)
    print(f"\nresults : {results}")

    print(f"Finished at {datetime.now()}")

    return {}