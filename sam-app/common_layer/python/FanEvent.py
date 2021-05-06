import json
from datetime import datetime
from collections import namedtuple

FAN_OUT = "fan_out"
TASK_CREATED = "task_created"
TASK_COMPLETED = "task_completed"
TASK_STARTED = "task_started"
TASK_COMPLETED = "task_completed"
TASK_ERROR = "task_error"

PROCESS_COMPLETED = "process_completed"

from NamedTupleBase import *


class FanEvent:
    def __init__(self, **kwargs):
        self.event_source = ""
        self.event_name = ""
        self.message = {}
        self.timestamp = ""

        if "event_source" in kwargs:
            self.event_source = kwargs["event_source"]
        if "event_name" in kwargs:
            self.event_name = kwargs["event_name"]
            possible_events = [
                FAN_OUT,
                TASK_CREATED,
                TASK_COMPLETED,
                TASK_STARTED,
                TASK_COMPLETED,
                TASK_ERROR,
                PROCESS_COMPLETED,
            ]
            if self.event_name not in possible_events:
                raise ValueError(
                    f"event_name of '{event_name}'' is not one of {possible_events}"
                )
        if "message" in kwargs:
            message = kwargs["message"]
            assert (
                type(message) == dict
            ), f"message parameter of {message} must be a dict"
            self.message = message
        if "timestamp" in kwargs:
            self.timestamp = kwargs["timestamp"]
        if "record_string" in kwargs:
            record_string = kwargs["record_string"].replace("'", '"')
            record_json = json.loads(record_string)
            self.event_source = record_json["event_source"]
            self.event_name = record_json["event_name"]
            self.message = record_json["message"]

    def json(self):
        dict_value = json.loads(json.dumps(vars(self)))
        return dict_value

    def __str__(self):
        value = self.json()
        return json.dumps(value, default=str)

    def get_formatted_line(self):
        line = f"{self.event_source:<20} {self.event_name:<40} "
        process_id = self.message.get("process_id", "")
        if process_id != "":
            line = line + f" {process_id:<40} "
        process_name = self.message.get("process_name", "")
        if process_name != "":
            line = line + f" {process_name:<40} "
        task_name = self.message.get("task_name", "")
        if task_name != "":
            line = line + f" {self.task_name:<40}"
        return line
