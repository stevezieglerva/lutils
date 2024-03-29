import glob
import json
import os
import sys
import time
from datetime import datetime

import boto3
from domain.FanManager import FanManager
from infrastructure.repository.IRepository import IRepository
from infrastructure.notifications.INotifier import INotifier
from infrastructure.repository.DynamoDBRepository import DynamoDBRepository
from infrastructure.notifications.SNSNotifier import *
from domain.ProcessDTO import *
from domain.TaskDTO import *
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
