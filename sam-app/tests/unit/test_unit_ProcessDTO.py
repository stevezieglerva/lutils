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


from common_layer_hex.python.domain.ProcessDTO import *


class ProcessDTOUnitTests(unittest.TestCase):
    def test_constructor__given_valid_field_input__then_no_exceptions(self):
        # Arrange

        # Act
        subject = ProcessDTO("procA")

        # Assert
        self.assertEqual(subject.process_name, "procA")
        self.assertEqual(subject.progress, 0)

    def test_constructor__given_valid_string_input__then_no_exceptions(self):
        # Arrange
        record = {
            "process_id": "456",
            "process_name": "keyword blast",
            "progress": 0.5,
            "started": "2021",
            "ended": "2021",
            "extra_field": "junk",
        }

        # Act
        results = convert_json_to_process(record)

        print(results)

        # Assert
        self.assertEqual(results.process_name, record["process_name"])
        self.assertEqual(results.progress, 0.5)


if __name__ == "__main__":
    unittest.main()