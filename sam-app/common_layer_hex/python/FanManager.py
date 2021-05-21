import os
from dataclasses import dataclass
from datetime import datetime
from typing import List

import ulid

from FanEventDTO import *
from INotifier import INotifier
from IRepository import IRepository
from ProcessDTO import *
from TaskDTO import *

TASK_STATUS_FAN_OUT = "fan_out"
TASK_STATUS_TASK_CREATED = "created"

EVENT_PROCESS_STARTED = "process_started"
EVENT_TASK_CREATED = "task_created"


class FanManager:
    def __init__(self, repository: IRepository, notifier: INotifier):
        self.repository = repository
        self.notifer = notifier
        self.event_source = os.environ.get("AWS_LAMBDA_FUNCTION_NAME", "fan_manager")

    def start_process(self, process, tasks: list) -> ProcessDTO:
        print(f"Starting process: {process.process_name}")
        process.process_id = str(ulid.ULID())
        process.started = datetime.now().isoformat()
        self.repository.save_process(process)

        for task in tasks:
            print(f"\n\nAdding: {task.task_name}")
            task.process_id = process.process_id
            task.created = datetime.now().isoformat()
            task.status = TASK_STATUS_FAN_OUT
            self.repository.save_task(task)

        event = FanEventDTO(self.event_source, EVENT_PROCESS_STARTED, process.__dict__)
        self.notifer.send_message(event)

        return process

    def fan_out(self, task_list: list) -> dict:
        print("Fanning out")
        notifications_sent = 0
        for task in task_list:
            print(f"\n\nProcessing task: {task.task_name}")
            task.status = TASK_STATUS_TASK_CREATED
            task.status_changed_timestamp = datetime.now().isoformat()
            self.repository.save_task(task)

            event = FanEventDTO(self.event_source, EVENT_TASK_CREATED, task.__dict__)
            self.notifer.send_message(event)
            notifications_sent = notifications_sent + 1

        return {"notifications_sent": notifications_sent}


@dataclass
class FanManagerResults:
    process_updates: ProcessDTO
    task_updates: List[TaskDTO]
    event_notifications: List[FanEventDTO]
