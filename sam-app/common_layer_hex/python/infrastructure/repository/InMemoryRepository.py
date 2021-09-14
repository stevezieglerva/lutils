import json

import boto3
import botocore
from domain.ProcessDTO import ProcessDTO
from domain.TaskDTO import TaskDTO
from infrastructure.repository.DynamoDB import DynamoDB
from infrastructure.repository.DynamoDBRepository import DynamoDBRepository


class InMemoryRepository(DynamoDBRepository):
    def __init__(self, source):
        self.source = source
        print(f"{__name__}: {self.source}")
        db = boto3.client("dynamodb")
        current_tables = db.list_tables()
        if self.source not in json.dumps(current_tables, indent=3, default=str):
            db.create_table(
                TableName=self.source,
                KeySchema=[
                    {"AttributeName": "pk", "KeyType": "HASH"},
                    {"AttributeName": "sk", "KeyType": "RANGE"},
                ],
                AttributeDefinitions=[
                    {"AttributeName": "pk", "AttributeType": "S"},
                    {"AttributeName": "sk", "AttributeType": "S"},
                ],
                ProvisionedThroughput={
                    "ReadCapacityUnits": 10,
                    "WriteCapacityUnits": 10,
                },
            )
        self.db = DynamoDB(self.source)
