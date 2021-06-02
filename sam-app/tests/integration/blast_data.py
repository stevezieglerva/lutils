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

from datetime import datetime

tmsp = datetime.now().isoformat()

db = DynamoDB("lutils-FanProcessingPartTestTable-1O7DX6QTMG6N8")
number = 100
for i in range(number):
    item = {}
    item["pk"] = f"BLAST-{tmsp}"
    item["sk"] = f"TASK-{i}"
    item["gs1_pk"] = "-"
    item["gs1_sk"] = "-"
    item["status"] = "created"
    db.put_item(item)

for i in range(number):
    item = {}
    item["pk"] = f"BLAST-{tmsp}"
    item["sk"] = f"TASK-{i}"
    item["gs1_pk"] = "-"
    item["gs1_sk"] = "-"
    item["status"] = "started"
    db.put_item(item)

for i in range(number):
    item = {}
    item["pk"] = f"BLAST-{tmsp}"
    item["sk"] = f"TASK-{i}"
    item["gs1_pk"] = "-"
    item["gs1_sk"] = "-"
    item["status"] = "completed"
    db.put_item(item)