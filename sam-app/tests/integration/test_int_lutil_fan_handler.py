import os
import boto3


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


os.environ["HANDLER_SNS_TOPIC_ARN"] = get_output_from_stack("FanEventsTestSNS")

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
                "Message": '{\n   "event_source": "fan handler tests",\n   "event_name": "fan_out",\n   "message": {\n      "process_id": "00-int-00",\n      "process_name": "fan handler tests",\n      "task_name": "task-9",\n      "task_message": {\n         "var_1": 297\n      },\n      \n      "created": "2021-05-04T22:53:46.738623"\n   },\n   "timestamp": "2021-05-04T22:53:46.738664"\n}',
                "Timestamp": "2021-05-04T22:53:46.749Z",
                "SignatureVersion": "1",
                "Signature": "v+N06nbQXbuoyP56Gwvbybz60feJKiMZ9sk9CnBGMNP85uIZ1c3Fvuozm+oPPgCmgyd1LPi+JUFxhLd52UaIewWXIRzZKErcOBsIrF30C+YIIyipKs8TEGp+B3vUhHAJVh/5px6u0H1EcMks/JFmJ/tepJj26JqBqEUHk3hvKtixPq37DIfY/o2ozNKu/AFAQmBXmUAGw6WMqFE7U761mojGO0fdD2HqIqxTUbmy6NY9mtck8Wvudtxq6mqKXlguG5KPSxp2IsW/bWYR2KPtK/1rVaC5OvWn3GS8kWwQ4+y8IeL+NfpfSx3tW2r2PvWKItBofNbFb+cwcT541Po/yg==",
                "SigningCertUrl": "https://sns.us-east-1.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem",
                "UnsubscribeUrl": "https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:112280397275:lutil_fan_events_test:65c9d2d8-1b58-4a31-b16d-59f83e78ca31",
                "MessageAttributes": {
                    "process_name": {"Type": "String", "Value": "fan handler tests"},
                    "event_name": {"Type": "String", "Value": "fan_out"},
                    "event_source": {"Type": "String", "Value": "fan handler tests"},
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
                "Message": '{"event_source": "lutils-FanTestE2EConsumerLambda-1VQQ5T0QWZE1S", "event_name": "task_started", "message": {"pk": "PROCESS#01F59Y46K6MK6DA3XT9WCH0VXY", "sk": "TASK#task-6", "gs1_pk": "-", "gs1_sk": "-", "process_id": "01F59Y46K6MK6DA3XT9WCH0VXY", "process_name": "e2e tests", "task_name": "task-6", "task_message": {"max_delay": 300}, "status": "created", "status_changed_timestamp": "", "created": "2021"}, "timestamp": ""}',
                "Timestamp": "2021-05-04T22:53:46.749Z",
                "SignatureVersion": "1",
                "Signature": "v+N06nbQXbuoyP56Gwvbybz60feJKiMZ9sk9CnBGMNP85uIZ1c3Fvuozm+oPPgCmgyd1LPi+JUFxhLd52UaIewWXIRzZKErcOBsIrF30C+YIIyipKs8TEGp+B3vUhHAJVh/5px6u0H1EcMks/JFmJ/tepJj26JqBqEUHk3hvKtixPq37DIfY/o2ozNKu/AFAQmBXmUAGw6WMqFE7U761mojGO0fdD2HqIqxTUbmy6NY9mtck8Wvudtxq6mqKXlguG5KPSxp2IsW/bWYR2KPtK/1rVaC5OvWn3GS8kWwQ4+y8IeL+NfpfSx3tW2r2PvWKItBofNbFb+cwcT541Po/yg==",
                "SigningCertUrl": "https://sns.us-east-1.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem",
                "UnsubscribeUrl": "https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:112280397275:lutil_fan_events_test:65c9d2d8-1b58-4a31-b16d-59f83e78ca31",
                "MessageAttributes": {
                    "process_name": {"Type": "String", "Value": "fan handler tests"},
                    "event_name": {"Type": "String", "Value": "task_started"},
                    "event_source": {"Type": "String", "Value": "fan handler tests"},
                },
            },
        }
    ]
}

