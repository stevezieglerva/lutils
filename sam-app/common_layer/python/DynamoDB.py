import json
from datetime import datetime, timedelta
from time import time

import boto3


class DynamoDB:
    def __init__(self, table_name):
        self._db = boto3.client("dynamodb")
        self.table_name = table_name
        self._set_key_fields()
        self._ttl = None

    def _set_key_fields(self):
        table_resp = self._db.describe_table(TableName=self.table_name)
        # print(json.dumps(table_resp, indent=3, default=str))
        key_schema = table_resp["Table"]["KeySchema"]
        self.key_fields = [k["AttributeName"] for k in key_schema]
        print(self.key_fields)

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
            if type(v) == dict:
                # convert to string for storage instead of using complicated dynamobd format for dicts
                data_type = "S"
                new_value = json.dumps(str(v), indent=3, default=str)
            if data_type == "":
                raise ValueError(f"no data type mapping for {type(v)}")

            new_field_value = {}
            new_field_value[data_type] = new_value
            results[k] = new_field_value
        print(json.dumps(results, indent=3, default=str))
        return results

    def convert_from_dynamodb_format(self, db_record):
        results = {}
        for k, v in db_record["Item"].items():
            field_name = k
            for sub_k, sub_v in v.items():
                type = sub_k
                field_value = sub_v
                # try to convert to dict
                if type == "S":
                    try:
                        json_str = field_value.replace("'", '"')
                        json_str = json_str[1:]
                        json_str = json_str[:-1]
                        field_dict = json.loads(json_str)
                        print(f"converted {field_name} to JSON")
                        field_value = field_dict
                    except json.decoder.JSONDecodeError:
                        # field is not JSON
                        pass
            results[field_name] = field_value
        return results

    def get_item(self, key):
        assert type(key) == dict, "Expecting key to be of type dict"
        db_format = self.convert_to_dynamodb_format(key)
        db_record = self._db.get_item(TableName=self.table_name, Key=db_format)
        results = self.convert_from_dynamodb_format(db_record)
        return results