import inspect
import json
import os
import sys

import boto3


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/common_layer/python"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

import unittest
from unittest import mock


from common_layer.python.ProcessRecord import *


class ProcessRecordUnitTests(unittest.TestCase):
    def test_constructor__given_valid_dict_input__then_no_exceptions(self):
        # Arrange
        input = "keyword blast"

        # Act
        subject = ProcessRecord(process_name=input)

        # Assert
        self.assertEqual(subject.process_name, input)
        self.assertEqual(subject.pk, "")


if __name__ == "__main__":
    unittest.main()