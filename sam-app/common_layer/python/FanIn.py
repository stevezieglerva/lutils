import json
import re
import uuid
from datetime import datetime

import boto3

from DynamoDB import DynamoDB
from NamedTupleBase import *


class FanIn:
    def __init__(self, sns_arn, **kwargs):
        assert (
            "stream_record" in kwargs or "event_string" in kwargs
        ), "Need argument for stream_record or event_string"

        assert not (
            "stream_record" in kwargs and "event_string" in kwargs
        ), "Can't provide both keyword arguments"
        stream_record = kwargs.get("stream_record", "")
        if stream_record != "":
            self._set_properties_from_record(stream_record)
        else:
            event_string = kwargs["event_string"]
            self._set_properties_from_event_string(event_string)
        self.sns_arn = sns_arn

    def _set_properties_from_record(self, stream_record):
        self.event_name = stream_record["eventName"]
        self.table_name = self._get_table_name_from_source_arn(
            stream_record["eventSourceARN"]
        )
        db = DynamoDB(self.table_name, "pk")
        item_format = {}
        item_format["Item"] = stream_record["dynamodb"]["NewImage"]
        image = db.convert_from_dynamodb_format(item_format)
        image_string = json.dumps(image, indent=3, default=str)
        self.created_fan_job = get_createdfanjob_from_string(image_string)

    def _set_properties_from_event_string(self, event_string):
        self.event_name = ""  # TODO this is dirty!
        self.table_name = ""  # TODO also dirty - data not know at this point
        self.created_fan_job = get_createdfanjob_from_string(event_string)

    def _get_table_name_from_source_arn(self, arn):
        parts = arn.split(":")
        table_name_position = 5
        table_name = parts[table_name_position]
        table_name = table_name.replace("table/", "")
        without_stream = re.sub("/stream.*", "", table_name)
        return without_stream

    def update_task(self, event):
        sns = boto3.client("sns")
        event = FanEvent(
            self.created_fan_job.process_id,
            self.created_fan_job.process_name,
            self.created_fan_job.task_name,
            event,
        )
        message = str(event)
        print(f"Sending message to {self.sns_arn}: {message}")
        sns = boto3.client("sns")
        result = sns.publish(
            TopicArn=self.sns_arn,
            Message=message,
            MessageAttributes={
                "event_name": {"DataType": "String", "StringValue": "task_update"},
                "process_name": {
                    "DataType": "String",
                    "StringValue": self.created_fan_job.process_name,
                },
            },
        )
        print("Sent!")