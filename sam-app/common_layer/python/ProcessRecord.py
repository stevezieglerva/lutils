import json


class ProcessRecord:
    def __init__(self, **kwargs):
        self.pk = ""
        self.sk = ""
        self.process_name = ""
        self.started = ""
        self.ended = ""
        self.progress = 0
        if "process_name" in kwargs:
            self.process_name = kwargs["process_name"]
        if "record_string" in kwargs:
            record_json = json.loads(kwargs["record_string"])
            self.process_name = record_json["process_name"]
            self.pk = record_json["pk"]

    def __str__(self):
        text = json.dumps(self.__dict__, indent=3, default=str)
        return text

    def __repr__(self):
        return str(self)
