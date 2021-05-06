import json


class ProcessRecord:
    def __init__(self, **kwargs):
        self.pk = ""
        self.sk = ""
        self.process_name = kwargs["process_name"]
        self.started = ""
        self.ended = ""
        self.progress = 0

    def __str__(self):
        text = json.dumps(self.__dict__, indent=3, default=str)
        return text

    def __repr__(self):
        return str(self)
