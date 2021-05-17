import ulid
from datetime import datetime

from ProcessDTO import *
from TaskDTO import *


class FanManager:
    def __init__(self, repository, notifier):
        self.repository = repository
        self.notifer = notifier

    def start_process(self, process, tasks: list) -> ProcessDTO:
        process.process_id = str(ulid.ULID())
        process.started = datetime.now().isoformat()
        self.repository.save_process(process)
        return process
