import json
from datetime import datetime, timedelta
from time import time

import boto3


class DynamoDB:
    def __init__(self, table_name, key_field):
        self.table_name = table_name
        self.key_field = key_field
        self._db = boto3.client("dynamodb")
        self._ttl = None

    def set_ttl_seconds(self, seconds):
        self._ttl = seconds

    def put_item(self, record):
        if self._ttl != None:
            ttl = self._calculate_ttl_epoch()
            record["ttl"] = ttl
        db_format = self.convert_to_dynamodb_format(record)
        self._db.put_item(TableName=self.table_name, Item=db_format)

    def _calculate_ttl_epoch(self):
        future_time = datetime.now() + timedelta(self._ttl)
        return int(future_time.strftime("%s"))

    def convert_to_dynamodb_format(self, record):
        results = {}
        for k, v in record.items():
            data_type = ""
            new_value = str(v)
            if type(v) == str:
                data_type = "S"
            if type(v) == int or type(v) == float:
                data_type = "N"
            if type(v) == datetime:
                data_type = "N"
            if data_type == "":
                raise ValueError(f"no data type mapping for {type(v)}")

            new_field_value = {}
            new_field_value[data_type] = new_value
            results[k] = new_field_value
        print(json.dumps(results, indent=3, default=str))
        return results

    def covert_from_dynamodb_format(self, db_record):
        results = {}
        for k, v in db_record["Item"].items():
            field_name = k
            for sub_k, sub_v in v.items():
                type = sub_k
                field_value = sub_v
            results[field_name] = field_value
        return results

    def get_item(self, key):
        key_json = {}
        key_json[self.key_field] = key
        db_format = self.convert_to_dynamodb_format(key_json)
        print(json.dumps(db_format, indent=3, default=str))
        db_record = self._db.get_item(TableName=self.table_name, Key=db_format)
        results = self.covert_from_dynamodb_format(db_record)
        return results