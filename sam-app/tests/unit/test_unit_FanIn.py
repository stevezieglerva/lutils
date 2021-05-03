import inspect
import json
import os
import sys

import boto3
from moto import mock_dynamodb2


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/common_layer/python"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

import unittest
from unittest import mock

from common_layer.python.FanIn import FanIn


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

EVENT_STRING = '{\n   "process_id": "e915fd0c-ac53-11eb-8f7e-c2ad2721aeef",\n   "process_name": "e2e test",\n   "task_name": "task #1",\n   "message": "{\\n   \\"parameters\\": \\"38jdjsls\\"\\n}",\n   "completion_sns_arn": "sns-done",\n   "timestamp": "2021-05-03T21:09:58.699450",\n   "pk": "FAN-OUT-JOB#e915fd0c-ac53-11eb-8f7e-c2ad2721aeef-TASK#task #1",\n   "status": "created",\n   "status_change_timestamp": "2021-05-03T21:09:55.814367"\n}'


class FanInUnitTests(unittest.TestCase):
    def test_constructor__given_insert_record_image__then_properties_correct(self):
        # Arrange
        table_name = "fake-table"

        # Act
        subject = FanIn(stream_record=STREAM_RECORD_INSERT)
        print(subject.created_fan_job)

        # Assert
        self.assertEqual(subject.event_name, "INSERT")
        self.assertEqual(
            subject.table_name, "lutils-FanProcessingTableTest-X541MIGMFYBW"
        )
        self.assertEqual(
            subject.created_fan_job.process_name,
            "processA",
        )

    def test_constructor__given_insert_image__then_properties_correct(self):
        # Arrange
        table_name = "fake-table"

        # Act
        subject = FanIn(event_string=EVENT_STRING)
        print(subject.created_fan_job)

        # Assert
        self.assertEqual(subject.event_name, "")
        self.assertEqual(subject.table_name, "")
        self.assertEqual(
            subject.created_fan_job.process_name,
            "e2e test",
        )