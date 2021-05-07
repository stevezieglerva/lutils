import inspect
import json
import os
import sys

import boto3

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/lutil_fan_e2e_consumer"
parentdir = os.path.dirname(parentdir) + "/common_layer/python"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

import unittest
from unittest import mock

from lutil_fan_e2e_consumer import app
from TaskRecord import TaskRecord
from FanEvent import *


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


task_json = {
    "process_id": "2e7d2b96-ae10-11eb-b5ab-acde48001122",
    "process_name": "e2e tests",
    "task_name": "task-9",
    "task_message": {"var_1": 297},
    "completion_sns_arn": "completion_sns_arn",
    "created": "2021-05-06T02:10:10.773986",
    "pk": "FAN-OUT-JOB#2e7d2b96-ae10-11eb-b5ab-acde48001122-TASK#task-9",
    "sk": "-",
    "gs1_pk": "-",
    "gs1_sk": "-",
    "status": "created",
    "status_changed_timestamp": "2021-05-06T02:10:10.577068",
}

task = TaskRecord(record_string=json.dumps(task_json, indent=3, default=str))
event = FanEvent(event_source="e2e tests", event_name=TASK_CREATED, message=task.json())

TASK_CREATED = {
    "Records": [
        {
            "EventSource": "aws:sns",
            "EventVersion": "1.0",
            "EventSubscriptionArn": "arn:aws:sns:us-east-1:112280397275:lutil_fan_events_test:58701519-f63e-46df-b837-d6e48f2caa2a",
            "Sns": {
                "Type": "Notification",
                "MessageId": "afc5e054-eab6-5906-a8d7-b959b8f41ec6",
                "TopicArn": "arn:aws:sns:us-east-1:112280397275:lutil_fan_events_test",
                "Subject": None,
                "Message": str(event),
                "Timestamp": "2021-05-06T02:10:10.968Z",
                "SignatureVersion": "1",
                "Signature": "GxRmH8dcwhDc/Ft1zH7K1MOnFeOhq2NJfuWkHFnRjA2IreQGk30OVIcKwtSkoPxL71wi6Up58oaoXXkiBLnRTAqucGzLtGpIFBT/nXvPW3NqCLew5HaB068ulkbpxHqjeWRmF6HgZbGnNlmelcKwyNUnMHu+2dNAL4UJ+slctGlK0p/Q8dxowO/TA/ZPMsiKv5xoA2z2Y/R1UfbTt7orDeAhfOew6eJP/4ZzHBharWM1UcR0XCUUPK2Q7N/X45c+vBuTffdtQYpA4SZhBRK2LwaWX2BsRN58LjUVGRypX/Zm9cOLuvAVaBb+j5dd3vya5oB516A29bxKqkymySE28A==",
                "SigningCertUrl": "https://sns.us-east-1.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem",
                "UnsubscribeUrl": "https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:112280397275:lutil_fan_events_test:58701519-f63e-46df-b837-d6e48f2caa2a",
                "MessageAttributes": {
                    "process_name": {"Type": "String", "Value": "e2e tests"},
                    "event_name": {"Type": "String", "Value": "task_created"},
                    "event_source": {"Type": "String", "Value": "e2e tests"},
                },
            },
        }
    ]
}


class ConsumerIntTests(unittest.TestCase):
    def test_lambda_handler__then_no_exception(self):
        # Arrange
        os.environ["HANDLER_SNS_TOPIC_ARN"] = get_sns_arn_from_stack("FanEventsTestSNS")

        # Act
        results = app.lambda_handler(TASK_CREATED, {})
