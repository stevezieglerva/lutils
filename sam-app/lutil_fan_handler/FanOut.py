import json
import uuid
import boto3

from NamedTupleBase import FanJob


class FanOut:
    def __init__(self, process_name, table_name="xyz"):
        self._db = boto3.client("dynamodb")
        if not self._table_exists(table_name):
            raise ValueError(f"{table_name} does not exist")
        self.table_name = table_name
        self.process_name = process_name
        self.process_id = str(uuid.uuid1())

    def _table_exists(self, table_name):
        results = self._db.describe_table(TableName=table_name)

    def __str__(self):
        text = ""
        return text

    def __repr__(self):
        return str(self)

    def fan_out(self, task_name, message):
        if type(message) != dict:
            raise TypeError("message must be a dict")
        job = FanJob(
            self.process_id,
            self.process_name,
            task_name,
            json.dumps(message, default=str),
        )
        self._put_item(job)
        return job

    def _put_item(self, job):
        raise ValueError()
