import json
from datetime import datetime
from collections import namedtuple

import FanEventOptions


class ClassConverter:
    def json(self):
        dict_value = json.loads(json.dumps(self._asdict()))
        dict_value["timestamp"] = datetime.now().isoformat()
        return dict_value

    def __str__(self):
        value = self.json()
        return json.dumps(value, indent=3, default=str)


class FanJob(
    namedtuple("X", "process_id process_name task_name message completion_sns_arn"),
    ClassConverter,
):
    def create_job(self, pk, timestamp, status, status_change_timestamp):
        new = CreatedFanJob(
            process_id=self.process_id,
            process_name=self.process_name,
            task_name=self.task_name,
            message=self.message,
            completion_sns_arn=self.completion_sns_arn,
            timestamp=timestamp,
            pk=pk,
            status=status,
            status_change_timestamp=status_change_timestamp,
        )
        return new


def get_fanjob_from_string(text):
    replaced_single_quote_identifiers = text.replace("'", '"')
    text_json = json.loads(replaced_single_quote_identifiers)

    return FanJob(
        process_id=text_json["process_id"],
        process_name=text_json["process_name"],
        task_name=text_json["task_name"],
        message=text_json["message"],
        completion_sns_arn=text_json["completion_sns_arn"],
    )


class CreatedFanJob(
    namedtuple(
        "X",
        "process_id process_name task_name message completion_sns_arn timestamp pk status status_change_timestamp",
    ),
    ClassConverter,
):
    pass


def get_createdfanjob_from_string(text):
    replaced_single_quote_identifiers = text.replace("'", '"')
    text_json = json.loads(replaced_single_quote_identifiers)

    return CreatedFanJob(
        process_id=text_json["process_id"],
        process_name=text_json["process_name"],
        task_name=text_json["task_name"],
        message=text_json["message"],
        completion_sns_arn=text_json["completion_sns_arn"],
        pk=text_json["pk"],
        timestamp=text_json["timestamp"],
        status=text_json["status"],
        status_change_timestamp=text_json["status_change_timestamp"],
    )


class FanEvent(
    namedtuple(
        "X",
        "process_id process_name task_name event",
    ),
    ClassConverter,
):
    def __init__(self, process_id, process_name, task_name, event):
        possible_events = [FanEventOptions.TASK_CREATED]
        if self.event not in possible_events:
            raise ValueError(
                f"event of '{self.event}'' in not one of {possible_events}"
            )


def get_fanevent_from_string(text):
    replaced_single_quote_identifiers = text.replace("'", '"')
    text_json = json.loads(replaced_single_quote_identifiers)

    return FanEvent(
        process_id=text_json["process_id"],
        process_name=text_json["process_name"],
        task_name=text_json["task_name"],
        event=text_json["event"],
    )
