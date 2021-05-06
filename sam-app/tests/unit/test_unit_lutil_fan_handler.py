import os

os.environ[
    "TABLE_NAME"
] = "table-name"  # put up here because Lambda caches code using this variable between executions
os.environ["HANDLER_SNS_TOPIC_ARN"] = "fake-topic"

import inspect
import json

import sys

import boto3
from moto import mock_dynamodb2


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
                "Message": '{\n   "event_source": "e2e tests",\n   "event_name": "fan_out",\n   "job": {\n      "process_id": "lhklhk-099087gjg87t8-ohoiuyiuh",\n      "process_name": "e2e tests",\n      "task_name": "task-9",\n      "message": {\n         "var_1": 297\n      },\n      "completion_sns_arn": "completion_sns_arn",\n      "timestamp": "2021-05-04T22:53:46.738623"\n   },\n   "timestamp": "2021-05-04T22:53:46.738664"\n}',
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
    def test_lambda_handler__given_single_insert_event__then_one_sns_sent(self):
        # Arrange

        # Act
        with mock.patch(
            "lutil_fan_handler.app.FanEventPublisher.task_created",
            mock.MagicMock(return_value="Fake sent!"),
        ):
            with mock.patch(
                "lutil_fan_handler.app.call_dynamodb",
                mock.MagicMock(return_value="Fake sent!"),
            ):
                results = app.lambda_handler(FAN_OUT, {})

        # Assert
        expected = {
            "fan_out": [
                {
                    "completion_sns_arn": "completion_sns_arn",
                    "message": {"var_1": 297},
                    "pk": "FAN-OUT-JOB#lhklhk-099087gjg87t8-ohoiuyiuh-TASK#task-9",
                    "process_id": "lhklhk-099087gjg87t8-ohoiuyiuh",
                    "process_name": "e2e tests",
                    "status": "created",
                    "status_change_timestamp": "2021-05-05T22:37:26.629346",
                    "task_name": "task-9",
                    "timestamp": "2021-05-05T22:37:26.629708",
                }
            ]
        }

        expected["fan_out"][0].pop("timestamp")
        expected["fan_out"][0].pop("status_change_timestamp")
        results["fan_out"][0].pop("timestamp")
        results["fan_out"][0].pop("status_change_timestamp")
        self.assertEqual(results, expected)
