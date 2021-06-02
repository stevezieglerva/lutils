from abc import ABC, abstractmethod
from domain.ProcessDTO import ProcessDTO
from domain.TaskDTO import TaskDTO


class IRepository(ABC):
    def __init__(self, source: str):
        self.source = source
        pass

    @abstractmethod
    def get_process(self, process_id: str) -> ProcessDTO:
        raise NotImplemented

    @abstractmethod
    def save_process(self, process: ProcessDTO):
        raise NotImplemented

    @abstractmethod
    def get_task(self, process_id: str, task_name: str) -> TaskDTO:
        raise NotImplemented

    @abstractmethod
    def save_task(self, task: TaskDTO):
        raise NotImplemented

    @abstractmethod
    def get_tasks_for_process(self, process: ProcessDTO) -> list:
        raise NotImplemented