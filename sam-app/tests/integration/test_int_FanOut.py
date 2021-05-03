import inspect
import json
import os
import sys

import boto3

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/lutil_fan_handler"
parentdir = os.path.dirname(parentdir) + "/common_layer/python"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from common_layer.python.FanOut import FanOut
from common_layer.python.DynamoDB import DynamoDB


def get_table_name_from_stack(output_key):
    cloudformation = boto3.client("cloudformation")
    stacks = cloudformation.describe_stacks(StackName="lutils")
    print(json.dumps(stacks, indent=3, default=str))
    stack_outputs = stacks["Stacks"][0]["Outputs"]
    s3_bucket = ""
    for output in stack_outputs:
        if output["OutputKey"] == output_key:
            output_value = output["OutputValue"]
            break
    return output_value


class FanOutIntTests(unittest.TestCase):
    def test_fan_out__given_one_task__then_item_added_to_db(self):
        # Arrange
        table_name = get_table_name_from_stack("FanProcesssingTestTableName")
        subject = FanOut("processA", "sns-arn", table_name)

        # Act
        results = subject.fan_out("task C", {"keywords": "hello world"})

        # Assert
        self.assertTrue("task C" in results)
        db = DynamoDB(table_name, "pk")
        added_item = db.get_item(results.pk)
        print(f"\n\n added item: {added_item}")
        added_item_str = json.dumps(added_item, indent=3, default=str)
        self.assertTrue("processA" in added_item_str)
        self.assertTrue("created" in added_item_str)
        self.assertTrue("pk" in added_item_str)

    def test_fan_out__given_three_tasks__then_item_added_to_db(self):
        # Arrange
        table_name = "lutils-FanProcessingTableTest-X541MIGMFYBW"
        subject = FanOut("processA", "sns-arn", table_name)

        # Act
        subject.fan_out("task A", {"keywords": "hello world"})
        subject.fan_out("task B", {"keywords": "api"})
        results = subject.fan_out("task C", {"keywords": "data governance"})

        # Assert
        db = DynamoDB(table_name, "pk")
        added_item = db.get_item(results.pk)
        print(f"\n\n added item: {added_item}")
        added_item_str = json.dumps(added_item, indent=3, default=str)
        self.assertTrue("processA" in added_item_str)
        self.assertTrue("task C" in added_item_str)