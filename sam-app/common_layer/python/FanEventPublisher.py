import json
from datetime import datetime
from collections import namedtuple

from FanEvent import *


class FanEventPublisher:
    def __init__(self, topic_arn):
        self.topic_arn = topic_arn

    def create_task(process_name, task_name):
        event = FanEvent()


def get_fanevent_from_string(text):
    replaced_single_quote_identifiers = text.replace("'", '"')
    text_json = json.loads(replaced_single_quote_identifiers)

    return FanEvent(
        process_id=text_json["process_id"],
        process_name=text_json["process_name"],
        task_name=text_json["task_name"],
        event=text_json["event"],
    )
