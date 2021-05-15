import inspect
import json
import os
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/common_layer/python"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

from DynamoDB import DynamoDB

process_id = sys.argv[1]
print(f"Getting data for: {process_id}")


db = DynamoDB("lutils2-FanProcessingPartTestTable-Q3PVEB6MO2AJ")


tasks = db.query_table_begins({"pk": process_id, "sk": "TASK"})
for task in tasks:
    task_name = task["task_name"]
    status = task["status"]
    print(f"{task_name:<20} - {status}")


main_data = db.get_item({"pk": process_id, "sk": process_id})
progress = main_data["progress"]
print(f"\n\nProgress: {progress}\n\n")
