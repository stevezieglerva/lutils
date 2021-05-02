import inspect
import json
import os
import sys

import boto3
from moto import mock_dynamodb2


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/lutil_fan_handler"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

import unittest
from unittest import mock

from lutil_fan_handler.FanIn import FanIn
from lutil_fan_handler.NamedTupleBase import FanJob


STREAM_RECORD_INSERT = {
    "eventID": "080ff8a233fb69e74ef8f1130f0cfa00",
    "eventName": "INSERT",
    "eventVersion": "1.1",
    "eventSource": "aws:dynamodb",
    "awsRegion": "us-east-1",
    "dynamodb": {
        "ApproximateCreationDateTime": 1619955850.0,
        "Keys": {
            "pk": {"S": "FAN-OUT-JOB#b530ebf0-ab3b-11eb-b19b-acde48001122-TASK#task C"}
        },
        "NewImage": {
            "task_name": {"S": "task C"},
            "process_id": {"S": "b530ebf0-ab3b-11eb-b19b-acde48001122"},
            "process_name": {"S": "processA"},
            "pk": {"S": "FAN-OUT-JOB#b530ebf0-ab3b-11eb-b19b-acde48001122-TASK#task C"},
            "message": {"S": '{\n   "keywords": "hello world"\n}'},
            "completion_sns_arn": {"S": "sns-arn"},
            "status": {"S": "created"},
            "status_change_timestamp": {"S": "2021-05-02T07:44:09.627753"},
            "timestamp": {"S": "2021-05-02T07:44:09.627604"},
        },
        "SequenceNumber": "3774300000000008979127455",
        "SizeBytes": 366,
        "StreamViewType": "NEW_AND_OLD_IMAGES",
    },
    "eventSourceARN": "arn:aws:dynamodb:us-east-1:112280397275:table/lutils-FanProcessingTableTest-X541MIGMFYBW/stream/2021-05-01T16:26:21.720",
}


class FanInUnitTests(unittest.TestCase):
    def test_constructor__given_insert_image__then_properties_correct(self):
        # Arrange
        table_name = "fake-table"

        # Act
        subject = FanIn(STREAM_RECORD_INSERT)
        print(subject.created_fan_job)

        # Assert
        self.assertEqual(subject.event_name, "INSERT")
        self.assertEqual(
            subject.table_name, "lutils-FanProcessingTableTest-X541MIGMFYBW"
        )
