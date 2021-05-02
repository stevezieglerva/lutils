import json
import re
import uuid
from datetime import datetime

import boto3

from DynamoDB import DynamoDB
from NamedTupleBase import CreatedFanJob, FanJob


class FanIn:
    def __init__(self, stream_record):
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
        self.created_fan_job = CreatedFanJob(
            process_id=image["process_id"],
            process_name=image["process_name"],
            task_name=image["task_name"],
            message=image["message"],
            completion_sns_arn=image["completion_sns_arn"],
            timestamp=image["timestamp"],
            pk=image["pk"],
            status=image["status"],
            status_change_timestamp=image["status_change_timestamp"],
        )

    def _get_table_name_from_source_arn(self, arn):
        parts = arn.split(":")
        table_name_position = 5
        table_name = parts[table_name_position]
        table_name = table_name.replace("table/", "")
        without_stream = re.sub("/stream.*", "", table_name)
        return without_stream
