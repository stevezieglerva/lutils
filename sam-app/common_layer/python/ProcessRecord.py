import json

PLACEHOLDER_INDEX_FIELD_VALUE = "-"


class ProcessRecord:
    def __init__(self, **kwargs):
        self.pk = ""
        self.sk = ""
        self.gs1_pk = ""
        self.gs1_sk = ""
        self.process_name = ""
        self.started = ""
        self.ended = ""
        self.progress = 0
        if "process_name" in kwargs:
            self.process_name = kwargs["process_name"]
        if "record_string" in kwargs:
            record_json = json.loads(kwargs["record_string"])
            self.pk = record_json["pk"]
            self.sk = record_json["sk"]
            self.gs1_pk = record_json["gs1_pk"]
            self.gs1_sk = record_json["gs1_sk"]
            self.process_name = record_json["process_name"]
            self.started = record_json["started"]
            self.ended = record_json["ended"]

    def json(self):
        return self.__dict__

    def __str__(self):
        text = json.dumps(self.__dict__, indent=3, default=str)
        return text

    def __repr__(self):
        return str(self)