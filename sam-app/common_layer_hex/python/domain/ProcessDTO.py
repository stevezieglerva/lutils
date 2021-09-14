from dataclasses import dataclass


@dataclass(frozen=True)
class ProcessDTO:
    process_name: str
    information: str
    process_id: str = ""
    started: str = ""
    ended: str = ""
    progress: float = 0.0

    @classmethod
    def create_from_dict(cls, process_json: dict):
        return ProcessDTO(**process_json)
