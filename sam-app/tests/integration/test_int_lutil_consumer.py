import inspect
import json
import os
import sys

import boto3

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/lutil_fan_e2e_consumer"
parentdir = os.path.dirname(parentdir) + "/common_layer_hex/python"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

import unittest
from unittest import mock

from lutil_fan_e2e_consumer import app
from domain.FanEventDTO import *
from domain.TaskDTO import *
from infrastructure.repository.DynamoDB import DynamoDB


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


table_name = get_output_from_stack("FanProcessingPartTestTableName")
os.environ["TABLE_NAME"] = table_name
db = DynamoDB(table_name)

task_json = {
    "process_id": "2e7d2b96-ae10-11eb-b5ab-acde48001122",
    "process_name": "e2e tests",
    "task_name": "task-9",
    "task_message": {"max_delay": 5},
    "completion_sns_arn": "completion_sns_arn",
    "created": "2021-05-06T02:10:10.773986",
    "pk": "FAN-OUT-JOB#2e7d2b96-ae10-11eb-b5ab-acde48001122-TASK#task-9",
    "sk": "-",
    "gs1_pk": "-",
    "gs1_sk": "-",
    "status": "created",
    "status_changed_timestamp": "2021-05-06T02:10:10.577068",
}

task = convert_json_to_task(task_json)


event = FanEventDTO(
    event_source="test consumer", event_name="task_created", event_message=task.__dict__
)
event_string = json.dumps(event.__dict__, indent=3, default=str)

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
                "Message": event_string,
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
        os.environ["COMPLETE_TASK_LAMBDA_NAME"] = get_output_from_stack(
            "FanCompleteTaskTestLambda"
        )

        # Act
        results = app.lambda_handler(TASK_CREATED, {})
