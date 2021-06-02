import json
from datetime import datetime

import ulid
from infrastructure.repository.DynamoDB import DynamoDB


class DynamoDBStream:
    def __init__(self, stream_event):
        self.stream_event = stream_event
        self.changes = []
        self._set_formated_changes_json()

    def __str__(self):
        text = json.dumps(self.changes, indent=3, default=str)
        return text

    def __repr__(self):
        return str(self)

    def _set_formated_changes_json(self):
        for record in self.stream_event["Records"]:
            new_item = {}
            primary_key_string = ""
            for k, v in record["dynamodb"]["Keys"].items():
                key_name = k
                key_value = list(v.values())[0]
                new_item[key_name] = key_value

            primary_key_string = str(ulid.ULID())
            new_item["key"] = primary_key_string

            old_image = record["dynamodb"].get("OldImage", None)
            new_image = record["dynamodb"].get("NewImage", None)
            action = self._determine_action(old_image, new_image)

            tmsp_epoch = record["dynamodb"]["ApproximateCreationDateTime"]
            new_item["tmsp"] = datetime.fromtimestamp(tmsp_epoch).isoformat()

            new_item["action"] = action
            changes = ""
            if new_image != None:
                for k, dynamodb_v in new_image.items():
                    new_value = list(dynamodb_v.values())[0]
                    old_value = "*"
                    if old_image != None:
                        if k in old_image:
                            old_value = list(old_image[k].values())[0]

                    if old_value != new_value:
                        field = f"{k}: '{old_value}' -> '{new_value}'"
                        changes = changes + field + " | "
            else:
                changes = "   -> X"
            new_item["changes"] = changes
            self.changes.append(new_item)

    def _determine_action(self, old_image, new_image):
        if old_image and new_image:
            return "UPDATE"
        elif old_image:
            return "DELETE"
        return "INSERT"

    def save_to_table(self, table_name):
        db = DynamoDB(table_name)
        for change in self.changes:
            db.put_item(change)
