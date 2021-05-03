import json
import re
import uuid
from datetime import datetime

import boto3

from DynamoDB import DynamoDB
from NamedTupleBase import *


class FanIn:
    def __init__(self, **kwargs):
        assert (
            "stream_record" in kwargs or "event_string" in kwargs
        ), "Need argument for stream_record or event_string"

        self._set_properties_from_record(stream_record)

    def _set_properties_from_record(self, stream_record):
        self.event_name = stream_record["eventName"]
        self.table_name = self._get_table_name_from_source_arn(
            stream_record["eventSourceARN"]
        )
        db = DynamoDB(self.table_name, "pk")
        item_format = {}
        item_format["Item"] = stream_record["dynamodb"]["NewImage"]
        image = db.covert_from_dynamodb_format(item_format)
        image_string = json.dumps(image, indent=3, default=str)
        self.created_fan_job = get_createdfanjob_from_string(image_string)

    def _get_table_name_from_source_arn(self, arn):
        parts = arn.split(":")
        table_name_position = 5
        table_name = parts[table_name_position]
        table_name = table_name.replace("table/", "")
        without_stream = re.sub("/stream.*", "", table_name)
        return without_stream
