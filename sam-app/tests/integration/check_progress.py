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
print()
for process in processes:
    name = process["process_name"]
    gs1_pk = process["gs1_pk"]
    progress = process["progress"]
    print(f"{name:<30} {gs1_pk:<15} {progress}")
print()