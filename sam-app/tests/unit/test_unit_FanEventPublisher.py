import inspect
import json
import os
import sys

import boto3
from moto import mock_sns


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/common_layer/python"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

import unittest
from unittest import mock


from common_layer.python.FanEventPublisher import FanEventPublisher
from common_layer.python.FanEvent import *
from common_layer.python.TaskRecord import TaskRecord


class FanEventPublisherUnitTests(unittest.TestCase):
    def test_constructor__given_valid_inputs__then_properties_set(self):
        # Arrange

        # Act
        subject = FanEventPublisher("test-sns-topic-arn")

        # Assert
        subject.topic_arn = "test-sns-topic-arn"

    def test_create_task__given_event__then_sns_sent(self):
        # Arrange
        subject = FanEventPublisher("test-sns-topic-arn")
        process_id = subject.generate_process_id()
        task = TaskRecord(
            process_id=process_id,
            process_name="procA",
            task_name="#1",
            task_message={"hello": "world"},
        )

        # Act
        with mock.patch(
            "common_layer.python.FanEventPublisher.FanEventPublisher._publish_sns",
            mock.MagicMock(return_value="sns sent"),
        ):

            results = subject.fan_out(
                process_id,
                "keyword_blast",
                "document-1",
                task.json(),
            )
        print(results)

        # Assert
        self.assertEqual(results.event_source, "keyword_blast")
        self.assertEqual(results.event_name, "fan_out")
