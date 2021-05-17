from dataclasses import dataclass


@dataclass
class TaskDTO:
    task_name: str
    task_message: dict
    process_id: str = ""
    status: str = ""
    created: str = ""