TASK_COMPLETED_SNS = {
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
                "Message": '{"event_source": "lutils-FanTestE2EConsumerLambda-1VQQ5T0QWZE1S", "event_name": "task_completed", "message": {"pk": "PROCESS#01F59Y46K6MK6DA3XT9WCH0VXY", "sk": "TASK#task-6", "gs1_pk": "-", "gs1_sk": "-", "process_id": "01F59Y46K6MK6DA3XT9WCH0VXY", "process_name": "e2e tests", "task_name": "task-6", "task_message": {"max_delay": 300}, "status": "task_completed", "status_changed_timestamp": "", "created": "2021"}, "timestamp": ""}',
                "Timestamp": "2021-05-04T22:53:46.749Z",
                "SignatureVersion": "1",
                "Signature": "v+N06nbQXbuoyP56Gwvbybz60feJKiMZ9sk9CnBGMNP85uIZ1c3Fvuozm+oPPgCmgyd1LPi+JUFxhLd52UaIewWXIRzZKErcOBsIrF30C+YIIyipKs8TEGp+B3vUhHAJVh/5px6u0H1EcMks/JFmJ/tepJj26JqBqEUHk3hvKtixPq37DIfY/o2ozNKu/AFAQmBXmUAGw6WMqFE7U761mojGO0fdD2HqIqxTUbmy6NY9mtck8Wvudtxq6mqKXlguG5KPSxp2IsW/bWYR2KPtK/1rVaC5OvWn3GS8kWwQ4+y8IeL+NfpfSx3tW2r2PvWKItBofNbFb+cwcT541Po/yg==",
                "SigningCertUrl": "https://sns.us-east-1.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem",
                "UnsubscribeUrl": "https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:112280397275:lutil_fan_events_test:65c9d2d8-1b58-4a31-b16d-59f83e78ca31",
                "MessageAttributes": {
                    "process_name": {"Type": "String", "Value": "fan handler tests"},
                    "event_name": {"Type": "String", "Value": "task_completed"},
                    "event_source": {"Type": "String", "Value": "fan handler tests"},
                },
            },
        }
    ]
}


class FanHandlerIntTests(unittest.TestCase):
    def test_lambda_handler__given_fan_out__then_one_sns_sent(self):
        # Arrange
        # repeat down here in case other test sets this
        os.environ["TABLE_NAME"] = get_output_from_stack(
            "FanProcessingPartTestTableName"
        )

        # Act
        results = app.lambda_handler(FAN_OUT_SNS, {})

        # Assert
        expected_record = {
            "pk": "PROCESS#00-int-00",
            "sk": "TASK#task-9",
            "gs1_pk": "-",
            "gs1_sk": "-",
            "process_id": "00-int-00",
            "process_name": "fan handler tests",
            "task_name": "task-9",
            "task_message": {"var_1": 297},
            "status": "created",
            "created": "",
            "status_changed_timestamp": "2021-05-09T21:51:19.962194",
            "ttl": "123",
        }
        results_record = results["fan_out"][0]
        print("*results_record:")
        print(json.dumps(results_record, indent=3, default=str))
        print("*expected_record:")
        print(json.dumps(expected_record, indent=3, default=str))

        self.assertEqual(results_record["pk"], expected_record["pk"])
        self.assertEqual(results_record["status"], expected_record["status"])

    def test_lambda_handler__given_task_started__then_one_sns_sent(self):
        # Arrange
        # repeat down here in case other test sets this
        os.environ["TABLE_NAME"] = get_output_from_stack(
            "FanProcessingPartTestTableName"
        )

        # Act
        action = "task_started"
        results = app.lambda_handler(TASK_STARTED_SNS, {})

        # Assert
        expected_record = {
            "pk": "PROCESS#01F59Y46K6MK6DA3XT9WCH0VXY",
            "sk": "TASK#task-6",
            "gs1_pk": "-",
            "gs1_sk": "-",
            "process_id": "",
            "process_name": "e2e tests",
            "task_name": "task-6",
            "task_message": {"max_delay": 300},
            "status": "task_started",
            "status_changed_timestamp": "2021-05-09T21:47:58.143252",
            "created": "2021",
            "ttl": "123",
        }
        results_record = results[action][0]

        print("*results_record:")
        print(json.dumps(results_record, indent=3, default=str))
        print("*expected_record:")
        print(json.dumps(expected_record, indent=3, default=str))

        self.assertEqual(results_record["pk"], expected_record["pk"])
        self.assertEqual(results_record["status"], expected_record["status"])

    def test_lambda_handler__given_task_completed__then_one_sns_sent(self):
        # Arrange
        # repeat down here in case other test sets this
        os.environ["TABLE_NAME"] = get_output_from_stack(
            "FanProcessingPartTestTableName"
        )

        # Act
        action = "task_completed"
        results = app.lambda_handler(TASK_COMPLETED_SNS, {})

        # Assert
        expected_record = {
            "pk": "PROCESS#01F59Y46K6MK6DA3XT9WCH0VXY",
            "sk": "TASK#task-6",
            "gs1_pk": "-",
            "gs1_sk": "-",
            "process_id": "",
            "process_name": "e2e tests",
            "task_name": "task-6",
            "task_message": {"max_delay": 300},
            "status": "task_completed",
            "status_changed_timestamp": "2021-05-09T21:47:58.143252",
            "created": "2021",
            "ttl": "123",
        }
        results_record = results[action][0]

        print("*results_record:")
        print(json.dumps(results_record, indent=3, default=str))
        print("*expected_record:")
        print(json.dumps(expected_record, indent=3, default=str))

        self.assertEqual(results_record["pk"], expected_record["pk"])
        self.assertEqual(results_record["status"], expected_record["status"])