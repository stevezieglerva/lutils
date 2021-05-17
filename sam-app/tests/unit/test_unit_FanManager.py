import inspect
import json
import os
import sys

import boto3
from moto import mock_dynamodb2


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/common_layer_hex/python"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

import unittest
from unittest import mock

from common_layer_hex.python.FanManager import FanManager
from common_layer_hex.python.InMemoryRepository import InMemoryRepository
from common_layer_hex.python.TestNotifier import TestNotifier
from common_layer_hex.python.ProcessDTO import *
from common_layer_hex.python.TaskDTO import *


class FanManagerUnitTests(unittest.TestCase):
    def test_constructor__given_valid_inputs__then_no_expections(self):
        # Arrange
        repo = InMemoryRepository("")
        notifier = TestNotifier("")

        # Act
        subject = FanManager(repo, notifier)

        # Assert

    def test_start_process__given_valid_inputs__then_process_and_task_in_repo(self):
        # Arrange
        repo = InMemoryRepository("")
        notifier = TestNotifier("")
        subject = FanManager(repo, notifier)
        task_1 = TaskDTO("task 01", {"action": "go"})
        task_2 = TaskDTO("task 02", {"action": "save"})

        process = ProcessDTO("fan manager test", [task_1, task_2])

        # Act
        results = subject.start_process(process, [task_1, task_2])

        # Assert
        self.assertNotEqual(results.process_id, "")
        self.assertNotEqual(results.started, "")
