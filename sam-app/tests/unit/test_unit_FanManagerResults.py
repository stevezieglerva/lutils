import inspect
import json
import os
import sys
from types import resolve_bases

import boto3


import unittest
from unittest import mock

from dataclasses import asdict
from common_layer_hex.python.domain.ProcessDTO import *
from common_layer_hex.python.domain.TaskDTO import *
from common_layer_hex.python.domain.FanEventDTO import *
from common_layer_hex.python.domain.FanManager import *


class ProcessDTOUnitTests(unittest.TestCase):
    def test_dunder_dict__given_valid_object__then_dict_json_is_valid(self):
        # Arrange
        process = ProcessDTO(
            process_id="456", process_name="keyword_blast", information=""
        )
        task = TaskDTO("task 1", {}, "456")
        event = FanEventDTO("source", "name", {})
        fan = FanManagerResults(process, [task], [event])

        # Act
        results = asdict(fan)
        print(results)

        # Assert
        self.assertEqual(type(results), dict)
        print(json.dumps(results, indent=3, default=str))


if __name__ == "__main__":
    unittest.main()
