import inspect
import json
import os
import sys

import boto3
from moto import mock_dynamodb2


def get_output_from_stack(output_key):
    cloudformation = boto3.client("cloudformation")
    stacks = cloudformation.describe_stacks(StackName="lutils")
    stack_outputs = stacks["Stacks"][0]["Outputs"]
    s3_bucket = ""
    for output in stack_outputs:
        if output["OutputKey"] == output_key:
            output_value = output["OutputValue"]
            break
    return output_value


os.environ["TABLE_NAME"] = get_output_from_stack(
    "FanProcessingPartTestTableName"
)  # put up here because Lambda caches code using this variable between executions

os.environ["HANDLER_SNS_TOPIC_ARN"] = "fake-sns"

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/lutil_fan_start_process"
sys.path.insert(0, parentdir)
parentdir = os.path.dirname(parentdir) + "/common_layer_hex/python"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

import unittest
from unittest import mock

from lutil_fan_start_process import app
from ProcessDTO import ProcessDTO
from TaskDTO import TaskDTO
from FakeRepository import FakeRepository
from TestNotifier import TestNotifier
from StartProcessAdapter import *


class StartProcessAdapterUnitTests(unittest.TestCase):
    def test_start_process__given_valid_event__then_no_exceptions(self):
        # Arrange
        event = {
            "process": {"process_name": "proc A"},
            "tasks": [
                {"task_name": "task 1", "task_message": {"hello": "world"}},
                {"task_name": "task 2", "task_message": {"apple": "pear"}},
            ],
        }
        db = FakeRepository("fake")
        notifier = TestNotifier("test")
        adapter = StartProcessAdapter(db, notifier)

        # Act
        results = adapter.start_process(event)
        print(results)

        # Assert
        self.assertEqual(results.updated_process.process_name, "proc A")
        self.assertTrue(results.updated_process.process_id != "")
        self.assertEqual(results.event_notifications[0].event_name, "process_started")
