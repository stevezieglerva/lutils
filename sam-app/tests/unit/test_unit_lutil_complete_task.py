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
parentdir = os.path.dirname(parentdir) + "/lutil_fan_complete_task"
sys.path.insert(0, parentdir)
parentdir = os.path.dirname(parentdir) + "/common_layer_hex/python"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

import unittest
from unittest import mock


from domain.ProcessDTO import ProcessDTO
from domain.TaskDTO import TaskDTO
from infrastructure.repository.FakeRepository import FakeRepository
from infrastructure.notifications.TestNotifier import TestNotifier
from CompleteTaskAdapter import *


class CompleteTaskAdapterUnitTests(unittest.TestCase):
    def test_complete_task__given_valid_event__then_no_exceptions(self):
        # Arrange
        event = {"process_id": "123", "task_name": "hello world 001"}
        db = FakeRepository("fake")
        notifier = TestNotifier("test")
        adapter = CompleteTaskAdapter(db, notifier)

        # Act
        results = adapter.complete_task(event)
        print(results)

        # Assert
