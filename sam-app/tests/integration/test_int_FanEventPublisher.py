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
from common_layer.python.TaskRecord import TaskRecord


class FanEventPublisherUnitTests(unittest.TestCase):
    def test_create_task__given_event__then_sns_sent(self):
        # Arrange
        subject = FanEventPublisher(
            "arn:aws:sns:us-east-1:112280397275:lutil_fan_events_test"
        )
        process_id = subject.generate_process_id()
        task = TaskRecord(process_id=process_id, process_name="procA", task_name="#1")

        # Act
        results = subject.fan_out(
            process_id, "keyword_blast", "document-1", task.json()
        )
        print(results)

        # Assert
        self.assertEqual(results.event_source, "keyword_blast")
        self.assertEqual(results.event_name, "fan_out")
