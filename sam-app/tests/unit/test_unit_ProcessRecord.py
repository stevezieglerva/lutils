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
        subject = ProcessRecord(process_id="123", process_name=input)

        # Assert
        self.assertEqual(subject.process_name, input)
        self.assertEqual(subject.pk, "PROCESS#123")
        self.assertEqual(subject.progress, 0)

    def test_constructor__given_valid_string_input__then_no_exceptions(self):
        # Arrange
        record = {
            "pk": "PROCESS#1819-00",
            "sk": "PROCESS#1819-00",
            "gs1_pk": "-",
            "gs1_sk": "-",
            "process_id": "456",
            "process_name": "keyword blast",
            "started": "2021",
            "ended": "2021",
        }

        # Act
        subject = ProcessRecord(record_string=json.dumps(record, indent=3, default=str))
        print(subject)
        print(subject.__dict__)

        # Assert
        self.assertEqual(subject.process_name, record["process_name"])
        self.assertEqual(subject.pk, "PROCESS#1819-00")
        self.assertEqual(subject.sk, "PROCESS#1819-00")


if __name__ == "__main__":
    unittest.main()