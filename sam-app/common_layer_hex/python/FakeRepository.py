import boto3

from DynamoDB import DynamoDB
from IRepository import IRepository
from domain.ProcessDTO import ProcessDTO
from domain.TaskDTO import TaskDTO


class FakeRepository(IRepository):
    def get_process(self, process_id: str) -> ProcessDTO:
        print("fake get process")
        return ProcessDTO("test")

    def save_process(self, process: ProcessDTO):
        print("fake save process")
        pass

    def get_task(self, process_id: str, task_name: str) -> TaskDTO:
        print("fake get task")
        return TaskDTO("fake task", {})

    def save_task(self, task: TaskDTO):
        print("fake save process")

    def get_tasks_for_process(self, process: ProcessDTO) -> list:
        return []
