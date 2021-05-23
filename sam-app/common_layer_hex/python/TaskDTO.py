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
    dummy_for_fields = TaskDTO("dummy", {})
    expected_fields = [field for field in dummy_for_fields.__dict__.keys()]
    constructor_arguments = []
    for field in expected_fields:
        try:
            field_value = task_json[field]
            constructor_arguments.append(field_value)
        except KeyError as e:
            # missing field might be optional so let it pass
            pass
    print(constructor_arguments)
    return TaskDTO(*constructor_arguments)
