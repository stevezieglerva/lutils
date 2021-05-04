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


from common_layer.python.FanEvent import *
from common_layer.python.NamedTupleBase import *


class FanEventUnitTests(unittest.TestCase):
    def test_constructor__given_create_task__then_no_exceptions(self):
        # Arrange
        job = FanJob(
            "123",
            "process X",
            "task 1",
            '{"message" : "hello world"}',
            "sns",
        )
        print(job)

        # Act
        subject = FanEvent("process-x", TASK_CREATED, job)

        # Assert
        results = subject.json()
        print(json.dumps(results, indent=3, default=str))
        self.assertEqual(results["job"]["process_id"], "123")
        self.assertTrue("timestamp" in results)

    def test_constructor__given_create_task_without_job__then_no_exceptions(self):
        # Arrange

        # Act
        subject = FanEvent("process-x", TASK_CREATED)

        # Assert
        results = subject.json()
        print(json.dumps(results, indent=3, default=str))
        self.assertTrue("timestamp" in results)

    def test_print(
        self,
    ):
        # Arrange
        job = FanJob(
            "123",
            "process X",
            "task 1",
            '{"message" : "hello world"}',
            "sns",
        )
        print(job)
        subject = FanEvent("process-x", TASK_CREATED, job)

        # Act
        results = subject.get_formatted_line()
        print(results)

        # Assert
        self.assertEqual(
            results,
            "process-x            task_created                             123                                      process X                                task 1",
        )
