import os, sys, inspect, json

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/lutil_fan_handler"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

import unittest
from lutil_fan_handler.FanOut import FanOut
from unittest.mock import patch, Mock, MagicMock, PropertyMock


class FanOutIntTests(unittest.TestCase):
    def test_constructor__given_valid_inputs__then_properties_correct(self):
        # Arrange

        # Act
        subject = FanOut("processA", "fake-location")

        # Assert
        self.assertEqual(subject.process_name, "processA")
        self.assertTrue(subject.process_id is not None)

    def test_fan_out__given_valid_message__then_job_returned(self):
        # Arrange
        subject = FanOut("processA")

        # Act
        results = subject.fan_out("task A", {"hello": "world"})

        # Assert
        self.assertEqual(results.process_name, "processA")
