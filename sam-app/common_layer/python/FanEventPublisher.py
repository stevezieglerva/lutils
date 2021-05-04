import json
from collections import namedtuple
from datetime import datetime

import boto3

from FanEvent import *
from NamedTupleBase import FanJob


class FanEventPublisher:
    def __init__(self, topic_arn):
        self.topic_arn = topic_arn
        self.sns = boto3.client("sns")

    def fan_out(self, process_name, task_name, message):
        job = FanJob("", process_name, task_name, message, "completion_sns_arn")
        event = FanEvent(process_name, FAN_OUT, job)
        result = self._publish_sns(event)
        print(result)
        return event

    def _publish_sns(self, event):
        result = self.sns.publish(
            TopicArn=self.topic_arn,
            Message=str(event),
            MessageAttributes={
                "event_name": {"DataType": "String", "StringValue": event.event_name},
                "process_name": {
                    "DataType": "String",
                    "StringValue": event.job.process_name,
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
