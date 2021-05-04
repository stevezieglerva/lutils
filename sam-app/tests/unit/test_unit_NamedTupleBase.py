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


from common_layer.python.NamedTupleBase import *
from common_layer.python import FanEventOptions


class FanJobUnitTests(unittest.TestCase):
    def test_constructor__given_valid_inputs__then_no_exceptions(self):
        # Arrange

        # Act
        subject = FanJob("id1", "name x", "task y", "message", "sns")

        # Assert

    def test_json__given_existing_object__then_json_is_correct(self):
        # Arrange
        subject = FanJob("id1", "name x", "task y", "message", "sns")

        # Act
        results = subject.json()
        results.pop("timestamp")

        # Assert
        self.assertEqual(
            results,
            {
                "completion_sns_arn": "sns",
                "message": "message",
                "process_id": "id1",
                "process_name": "name x",
                "task_name": "task y",
            },
        )

    def test_get_fanjob_from_string__given_valid_json_string__then_object_created(self):
        # Arrange
        input = json.dumps(
            {
                "completion_sns_arn": "sns",
                "message": "message",
                "process_id": "id1",
                "process_name": "name x",
                "task_name": "task y",
            },
            indent=3,
            default=str,
        )

        # Act
        results = get_fanjob_from_string(input)

        # Assert
        self.assertEqual(results.process_name, "name x")


class CreatedFanJobUnitTests(unittest.TestCase):
    def test_constructor__given_valid_inputs__then_no_exceptions(self):
        # Arrange

        # Act
        fan_job = FanJob("id1", "name x", "task y", "message", "sns")
        subject = fan_job.create_job("pk1", "today", "created", "today")

        # Assert
        self.assertGreater(len(subject.timestamp), 0)

    def test_json__given_existing_object__then_json_is_correct(self):
        # Arrange
        subject = FanJob("id1", "name x", "task y", "message", "sns")

        # Act
        results = subject.json()
        results.pop("timestamp")

        # Assert
        self.assertEqual(
            results,
            {
                "completion_sns_arn": "sns",
                "message": "message",
                "process_id": "id1",
                "process_name": "name x",
                "task_name": "task y",
            },
        )

    def test_get_createdfanjob_from_string__given_valid_json_string__then_object_created(
        self,
    ):
        # Arrange
        input = json.dumps(
            {
                "completion_sns_arn": "sns",
                "message": "message",
                "process_id": "id1",
                "process_name": "name x",
                "task_name": "task y",
                "pk": "pk 1",
                "timestamp": "today",
                "status": "created",
                "status_change_timestamp": "today",
            },
            indent=3,
            default=str,
        )

        # Act
        results = get_createdfanjob_from_string(input)

        # Assert
        self.assertEqual(results.process_name, "name x")


class FanEventUnitTests(unittest.TestCase):
    def test_constructor__given_valid_inputs__then_no_exceptions(self):
        # Arrange

        # Act
        subject = FanEvent("123", "processA", "task C", FanEventOptions.TASK_CREATED)

        # Assert
        results = subject.json()
        self.assertTrue("timestamp" in results)

    def test_get_fanevent_from_string__given_valid_json_string__then_object_created(
        self,
    ):
        # Arrange
        input = json.dumps(
            {
                "process_id": "id1",
                "process_name": "name x",
                "task_name": "task y",
                "event": FanEventOptions.TASK_CREATED,
            },
            indent=3,
            default=str,
        )

        # Act
        results = get_fanevent_from_string(input)

        # Assert
        self.assertEqual(results.process_name, "name x")

    def test_print(
        self,
    ):
        # Arrange
        subject = FanEvent("123", "processA", "task C", FanEventOptions.TASK_CREATED)

        # Act
        results = subject.get_formatted_line()

        # Assert
        self.assertEqual(
            results,
            "task_created         123                                      processA                                 task C",
        )
