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
    namedtuple("X", "process_id process_name task_name message"), ClassConverter
):
    pass