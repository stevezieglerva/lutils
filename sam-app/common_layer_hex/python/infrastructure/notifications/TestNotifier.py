from abc import ABC, abstractmethod

from infrastructure.notifications.INotifier import *
from domain.FanEventDTO import FanEventDTO


class TestNotifier(INotifier):
    def send_message(self, message: FanEventDTO):
        print(f"Sending message: {message}")
