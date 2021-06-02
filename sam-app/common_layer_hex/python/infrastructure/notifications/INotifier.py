import json
from abc import ABC, abstractmethod

from domain.FanEventDTO import FanEventDTO


class INotifier(ABC):
    def __init__(self, source: str):
        self.source = source
        pass

    @abstractmethod
    def send_message(self, message: FanEventDTO):
        raise NotImplemented
