import json
from datetime import datetime

from TaskRecord import *
from ProcessRecord import *
from FanEvent import FanEvent
from FanEventPublisher import FanEventPublisher


class TaskUpdateProcessor:
    def __init__(self, fan_publisher: FanEventPublisher):
        self.publisher = fan_publisher

    def process_task(self, task):

        current_task_status = task.status
        if current_task_status == FAN_OUT:
            process = self._process_fan_out(task)
        results = {"process_record": process.json(), "event": {}}
        return results

    def _process_fan_out(self, task):
        print("Task:")
        print(task)
        process_record = ProcessRecord(
            process_id=task.process_id, process_name=task.process_name
        )
        print(process_record)
        self._put_db_item(process_record.json)
        return process_record

    def _put_db_item(self, item):
        return self.db.put_item(item)
