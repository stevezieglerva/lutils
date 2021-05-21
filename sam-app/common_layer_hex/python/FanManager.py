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
        updated_process = ProcessDTO(
            process.process_name, str(ulid.ULID()), datetime.now().isoformat()
        )
        self.repository.save_process(updated_process)

        updated_tasks = []
        for task in tasks:
            print(f"\n\nAdding: {task.task_name}")
            new_task = TaskDTO(
                task.task_name,
                task.task_message,
                updated_process.process_id,
                updated_process.process_name,
                TASK_STATUS_FAN_OUT,
                datetime.now().isoformat(),
                datetime.now().isoformat(),
            )
            self.repository.save_task(new_task)
            updated_tasks.append(new_task)

        event = FanEventDTO(
            self.event_source, EVENT_PROCESS_STARTED, updated_process.__dict__
        )
        self.notifer.send_message(event)
        return FanManagerResults(updated_process, updated_tasks, [event])

    def fan_out(self, task_list: list) -> dict:
        print("Fanning out")
        updated_tasks = []
        for task in task_list:
            print(f"\n\nProcessing task: {task.task_name}")
            new_task = TaskDTO(
                task.task_name,
                task.task_message,
                task.process_id,
                task.process_name,
                TASK_STATUS_TASK_CREATED,
                datetime.now().isoformat(),
                task.created,
            )
            self.repository.save_task(new_task)
            updated_tasks.append(new_task)

            event = FanEventDTO(
                self.event_source, EVENT_TASK_CREATED, new_task.__dict__
            )
            self.notifer.send_message(event)

        return FanManagerResults(None, updated_tasks, [event])


@dataclass
class FanManagerResults:
    process_updates: ProcessDTO
    task_updates: List[TaskDTO]
    event_notifications: List[FanEventDTO]
