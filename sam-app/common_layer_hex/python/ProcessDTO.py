from dataclasses import dataclass


@dataclass
class ProcessDTO:
    process_name: str
    process_id: str = ""
    started: str = ""
    ended: str = ""
    progress: float = 0.0
