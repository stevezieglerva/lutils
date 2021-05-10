import json
from datetime import datetime

PLACEHOLDER_INDEX_FIELD_VALUE = "-"


class ProcessRecord:
    def __init__(self, **kwargs):

        kwargs_set = list(kwargs.keys())
        assert sorted(kwargs_set) == sorted(
            ["process_id", "process_name"]
        ) or kwargs_set == [
            "record_string"
        ], "keyword arguments must be (record_string) or (process_id, process_name)"

        self.pk = ""
        self.sk = ""
        self.gs1_pk = PLACEHOLDER_INDEX_FIELD_VALUE
        self.gs1_sk = PLACEHOLDER_INDEX_FIELD_VALUE
        self.process_id = ""
        self.process_name = ""
        self.started = ""
        self.ended = ""
        self.progress = 0
        if "process_name" in kwargs and "process_id" in kwargs:
            self.process_id = kwargs["process_id"]
            self.process_name = kwargs["process_name"]
            self.pk = f"PROCESS#{self.process_id}"
            self.sk = self.pk
            self.started = datetime.now().isoformat()
            self.progress = 0
        if "record_string" in kwargs:
            record_json = json.loads(kwargs["record_string"])
            self.pk = record_json["pk"]
            self.sk = record_json["sk"]
            self.gs1_pk = record_json["gs1_pk"]
            self.gs1_sk = record_json["gs1_sk"]
            self.process_id = record_json["process_id"]
            self.process_name = record_json["process_name"]
            self.started = record_json["started"]
            self.ended = record_json["ended"]
            for k, v in vars(self).items():
                if type(v) == str:
                    if v == "":
                        raise ValueError(f"Missing value for {k} in json")

    def json(self):
        return self.__dict__

    def __str__(self):
        text = json.dumps(self.__dict__, indent=3, default=str)
        return text

    def __repr__(self):
        return str(self)