import inspect
import json
import os
import sys

import boto3


import unittest
from unittest import mock


from common_layer_hex.python.domain.ProcessDTO import *


class ProcessDTOUnitTests(unittest.TestCase):
    def test_constructor__given_valid_field_input__then_no_exceptions(self):
        # Arrange

        # Act
        subject = ProcessDTO(process_name="procA", information="")

        # Assert
        self.assertEqual(subject.process_name, "procA")
        self.assertEqual(subject.progress, 0)

    def test_constructor__given_only_name_and_info__then_no_exceptions(self):
        # Arrange
        record = {
            "process_name": "keyword blast",
            "information": "basic info",
        }

        # Act
        results = ProcessDTO.create_from_dict(record)

        print(results)

        # Assert
        self.assertEqual(results.process_name, record["process_name"])
        self.assertEqual(results.progress, 0.0)
        self.assertEqual(results.information, "basic info")

    def test_constructor__given_valid_string_input__then_no_exceptions(self):
        # Arrange
        record = {
            "process_id": "456",
            "process_name": "keyword blast",
            "progress": 0.5,
            "started": "2021",
            "ended": "2021",
            "information": "should appear",
        }

        # Act
        results = ProcessDTO.create_from_dict(record)

        print(results)

        # Assert
        self.assertEqual(results.process_name, record["process_name"])
        self.assertEqual(results.progress, 0.5)
        self.assertEqual(results.information, "should appear")

    def test_dunder_dict__given_valid_object__then_dict_json_is_valid(self):
        # Arrange
        record = {
            "process_id": "456",
            "process_name": "keyword blast",
            "progress": 0.5,
            "started": "2021",
            "ended": "2021",
            "information": '{"hello":"world"}',
        }
        dto_object = ProcessDTO.create_from_dict(record)

        # Act
        project_json = dto_object.__dict__

        # Assert
        self.assertEqual(type(project_json), dict)
        print(json.dumps(project_json, indent=3, default=str))


if __name__ == "__main__":
    unittest.main()
