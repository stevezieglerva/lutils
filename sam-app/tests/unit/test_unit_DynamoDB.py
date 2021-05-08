import inspect
import json
import os
import sys

import boto3
from moto import mock_dynamodb2


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/common_layer/python"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

import unittest
from unittest import mock

from common_layer.python.DynamoDB import DynamoDB


class DynamoDBUnitTests(unittest.TestCase):
    def test_constructor__given_valid_inputs__then_properties_correct(self):
        # Arrange
        table_name = "fake-table"

        # Act

        subject = DynamoDB(table_name, "key_field")

        # Assert
        self.assertEqual(subject.table_name, table_name)

    @mock_dynamodb2
    def test_put_item__given_valid_inputs__then_return_correct(self):
        # Arrange
        table_name = "fake-table"
        db = boto3.client("dynamodb")
        db.create_table(
            TableName=table_name,
            KeySchema=[{"AttributeName": "key_field", "KeyType": "HASH"}],
            AttributeDefinitions=[
                {"AttributeName": "key_field", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
        )

        subject = DynamoDB(table_name, "key_field")

        # Act
        results = subject.put_item({"key_field": "world", "value": 8.2})

        # Assert
        new_item = db.get_item(TableName=table_name, Key={"key_field": {"S": "world"}})[
            "Item"
        ]
        print(new_item)
        self.assertEqual(new_item, {"key_field": {"S": "world"}, "value": {"N": "8.2"}})

    @mock_dynamodb2
    def test_get_item__given_valid_inputs__then_return_correct(self):
        # Arrange
        table_name = "fake-table"
        key_field = "id"
        db = boto3.client("dynamodb")
        db.create_table(
            TableName=table_name,
            KeySchema=[{"AttributeName": key_field, "KeyType": "HASH"}],
            AttributeDefinitions=[
                {"AttributeName": key_field, "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
        )

        subject = DynamoDB(table_name, key_field)
        subject.set_ttl_seconds(10)
        subject.put_item({key_field: "J1K4", "value": 2000})

        # Act
        new_item = subject.get_item("J1K4")
        print(new_item)

        # Assert
        self.assertTrue("ttl" in new_item)
        new_item.pop("ttl")
        self.assertEqual(new_item, {"id": "J1K4", "value": "2000"})

    @mock_dynamodb2
    def test_get_item__given_dict_is_subvalue__then_return_correct(self):
        # Arrange
        table_name = "fake-table"
        key_field = "id"
        db = boto3.client("dynamodb")
        db.create_table(
            TableName=table_name,
            KeySchema=[{"AttributeName": key_field, "KeyType": "HASH"}],
            AttributeDefinitions=[
                {"AttributeName": key_field, "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
        )

        subject = DynamoDB(table_name, key_field)
        subject.set_ttl_seconds(10)
        subject.put_item({key_field: "J1K4", "value": {"subkey": "subvalue"}})

        # Act
        new_item = subject.get_item("J1K4")
        print(new_item)

        # Assert
        self.assertTrue("ttl" in new_item)
        new_item.pop("ttl")
        self.assertEqual(new_item, {"id": "J1K4", "value": {"subkey": "subvalue"}})
