import json
from abc import ABC, abstractmethod

from FanEventDTO import FanEventDTO


class INotifier(ABC):
    def __init__(self, source: str):
        self.source = source
        pass

    @abstractmethod
    def send_message(self, message: FanEventDTO):
        raise NotImplemented
