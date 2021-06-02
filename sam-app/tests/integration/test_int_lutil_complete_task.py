import inspect
import json
import os
import sys

import boto3
from moto import mock_dynamodb2


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

from lutil_fan_complete_task import app
from domain.ProcessDTO import ProcessDTO
from domain.TaskDTO import TaskDTO
from DynamoDBRepository import DynamoDBRepository
from SNSNotifier import *
from FanManager import *


def get_output_from_stack(output_key):
    cloudformation = boto3.client("cloudformation")
    stacks = cloudformation.describe_stacks(StackName="lutils2")
    stack_outputs = stacks["Stacks"][0]["Outputs"]
    s3_bucket = ""
    for output in stack_outputs:
        if output["OutputKey"] == output_key:
            output_value = output["OutputValue"]
            break
    return output_value


class LutilCompleteTaskUnitTests(unittest.TestCase):
    def test_lambda_handler__given_valid_event__then_no_exceptions(self):
        # Arrange
        os.environ["TABLE_NAME"] = get_output_from_stack(
            "FanProcessingPartTestTableName"
        )
        os.environ["HANDLER_SNS_TOPIC_ARN"] = get_output_from_stack("FanEventsTestSNS")

        repo = DynamoDBRepository(os.environ["TABLE_NAME"])
        notifier = SNSNotifier(os.environ["HANDLER_SNS_TOPIC_ARN"])
        subject = FanManager(repo, notifier)
        task_1 = TaskDTO("task 01", {"action": "go"})

        process = ProcessDTO("LutilCompleteTaskUnitTests")
        start_results = subject.start_process(process, [task_1])
        print(f"\n\nstart process: {start_results}")

        fan_out_results = subject.fan_out(start_results.updated_tasks)
        print(f"\n\nfan out: {fan_out_results}")

        event = {
            "process_id": start_results.updated_process.process_id,
            "task_name": fan_out_results.updated_tasks[0].task_name,
        }
        print("Testing event:")
        print(json.dumps(event, indent=3, default=str))

        # Act
        results = app.lambda_handler(event, "")

        # Assert
