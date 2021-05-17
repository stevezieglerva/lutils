from abc import ABC, abstractmethod

from INotifier import *


class TestNotifier(INotifier):
    def send_message(self, message):
        print(message)
