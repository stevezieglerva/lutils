import json
from datetime import datetime

PLACEHOLDER_INDEX_FIELD_VALUE = "-"


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