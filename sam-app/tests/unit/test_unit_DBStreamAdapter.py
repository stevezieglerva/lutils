import inspect
import json
import os
import sys
import unittest
from unittest import mock

import boto3
from common_layer_hex.python.domain.FanManager import *
from common_layer_hex.python.domain.IRunProcess import *
from common_layer_hex.python.domain.TaskDTO import *
from common_layer_hex.python.infrastructure.notifications.TestNotifier import *
from common_layer_hex.python.infrastructure.repository.InMemoryRepository import *
from FanManagerTestDriver import *
from lutil_fan_dbstream_handler.DBStreamAdapter import DBStreamAdapter
from moto import mock_dynamodb2, mock_sns

EVENT_FAN_OUT = {
    "Records": [
        {
            "eventID": "f1c2fa59c0b128193cf9575ed54811d2",
            "eventName": "INSERT",
            "eventVersion": "1.1",
            "eventSource": "aws:dynamodb",
            "awsRegion": "us-east-1",
            "dynamodb": {
                "ApproximateCreationDateTime": 1621025176.0,
                "Keys": {
                    "sk": {"S": "TASK#task_00"},
                    "pk": {"S": "PROCESS#01F5PA2EMNDQ9YJ0WGGC4KDMNW"},
                },
                "NewImage": {
                    "task_name": {"S": "task_00"},
                    "process_id": {"S": "01F5PA2EMNDQ9YJ0WGGC4KDMNW"},
                    "status_changed_timestamp": {"S": "2021-05-14T16:46:16.627334"},
                    "task_message": {"S": "\"{'go': 'caps!'}\""},
                    "created": {"S": "2021-05-14T16:46:16.627306"},
                    "process_name": {"S": "ProcessRecord Int Test"},
                    "sk": {"S": "TASK#task_00"},
                    "gs1_pk": {"S": "-"},
                    "pk": {"S": "PROCESS#01F5PA2EMNDQ9YJ0WGGC4KDMNW"},
                    "gs1_sk": {"S": "-"},
                    "status": {"S": "fan_out"},
                },
                "SequenceNumber": "875400000000009959396144",
                "SizeBytes": 325,
                "StreamViewType": "NEW_AND_OLD_IMAGES",
            },
            "eventSourceARN": "arn:aws:dynamodb:us-east-1:112280397275:table/lutils-FanProcessingPartTestTable-Q3PVEB6MO2AJ/stream/2021-05-14T13:21:33.706",
        },
    ]
}

EVENT_TASK_COMPLETED = {
    "Records": [
        {
            "eventID": "f1c2fa59c0b128193cf9575ed54811d2",
            "eventName": "MODIFY",
            "eventVersion": "1.1",
            "eventSource": "aws:dynamodb",
            "awsRegion": "us-east-1",
            "dynamodb": {
                "ApproximateCreationDateTime": 1621025176.0,
                "Keys": {
                    "sk": {"S": "TASK#task_00"},
                    "pk": {"S": "PROCESS#01F5PA2EMNDQ9YJ0WGGC4KDMNW"},
                },
                "NewImage": {
                    "task_name": {"S": "task_00"},
                    "process_id": {"S": "01F5PA2EMNDQ9YJ0WGGC4KDMNW"},
                    "status_changed_timestamp": {"S": "2021-05-14T16:46:16.627334"},
                    "task_message": {"S": "\"{'go': 'caps!'}\""},
                    "created": {"S": "2021-05-14T16:46:16.627306"},
                    "process_name": {"S": "ProcessRecord Int Test"},
                    "sk": {"S": "TASK#task_00"},
                    "gs1_pk": {"S": "-"},
                    "pk": {"S": "PROCESS#01F5PA2EMNDQ9YJ0WGGC4KDMNW"},
                    "gs1_sk": {"S": "-"},
                    "status": {"S": "completed"},
                },
                "OldImage": {
                    "task_name": {"S": "task_00"},
                    "process_id": {"S": "01F5PA2EMNDQ9YJ0WGGC4KDMNW"},
                    "status_changed_timestamp": {"S": "2021-05-14T16:46:16.627334"},
                    "task_message": {"S": "\"{'go': 'caps!'}\""},
                    "created": {"S": "2021-05-14T16:46:16.627306"},
                    "process_name": {"S": "ProcessRecord Int Test"},
                    "sk": {"S": "TASK#task_00"},
                    "gs1_pk": {"S": "-"},
                    "pk": {"S": "PROCESS#01F5PA2EMNDQ9YJ0WGGC4KDMNW"},
                    "gs1_sk": {"S": "-"},
                    "status": {"S": "created"},
                },
                "SequenceNumber": "875400000000009959396144",
                "SizeBytes": 325,
                "StreamViewType": "NEW_AND_OLD_IMAGES",
            },
            "eventSourceARN": "arn:aws:dynamodb:us-east-1:112280397275:table/lutils-FanProcessingPartTestTable-Q3PVEB6MO2AJ/stream/2021-05-14T13:21:33.706",
        },
    ]
}

