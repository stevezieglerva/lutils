from datetime import datetime
import ulid


class DynamoDBStream:
    def __init__(self, stream_event):
        self.stream_event = stream_event
        pass

    def __str__(self):
        text = ""
        return text

    def __repr__(self):
        return str(self)

    def get_formated_changes_json(self):
        results = []
        for record in self.stream_event["Records"]:
            new_item = {}
            primary_key_string = ""
            for k, v in record["dynamodb"]["Keys"].items():
                key_name = k
                key_value = list(v.values())[0]
                primary_key_string = primary_key_string + f"{key_name} / {key_value}"
            primary_key_string = primary_key_string + " #" + str(ulid.ULID())
            print(primary_key_string)
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
                    print(f"processing {k}")
                    new_value = list(dynamodb_v.values())[0]
                    old_value = "*"
                    if old_image != None:
                        if k in old_image:
                            print(old_image[k])
                            old_value = list(old_image[k].values())[0]

                    if old_value != new_value:
                        field = f"{k}: '{old_value}' -> '{new_value}'"
                        changes = changes + field + " | "
            else:
                changes = "   -> X"
            new_item["changes"] = changes
            results.append(new_item)
        return results

    def _determine_action(self, old_image, new_image):
        if old_image and new_image:
            return "UPDATE"
        elif old_image:
            return "DELETE"
        return "INSERT"
