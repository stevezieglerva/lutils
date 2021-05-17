from abc import ABC, abstractmethod
from ProcessDTO import ProcessDTO


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
