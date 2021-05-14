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
    def test_constructor__given_valid_input__then_no_exceptions(self):
        # Arrange
        publisher = FanEventPublisher("test_event_source", "fake-topic")

        # Act
        subject = TaskUpdateProcessor(publisher)

        # Assert
        self.assertEqual(subject.publisher, publisher)

    def test_process__given_newly_created_fan_out__then_create_new_process_and_notify(
        self,
    ):
        # Arrange
        publisher = FanEventPublisher("test_event_source", "fake-topic")

        subject = TaskUpdateProcessor(publisher)
        record = {
            "pk": "PROCESS#777",
            "sk": "TASK#93020939F",
            "gs1_pk": "-",
            "gs1_sk": "",
            "process_id": "777",
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
        with mock.patch(
            "common_layer.python.TaskUpdateProcessor.TaskUpdateProcessor._save_process",
            mock.MagicMock(return_value="db_update_made"),
        ):
            with mock.patch(
                "common_layer.python.TaskUpdateProcessor.TaskUpdateProcessor._publish_next_event",
                mock.MagicMock(return_value={"sns_sent": "yes"}),
            ):
                results = subject.process_task(new_fan_out_task)
                print(json.dumps(results, indent=3, default=str))

        # Assert
        self.assertEqual(results["process_record"]["pk"], "PROCESS#777")
        self.assertEqual(results["event"], {"sns_sent": "yes"})

    def test_process__given_newly_started__then_nothing_processed(
        self,
    ):
        # Arrange
        publisher = FanEventPublisher("test_event_source", "fake-topic")

        subject = TaskUpdateProcessor(publisher)
        record = {
            "pk": "PROCESS#777",
            "sk": "TASK#93020939F",
            "gs1_pk": "-",
            "gs1_sk": "",
            "process_id": "777",
            "process_name": "keyword blast",
            "status": "task_stared",
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
        with mock.patch(
            "common_layer.python.TaskUpdateProcessor.TaskUpdateProcessor._save_process",
            mock.MagicMock(return_value="db_update_made"),
        ):
            with mock.patch(
                "common_layer.python.TaskUpdateProcessor.TaskUpdateProcessor._publish_next_event",
                mock.MagicMock(return_value={"sns_sent": "yes"}),
            ):
                results = subject.process_task(new_fan_out_task)
                print(json.dumps(results, indent=3, default=str))

        # Assert
        self.assertEqual(results["process_record"], {})
        self.assertEqual(results["event"], {})


if __name__ == "__main__":
    unittest.main()