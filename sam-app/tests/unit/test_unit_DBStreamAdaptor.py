import inspect
import json
import os
import sys

import boto3


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/lutil_fan_dbstream_handler"
sys.path.insert(0, parentdir)
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/common_layer/python"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

import unittest
from unittest import mock
from moto import mock_dynamodb2, mock_sns

from common_layer.python.TaskUpdateProcessor import *
from common_layer.python.TaskRecord import *
from common_layer.python.FanEventPublisher import FanEventPublisher

from lutil_fan_dbstream_handler.DBStreamAdapter import DBStreamAdapter


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
            "eventSourceARN": "arn:aws:dynamodb:us-east-1:112280397275:table/lutils2-FanProcessingPartTestTable-Q3PVEB6MO2AJ/stream/2021-05-14T13:21:33.706",
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
                    "status": {"S": "task_completed"},
                },
                "SequenceNumber": "875400000000009959396144",
                "SizeBytes": 325,
                "StreamViewType": "NEW_AND_OLD_IMAGES",
            },
            "eventSourceARN": "arn:aws:dynamodb:us-east-1:112280397275:table/lutils2-FanProcessingPartTestTable-Q3PVEB6MO2AJ/stream/2021-05-14T13:21:33.706",
        },
    ]
}


class DBStreamAdapterUnitTests(unittest.TestCase):
    ##    @mock_sns
    ##    @mock_dynamodb2
    ##    def test_process_single_event__given_fan_out__then_process_created_and_sns_sent(
    ##        self,
    ##    ):
    ##        # Arrange
    ##        table_name = "fake-table"
    ##        db = boto3.client("dynamodb")
    ##        db.create_table(
    ##            TableName=table_name,
    ##            KeySchema=[
    ##                {"AttributeName": "pk", "KeyType": "HASH"},
    ##                {"AttributeName": "sk", "KeyType": "RANGE"},
    ##            ],
    ##            AttributeDefinitions=[
    ##                {"AttributeName": "pk", "AttributeType": "S"},
    ##                {"AttributeName": "sk", "AttributeType": "S"},
    ##            ],
    ##            ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
    ##        )
    ##        db = DynamoDB("fake-table")
    ##        task_json = db.convert_from_dict_format(
    ##            EVENT_TASK_COMPLETED["Records"][0]["dynamodb"]["NewImage"]
    ##        )
    ##        task_record = TaskRecord(
    ##            record_string=json.dumps(task_json, indent=3, default=str), db=db
    ##        )
    ##        db.put_item(task_record.json())
    ##
    ##        sns = boto3.client("sns")
    ##        sns_resp = sns.create_topic(Name="fake-sns")
    ##        print(sns_resp)
    ##        topic_arn = sns_resp["TopicArn"]
    ##        publisher = FanEventPublisher("DBStreamAdapterUnitTests", topic_arn)
    ##        subject = DBStreamAdapter(db, publisher)
    ##
    ##        # Act
    ##        results = subject.process_single_event(EVENT_FAN_OUT["Records"][0])
    ##        print(json.dumps(results, indent=3, default=str))
    ##
    ##        # Assert
    ##        self.assertEqual(
    ##            results["process_record"]["pk"], "PROCESS#01F5PA2EMNDQ9YJ0WGGC4KDMNW"
    ##        )
    ##        self.assertEqual(results["process_record"]["progress"], 0)
    ##        self.assertTrue("MessageId" in results["event"])

    @mock_sns
    @mock_dynamodb2
    def test_process_single_event__given_task_completed__then_progress_is_complete(
        self,
    ):
        # Arrange
        table_name = "fake-table"
        db = boto3.client("dynamodb")
        db.create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "pk", "KeyType": "HASH"},
                {"AttributeName": "sk", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "pk", "AttributeType": "S"},
                {"AttributeName": "sk", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
        )

        print("adding fake task record")
        db = DynamoDB("fake-table")
        task_json = db.convert_from_dict_format(
            EVENT_TASK_COMPLETED["Records"][0]["dynamodb"]["NewImage"]
        )
        task_record = TaskRecord(
            record_string=json.dumps(task_json, indent=3, default=str), db=db
        )
        db.put_item(task_record.json())

        sns = boto3.client("sns")
        sns_resp = sns.create_topic(Name="fake-sns")
        print(sns_resp)
        topic_arn = sns_resp["TopicArn"]
        publisher = FanEventPublisher("DBStreamAdapterUnitTests", topic_arn)
        subject = DBStreamAdapter(db, publisher)

        # Act
        results = subject.process_single_event(EVENT_TASK_COMPLETED["Records"][0])
        print(json.dumps(results, indent=3, default=str))

        # Assert
        self.assertEqual(
            results["process_record"]["pk"], "PROCESS#01F5PA2EMNDQ9YJ0WGGC4KDMNW"
        )
        self.assertEqual(results["process_record"]["progress"], 1)
        self.assertTrue("MessageId" in results["event"])


if __name__ == "__main__":
    unittest.main()