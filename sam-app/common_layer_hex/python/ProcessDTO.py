from dataclasses import dataclass


@dataclass(frozen=True)
class ProcessDTO:
    process_name: str
    process_id: str = ""
    started: str = ""
    ended: str = ""
    progress: float = 0.0


def convert_json_to_process(process_json: dict) -> ProcessDTO:
    dummy_for_fields = ProcessDTO("dummy")
    expected_fields = [field for field in dummy_for_fields.__dict__.keys()]
    constructor_arguments = []
    for field in expected_fields:
        try:
            field_value = process_json[field]
        except KeyError as e:
            raise KeyError(f"ProcessDTO missing value for '{field}'")
        constructor_arguments.append(field_value)
    print(constructor_arguments)
    return ProcessDTO(*constructor_arguments)