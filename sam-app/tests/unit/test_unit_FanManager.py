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
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/lutil_fan_start_process"
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
from common_layer_hex.python.DynamoDB import DynamoDB


class LutilStartProcessLambdaUnitTests(unittest.TestCase):
    def is_process_in_repo(self, process_id):
        db = DynamoDB("fake-table")
        process_json = db.get_item(
            {"pk": f"PROCESS#{process_id}", "sk": f"PROCESS#{process_id}"}
        )
        if "pk" in process_json:
            return True
        return False

    def count_of_tasks_in_status(self, process_id, status):
        db = DynamoDB("fake-table")
        tasks_json = db.query_table_begins(
            {"pk": f"PROCESS#{process_id}", "sk": f"TASK"}
        )
        tasks_in_status = [t for t in tasks_json if t["status"] == status]
        print(json.dumps(tasks_in_status, indent=3, default=str))
        return len(tasks_in_status)

    def test_constructor__given_valid_inputs__then_no_expections(self):
        # Arrange
        repo = InMemoryRepository("")
        notifier = TestNotifier("")

        # Act
        subject = FanManager(repo, notifier)

        # Assert

    @mock_dynamodb2
    def test_start_process__given_valid_inputs__then_process_and_task_in_repo(self):
        # Arrange
        repo = InMemoryRepository("fake-table")
        repo.prep_for_test()
        notifier = TestNotifier("fake-sns")
        subject = FanManager(repo, notifier)
        task_1 = TaskDTO("task 01", {"action": "go"})
        task_2 = TaskDTO("task 02", {"action": "save"})

        process = ProcessDTO("fan manager test")

        # Act
        results = subject.start_process(process, [task_1, task_2])
        process_added = repo.get_process(process.process_id)

        # Assert
        self.assertNotEqual(results.process_id, "")
        self.assertNotEqual(results.started, "")
        self.assertTrue(self.is_process_in_repo(process.process_id))
        self.assertEqual(
            self.count_of_tasks_in_status(process.process_id, "fan_out"), 2
        )
