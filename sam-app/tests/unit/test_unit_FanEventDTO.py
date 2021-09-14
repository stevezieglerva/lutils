import inspect
import json
import os
import sys

import boto3


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
        results = FanEventDTO.create_from_dict(record)

        print(results)

        # Assert
        self.assertEqual(results.event_source, record["event_source"])


if __name__ == "__main__":
    unittest.main()
