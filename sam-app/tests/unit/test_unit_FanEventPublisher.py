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
        subject = FanEventPublisher("test_process_one", "test-sns-topic-arn")

        # Assert
        subject.topic_arn = "test-sns-topic-arn"
