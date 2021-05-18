import ulid
from datetime import datetime

from ProcessDTO import *
from TaskDTO import *
from IRepository import IRepository
from INotifier import INotifier

TASK_STATUS_FAN_OUT = "fan_out"
TASK_STATUS_TASK_CREATED = "created"


class FanManager:
    def __init__(self, repository: IRepository, notifier: INotifier):
        self.repository = repository
        self.notifer = notifier

    def start_process(self, process, tasks: list) -> ProcessDTO:
        print(f"Starting process: {process.process_name}")
        process.process_id = str(ulid.ULID())
        process.started = datetime.now().isoformat()
        self.repository.save_process(process)

        for task in tasks:
            print(f"\n\nAdding: {task.task_name}")
            task.process_id = process.process_id
            task.created = datetime.now().isoformat()
            task.status = TASK_STATUS_FAN_OUT
            self.repository.save_task(task)

        return process

    def fan_out(self, task_list: list) -> dict:
        print("Fanning out")
        for task in task_list:
            print(f"\n\nProcessing task: {task.task_name}")
            task.status = TASK_STATUS_TASK_CREATED
            task.status_changed = datetime.now().isoformat()
            self.repository.save_task(task)
            self.notifer.send_message({})

        return {"notifications_sent": 0}
