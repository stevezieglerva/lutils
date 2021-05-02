import json
from datetime import datetime
from collections import namedtuple


class ClassConverter:
    def json(self):
        dict_value = json.loads(json.dumps(self._asdict()))
        dict_value["timestamp"] = datetime.now().isoformat()
        return dict_value

    def __str__(self):
        value = self.json()
        return json.dumps(value, indent=3, default=str)


class IndexQueueEvent(namedtuple("X", "bucket key domain index"), ClassConverter):
    pass


def get_indexqueueevent_from_string(text):
    replaced_single_quote_identifiers = text.replace("'", '"')
    text_json = json.loads(replaced_single_quote_identifiers)

    return IndexQueueEvent(
        bucket=text_json["bucket"],
        key=text_json["key"],
        domain=text_json["domain"],
        index=text_json["index"],
    )


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


class CreatedFanJob(
    namedtuple(
        "X",
        "process_id process_name task_name message completion_sns_arn timestamp pk status status_change_timestamp",
    ),
    ClassConverter,
):
    pass