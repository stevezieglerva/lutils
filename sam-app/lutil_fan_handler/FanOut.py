import json
import uuid
import boto3

from NamedTupleBase import FanJob


class FanOut:
    def __init__(self, process_name, storage_location="xyz"):
        self.storage_location = storage_location
        self.process_name = process_name
        self.process_id = uuid.uuid1()

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
            json.dumps(message, default=str),
        )
        return job
