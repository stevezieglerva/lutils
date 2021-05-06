import json

PLACEHOLDER_INDEX_FIELD_VALUE = "-"


class TaskRecord:
    def __init__(self, **kwargs):
        self.pk = ""
        self.sk = ""
        self.gsk1_pk = ""
        self.gsk1_sk = ""
        self.process_name = ""
        self.task_name = ""
        self.status = ""
        self.status_changed = ""
        self.created = ""
        if "process_name" in kwargs:
            self.process_name = kwargs["process_name"]
        if "task_name" in kwargs:
            self.task_name = kwargs["task_name"]
        if "record_string" in kwargs:
            record_json = json.loads(kwargs["record_string"])
            self.pk = record_json["pk"]
            self.sk = record_json["sk"]
            self.gsk1_pk = record_json["gsk1_pk"]
            self.gsk1_sk = record_json["gsk1_sk"]
            self.process_name = record_json["process_name"]
            self.task_name = record_json["task_name"]
            self.status = record_json["status"]
            self.status_changed = record_json["status_changed"]
            self.created = record_json["created"]

    def json(self):
        return self.__dict__

    def __str__(self):
        text = json.dumps(self.__dict__, indent=3, default=str)
        return text

    def __repr__(self):
        return str(self)