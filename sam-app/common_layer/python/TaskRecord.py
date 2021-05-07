import json


class TaskRecord:
    def __init__(self, **kwargs):

        kwargs_set = list(kwargs.keys())
        assert sorted(kwargs_set) == sorted(
            ["process_id", "process_name", "task_name", "task_message"]
        ) or kwargs_set == [
            "record_string"
        ], "keyword arguments must be record_string or process_id, process_name, task_name, or message"

        self.pk = ""
        self.sk = ""
        self.gsk1_pk = ""
        self.gsk1_sk = ""
        self.process_id = ""
        self.process_name = ""
        self.task_name = ""
        self.task_message = ""
        self.status = ""
        self.status_changed = ""
        self.created = ""

        if "record_string" in kwargs:
            record_json = json.loads(kwargs["record_string"])
            self.pk = record_json["pk"]
            self.sk = record_json["sk"]
            self.gsk1_pk = record_json["gsk1_pk"]
            self.gsk1_sk = record_json["gsk1_sk"]
            self.process_name = record_json["process_name"]
            self.task_name = record_json["task_name"]
            self.task_message = record_json["task_message"]
            self.status = record_json["status"]
            self.status_changed = record_json["status_changed"]
            self.created = record_json["created"]
        else:
            self.process_id = kwargs["process_id"]
            self.process_name = kwargs["process_name"]
            self.task_name = kwargs["task_name"]
            self.task_message = kwargs["task_message"]
            self.pk = f"PROCESS#{self.process_id}"
            self.sk = f"TASK#{self.task_name}"

    def json(self):
        return self.__dict__

    def __str__(self):
        text = json.dumps(self.__dict__, indent=3, default=str)
        return text

    def __repr__(self):
        return str(self)