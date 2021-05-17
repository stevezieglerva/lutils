import boto3

from DynamoDB import DynamoDB
from IRepository import IRepository
from ProcessDTO import ProcessDTO
from TaskDTO import TaskDTO


class DynamoDBRepository(IRepository):
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

    def get_process(self, process_id: str) -> ProcessDTO:
        process_json = self.db.get_item(
            {"pk": f"PROCESS#{process_id}", "sk": f"PROCESS#{process_id}"}
        )
        print(process_json)

        return ProcessDTO("test")

    def save_process(self, process: ProcessDTO):
        db_record = self._convert_process_to_db_record(process)
        print(f"Saving: {db_record}")
        self.db.put_item(db_record)

    def _convert_process_to_db_record(self, process: ProcessDTO) -> dict:
        db_record = process.__dict__.copy()
        db_record["pk"] = f"PROCESS#{process.process_id}"
        db_record["sk"] = f"PROCESS#{process.process_id}"
        db_record["gs1_pk"] = "-"
        db_record["gs1_sk"] = "-"
        if process.progress == 0.0:
            db_record["gs1_pk"] = "STATUS#in_progress"
        return db_record

    def get_task(self, process_id: str, task_name: str) -> TaskDTO:
        task_json = self.db.get_item(
            {"pk": f"PROCESS#{process_id}", "sk": f"TASK#{task_name}"}
        )
        print(process_json)
        return ProcessDTO("test")

    def save_task(self, task: TaskDTO):
        db_record = self._convert_task_to_db_record(task)
        print(f"Saving: {db_record}")
        self.db.put_item(db_record)

    def _convert_task_to_db_record(self, task: TaskDTO) -> dict:
        db_record = task.__dict__.copy()
        db_record["pk"] = f"PROCESS#{task.process_id}"
        db_record["sk"] = f"TASK#{task.task_name}"
        db_record["gs1_pk"] = "-"
        db_record["gs1_sk"] = "-"
        return db_record