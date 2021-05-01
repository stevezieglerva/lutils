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
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from lutil_fan_handler.FanOut import FanOut


class FanOutIntTests(unittest.TestCase):
    def test_fan_out__given_valid_inputs__then_item_added_to_db(self):
        # Arrange
        table_name = "lutil-fan-processing"
        subject = FanOut("processA", table_name)

        # Act
        results = subject.fan_out("task C", {"keywords": "hello world"})
        print(results)

        # Assert
        self.assertTrue(False)
