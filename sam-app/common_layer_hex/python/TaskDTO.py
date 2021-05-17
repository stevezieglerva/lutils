from dataclasses import dataclass


@dataclass
class TaskDTO:
    task_name: str
    task_message: dict
    status: str = ""
    process_id: str = ""
