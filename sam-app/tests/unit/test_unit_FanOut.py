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
from unittest import mock

from lutil_fan_handler.FanOut import FanOut


class FanOutUnitTests(unittest.TestCase):
    def test_constructor__given_valid_inputs__then_properties_correct(self):
        # Arrange
        table_name = "fake-table"

        # Act
        with mock.patch(
            "lutil_fan_handler.FanOut.FanOut._table_exists",
            mock.MagicMock(return_value=True),
        ):
            subject = FanOut("processA", table_name)

        # Assert
        self.assertEqual(subject.process_name, "processA")
        self.assertTrue(subject.process_id is not None)

    def test_fan_out__given_valid_message__then_job_returned(self):
        # Arrange

        # Act
        with mock.patch(
            "lutil_fan_handler.FanOut.FanOut._table_exists",
            mock.MagicMock(return_value=True),
        ):
            with mock.patch(
                "lutil_fan_handler.FanOut.FanOut._put_item",
                mock.MagicMock(return_value=True),
            ):
                subject = FanOut("processA")
                results = subject.fan_out("task A", {"hello": "world"})

        # Assert
        self.assertEqual(results.process_name, "processA")
        self.assertEqual(results.message, '{"hello": "world"}')
