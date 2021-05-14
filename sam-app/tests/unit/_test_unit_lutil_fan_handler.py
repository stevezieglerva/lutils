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
parentdir = os.path.dirname(parentdir) + "/lutil_fan_handler"
sys.path.insert(0, parentdir)
parentdir = os.path.dirname(parentdir) + "/common_layer/python"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

import unittest
from unittest import mock

from lutil_fan_handler import app
from moto import mock_dynamodb2

FAN_OUT = {
    "Records": [
        {
            "EventSource": "aws:sns",
            "EventVersion": "1.0",
            "EventSubscriptionArn": "arn:aws:sns:us-east-1:112280397275:lutil_fan_events_test:65c9d2d8-1b58-4a31-b16d-59f83e78ca31",
            "Sns": {
                "Type": "Notification",
                "MessageId": "24c29dfb-f208-5e91-aee5-c4f020b25459",
                "TopicArn": "arn:aws:sns:us-east-1:112280397275:lutil_fan_events_test",
                "Subject": None,
                "Message": '{\n   "event_source": "e2e tests",\n   "event_name": "fan_out",\n   "message": {\n      "process_id": "lhklhk-099087gjg87t8-ohoiuyiuh",\n      "process_name": "e2e tests",\n      "task_name": "task-9",\n      "task_message": {\n         "var_1": 297\n      },\n        "timestamp": "2021-05-04T22:53:46.738623"\n   },\n   "timestamp": "2021-05-04T22:53:46.738664"\n}',
                "Timestamp": "2021-05-04T22:53:46.749Z",
                "SignatureVersion": "1",
                "Signature": "v+N06nbQXbuoyP56Gwvbybz60feJKiMZ9sk9CnBGMNP85uIZ1c3Fvuozm+oPPgCmgyd1LPi+JUFxhLd52UaIewWXIRzZKErcOBsIrF30C+YIIyipKs8TEGp+B3vUhHAJVh/5px6u0H1EcMks/JFmJ/tepJj26JqBqEUHk3hvKtixPq37DIfY/o2ozNKu/AFAQmBXmUAGw6WMqFE7U761mojGO0fdD2HqIqxTUbmy6NY9mtck8Wvudtxq6mqKXlguG5KPSxp2IsW/bWYR2KPtK/1rVaC5OvWn3GS8kWwQ4+y8IeL+NfpfSx3tW2r2PvWKItBofNbFb+cwcT541Po/yg==",
                "SigningCertUrl": "https://sns.us-east-1.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem",
                "UnsubscribeUrl": "https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:112280397275:lutil_fan_events_test:65c9d2d8-1b58-4a31-b16d-59f83e78ca31",
                "MessageAttributes": {
                    "process_name": {"Type": "String", "Value": "e2e tests"},
                    "event_name": {"Type": "String", "Value": "fan_out"},
                    "event_source": {"Type": "String", "Value": "e2e tests"},
                },
            },
        }
    ]
}


class FanHandlerUnitTests(unittest.TestCase):
    @mock_dynamodb2
    def test_lambda_handler__given_single_insert_event__then_one_sns_sent(self):
        # Arrange
        db = boto3.client("dynamodb")
        db.create_table(
            TableName=os.environ["TABLE_NAME"],
            KeySchema=[{"AttributeName": "key_field", "KeyType": "HASH"}],
            AttributeDefinitions=[
                {"AttributeName": "key_field", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
        )

        # Act
        with mock.patch(
            "lutil_fan_handler.app.publish_next_event",
            mock.MagicMock(return_value="Fake sent!"),
        ):
            with mock.patch(
                "lutil_fan_handler.app.call_dynamodb",
                mock.MagicMock(return_value="Fake sent!"),
            ):
                results = app.lambda_handler(FAN_OUT, {})

        # Assert
        expected = {
            "table_name": "table-name",
            "fan_out": [
                {
                    "pk": "PROCESS#lhklhk-099087gjg87t8-ohoiuyiuh",
                    "sk": "TASK#task-9",
                    "gs1_pk": "-",
                    "gs1_sk": "-",
                    "process_id": "lhklhk-099087gjg87t8-ohoiuyiuh",
                    "process_name": "e2e tests",
                    "task_name": "task-9",
                    "task_message": '{\n   "var_1": 297\n}',
                    "status": "created",
                    "created": "",
                    "status_changed_timestamp": "2021-05-07T17:13:14.078883",
                }
            ],
        }

        expected["fan_out"][0].pop("created")
        expected["fan_out"][0].pop("status_changed_timestamp")
        results["fan_out"][0].pop("created")
        results["fan_out"][0].pop("status_changed_timestamp")

        self.assertEqual(results["fan_out"][0]["pk"], expected["fan_out"][0]["pk"])
