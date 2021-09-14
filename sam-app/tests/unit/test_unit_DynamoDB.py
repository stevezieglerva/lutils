import inspect
import json
import os
import sys

import boto3
from moto import mock_dynamodb2


import unittest
from unittest import mock

from common_layer_hex.python.infrastructure.repository.DynamoDB import DynamoDB


class DynamoDBUnitTests(unittest.TestCase):
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

        subject = DynamoDB(table_name)

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

        subject = DynamoDB(table_name)
        subject.set_ttl_seconds(10)
        subject.put_item({key_field: "J1K4", "value": 2000})

        # Act
        new_item = subject.get_item({"id": "J1K4"})
        print(new_item)

        # Assert
        self.assertTrue("ttl" in new_item)
        new_item.pop("ttl")
        self.assertEqual(new_item, {"id": "J1K4", "value": 2000})

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

        subject = DynamoDB(table_name)
        subject.set_ttl_seconds(10)
        subject.put_item({key_field: "J1K4", "value": {"subkey": "subvalue"}})

        # Act
        new_item = subject.get_item({"id": "J1K4"})
        print(new_item)

        # Assert
        self.assertTrue("ttl" in new_item)
        new_item.pop("ttl")
        self.assertEqual(new_item, {"id": "J1K4", "value": {"subkey": "subvalue"}})

    @mock_dynamodb2
    def test_get_item__given_table_has_composite_key__then_return_correct(self):
        # Arrange
        table_name = "fake-table"

        db = boto3.client("dynamodb")
        db.create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "pk", "KeyType": "HASH"},
                {"AttributeName": "sk", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "pk", "AttributeType": "S"},
                {"AttributeName": "sk", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
        )

        subject = DynamoDB(table_name)
        subject.set_ttl_seconds(10)
        subject.put_item(
            {"pk": "J1K4", "sk": "TASK#03939", "value": {"subkey": "subvalue"}}
        )

        # Act
        new_item = subject.get_item({"pk": "J1K4", "sk": "TASK#03939"})
        print(f"New item: {new_item}")

        # Assert
        self.assertTrue("ttl" in new_item)
        new_item.pop("ttl")
        self.assertEqual(
            new_item,
            {"pk": "J1K4", "sk": "TASK#03939", "value": {"subkey": "subvalue"}},
        )

    @mock_dynamodb2
    def test_query_table_equal__given_valid_composite_key__then_return_correct(self):
        # Arrange
        table_name = "fake-table"

        db = boto3.client("dynamodb")
        db.create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "pk", "KeyType": "HASH"},
                {"AttributeName": "sk", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "pk", "AttributeType": "S"},
                {"AttributeName": "sk", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
        )

        subject = DynamoDB(table_name)
        subject.set_ttl_seconds(10)
        subject.put_item(
            {"pk": "J1K4", "sk": "TASK#03939", "value": {"subkey": "03939"}}
        )
        subject.put_item(
            {"pk": "J1K4", "sk": "TASK#03940", "value": {"subkey": "03940"}}
        )

        # Act
        results = subject.query_table_equal({"pk": "J1K4", "sk": "TASK#03940"})
        print(f"Query results: {results}")

        # Assert
        self.assertTrue("ttl" in results[0])
        results[0].pop("ttl")
        self.assertEqual(
            results,
            [
                {
                    "pk": "J1K4",
                    "sk": "TASK#03940",
                    "value": {"subkey": "03940"},
                }
            ],
        )

    @mock_dynamodb2
    def test_query_table_equal__given_only_pk_of_composite_key__then_return_correct(
        self,
    ):
        # Arrange
        table_name = "fake-table"

        db = boto3.client("dynamodb")
        db.create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "pk", "KeyType": "HASH"},
                {"AttributeName": "sk", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "pk", "AttributeType": "S"},
                {"AttributeName": "sk", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
        )

        subject = DynamoDB(table_name)
        subject.set_ttl_seconds(10)
        subject.put_item(
            {"pk": "J1K4", "sk": "TASK#03939", "value": {"subkey": "03939"}}
        )
        subject.put_item(
            {"pk": "J1K4", "sk": "TASK#03940", "value": {"subkey": "03940"}}
        )

        # Act
        results = subject.query_table_equal({"pk": "J1K4"})
        print(f"Query results: {results}")

        # Assert
        self.assertTrue("ttl" in results[0])
        results[0].pop("ttl")
        results[1].pop("ttl")
        self.assertEqual(
            results,
            [
                {
                    "pk": "J1K4",
                    "sk": "TASK#03939",
                    "value": {"subkey": "03939"},
                },
                {
                    "pk": "J1K4",
                    "sk": "TASK#03940",
                    "value": {"subkey": "03940"},
                },
            ],
        )

    @mock_dynamodb2
    def test_query_table_begins__given_valid_composite_key__then_return_correct(self):
        # Arrange
        table_name = "fake-table"

        db = boto3.client("dynamodb")
        db.create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "pk", "KeyType": "HASH"},
                {"AttributeName": "sk", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "pk", "AttributeType": "S"},
                {"AttributeName": "sk", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
        )

        subject = DynamoDB(table_name)
        subject.set_ttl_seconds(10)
        subject.put_item(
            {"pk": "J1K4", "sk": "TASK#03939", "value": {"subkey": "03939"}}
        )
        subject.put_item(
            {"pk": "J1K4", "sk": "TASK#03940", "value": {"subkey": "03940"}}
        )

        # Act
        results = subject.query_table_begins({"pk": "J1K4", "sk": "T"})
        print(f"Query results: {results}")

        # Assert
        self.assertTrue("ttl" in results[0])
        results[0].pop("ttl")
        results[1].pop("ttl")
        self.assertEqual(
            results,
            [
                {
                    "pk": "J1K4",
                    "sk": "TASK#03939",
                    "value": {"subkey": "03939"},
                },
                {
                    "pk": "J1K4",
                    "sk": "TASK#03940",
                    "value": {"subkey": "03940"},
                },
            ],
        )
