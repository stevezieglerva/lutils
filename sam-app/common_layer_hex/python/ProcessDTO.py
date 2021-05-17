from dataclasses import dataclass


@dataclass
class ProcessDTO:
    process_name: str
    process_id: str = ""
    started: str = ""
    ended: str = ""
    progress: float = 0.0


def convert_json_to_process(process_json: dict) -> ProcessDTO:
    return ProcessDTO(process_json["process_name"])
