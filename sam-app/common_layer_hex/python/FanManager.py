import json
import os
from dataclasses import dataclass
from datetime import datetime
from typing import List

import ulid

from FanEventDTO import *
from INotifier import INotifier
from IRepository import IRepository
from ProcessDTO import *
from ProcessDTO import ProcessDTO
from TaskDTO import *

TASK_STATUS_FAN_OUT = "fan_out"
TASK_STATUS_TASK_CREATED = "created"
TASK_STATUS_TASK_COMPLETED = "completed"

EVENT_PROCESS_STARTED = "process_started"
EVENT_TASK_CREATED = "task_created"
EVENT_PROCESS_CREATED = "process_completed"


@dataclass
class FanManagerResults:
    updated_process: ProcessDTO
    updated_tasks: List[TaskDTO]
    event_notifications: List[FanEventDTO]


class FanManager:
    def __init__(self, repository: IRepository, notifier: INotifier):
        self.repository = repository
        self.notifer = notifier
        self.event_source = os.environ.get("AWS_LAMBDA_FUNCTION_NAME", "fan_manager")

    def start_process(self, process, tasks: list) -> FanManagerResults:
        print(f"\n\n--- Starting process: {process.process_name}")
        updated_process = ProcessDTO(
            process.process_name, str(ulid.ULID()), datetime.now().isoformat()
        )
        self.repository.save_process(updated_process)

        updated_tasks = []
        for task in tasks:
            print(f"\n--- Adding: {task.task_name}")
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

    def fan_out(self, task_list: list) -> FanManagerResults:
        print(f"\n\n--- Fanning out: {task_list}")
        updated_tasks = []
        event_notifications = []
        for task in task_list:
            print(f"\n--- Processing task: {task.task_name}")
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
            event_notifications.append(event)
        return FanManagerResults(None, updated_tasks, event_notifications)

    def complete_task(self, task: TaskDTO) -> FanManagerResults:
        print(f"\n\n--- Completing task: {task.task_name}")
        updated_tasks = []
        event_notifications = []
        new_task = TaskDTO(
            task.task_name,
            task.task_message,
            task.process_id,
            task.process_name,
            TASK_STATUS_TASK_COMPLETED,
            datetime.now().isoformat(),
            task.created,
        )
        self.repository.save_task(new_task)
        updated_tasks.append(new_task)

        process_progress = self._calculate_process_progress(task)
        current_process = self.repository.get_process(task.process_id)
        print(f"\n\ncurrent_process: {current_process}")
        updated_process = ProcessDTO(
            current_process.process_name,
            current_process.process_id,
            current_process.started,
            current_process.ended,
            process_progress,
        )
        self.repository.save_process(updated_process)
        if updated_process.progress == 1.0:
            event = FanEventDTO(
                self.event_source, EVENT_PROCESS_CREATED, updated_process.__dict__
            )
            self.notifer.send_message(event)
            event_notifications.append(event)
        return FanManagerResults(updated_process, updated_tasks, event_notifications)

    def _calculate_process_progress(self, process_id: str) -> float:
        process_task_list = self.repository.get_tasks_for_process(process_id)
        print("all tasks:")
        print(json.dumps(process_task_list, indent=3, default=str))
        total_tasks = len(process_task_list)
        completed_tasks = [
            t for t in process_task_list if t.status == TASK_STATUS_TASK_COMPLETED
        ]
        completed_count = len(completed_tasks)
        progress = 0.0
        if total_tasks > 0:
            progress = float(completed_count / total_tasks)
        return progress
