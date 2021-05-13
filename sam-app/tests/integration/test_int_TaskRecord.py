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


from common_layer.python.TaskRecord import *
from common_layer.python.DynamoDB import DynamoDB
from common_layer.python.FanEvent import *


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


os.environ["TABLE_NAME"] = get_output_from_stack("FanProcessingPartTestTableName")


class TaskRecordIntTests(unittest.TestCase):
    def test_start__given_valid_object__then_no_exceptions(self):
        # Arrange
        record = {
            "pk": "PROCESS#777-00",
            "sk": "TASK#93020939F",
            "gs1_pk": "-",
            "gs1_sk": "-",
            "process_name": "keyword blast",
            "status": "created",
            "task_name": "document-2",
            "status_changed_timestamp": "2021",
            "created": "2021",
            "task_message": "hello",
        }
        db = DynamoDB(os.environ["TABLE_NAME"])
        subject = TaskRecord(
            record_string=json.dumps(record, indent=3, default=str), db=db
        )

        # Act
        results = subject.start()
        print(results)

        # Assert
        added_item = db.get_item({"pk": "PROCESS#777-00", "sk": "TASK#93020939F"})
        self.assertEqual(added_item["status"], TASK_STARTED)

    def test_completed__given_valid_object__then_no_exceptions(self):
        # Arrange
        record = {
            "pk": "PROCESS#777-00",
            "sk": "TASK#93020939F",
            "gs1_pk": "-",
            "gs1_sk": "-",
            "process_name": "keyword blast",
            "status": "created",
            "task_name": "document-2",
            "status_changed_timestamp": "2021",
            "created": "2021",
            "task_message": "hello",
        }
        db = DynamoDB(os.environ["TABLE_NAME"])
        subject = TaskRecord(
            record_string=json.dumps(record, indent=3, default=str), db=db
        )

        # Act
        results = subject.complete()
        print(results)

        # Assert
        added_item = db.get_item({"pk": "PROCESS#777-00", "sk": "TASK#93020939F"})
        self.assertEqual(added_item["status"], TASK_COMPLETED)


if __name__ == "__main__":
    unittest.main()