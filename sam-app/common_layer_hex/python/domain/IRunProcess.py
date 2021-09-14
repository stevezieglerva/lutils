from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from infrastructure.notifications import INotifier
from infrastructure.repository import IRepository

from domain.FanEventDTO import FanEventDTO
from domain.ProcessDTO import ProcessDTO
from domain.TaskDTO import TaskDTO


@dataclass
class FanManagerResults:
    updated_process: ProcessDTO
    updated_tasks: List[TaskDTO]
    event_notifications: List[FanEventDTO]


class IRunProcess(ABC):
    """Abstract class for the fan manager"""

    def __init__(self, repository: IRepository, notifier: INotifier):
        raise NotImplemented

    @abstractmethod
    def start_process(self, process, tasks: list) -> FanManagerResults:
        raise NotImplemented

    @abstractmethod
    def fan_out(self, task_list: list) -> FanManagerResults:
        raise NotImplemented

    @abstractmethod
    def complete_task(self, task: TaskDTO) -> FanManagerResults:
        raise NotImplemented

    @abstractmethod
    def complete_process_if_needed(self, process: ProcessDTO) -> FanManagerResults:
        raise NotImplemented
