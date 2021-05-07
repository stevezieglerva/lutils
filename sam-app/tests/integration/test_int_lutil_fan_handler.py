import os

os.environ[
    "TABLE_NAME"
] = "lutils-FanProcessingTableTest-X541MIGMFYBW"  # put up here because Lambda caches code using this variable between executions

import boto3


def get_sns_arn_from_stack(output_key):
    cloudformation = boto3.client("cloudformation")
    stacks = cloudformation.describe_stacks(StackName="lutils")
    stack_outputs = stacks["Stacks"][0]["Outputs"]
    s3_bucket = ""
    for output in stack_outputs:
        if output["OutputKey"] == output_key:
            output_value = output["OutputValue"]
            break
    return output_value


os.environ["HANDLER_SNS_TOPIC_ARN"] = get_sns_arn_from_stack("FanEventsTestSNS")

import inspect
import json
import os
import sys


from moto import mock_dynamodb2


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/lutil_fan_handler"
parentdir = os.path.dirname(parentdir) + "/common_layer/python"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

import unittest
from unittest import mock

from lutil_fan_handler import app


FAN_OUT_SNS = {
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
                "Message": '{\n   "event_source": "e2e tests",\n   "event_name": "fan_out",\n   "message": {\n      "process_id": "lhklhk-099087gjg87t8-ohoiuyiuh",\n      "process_name": "e2e tests",\n      "task_name": "task-9",\n      "message": {\n         "var_1": 297\n      },\n      \n      "timestamp": "2021-05-04T22:53:46.738623"\n   },\n   "timestamp": "2021-05-04T22:53:46.738664"\n}',
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


TASK_STARTED_SNS = {
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
                    "event_name": {"Type": "String", "Value": "task_started"},
                    "event_source": {"Type": "String", "Value": "e2e tests"},
                },
            },
        }
    ]
}


class FanHandlerIntTests(unittest.TestCase):
    def test_lambda_handler__given_fan_out__then_one_sns_sent(self):
        # Arrange

        # Act
        results = app.lambda_handler(FAN_OUT_SNS, {})

        # Assert
        expected = {
            "fan_out": [
                {
                    "process_id": "lhklhk-099087gjg87t8-ohoiuyiuh",
                    "process_name": "e2e tests",
                    "task_name": "task-9",
                    "message": {"var_1": 297},
                    "completion_sns_arn": "completion_sns_arn",
                    "timestamp": "2021-05-05T09:17:15.285217",
                    "pk": "FAN-OUT-JOB#lhklhk-099087gjg87t8-ohoiuyiuh-TASK#task-9",
                    "status": "created",
                    "status_change_timestamp": "2021-05-05T09:17:15.221737",
                }
            ]
        }
        expected["fan_out"][0].pop("timestamp")
        expected["fan_out"][0].pop("status_change_timestamp")
        results["fan_out"][0].pop("timestamp")
        results["fan_out"][0].pop("status_change_timestamp")
        self.assertEqual(results, expected)

    def test_lambda_handler__given_task_started__then_one_sns_sent(self):
        # Arrange

        # Act
        results = app.lambda_handler(TASK_STARTED_SNS, {})

        # Assert
        expected = {"inserted": {"processA": 1}}
        self.assertEqual(results, expected)