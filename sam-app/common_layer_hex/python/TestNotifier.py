from abc import ABC, abstractmethod

from INotifier import *


class TestNotifier(INotifier):
    def send_message(self, message: dict):
        print(json.dumps(message, indent=3, default=str))
