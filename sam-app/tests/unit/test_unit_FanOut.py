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

from common_layer.python.FanOut import FanOut


class FanOutUnitTests(unittest.TestCase):
    def test_constructor__given_valid_inputs__then_properties_correct(self):
        # Arrange
        table_name = "fake-table"

        # Act
        with mock.patch(
            "common_layer.python.FanOut.FanOut._table_exists",
            mock.MagicMock(return_value=True),
        ):
            subject = FanOut("processA", "arn::fake-sns", table_name)

        # Assert
        self.assertEqual(subject.process_name, "processA")
        self.assertTrue(subject.process_id is not None)
