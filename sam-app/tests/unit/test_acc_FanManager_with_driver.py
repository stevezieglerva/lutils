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
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))


import unittest
from unittest import mock

from common_layer_hex.python.domain.FanManager import *
from FanManagerTestDriver import *
from common_layer_hex.python.infrastructure.repository.InMemoryRepository import (
    InMemoryRepository,
)
from common_layer_hex.python.infrastructure.notifications.TestNotifier import (
    TestNotifier,
)
from common_layer_hex.python.domain.ProcessDTO import *
from common_layer_hex.python.domain.TaskDTO import *
from common_layer_hex.python.infrastructure.repository.DynamoDB import DynamoDB
from common_layer_hex.python.domain.FanEventDTO import FanEventDTO


class FanManagerDriverUnitTests(unittest.TestCase):
    @mock_dynamodb2
    def test_start_process__given_valid_inputs__then_process_and_task_in_repo(self):
        # Arrange
        driver = FanManagerTestDriver()
        tasks = driver.create_task_array(
            [
                {"task_name": "task 01", "message": {"action": "go"}},
                {"task_name": "task 02", "message": {"action": "save"}},
            ]
        )

        # Act
        results = driver.when_start_process("fan manager test", tasks)

        # Assert
        driver.then_process_in_repo(results.updated_process.process_id)
        driver.then_count_of_tasks_in_status(results.updated_process, "fan_out", 2)
        driver.then_tasks_linked_to_process(
            results.updated_process, results.updated_tasks[0]
        )
        driver.then_event_created_for(
            results.event_notifications[0], EVENT_PROCESS_STARTED
        )
        self.assertEqual(results.updated_process.information, "special info")

    @mock_dynamodb2
    def test_fan_out__given_newly_created_tasks__then_tasks_status_changed_and_notifications_sent(
        self,
    ):
        # Arrange
        driver = FanManagerTestDriver()
        tasks = driver.create_task_array(
            [
                {"task_name": "task 01", "message": {"action": "go"}},
                {"task_name": "task 02", "message": {"action": "save"}},
            ]
        )
        results = driver.when_start_process("fan manager test", tasks)
        process = results.updated_process

        # Act
        results = driver.when_fan_out(results.updated_tasks)
        print(f"\n\n{results}")

        # Assert
        driver.then_count_of_tasks_in_status(process, "created", 2)
        driver.then_event_created_for(
            results.event_notifications[0], EVENT_TASK_CREATED
        )

    @mock_dynamodb2
    def test_complete_task__given_some_tasks_open__then_tasks_status_changed_and_process_progress_set(
        self,
    ):
        # Arrange
        driver = FanManagerTestDriver()
        tasks = driver.create_task_array(
            [
                {"task_name": "task 01", "message": {"action": "go"}},
                {"task_name": "task 02", "message": {"action": "save"}},
            ]
        )
        results = driver.when_start_process("fan manager test", tasks)
        results = driver.when_fan_out(results.updated_tasks)
        second_updated_task = results.updated_tasks[1]

        # Act
        results = driver.when_complete_task(second_updated_task)
        print(results)

        # Assert
        driver.then_count_of_tasks_in_status(
            results.updated_process,
            "completed",
            1,
        )
        driver.then_progress_is(results.updated_process.progress, 0.5)
        driver.then_event_created_for(
            results.event_notifications[0], EVENT_TASK_COMPLETED
        )
        self.assertEqual(results.updated_process.information, "special info")

    @mock_dynamodb2
    def test_complete_task__given_all_tasks_completed__then_tasks_status_changed_and_process_progress_set(
        self,
    ):
        # Arrange
        driver = FanManagerTestDriver()
        tasks = driver.create_task_array(
            [
                {"task_name": "task 01", "message": {"action": "go"}},
                {"task_name": "task 02", "message": {"action": "save"}},
            ]
        )
        results = driver.when_start_process("fan manager test", tasks)
        process = results.updated_process
        saved_tasks = results.updated_tasks

        results = driver.when_fan_out(saved_tasks)

        # Act
        results = driver.when_complete_task(saved_tasks[0])
        results = driver.when_complete_task(saved_tasks[1])
        print(results)

        # Assert
        driver.then_count_of_tasks_in_status(
            results.updated_process,
            "completed",
            2,
        )
        driver.then_progress_is(results.updated_process.progress, 1)
        driver.then_event_created_for(
            results.event_notifications[0], EVENT_TASK_COMPLETED
        )

    @mock_dynamodb2
    def test_complete_process__given_all_tasks_completed__then_tasks_status_changed_and_process_progress_set(
        self,
    ):
        # Arrange
        driver = FanManagerTestDriver()
        tasks = driver.create_task_array(
            [
                {"task_name": "task 01", "message": {"action": "go"}},
                {"task_name": "task 02", "message": {"action": "save"}},
            ]
        )
        results = driver.when_start_process("fan manager test", tasks)
        saved_tasks = results.updated_tasks
        results = driver.when_fan_out(saved_tasks)
        results = driver.when_complete_task(saved_tasks[0])
        results = driver.when_complete_task(saved_tasks[1])

        # Act
        results = driver.when_complete_process_if_needed(results.updated_process)

        # Assert
        driver.then_count_of_tasks_in_status(
            results.updated_process,
            "completed",
            2,
        )
        driver.then_progress_is(results.updated_process.progress, 1)
        driver.then_event_created_for(
            results.event_notifications[0], EVENT_PROCESS_COMPLETED
        )

    @mock_dynamodb2
    def test_complete_proceess__given_some_tasks_open__then_progress_not_1_and_process_complete_event_not_sent(
        self,
    ):
        # Arrange
        driver = FanManagerTestDriver()
        tasks = driver.create_task_array(
            [
                {"task_name": "task 01", "message": {"action": "go"}},
                {"task_name": "task 02", "message": {"action": "save"}},
            ]
        )
        results = driver.when_start_process("fan manager test", tasks)
        process = results.updated_process
        saved_tasks = results.updated_tasks

        results = driver.when_fan_out(saved_tasks)
        results = driver.when_complete_task(saved_tasks[0])
        results = driver.when_complete_task(saved_tasks[1])

        # Act
        results = driver.when_complete_process_if_needed(process)

        # Assert
        driver.then_count_of_tasks_in_status(
            results.updated_process,
            "completed",
            2,
        )
        driver.then_progress_is(results.updated_process.progress, 1)
        driver.then_event_created_for(
            results.event_notifications[0], EVENT_PROCESS_COMPLETED
        )
