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

from common_layer.python.TaskUpdateProcessor import *
from common_layer.python.TaskRecord import *


class TaskUpdateProcessorUnitTests(unittest.TestCase):
    def test_constructor__given_valid_dict_input__then_no_exceptions(self):
        # Arrange

        # Act
        subject = TaskUpdateProcessor("sns-topic-name-fake", "table-name-fake")

        # Assert
        self.assertEqual(subject.sns_topic_name, "sns-topic-name-fake")
        self.assertEqual(subject.table_name, "table-name-fake")

    def test_process__given_newly_created_fan_out__then_create_new_process_and_notify(
        self,
    ):
        # Arrange
        subject = TaskUpdateProcessor("sns-topic-name-fake", "table-name-fake")
        record = {
            "pk": "PROCESS#1819-00",
            "sk": "TASK#93020939F",
            "gs1_pk": "-",
            "gs1_sk": "-",
            "process_name": "keyword blast",
            "status": "fan_out",
            "task_name": "document-2",
            "status_changed_timestamp": "2021",
            "created": "2021",
            "task_message": {"hello": "world"},
        }
        new_fan_out_task = TaskRecord(
            record_string=json.dumps(record, indent=3, default=str),
            db="fake",
        )

        # Act
        results = subject.process_task(new_fan_out_task)

        # Assert
        self.assertEqual(results["process_record"], {})
        self.assertEqual(results["event"], {})


if __name__ == "__main__":
    unittest.main()