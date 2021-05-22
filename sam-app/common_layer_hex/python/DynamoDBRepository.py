import boto3

from DynamoDB import DynamoDB
from IRepository import IRepository
from ProcessDTO import *
from TaskDTO import *


class DynamoDBRepository(IRepository):
    def __init__(self, source):
        self.db = DynamoDB(source)
        seconds_in_24_hours = 60 * 60 * 24
        self.db.set_ttl_seconds(seconds_in_24_hours)

    def get_process(self, process_id: str) -> ProcessDTO:
        process_json = self.db.get_item(
            {"pk": f"PROCESS#{process_id}", "sk": f"PROCESS#{process_id}"}
        )
        print(process_json)
        process = ProcessDTO(
            process_json["process_name"],
            process_json["process_id"],
            process_json["started"],
            process_json["ended"],
            process_json["progress"],
        )
        return process

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
        print(task_json)
        task = TaskDTO(
            task_json["task_name"],
            task_json["task_message"],
            task_json["process_id"],
            task_json["process_name"],
            task_json["status"],
            task_json["status_changed_timestamp"],
            task_json["created"],
        )
        return task

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

    def get_tasks_for_process(self, process: ProcessDTO) -> list:
        results = []
        records = self.db.query_table_begins(
            {"pk": f"PROCESS#{process.process_id}", "sk": "TASK"}
        )
        results = [convert_json_to_task(t) for t in records]
        return results
