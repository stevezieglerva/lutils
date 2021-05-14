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

from common_layer.python.TaskUpdateProcessor import *
from common_layer.python.TaskRecord import *


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


class TaskUpdateProcessorUnitTests(unittest.TestCase):
    def test_process__given_newly_created_fan_out__then_create_new_process_and_notify(
        self,
    ):
        # Arrange
        sns_arn = get_output_from_stack("FanEventsTestSNS")
        publisher = FanEventPublisher("TaskUpdateProcessorUnitTests", sns_arn)

        subject = TaskUpdateProcessor(publisher)
        record = {
            "pk": "PROCESS#888",
            "sk": "TASK#93020939F",
            "gs1_pk": "-",
            "gs1_sk": "",
            "process_id": "888",
            "process_name": "keyword blast",
            "status": "fan_out",
            "task_name": "document-2",
            "status_changed_timestamp": "2021",
            "created": "2021",
            "task_message": {"hello": "world"},
        }

        table_name = get_output_from_stack("FanProcessingPartTestTableName")
        db = DynamoDB(table_name)
        new_fan_out_task = TaskRecord(
            record_string=json.dumps(record, indent=3, default=str),
            db=db,
        )

        # Act
        results = subject.process_task(new_fan_out_task)
        print(json.dumps(results, indent=3, default=str))

        # Assert
        self.assertEqual(results["process_record"]["pk"], "PROCESS#888")
        self.assertEqual(results["event"], {"sns_sent": "yes"})


if __name__ == "__main__":
    unittest.main()