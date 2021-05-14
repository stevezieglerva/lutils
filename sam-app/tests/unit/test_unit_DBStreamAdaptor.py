import inspect
import json
import os
import sys

import boto3


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/lutil_fan_dbstream_handler"
sys.path.insert(0, parentdir)
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/common_layer/python"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

import unittest
from unittest import mock

from common_layer.python.TaskUpdateProcessor import *
from common_layer.python.TaskRecord import *

from lutil_fan_dbstream_handler import DBStreamTaskUpdateProcessorAdapter


class DBStreamTaskUpdateProcessorAdapterUnitTests(unittest.TestCase):
    def test_constructor__given_valid_input__then_no_exceptions(self):
        # Arrange
        subject = DBStreamTaskUpdateProcessorAdapter()

        # Act
        subject = TaskUpdateProcessor(publisher)

        # Assert
        self.assertEqual(subject.publisher, publisher)


if __name__ == "__main__":
    unittest.main()