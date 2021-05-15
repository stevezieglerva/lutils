import inspect
import json
import os
import sys

import boto3
import ulid

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/common_layer/python"
sys.path.insert(0, parentdir)
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/lutil_fan_dbstream_handler"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

import unittest
from unittest import mock

from common_layer.python.TaskRecord import *
from common_layer.python.TaskUpdateProcessor import *
from common_layer.python.DynamoDB import DynamoDB
from lutil_fan_dbstream_handler.app import *
from FanEventPublisher import FanEventPublisher


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


class DBStreamLambdaIntTests(unittest.TestCase):
    def test_lambda_hander__given_fan_out_event__then_no_exceptions(
        self,
    ):
        # Arrange
        sns_arn = get_output_from_stack("FanEventsTestSNS")
        os.environ["HANDLER_SNS_TOPIC_ARN"] = sns_arn
        table_name = get_output_from_stack("FanProcessingPartTestTableName")
        os.environ["TABLE_NAME"] = table_name

        db = DynamoDB(table_name)
        task = TaskRecord(
            process_id="123456789",
            process_name="DBStreamLambdaIntTests",
            task_name="task001",
            task_message={"one": "two"},
            db=db,
        )
        task.fan_out()

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
                    "eventSourceARN": "arn:aws:dynamodb:us-east-1:112280397275:table/lutils2-FanProcessingPartTestTable-Q3PVEB6MO2AJ/stream/2021-05-14T13:21:33.706",
                },
            ]
        }

        # Act
        results = lambda_handler(event_fan_out, "")
        print(json.dumps(results, indent=3, default=str))

        # Assert
        process = db.get_item({"pk": "PROCESS#123456789", "sk": "PROCESS#123456789"})
        self.assertEqual(process["progress"], 0)

    def test_lambda_hander__given_completed__then_no_exceptions(
        self,
    ):
        # Arrange
        sns_arn = get_output_from_stack("FanEventsTestSNS")
        os.environ["HANDLER_SNS_TOPIC_ARN"] = sns_arn
        table_name = get_output_from_stack("FanProcessingPartTestTableName")
        os.environ["TABLE_NAME"] = table_name

        db = DynamoDB(table_name)
        task = TaskRecord(
            process_id="x123456789",
            process_name="DBStreamLambdaIntTests",
            task_name="task999",
            task_message={"one": "two"},
            db=db,
        )
        print("\nUpdate simulated task:")
        task.fan_out()
        task.start()
        task.complete()

        event_task_completed = {
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
                            "sk": {"S": "TASK#task999"},
                            "pk": {"S": "PROCESS#x123456789"},
                        },
                        "NewImage": {
                            "task_name": {"S": "task999"},
                            "process_id": {"S": "x123456789"},
                            "status_changed_timestamp": {
                                "S": "2021-05-14T16:46:16.627334"
                            },
                            "task_message": {"S": "\"{'go': 'caps!'}\""},
                            "created": {"S": "2021-05-14T16:46:16.627306"},
                            "process_name": {"S": "DBStreamLambdaIntTests"},
                            "sk": {"S": "TASK#task_00"},
                            "gs1_pk": {"S": "-"},
                            "pk": {"S": "PROCESS#x123456789"},
                            "gs1_sk": {"S": "-"},
                            "status": {"S": "task_completed"},
                        },
                        "SequenceNumber": "875400000000009959396144",
                        "SizeBytes": 325,
                        "StreamViewType": "NEW_AND_OLD_IMAGES",
                    },
                    "eventSourceARN": "arn:aws:dynamodb:us-east-1:112280397275:table/lutils2-FanProcessingPartTestTable-Q3PVEB6MO2AJ/stream/2021-05-14T13:21:33.706",
                },
            ]
        }

        # Act
        results = lambda_handler(event_task_completed, "")
        print(json.dumps(results, indent=3, default=str))

        # Assert
        process = db.get_item({"pk": "PROCESS#x123456789", "sk": "PROCESS#x123456789"})
        self.assertEqual(process["progress"], 1)


if __name__ == "__main__":
    unittest.main()
