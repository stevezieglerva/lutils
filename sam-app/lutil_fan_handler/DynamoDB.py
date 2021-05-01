import json
from datetime import datetime

import boto3


class DynamoDB:
    def __init__(self, table_name, key_field):
        self.table_name = table_name
        self.key_field = key_field
        self._db = boto3.client("dynamodb")

    def __str__(self):
        text = ""
        return text

    def __repr__(self):
        return str(self)

    def put_item(self, record):
        db_format = self._convert_json_format(record)
        self._db.put_item(TableName=self.table_name, Item=db_format)

    def _convert_json_format(self, record):
        results = {}
        for k, v in record.items():
            print(f"{k} : {v}")
            if type(v) == str:
                data_type = "S"
            if type(v) == int or type(v) == float:
                data_type = "N"
            if type(v) == datetime:
                data_type = "N"

            new_field_value = {}
            new_field_value[data_type] = str(v)
            results[k] = new_field_value
        print(json.dumps(results, indent=3, default=str))
        return results

    def get_item(self, key):
        key_json = {}
        key_json[self.key_field] = key
        db_format = self._convert_json_format(key_json)
        print(json.dumps(db_format, indent=3, default=str))
        results = self._db.get_item(TableName=self.table_name, Key=db_format)
        return results