from dataclasses import dataclass


@dataclass(frozen=True)
class TaskDTO:
    task_name: str
    task_message: dict
    process_id: str = ""
    process_name: str = ""
    status: str = ""
    status_changed_timestamp: str = ""
    created: str = ""


def convert_json_to_task(task_json: dict) -> TaskDTO:
    return TaskDTO(
        task_json["task_name"],
        task_json["task_message"],
        task_json.get("process_id", ""),
        task_json.get("process_name", ""),
        task_json.get("status", ""),
        task_json.get("status_changed_timestamp", ""),
        task_json.get("created"),
    )
