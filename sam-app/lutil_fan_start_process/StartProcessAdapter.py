import boto3
from domain.IRunProcess import IRunProcess
from infrastructure.repository.IRepository import IRepository
from infrastructure.notifications.INotifier import INotifier

from domain.ProcessDTO import *
from domain.TaskDTO import *


class StartProcessAdapter:
    def __init__(self, fan_manager: IRunProcess):
        self.fan_manager = fan_manager
        self.repository = fan_manager.repository
        self.notifier = fan_manager.notifier

    def _convert_process_from_event(self, event: dict) -> ProcessDTO:
        return ProcessDTO.create_from_dict(event["process"])

    def _convert_tasks_from_event(self, event: dict) -> list:
        json_task_list = event["tasks"]
        task_list = [TaskDTO.create_from_dict(t) for t in json_task_list]
        return task_list

    def start_process(self, event) -> dict:
        if "information" not in event["process"]:
            event["process"]["information"] = ""
        process = self._convert_process_from_event(event)
        tasks = self._convert_tasks_from_event(event)

        print(f"Adapter process: {process}")

        return self.fan_manager.start_process(process, tasks)