REMOVE_EVENT = {
    "Records": [
        {
            "eventID": "f1c2fa59c0b128193cf9575ed54811d2",
            "eventName": "REMOVE",
            "eventVersion": "1.1",
            "eventSource": "aws:dynamodb",
            "awsRegion": "us-east-1",
            "dynamodb": {
                "ApproximateCreationDateTime": 1621025176.0,
                "Keys": {
                    "sk": {"S": "TASK#task_00"},
                    "pk": {"S": "PROCESS#01F5PA2EMNDQ9YJ0WGGC4KDMNW"},
                },
                "NewImage": {
                    "task_name": {"S": "task_00"},
                    "process_id": {"S": "01F5PA2EMNDQ9YJ0WGGC4KDMNW"},
                    "status_changed_timestamp": {"S": "2021-05-14T16:46:16.627334"},
                    "task_message": {"S": "\"{'go': 'caps!'}\""},
                    "created": {"S": "2021-05-14T16:46:16.627306"},
                    "process_name": {"S": "ProcessRecord Int Test"},
                    "sk": {"S": "TASK#task_00"},
                    "gs1_pk": {"S": "-"},
                    "pk": {"S": "PROCESS#01F5PA2EMNDQ9YJ0WGGC4KDMNW"},
                    "gs1_sk": {"S": "-"},
                    "status": {"S": "fan_out"},
                },
                "SequenceNumber": "875400000000009959396144",
                "SizeBytes": 325,
                "StreamViewType": "NEW_AND_OLD_IMAGES",
            },
            "eventSourceARN": "arn:aws:dynamodb:us-east-1:112280397275:table/lutils-FanProcessingPartTestTable-Q3PVEB6MO2AJ/stream/2021-05-14T13:21:33.706",
        },
    ]
}


class DBStreamAdapterUnitTests(unittest.TestCase):
    def event_created_for(self, event: FanEventDTO, event_name):
        self.assertEqual(event.event_name, event_name)

    @mock_dynamodb2
    def test_process_events__given_only_task_completed__then_process_completed_notification_sent(
        self,
    ):
        # Arrange
        driver = FanManagerTestDriver()
        tasks = driver.create_task_array(
            [
                {"task_name": "task 01", "message": {"action": "go"}},
            ]
        )
        results = driver.when_start_process("fan manager test", tasks)
        saved_tasks = results.updated_tasks
        results = driver.when_fan_out(saved_tasks)
        results = driver.when_complete_task(saved_tasks[0])
        print(f"\n\ncomplete task results: {results}")

        task_completion_db_stream = driver.create_task_completed_dynamodb_change_stream(
            results.updated_process, saved_tasks[0]
        )

        repo = InMemoryRepository("fake-table")
        notifier = TestNotifier("fake-sns")
        subject = DBStreamAdapter(FanManager(repo, notifier))

        # Act
        results = subject.process_events(task_completion_db_stream)
        print(f"\n\n***** results from test call: {results}")

        # Assert
        driver.then_count_of_tasks_in_status(
            results[0].updated_process,
            "completed",
            1,
        )
        driver.then_progress_is(results[0].updated_process.progress, 1)
        driver.then_event_created_for(
            results[0].event_notifications[0], EVENT_PROCESS_COMPLETED
        )

    def test_process_singe_event__given_remove_event__then_event_skipped(self):
        # Arrange
        repo = InMemoryRepository("fake")
        notifier = TestNotifier("fake")
        fan_manager = FanManager(repo, notifier)
        subject = DBStreamAdapter(fan_manager)

        # Act
        results = subject.process_events(REMOVE_EVENT)

        # Assert
        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()
