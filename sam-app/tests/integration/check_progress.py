import inspect
import json
import os
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/common_layer_hex/python"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

from DynamoDB import DynamoDB


db = DynamoDB("lutils2-FanProcessingPartTestTable-Q3PVEB6MO2AJ")


processes = db.query_index_begins(
    "gs1", {"gs1_pk": "STATUS#in_progress", "gs1_sk": "-"}
)

sorted_processes = sorted(processes, key=lambda item: item["started"])

print()
for process in sorted_processes:
    name = process["process_name"]
    gs1_pk = process["gs1_pk"]
    progress = process["progress"]
    started = process["started"]
    process_id = process["process_id"]
    print(
        f"{started:<20}   {name:<30}   {gs1_pk:<15}   {progress:<3}   {process_id:<20}"
    )
print()