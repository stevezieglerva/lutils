import inspect
import json
import os
import sys

import boto3


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/common_layer_hex/python"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

import unittest
from unittest import mock

from common_layer_hex.python.infrastructure.repository.DynamoDB import DynamoDB


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


class DynamoDBUnitTests(unittest.TestCase):
    def test_query_index_begins__given_index_key__then_return_correct(self):
        table_name = get_output_from_stack("FanProcessingPartTestTableName")

        subject = DynamoDB(table_name)
        subject.set_ttl_seconds(10)
        subject.put_item(
            {
                "pk": "J1K4",
                "sk": "TASK#03939",
                "value": {"subkey": "03939"},
                "gs1_pk": "INDEX",
                "gs1_sk": "ABCDEF",
                "status": "created",
            }
        )

        # Act
        results = subject.query_index_begins(
            "gs1", {"gs1_pk": "INDEX", "gs1_sk": "ABC"}
        )
        print(f"Query results: {results}")

        # Assert
        self.assertTrue("ttl" in results[0])
        results[0].pop("ttl")
        self.assertEqual(
            results,
            [
                {
                    "value": {"subkey": "03939"},
                    "sk": "TASK#03939",
                    "gs1_pk": "INDEX",
                    "pk": "J1K4",
                    "gs1_sk": "ABCDEF",
                    "status": "created",
                }
            ],
        )
