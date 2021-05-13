import json
from datetime import datetime

from DynamoDB import DynamoDB
from FanEvent import *


class TaskRecord:
    def __init__(self, **kwargs):

        kwargs_set = list(kwargs.keys())
        print(kwargs_set)
        assert sorted(kwargs_set) == sorted(
            ["db", "process_id", "process_name", "task_name", "task_message"]
        ) or sorted(kwargs_set) == [
            "db",
            "record_string",
        ], "keyword arguments must be (record_string) or (process_id, process_name, task_name, and task_message)"

        self.pk = ""
        self.sk = ""
        self.gs1_pk = "-"
        self.gs1_sk = "-"
        self.process_id = ""
        self.process_name = ""
        self.task_name = ""
        self.task_message = ""
        self.status = ""
        self.status_changed_timestamp = "-none-"
        self.created = ""

        if "record_string" in kwargs:
            record_json = json.loads(kwargs["record_string"])
            self.pk = record_json["pk"]
            self.sk = record_json["sk"]
            self.gs1_pk = record_json["gs1_pk"]
            self.gs1_sk = record_json["gs1_sk"]
            self.process_name = record_json["process_name"]
            self.task_name = record_json["task_name"]
            self.task_message = record_json["task_message"]
            self.status = record_json["status"]
            self.status_changed_timestamp = record_json["status_changed_timestamp"]
            self.created = record_json["created"]
        else:
            self.process_id = kwargs["process_id"]
            self.process_name = kwargs["process_name"]
            self.task_name = kwargs["task_name"]
            self.task_message = kwargs["task_message"]
            self.pk = f"PROCESS#{self.process_id}"
            self.sk = f"TASK#{self.task_name}"
            self.created = datetime.now().isoformat()

        self.db = None
        if "db" in kwargs:
            self.db = kwargs["db"]

    def json(self):
        dict_values = self.__dict__.copy()
        dict_values.pop("db")
        return dict_values

    def __str__(self):
        text = json.dumps(self.json(), indent=3, default=str)
        return text

    def __repr__(self):
        return str(self)

    def fan_out(self):
        assert self.db is not None, "Need to pass the db parameter in for DB updates"
        self.status = FAN_OUT
        self.status_changed_timestamp = datetime.now().isoformat()
        print(self.json())
        self.db.put_item(self.json())

    def start(self):
        assert self.db is not None, "Need to pass the db parameter in for DB updates"
        self.status = TASK_STARTED
        self.status_changed_timestamp = datetime.now().isoformat()
        print(self.json())
        self.db.put_item(self.json())

    def complete(self):
        assert self.db is not None, "Need to pass the db parameter in for DB updates"
        self.status = TASK_COMPLETED
        self.status_changed_timestamp = datetime.now().isoformat()
        print(self.json())
        self.db.put_item(self.json())
