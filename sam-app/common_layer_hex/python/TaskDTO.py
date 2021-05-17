from dataclasses import dataclass


@dataclass
class TaskDTO:
    task_name: str
    task_message: dict
    process_id: str = ""
    status: str = ""
    created: str = ""


def convert_json_to_task(task_json: dict) -> TaskDTO:
    return TaskDTO(task_json["task_name"], task_json["task_message"])