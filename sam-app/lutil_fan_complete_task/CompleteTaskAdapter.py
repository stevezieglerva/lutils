import boto3
from FanManager import FanManager
from IRepository import IRepository
from INotifier import INotifier

from ProcessDTO import *
from TaskDTO import *


class StartProcessAdapter:
    def __init__(self, repository: IRepository, notifier: INotifier):
        self.repository = repository
        self.notifier = notifier

    def _convert_process_from_event(self, event: dict) -> ProcessDTO:
        return convert_json_to_process(event["process"])

    def _convert_tasks_from_event(self, event: dict) -> list:
        json_task_list = event["tasks"]
        task_list = [convert_json_to_task(t) for t in json_task_list]
        return task_list

    def start_process(self, event) -> dict:
        process = self._convert_process_from_event(event)
        tasks = self._convert_tasks_from_event(event)
        fan_manager = FanManager(self.repository, self.notifier)
        return fan_manager.start_process(process, tasks)
