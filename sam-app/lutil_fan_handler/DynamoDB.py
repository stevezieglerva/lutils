import boto3


class DDB:
    def __init__(self, table_name):
        self.table_name = table_name
        self._db = boto3.client("dynamodb")

    def __str__(self):
        text = ""
        return text

    def __repr__(self):
        return str(self)

    def put_item(record):
        pass