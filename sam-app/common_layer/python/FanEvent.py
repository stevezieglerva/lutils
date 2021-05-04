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


class FanEvent:
    def __init__(self, event_source, event_name, fan_job=None):
        self.event_source = event_source
        self.event_name = event_name
        self.job = fan_job
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
                f"event_name of '{self.event_name}'' is not one of {possible_events}"
            )

    def json(self):
        job_dict = {}
        if self.job != None:
            job_dict = self.job.json()
        dict_value = json.loads(json.dumps(vars(self)))
        dict_value["job"] = job_dict
        dict_value["timestamp"] = datetime.now().isoformat()
        return dict_value

    def __str__(self):
        value = self.json()
        return json.dumps(value, indent=3, default=str)

    def get_formatted_line(self):
        line = f"{self.event_source:<20} {self.event_name:<40} {self.job.process_id:<40} {self.job.process_name:<40} {self.job.task_name}"
        return line
