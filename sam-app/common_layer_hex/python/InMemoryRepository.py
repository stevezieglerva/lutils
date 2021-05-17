import boto3

from DynamoDB import DynamoDB
from DynamoDBRepository import DynamoDBRepository
from ProcessDTO import ProcessDTO
from TaskDTO import TaskDTO


class InMemoryRepository(DynamoDBRepository):
    def prep_for_test(self):
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
