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


from common_layer_hex.python.domain.FanEventDTO import *


class ProcessDTOUnitTests(unittest.TestCase):
    def test_constructor__given_valid_field_input__then_no_exceptions(self):
        # Arrange

        # Act
        subject = FanEventDTO("x", "y", "z")

        # Assert
        self.assertEqual(subject.event_source, "x")
        self.assertEqual(subject.event_name, "y")

    def test_constructor__given_valid_string_input__then_no_exceptions(self):
        # Arrange
        record = {
            "event_source": "456",
            "event_name": "keyword blast",
            "event_message": {"hello": "world"},
        }

        # Act
        results = convert_json_to_fanevent(record)

        print(results)

        # Assert
        self.assertEqual(results.event_source, record["event_source"])


if __name__ == "__main__":
    unittest.main()