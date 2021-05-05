import os

os.environ[
    "TABLE_NAME"
] = "lutils-FanProcessingTableTest-X541MIGMFYBW"  # put up here because Lambda caches code using this variable between executions
import inspect
import json
import os
import sys

import boto3
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

EVENT_ALL = {
    "Records": [
        {
            "eventID": "080ff8a233fb69e74ef8f1130f0cfa00",
            "eventName": "INSERT",
            "eventVersion": "1.1",
            "eventSource": "aws:dynamodb",
            "awsRegion": "us-east-1",
            "dynamodb": {
                "ApproximateCreationDateTime": 1619955850.0,
                "Keys": {
                    "pk": {
                        "S": "FAN-OUT-JOB#b530ebf0-ab3b-11eb-b19b-acde48001122-TASK#task C"
                    }
                },
                "NewImage": {
                    "task_name": {"S": "task C"},
                    "process_id": {"S": "b530ebf0-ab3b-11eb-b19b-acde48001122"},
                    "process_name": {"S": "processA"},
                    "pk": {
                        "S": "FAN-OUT-JOB#b530ebf0-ab3b-11eb-b19b-acde48001122-TASK#task C"
                    },
                    "message": {"S": '{\n   "keywords": "hello world"\n}'},
                    "completion_sns_arn": {"S": "sns-arn"},
                    "status": {"S": "created"},
                    "status_change_timestamp": {"S": "2021-05-02T07:44:09.627753"},
                    "timestamp": {"S": "2021-05-02T07:44:09.627604"},
                },
                "SequenceNumber": "3774300000000008979127455",
                "SizeBytes": 366,
                "StreamViewType": "NEW_AND_OLD_IMAGES",
            },
            "eventSourceARN": "arn:aws:dynamodb:us-east-1:112280397275:table/lutils-FanProcessingTableTest-X541MIGMFYBW/stream/2021-05-01T16:26:21.720",
        },
        {
            "eventID": "d61e2f695e9d175627339502c4010162",
            "eventName": "INSERT",
            "eventVersion": "1.1",
            "eventSource": "aws:dynamodb",
            "awsRegion": "us-east-1",
            "dynamodb": {
                "ApproximateCreationDateTime": 1619955850.0,
                "Keys": {
                    "pk": {
                        "S": "FAN-OUT-JOB#b5be9c3e-ab3b-11eb-b19b-acde48001122-TASK#task B"
                    }
                },
                "NewImage": {
                    "task_name": {"S": "task B"},
                    "process_id": {"S": "b5be9c3e-ab3b-11eb-b19b-acde48001122"},
                    "process_name": {"S": "processA"},
                    "pk": {
                        "S": "FAN-OUT-JOB#b5be9c3e-ab3b-11eb-b19b-acde48001122-TASK#task B"
                    },
                    "message": {"S": '{\n   "keywords": "api"\n}'},
                    "completion_sns_arn": {"S": "sns-arn"},
                    "status": {"S": "created"},
                    "status_change_timestamp": {"S": "2021-05-02T07:44:10.759104"},
                    "timestamp": {"S": "2021-05-02T07:44:10.556342"},
                },
                "SequenceNumber": "3774400000000008979127620",
                "SizeBytes": 358,
                "StreamViewType": "NEW_AND_OLD_IMAGES",
            },
            "eventSourceARN": "arn:aws:dynamodb:us-east-1:112280397275:table/lutils-FanProcessingTableTest-X541MIGMFYBW/stream/2021-05-01T16:26:21.720",
        },
        {
            "eventID": "dd7ad73b5f48a7816fc38465be381d42",
            "eventName": "REMOVE",
            "eventVersion": "1.1",
            "eventSource": "aws:dynamodb",
            "awsRegion": "us-east-1",
            "dynamodb": {
                "ApproximateCreationDateTime": 1619956024.0,
                "Keys": {
                    "pk": {
                        "S": "26a551c4-aa81-11eb-b1c3-acde48001122-2021-05-01T09:28:44.086742-task C"
                    }
                },
                "OldImage": {
                    "task_name": {"S": "task C"},
                    "process_id": {"S": "26a551c4-aa81-11eb-b1c3-acde48001122"},
                    "process_name": {"S": "processA"},
                    "pk": {
                        "S": "26a551c4-aa81-11eb-b1c3-acde48001122-2021-05-01T09:28:44.086742-task C"
                    },
                    "message": {"S": '{"keywords": "hello world"}'},
                    "status": {"S": "created"},
                    "status_change_timestamp": {"S": "2021-05-01T09:28:44.086872"},
                    "timestamp": {"S": "2021-05-01T09:28:44.086864"},
                },
                "SequenceNumber": "3774500000000008979178778",
                "SizeBytes": 356,
                "StreamViewType": "NEW_AND_OLD_IMAGES",
            },
            "eventSourceARN": "arn:aws:dynamodb:us-east-1:112280397275:table/lutils-FanProcessingTableTest-X541MIGMFYBW/stream/2021-05-01T16:26:21.720",
        },
    ]
}


