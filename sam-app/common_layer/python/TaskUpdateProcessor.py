import json
from datetime import datetime

from TaskRecord import *
from ProcessRecord import *
from FanEvent import *
from FanEventPublisher import FanEventPublisher


class TaskUpdateProcessor:
    def __init__(self, fan_publisher: FanEventPublisher):
        self.publisher = fan_publisher

    def process_task(self, task):
        print("Task:")
        print(task)

        current_task_status = task.status
        if current_task_status == FAN_OUT:
            process, event = self._process_fan_out(task)
        results = {"process_record": process.json(), "event": event}
        return results

    def _process_fan_out(self, task):
        process_record = ProcessRecord(
            process_id=task.process_id, process_name=task.process_name
        )

        self._put_db_item(process_record.json)
        print("process record added:")
        print(process_record)

        event = self._publish_next_event(TASK_CREATED, task.json())
        return (process_record, event)

    def _publish_next_event(self, event_name, message_json):
        return self.publisher.publish_event(event_name, message_json)

    def _put_db_item(self, item):
        return self.db.put_item(item)
