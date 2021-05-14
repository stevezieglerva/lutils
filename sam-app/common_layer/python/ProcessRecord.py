import json
from datetime import datetime

PLACEHOLDER_INDEX_FIELD_VALUE = "-"

from FanEvent import *


class ProcessRecord:
    def __init__(self, **kwargs):

        kwargs_set = sorted(list(kwargs.keys()))
        assert kwargs_set == sorted(
            ["db", "process_id", "process_name"]
        ) or kwargs_set == [
            "db",
            "record_string",
        ], "keyword arguments must be (db, record_string) or (db, process_id, process_name)"

        self.pk = ""
        self.sk = ""
        self.gs1_pk = PLACEHOLDER_INDEX_FIELD_VALUE
        self.gs1_sk = PLACEHOLDER_INDEX_FIELD_VALUE
        self.process_id = ""
        self.process_name = ""
        self.started = ""
        self.ended = ""
        self.progress = 0
        self.db = None
        if "process_name" in kwargs and "process_id" in kwargs:
            self.process_id = kwargs["process_id"]
            self.process_name = kwargs["process_name"]
            self.pk = f"PROCESS#{self.process_id}"
            self.sk = self.pk
            self.started = datetime.now().isoformat()
            self.progress = 0
            self.db = kwargs["db"]
        if "record_string" in kwargs:
            record_json = json.loads(kwargs["record_string"])
            self.pk = record_json["pk"]
            self.sk = record_json["sk"]
            self.gs1_pk = record_json["gs1_pk"]
            self.gs1_sk = record_json["gs1_sk"]
            self.process_id = record_json["process_id"]
            self.process_name = record_json["process_name"]
            self.progress = float(record_json["progress"])
            self.started = record_json["started"]
            self.ended = record_json["ended"]
            self.db = kwargs["db"]
            self_properties = vars(self)
            for k, v in self_properties.items():
                if type(v) == str:
                    if v == "" and k != "ended":
                        raise ValueError(f"Missing value for {k} in json")

    def json(self):
        dict_values = self.__dict__.copy()
        dict_values.pop("db")
        return dict_values

    def __str__(self):
        text = json.dumps(self.__dict__, indent=3, default=str)
        return text

    def __repr__(self):
        return str(self)

    def save(self):
        self.db.put_item(self.json())

    def update_process_record_based_on_completions(self):
        # check if all tasks completed
        process_tasks_list = self._get_all_tasks_for_process()
        print("all tasks:")
        print(json.dumps(process_tasks_list, indent=3, default=str))
        progress = self._calculate_progress(process_tasks_list)
        print(f"Progress: {progress}")

        self.progress = progress
        if self.progress == 1.0:
            self.ended = datetime.now().isoformat()
        self.save()

    def _calculate_progress(self, process_task_list):
        total_tasks = len(process_task_list)
        completed_tasks = [
            t for t in process_task_list if t["status"] == TASK_COMPLETED
        ]
        completed_count = len(completed_tasks)
        return float(completed_count / total_tasks)

    def _get_all_tasks_for_process(self):
        return self.db.query_table_begins({"pk": self.pk, "sk": "TASK"})