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
        results = {"process_record": {}, "event": {}}
        print("Task:")
        print(task)

        current_task_status = task.status
        if current_task_status == FAN_OUT:
            process, event = self._process_fan_out(task)
            results = {"process_record": process.json(), "event": event}
        if current_task_status == TASK_COMPLETED:
            process, event = self._process_task_completed(task)
            results = {"process_record": process.json(), "event": event}
        return results

    def _process_fan_out(self, task):
        print(f"\n\nprocessing fan out for {task.pk}/{task.sk}/{task.status}\n\n")

        event = self._publish_next_event(TASK_CREATED, task.json())
        return (process_record, event)

    def _process_task_completed(self, task):
        print(f"\n\nprocessing completed for {task.pk}/{task.sk}/{task.status}\n\n")
        process_record = ProcessRecord(
            process_id=task.process_id, process_name=task.process_name, db=task.db
        )
        process_record.update_process_record_based_on_completions()
        event = {}
        if process_record.progress == 1.0:
            event = self._publish_next_event(PROCESS_COMPLETED, task.json())
        return (process_record, event)

    def _publish_next_event(self, event_name, message_json):
        return self.publisher.publish_event(event_name, message_json)

    def _save_process(self, process):
        return process.save()
