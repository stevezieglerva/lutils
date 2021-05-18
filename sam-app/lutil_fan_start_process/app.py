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
from TestNotifier import TestNotifier
from ProcessDTO import *
from TaskDTO import *
from StartProcessAdapter import *


def lambda_handler(event, context):
    print(f"Started at {datetime.now()}")

    print(json.dumps(event, indent=3, default=str))
    db = DynamoDBRepository(os.environ["TABLE_NAME"])
    notifier = TestNotifier(os.environ["HANDLER_SNS_TOPIC_ARN"])
    adapter = StartProcessAdapter(db, notifier)
    adapter.start_process(event)

    print(f"Finished at {datetime.now()}")

    return {}
