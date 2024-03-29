import inspect
import json
from logging import Formatter
import os
import sys

import boto3
import ulid

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/common_layer_hex/python"
sys.path.insert(0, parentdir)
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/lutil_fan_dbstream_handler"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

import unittest
from unittest import mock


from common_layer_hex.python.domain.FanManager import FanManager
from common_layer_hex.python.infrastructure.repository.DynamoDBRepository import (
    DynamoDBRepository,
)
from common_layer_hex.python.infrastructure.notifications.TestNotifier import (
    TestNotifier,
)
from common_layer_hex.python.domain.TaskDTO import TaskDTO
from common_layer_hex.python.domain.ProcessDTO import ProcessDTO
from common_layer_hex.python.infrastructure.repository.DynamoDB import DynamoDB
from lutil_fan_dbstream_handler.app import *


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


class DBStreamLambdaIntTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sns_arn = get_output_from_stack("FanEventsTestSNS")
        os.environ["HANDLER_SNS_TOPIC_ARN"] = sns_arn
        table_name = get_output_from_stack("FanProcessingPartTestTableName")
        os.environ["TABLE_NAME"] = table_name

        cls.repo = DynamoDBRepository(table_name)
        cls.notifier = TestNotifier("fake")
        cls.fan_manager = FanManager(cls.repo, cls.notifier)

    def create_process_with_two_tasks(self):
        task_1 = TaskDTO("task 01", {"action": "go"})
        task_2 = TaskDTO("task 02", {"action": "save"})
        process = ProcessDTO(process_name="DBStreamLambdaIntTests", information="")
        fan_results = self.fan_manager.start_process(process, [task_1, task_2])
        return fan_results.updated_process

    def test_lambda_hander__given_fan_out_event__then_no_exceptions(
        self,
    ):
        # Arrange
        new_process = self.create_process_with_two_tasks()
        print(new_process)
        task_list = self.repo.get_tasks_for_process(new_process)
        print("\n\n\n")
        print(task_list)

        # Act
        event_fan_out = {
            "Records": [
                {
                    "eventID": "f1c2fa59c0b128193cf9575ed54811d2",
                    "eventName": "INSERT",
                    "eventVersion": "1.1",
                    "eventSource": "aws:dynamodb",
                    "awsRegion": "us-east-1",
                    "dynamodb": {
                        "ApproximateCreationDateTime": 1621025176.0,
                        "Keys": {
                            "sk": {"S": "TASK#task_00"},
                            "pk": {"S": "PROCESS#123456789"},
                        },
                        "NewImage": {
                            "task_name": {"S": "task001"},
                            "process_id": {"S": "123456789"},
                            "status_changed_timestamp": {
                                "S": "2021-05-14T16:46:16.627334"
                            },
                            "task_message": {"S": "\"{'go': 'caps!'}\""},
                            "created": {"S": "2021-05-14T16:46:16.627306"},
                            "process_name": {"S": "DBStreamLambdaIntTests"},
                            "sk": {"S": "TASK#task_00"},
                            "gs1_pk": {"S": "-"},
                            "pk": {"S": "PROCESS#123456789"},
                            "gs1_sk": {"S": "-"},
                            "status": {"S": "fan_out"},
                        },
                        "SequenceNumber": "875400000000009959396144",
                        "SizeBytes": 325,
                        "StreamViewType": "NEW_AND_OLD_IMAGES",
                    },
                    "eventSourceARN": "arn:aws:dynamodb:us-east-1:112280397275:table/lutils-FanProcessingPartTestTable-Q3PVEB6MO2AJ/stream/2021-05-14T13:21:33.706",
                },
            ]
        }

        # Act
        results = lambda_handler(event_fan_out, "")
        print(json.dumps(results, indent=3, default=str))

        # Assert
        process = self.repo.get_process(new_process.process_id)
        self.assertEqual(process.progress, 0)


if __name__ == "__main__":
    unittest.main()
