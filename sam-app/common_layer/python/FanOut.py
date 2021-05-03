import json
import uuid
from datetime import datetime

import boto3

from DynamoDB import DynamoDB
from NamedTupleBase import FanJob, CreatedFanJob
import FanTaskStatus


class FanOut:
    def __init__(self, process_name, completion_sns_arn, table_name="xyz"):

        if not self._table_exists(table_name):
            raise ValueError(f"{table_name} does not exist")
        self.table_name = table_name
        self.completion_sns_arn = completion_sns_arn
        self.process_name = process_name
        self.process_id = str(uuid.uuid1())
        self._dynamodb = DynamoDB(self.table_name, "pk")
        self.job_tmsp = datetime.now().isoformat()

    def _table_exists(self, table_name):
        db = boto3.client("dynamodb")
        try:
            results = db.describe_table(TableName=table_name)
            return True
        except Exception as e:
            print(e)
            return False

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
            json.dumps(message, indent=3, default=str),
            self.completion_sns_arn,
        )
        added_data = self._put_item(job)
        return added_data

    def _put_item(self, job):
        job_dict = job.json()
        job_dict["timestamp"] = self.job_tmsp
        job_dict["pk"] = "FAN-OUT-JOB#" + job.process_id + "-TASK#" + job.task_name
        job_dict["status"] = FanTaskStatus.TASK_CREATED
        job_dict["status_change_timestamp"] = datetime.now().isoformat()
        print(json.dumps(job_dict, indent=3, default=str))
        self._dynamodb.put_item(job_dict)
        fan_job_created = job.create_job(
            job_dict["pk"],
            job_dict["timestamp"],
            job_dict["status"],
            job_dict["status_change_timestamp"],
        )
        print(fan_job_created)
        return fan_job_created
