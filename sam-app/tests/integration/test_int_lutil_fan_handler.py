import inspect
import json
import os
import sys

import boto3
from moto import mock_dynamodb2


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/lutil_fan_handler"
parentdir = os.path.dirname(parentdir) + "/common_layer"
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


class FanHandlerIntTests(unittest.TestCase):
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
