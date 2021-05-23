import inspect
import json
import os
import sys

import boto3


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/common_layer_hex/python"
sys.path.insert(0, parentdir)
parentdir = os.path.dirname(parentdir) + "/lutil_fan_log_events"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

import unittest
from unittest import mock


from lutil_fan_log_events.app import *


event = {
    "Records": [
        {
            "eventID": "c81e728d9d4c2f636f067f89cc14862c",
            "eventName": "MODIFY",
            "eventVersion": "1.1",
            "eventSource": "aws:dynamodb",
            "awsRegion": "us-east-1",
            "dynamodb": {
                "Keys": {"Id": {"N": "101"}},
                "NewImage": {
                    "pk": {"S": "0001"},
                    "sk": {"S": "9999"},
                    "field1": {"S": "started"},
                    "Id": {"N": "101"},
                },
                "OldImage": {
                    "pk": {"S": "0001"},
                    "sk": {"S": "9999"},
                    "field1": {"S": "completed"},
                    "Id": {"N": "101"},
                },
                "ApproximateCreationDateTime": 1428537600,
                "SequenceNumber": "4421584500000000017450439092",
                "SizeBytes": 59,
                "StreamViewType": "NEW_AND_OLD_IMAGES",
            },
            "eventSourceARN": "arn:aws:dynamodb:us-east-1:123456789012:table/ExampleTableWithStream/stream/2015-06-27T00:48:05.899",
        }
    ]
}


class FanEventUnitTests(unittest.TestCase):
    def test_lambda_handler__given_event__then_done(self):
        # Arrange

        # Act
        results = lambda_handler(event, "")

        # Assert
