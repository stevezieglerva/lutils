import json
from abc import ABC, abstractmethod


class INotifier(ABC):
    def __init__(self, source: str):
        self.source = source
        pass

    @abstractmethod
    def send_message(self, message: dict):
        raise NotImplemented
