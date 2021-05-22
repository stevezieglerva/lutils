import boto3
from FanManager import FanManager
from IRepository import IRepository
from INotifier import INotifier


from ProcessDTO import *
from TaskDTO import *


class CompleteTaskAdapter:
    def __init__(self, repository: IRepository, notifier: INotifier):
        self.repository = repository
        self.notifier = notifier

    def _convert_tasks_from_event(self, event: dict) -> list:
        json_task_list = event["tasks"]
        task_list = [convert_json_to_task(t) for t in json_task_list]
        return task_list

    def complete_task(self, event) -> TaskDTO:
        process_id = event["process_id"]
        task_name = event["task_name"]
        task = self.repository.get_task(process_id, task_name)
        fan_manager = FanManager(self.repository, self.notifier)
        return fan_manager.complete_task(task)