import boto3

from infrastructure.repository.DynamoDB import DynamoDB
from infrastructure.repository.DynamoDBRepository import DynamoDBRepository
from domain.ProcessDTO import ProcessDTO
from domain.TaskDTO import TaskDTO


class InMemoryRepository(DynamoDBRepository):
    def __init__(self, source):
        self.source = source
        print(self.source)
        db = boto3.client("dynamodb")
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
            ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
        )
        self.db = DynamoDB(self.source)
