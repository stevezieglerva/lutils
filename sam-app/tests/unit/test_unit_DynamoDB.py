import inspect
import json
import os
import sys

import boto3


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/lutil_fan_handler"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

import unittest
from unittest import mock

from lutil_fan_handler.DynamoDB import DDB


class DynamoDBUnitTests(unittest.TestCase):
    def test_constructor__given_valid_inputs__then_properties_correct(self):
        # Arrange
        table_name = "fake-table"

        # Act

        subject = DDB(table_name)

        # Assert
        self.assertEqual(subject.table_name, table_name)
