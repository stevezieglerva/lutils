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
        key_schema = table_resp["Table"]["KeySchema"]
        self.key_fields = [k["AttributeName"] for k in key_schema]

    def set_ttl_seconds(self, seconds):
        self._ttl = seconds

    def put_item(self, record):
        if self._ttl != None:
            ttl = self._calculate_ttl_epoch()
            record["ttl"] = ttl
        db_format = self.convert_to_dynamodb_format(record)
        self._db.put_item(TableName=self.table_name, Item=db_format)
        print(f"put item successful: {db_format}")

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
        return results

    def convert_from_dynamodb_format(self, db_record):
        return self.convert_from_dict_format(db_record["Item"])

    def convert_from_dict_format(self, dict):
        results = {}
        for k, v in dict.items():
            field_name = k
            for sub_k, sub_v in v.items():
                type = sub_k
                field_value = sub_v
                # try to convert to dict
                if type == "S":
                    if "{" in field_value:
                        try:
                            json_str = field_value.replace("'", '"')
                            json_str = json_str[1:]
                            json_str = json_str[:-1]
                            field_dict = json.loads(json_str)
                            field_value = field_dict
                        except json.decoder.JSONDecodeError:
                            # field is not JSON
                            pass
                if type == "N":
                    field_value = float(field_value)
            results[field_name] = field_value
        return results

    def convert_list_from_dynamodb_format(self, query_results):
        converted_results = []
        for item in query_results["Items"]:
            converted_results.append(self.convert_from_dict_format(item))
        return converted_results

    def get_item(self, key):
        assert type(key) == dict, "Expecting key to be of type dict"
        db_format = self.convert_to_dynamodb_format(key)
        print(f"Getting: {db_format}")
        db_record = self._db.get_item(TableName=self.table_name, Key=db_format)
        results = self.convert_from_dynamodb_format(db_record)
        return results

    def query_table_equal(self, key):
        key_condition_exp_parts = [f"{k} = :{k}" for k in key.keys()]
        key_condition_exp = " AND ".join(key_condition_exp_parts)
        print(f"key_condition_exp: {key_condition_exp}")
        return self._query_table_by_operator(key, key_condition_exp)

    def query_table_begins(self, key):
        key_names = list(key.keys())
        if len(key_names) == 1:
            field_name = key_names[0]
            key_condition_exp = f"begins_with( {field_name}, :{field_name} )"
        if len(key_names) == 2:
            field_name_1 = key_names[0]
            field_name_2 = key_names[1]
            key_condition_exp = f"{field_name_1} = :{field_name_1} AND begins_with( {field_name_2}, :{field_name_2})"
        print(f"key_condition_exp: {key_condition_exp}")
        return self._query_table_by_operator(key, key_condition_exp)

    def scan_full(self):
        scan_results = self._db.scan(TableName=self.table_name)
        return self.convert_list_from_dynamodb_format(scan_results)

    def _query_table_by_operator(self, key, key_condition_exp):
        assert type(key) == dict, "Expecting key to be of type dict"
        exp_attribute_values = key
        original_key_list = list(key.keys())
        for key_name in original_key_list:
            expr_key_name = f":{key_name}"
            exp_attribute_values[expr_key_name] = key[key_name]
            exp_attribute_values.pop(key_name)
        exp_attribute_values_db_format = self.convert_to_dynamodb_format(
            exp_attribute_values
        )
        print(f"exp_attribute_values_db_format: {exp_attribute_values_db_format}")

        query_response = self._db.query(
            TableName=self.table_name,
            KeyConditionExpression=key_condition_exp,
            ExpressionAttributeValues=exp_attribute_values_db_format,
        )
        results = self.convert_list_from_dynamodb_format(query_response)
        return results