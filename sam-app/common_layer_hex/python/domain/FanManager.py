import json
import os
from dataclasses import dataclass
from datetime import datetime
from typing import List

from ulid import ULID
from infrastructure.notifications.INotifier import INotifier
from infrastructure.repository.IRepository import IRepository

from domain.FanEventDTO import *
from domain.IRunProcess import IRunProcess
from domain.ProcessDTO import *
from domain.ProcessDTO import ProcessDTO
from domain.TaskDTO import *

TASK_STATUS_FAN_OUT = "fan_out"
TASK_STATUS_TASK_CREATED = "created"
TASK_STATUS_TASK_COMPLETED = "completed"

EVENT_PROCESS_STARTED = "process_started"
EVENT_TASK_CREATED = "task_created"
EVENT_TASK_COMPLETED = "task_completed"
EVENT_PROCESS_COMPLETED = "process_completed"


@dataclass
class FanManagerResults:
    updated_process: ProcessDTO
    updated_tasks: List[TaskDTO]
    event_notifications: List[FanEventDTO]


class FanManager(IRunProcess):
    def __init__(self, repository: IRepository, notifier: INotifier):
        self.repository = repository
        self.notifier = notifier
        self.event_source = os.environ.get("AWS_LAMBDA_FUNCTION_NAME", "fan_manager")

    def start_process(self, process, tasks: list) -> FanManagerResults:
        print(f"\n\nDEBUG Starting process: {process}")
        updated_process = ProcessDTO(
            process_name=process.process_name,
            process_id=str(ULID()),
            started=datetime.now().isoformat(),
            information=process.information,
        )
        self.repository.save_process(updated_process)

        updated_tasks = []
        for task in tasks:
            print(f"\nDEBUG Adding: {task.task_name}")
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
        self.notifier.send_message(event)

        return FanManagerResults(updated_process, updated_tasks, [event])

    def fan_out(self, task_list: list) -> FanManagerResults:
        print(f"\n\nDEBUG Fanning out: {task_list}")
        updated_tasks = []
        event_notifications = []
        for task in task_list:
            print(f"\nDEBUG Processing task: {task.task_name}")
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
            self.notifier.send_message(event)
            event_notifications.append(event)
        return FanManagerResults(None, updated_tasks, event_notifications)

    def complete_task(self, task: TaskDTO) -> FanManagerResults:
        print(f"\n\nDEBUG Completing task: {task.task_name}")
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

        current_process = self.repository.get_process(task.process_id)
        print(f"\n\ncurrent info: {current_process.information}")
        process_progress = self._calculate_process_progress(current_process)
        process_with_progress_updated = ProcessDTO(
            process_name=current_process.process_name,
            process_id=current_process.process_id,
            started=current_process.started,
            ended=current_process.ended,
            progress=process_progress,
            information=current_process.information,
        )
        self.repository.save_process(process_with_progress_updated)
        print(f"\n\ncurrent_process: {process_with_progress_updated}")

        event = FanEventDTO(self.event_source, EVENT_TASK_COMPLETED, task.__dict__)
        self.notifier.send_message(event)
        event_notifications.append(event)
        return FanManagerResults(
            process_with_progress_updated, updated_tasks, event_notifications
        )

    def complete_process_if_needed(self, process: ProcessDTO) -> FanManagerResults:
        print(f"\n\n************ DEBUG Completing process: {process.process_name}")
        print(f"incoming process: {process}")
        event_notifications = []
        latest_process = self.repository.get_process(process.process_id)
        updated_process = latest_process
        if self._need_to_notifiy_process_completion(latest_process):
            ended = datetime.now().isoformat()
            updated_process = ProcessDTO(
                process_name=latest_process.process_name,
                process_id=latest_process.process_id,
                started=latest_process.started,
                ended=ended,
                progress=latest_process.progress,
                information=latest_process.information,
            )
            self.repository.save_process(updated_process)

            event = FanEventDTO(
                self.event_source, EVENT_PROCESS_COMPLETED, updated_process.__dict__
            )
            self.notifier.send_message(event)
            event_notifications.append(event)

        return FanManagerResults(updated_process, [], event_notifications)

    def _need_to_notifiy_process_completion(self, process: ProcessDTO) -> bool:
        latest_tasks = self.repository.get_tasks_for_process(process)
        completed_tasks = [
            t for t in latest_tasks if t.status == TASK_STATUS_TASK_COMPLETED
        ]

        all_tasks_completed = False
        if len(latest_tasks) == len(completed_tasks):
            all_tasks_completed = True

        if process.progress == 1.0 and process.ended == "" and all_tasks_completed:
            return True
        return False

    def _calculate_process_progress(self, process: ProcessDTO) -> float:
        process_task_list = self.repository.get_tasks_for_process(process)
        print("all tasks:")
        print(json.dumps(process_task_list, indent=3, default=str))
        total_tasks = len(process_task_list)
        completed_tasks = [
            t for t in process_task_list if t.status == TASK_STATUS_TASK_COMPLETED
        ]
        completed_count = len(completed_tasks)
        progress = 0.0
        print(f"completed_count: {completed_count}, total_tasks: {total_tasks} ")
        if total_tasks > 0:
            progress = round(float(completed_count / total_tasks), 2)
        return progress