EVENT_INSERT = {
    "Records": [
        {
            "eventID": "080ff8a233fb69e74ef8f1130f0cfa00",
            "eventName": "INSERT",
            "eventVersion": "1.1",
            "eventSource": "aws:dynamodb",
            "awsRegion": "us-east-1",
            "dynamodb": {
                "ApproximateCreationDateTime": 1619955850.0,
                "Keys": {
                    "pk": {
                        "S": "FAN-OUT-JOB#b530ebf0-ab3b-11eb-b19b-acde48001122-TASK#task C"
                    }
                },
                "NewImage": {
                    "task_name": {"S": "task C"},
                    "process_id": {"S": "b530ebf0-ab3b-11eb-b19b-acde48001122"},
                    "process_name": {"S": "processA"},
                    "pk": {
                        "S": "FAN-OUT-JOB#b530ebf0-ab3b-11eb-b19b-acde48001122-TASK#task C"
                    },
                    "message": {"S": '{\n   "keywords": "hello world"\n}'},
                    "completion_sns_arn": {"S": "sns-arn"},
                    "status": {"S": "created"},
                    "status_change_timestamp": {"S": "2021-05-02T07:44:09.627753"},
                    "timestamp": {"S": "2021-05-02T07:44:09.627604"},
                },
                "SequenceNumber": "3774300000000008979127455",
                "SizeBytes": 366,
                "StreamViewType": "NEW_AND_OLD_IMAGES",
            },
            "eventSourceARN": "arn:aws:dynamodb:us-east-1:112280397275:table/lutils-FanProcessingTableTest-X541MIGMFYBW/stream/2021-05-01T16:26:21.720",
        }
    ]
}

EVENT_INSERT_INVALID_SNS_ARN = {
    "Records": [
        {
            "eventID": "080ff8a233fb69e74ef8f1130f0cfa00",
            "eventName": "INSERT",
            "eventVersion": "1.1",
            "eventSource": "aws:dynamodb",
            "awsRegion": "us-east-1",
            "dynamodb": {
                "ApproximateCreationDateTime": 1619955850.0,
                "Keys": {
                    "pk": {
                        "S": "FAN-OUT-JOB#b530ebf0-ab3b-11eb-b19b-acde48001122-TASK#task C"
                    }
                },
                "NewImage": {
                    "task_name": {"S": "task C"},
                    "process_id": {"S": "b530ebf0-ab3b-11eb-b19b-acde48001122"},
                    "process_name": {"S": "processA"},
                    "pk": {
                        "S": "FAN-OUT-JOB#b530ebf0-ab3b-11eb-b19b-acde48001122-TASK#task C"
                    },
                    "message": {"S": '{\n   "keywords": "hello world"\n}'},
                    "completion_sns_arn": {"S": "sns-arn"},
                    "status": {"S": "created"},
                    "status_change_timestamp": {"S": "2021-05-02T07:44:09.627753"},
                    "timestamp": {"S": "2021-05-02T07:44:09.627604"},
                },
                "SequenceNumber": "3774300000000008979127455",
                "SizeBytes": 366,
                "StreamViewType": "NEW_AND_OLD_IMAGES",
            },
            "eventSourceARN": "arn:aws:dynamodb:us-east-1:112280397275:table/lutils-FanProcessingTableTest-X541MIGMFYBW/stream/2021-05-01T16:26:21.720",
        }
    ]
}


