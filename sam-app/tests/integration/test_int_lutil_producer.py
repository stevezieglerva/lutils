import inspect
import json
import os
import sys

import boto3

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/lutil_fan_e2e_producer"
parentdir = os.path.dirname(parentdir) + "/common_layer/python"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

import unittest
from unittest import mock

from lutil_fan_e2e_producer import app


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


class ProducerIntTests(unittest.TestCase):
    def test_lambda_handler__then_no_exception(self):
        # Arrange
        os.environ["HANDLER_SNS_TOPIC_ARN"] = get_sns_arn_from_stack("FanEventsTestSNS")

        # Act
        results = app.lambda_handler({}, {})
