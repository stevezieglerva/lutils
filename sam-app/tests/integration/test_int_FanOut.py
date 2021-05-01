import os, sys, inspect, json
import boto3

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/lutil_fan_handler"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

import unittest
from lutil_fan_handler.FanOut import FanOut
from unittest.mock import patch, Mock, MagicMock, PropertyMock


class FanOutIntTests(unittest.TestCase):
    def test_fan_out__given_valid_inputs__then_item_added_to_db(self):
        # Arrange
        table_name = "fake-table"
        key_field = "pk"
        db = boto3.client("dynamodb")
        db.create_table(
            TableName=table_name,
            KeySchema=[{"AttributeName": key_field, "KeyType": "HASH"}],
            AttributeDefinitions=[
                {"AttributeName": key_field, "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
        )
        test = db.describe_table(TableName=table_name)
        print(test)

        subject = FanOut("processA", table_name)

        # Act
        results = subject.put_item({"pk": "dkdlkj987sd"})
        print(results)

        # Assert
        self.assertEqual(new_item, {key_field: {"S": "J1K4"}, "value": {"N": "2000"}})
