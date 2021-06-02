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

from infrastructure.repository.DynamoDB import DynamoDB

process_id = sys.argv[1]
print(f"Getting data for: {process_id}")


audit = DynamoDB("AUDIT")
scan = audit.scan_full()
only_tasks = [i for i in scan if i["pk"] == process_id and i["sk"].startswith("TASK")]
sorted_scan = sorted(only_tasks, key=lambda k: k["key"])
print("\n\n\n\n************************************")
for i in sorted_scan:
    print(i["sk"] + " - " + i["action"])
    changes = i["changes"]
    changes = "\t" + changes.replace(" | ", "\n\t")
    print(changes)

db = DynamoDB("lutils-FanProcessingPartTestTable-1O7DX6QTMG6N8")
main_data = db.query_table_equal({"pk": process_id, "sk": process_id})
print(json.dumps(main_data, indent=3, default=str))