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


from common_layer.python.TaskRecord import *


class TaskRecordUnitTests(unittest.TestCase):
    def test_constructor__given_valid_dict_input__then_no_exceptions(self):
        # Arrange
        input = "document-3"

        # Act
        subject = TaskRecord(
            process_id="123", task_name=input, process_name="proc_name"
        )

        # Assert
        self.assertEqual(subject.task_name, input)
        self.assertEqual(subject.pk, "PROCESS#123")
        self.assertEqual(subject.sk, "TASK#document-3")

    def test_constructor__given_valid_string_input__then_no_exceptions(self):
        # Arrange
        record = {
            "pk": "PROCESS#1819-00",
            "sk": "TASK#93020939F",
            "gsk1_pk": "-",
            "gsk1_sk": "-",
            "process_name": "keyword blast",
            "status": "created",
            "task_name": "document-2",
            "status_changed": "2021",
            "created": "2021",
        }

        # Act
        subject = TaskRecord(record_string=json.dumps(record, indent=3, default=str))
        print(subject)
        print(subject.__dict__)

        # Assert
        self.assertEqual(subject.process_name, record["process_name"])
        self.assertEqual(subject.pk, "PROCESS#1819-00")
        self.assertEqual(subject.task_name, "document-2")


if __name__ == "__main__":
    unittest.main()