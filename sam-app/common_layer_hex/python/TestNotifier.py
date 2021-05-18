from abc import ABC, abstractmethod

from INotifier import *
from FanEventDTO import FanEventDTO


class TestNotifier(INotifier):
    def send_message(self, message: FanEventDTO):
        print(f"Sending message: {message}")
