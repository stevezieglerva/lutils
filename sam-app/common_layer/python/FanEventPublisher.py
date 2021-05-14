import json
from ulid import ULID
from collections import namedtuple
from datetime import datetime

import boto3

from FanEvent import *
from NamedTupleBase import FanJob


class FanEventPublisher:
    def __init__(self, event_source, topic_arn):
        self.event_source = event_source
        self.topic_arn = topic_arn
        self.sns = boto3.client("sns")

    def generate_process_id(self):
        return str(ULID())

    def publish_event(self, event_name, message_json):
        new_event = FanEvent(
            event_source=self.event_source, event_name=event_name, message=message_json
        )
        result = self._publish_sns(new_event)
        print(result)
        return result

    def _publish_sns(self, event):
        result = self.sns.publish(
            TopicArn=self.topic_arn,
            Message=str(event),
            MessageAttributes={
                "event_name": {"DataType": "String", "StringValue": event.event_name},
                "process_name": {
                    "DataType": "String",
                    "StringValue": event.message["process_name"],
                },
                "event_source": {
                    "DataType": "String",
                    "StringValue": event.event_source,
                },
            },
        )
        return result

    def get_fanevent_from_string(self, text):
        replaced_single_quote_identifiers = text.replace("'", '"')
        text_json = json.loads(replaced_single_quote_identifiers)

        return FanEvent(
            process_id=text_json["process_id"],
            process_name=text_json["process_name"],
            task_name=text_json["task_name"],
            event=text_json["event"],
        )
