import inspect
import json
import os
import sys

import boto3


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/lutil_fan_dbstream_handler"
sys.path.insert(0, parentdir)
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/common_layer/python"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

import unittest
from unittest import mock

from common_layer.python.TaskUpdateProcessor import *
from common_layer.python.TaskRecord import *

from lutil_fan_dbstream_handler import DBStreamTaskUpdateProcessorAdapter


EVENT_FAN_OUT = {
    "Records": [
        {
            "eventID": "f1c2fa59c0b128193cf9575ed54811d2",
            "eventName": "INSERT",
            "eventVersion": "1.1",
            "eventSource": "aws:dynamodb",
            "awsRegion": "us-east-1",
            "dynamodb": {
                "ApproximateCreationDateTime": 1621025176.0,
                "Keys": {
                    "sk": {"S": "TASK#task_00"},
                    "pk": {"S": "PROCESS#01F5PA2EMNDQ9YJ0WGGC4KDMNW"},
                },
                "NewImage": {
                    "task_name": {"S": "task_00"},
                    "process_id": {"S": "01F5PA2EMNDQ9YJ0WGGC4KDMNW"},
                    "status_changed_timestamp": {"S": "2021-05-14T16:46:16.627334"},
                    "task_message": {"S": "\"{'go': 'caps!'}\""},
                    "created": {"S": "2021-05-14T16:46:16.627306"},
                    "process_name": {"S": "ProcessRecord Int Test"},
                    "sk": {"S": "TASK#task_00"},
                    "gs1_pk": {"S": "-"},
                    "pk": {"S": "PROCESS#01F5PA2EMNDQ9YJ0WGGC4KDMNW"},
                    "gs1_sk": {"S": "-"},
                    "status": {"S": "fan_out"},
                },
                "SequenceNumber": "875400000000009959396144",
                "SizeBytes": 325,
                "StreamViewType": "NEW_AND_OLD_IMAGES",
            },
            "eventSourceARN": "arn:aws:dynamodb:us-east-1:112280397275:table/lutils2-FanProcessingPartTestTable-Q3PVEB6MO2AJ/stream/2021-05-14T13:21:33.706",
        },
    ]
}


class DBStreamTaskUpdateProcessorAdapterUnitTests(unittest.TestCase):
    def test_constructor__given_valid_input__then_no_exceptions(self):
        # Arrange
        subject = DBStreamTaskUpdateProcessorAdapter()

        # Act
        results = subject.process_event(EVENT_FAN_OUT)

        # Assert
        self.assertEqual(results, "")


if __name__ == "__main__":
    unittest.main()