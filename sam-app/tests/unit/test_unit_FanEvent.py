import inspect
import json
import os
import sys

import boto3


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/common_layer/python"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

import unittest
from unittest import mock


from common_layer.python.FanEvent import *
from common_layer.python.NamedTupleBase import *


class FanEventUnitTests(unittest.TestCase):
    def test_constructor__given_keywords_for_create_task__then_no_exceptions(self):
        # Arrange

        # Act
        subject = FanEvent(
            event_source="process-x",
            event_name=TASK_CREATED,
            message={"process_id": "123"},
            timestamp="2021",
        )
        print("****")
        print(subject)

        # Assert
        results = subject.json()
        print(json.dumps(results, indent=3, default=str))
        self.assertEqual(results["message"], {"process_id": "123"})
        self.assertEqual(subject.timestamp, "2021")

    def test_constructor__given_create_task_without_job__then_no_exceptions(self):
        # Arrange

        # Act
        subject = FanEvent(
            event_source="process-x",
            event_name=TASK_CREATED,
        )

        # Assert
        results = subject.json()
        print(json.dumps(results, indent=3, default=str))

    def test_print(
        self,
    ):
        # Arrange
        subject = FanEvent(
            event_source="process-x",
            event_name=TASK_CREATED,
            message={"process_id": "123"},
            timestamp="2021",
        )

        # Act
        results = subject.get_formatted_line()
        print(results)

        # Assert
        self.assertTrue("process-x" in results)

    def test_get_fanevent_from_string__given_valid_string__then_event_returned(self):
        # Arrange
        input = '{\n   "event_source": "e2e tests",\n   "event_name": "task_started",\n   "message": {\n      "process_id": "2e7d2b96-ae10-11eb-b5ab-acde48001122",\n      "process_name": "e2e tests",\n      "task_name": "task-9",\n      "message": {\n         "var_1": 297\n      },\n      "completion_sns_arn": "completion_sns_arn",\n      "timestamp": "2021-05-06T09:20:40.055717"\n   },\n   "timestamp": "2021-05-06T09:20:40.055754"\n}'
        # Act
        subject = FanEvent(record_string=input)

        # Assert
        self.assertEqual(subject.event_source, "e2e tests")