EVENT_INSERT_3 = {
    "Records": [
        {
            "eventID": "080ff8a233fb69e74ef8f1130f0cfa00",
            "eventName": "INSERT",
            "eventVersion": "1.1",
            "eventSource": "aws:dynamodb",
            "awsRegion": "us-east-1",
            "dynamodb": {
                "ApproximateCreationDateTime": 1619955850.0,
                "Keys": {
                    "pk": {
                        "S": "FAN-OUT-JOB#b530ebf0-ab3b-11eb-b19b-acde48001122-TASK#task C"
                    }
                },
                "NewImage": {
                    "task_name": {"S": "task C"},
                    "process_id": {"S": "b530ebf0-ab3b-11eb-b19b-acde48001122"},
                    "process_name": {"S": "processA"},
                    "pk": {
                        "S": "FAN-OUT-JOB#b530ebf0-ab3b-11eb-b19b-acde48001122-TASK#task C"
                    },
                    "message": {"S": '{\n   "keywords": "hello world"\n}'},
                    "completion_sns_arn": {"S": "sns-arn"},
                    "status": {"S": "created"},
                    "status_change_timestamp": {"S": "2021-05-02T07:44:09.627753"},
                    "timestamp": {"S": "2021-05-02T07:44:09.627604"},
                },
                "SequenceNumber": "3774300000000008979127455",
                "SizeBytes": 366,
                "StreamViewType": "NEW_AND_OLD_IMAGES",
            },
            "eventSourceARN": "arn:aws:dynamodb:us-east-1:112280397275:table/lutils-FanProcessingTableTest-X541MIGMFYBW/stream/2021-05-01T16:26:21.720",
        },
        {
            "eventID": "080ff8a233fb69e74ef8f1130f0cfa00",
            "eventName": "INSERT",
            "eventVersion": "1.1",
            "eventSource": "aws:dynamodb",
            "awsRegion": "us-east-1",
            "dynamodb": {
                "ApproximateCreationDateTime": 1619955850.0,
                "Keys": {
                    "pk": {
                        "S": "FAN-OUT-JOB#b530ebf0-ab3b-11eb-b19b-acde48001122-TASK#task C"
                    }
                },
                "NewImage": {
                    "task_name": {"S": "task C"},
                    "process_id": {"S": "b530ebf0-ab3b-11eb-b19b-acde48001122"},
                    "process_name": {"S": "processB"},
                    "pk": {
                        "S": "FAN-OUT-JOB#b530ebf0-ab3b-11eb-b19b-acde48001122-TASK#task C"
                    },
                    "message": {"S": '{\n   "keywords": "hello world"\n}'},
                    "completion_sns_arn": {"S": "sns-arn"},
                    "status": {"S": "created"},
                    "status_change_timestamp": {"S": "2021-05-02T07:44:09.627753"},
                    "timestamp": {"S": "2021-05-02T07:44:09.627604"},
                },
                "SequenceNumber": "3774300000000008979127455",
                "SizeBytes": 366,
                "StreamViewType": "NEW_AND_OLD_IMAGES",
            },
            "eventSourceARN": "arn:aws:dynamodb:us-east-1:112280397275:table/lutils-FanProcessingTableTest-X541MIGMFYBW/stream/2021-05-01T16:26:21.720",
        },
        {
            "eventID": "080ff8a233fb69e74ef8f1130f0cfa00",
            "eventName": "INSERT",
            "eventVersion": "1.1",
            "eventSource": "aws:dynamodb",
            "awsRegion": "us-east-1",
            "dynamodb": {
                "ApproximateCreationDateTime": 1619955850.0,
                "Keys": {
                    "pk": {
                        "S": "FAN-OUT-JOB#b530ebf0-ab3b-11eb-b19b-acde48001122-TASK#task C"
                    }
                },
                "NewImage": {
                    "task_name": {"S": "task C"},
                    "process_id": {"S": "b530ebf0-ab3b-11eb-b19b-acde48001122"},
                    "process_name": {"S": "processC"},
                    "pk": {
                        "S": "FAN-OUT-JOB#b530ebf0-ab3b-11eb-b19b-acde48001122-TASK#task C"
                    },
                    "message": {"S": '{\n   "keywords": "hello world"\n}'},
                    "completion_sns_arn": {"S": "sns-arn"},
                    "status": {"S": "created"},
                    "status_change_timestamp": {"S": "2021-05-02T07:44:09.627753"},
                    "timestamp": {"S": "2021-05-02T07:44:09.627604"},
                },
                "SequenceNumber": "3774300000000008979127455",
                "SizeBytes": 366,
                "StreamViewType": "NEW_AND_OLD_IMAGES",
            },
            "eventSourceARN": "arn:aws:dynamodb:us-east-1:112280397275:table/lutils-FanProcessingTableTest-X541MIGMFYBW/stream/2021-05-01T16:26:21.720",
        },
    ]
}


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


class FanHandlerIntOldTests(unittest.TestCase):
    def test_lambda_handler__given_single_insert_event__then_one_sns_sent(self):
        # Arrange
        os.environ["HANDLER_SNS_TOPIC_ARN"] = get_sns_arn_from_stack("FanEventsTestSNS")

        # Act
        results = app.lambda_handler(EVENT_INSERT, {})

        # Assert
        expected = {"inserted": {"processA": 1}}
        self.assertEqual(results, expected)

    def test_lambda_handler__given_three_insert_events__then_three_sns_sent(self):
        # Arrange
        os.environ["HANDLER_SNS_TOPIC_ARN"] = get_sns_arn_from_stack("FanEventsTestSNS")

        # Act
        results = app.lambda_handler(EVENT_INSERT_3, {})

        # Assert
        expected = {"inserted": {"processA": 1, "processB": 1, "processC": 1}}
        self.assertEqual(results, expected)


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


class FanHandlerIntTests(unittest.TestCase):
    def test_lambda_handler__given_single_insert_event__then_one_sns_sent(self):
        # Arrange
        os.environ["HANDLER_SNS_TOPIC_ARN"] = "fake-topic"
        os.environ["TABLE_NAME"] = "table-name"

        # Act
        with mock.patch(
            "lutil_fan_handler.app.send_start_sns_message",
            mock.MagicMock(return_value="Fake sent!"),
        ):
            with mock.patch(
                "lutil_fan_handler.app.call_dynamodb",
                mock.MagicMock(return_value="Fake sent!"),
            ):
                results = app.lambda_handler(FAN_OUT, {})

        # Assert
        expected = {"inserted": {"processA": 1}}
        self.assertEqual(results, expected)