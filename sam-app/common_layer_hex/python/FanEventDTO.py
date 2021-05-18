from dataclasses import dataclass


@dataclass
class FanEventDTO:
    event_source: str
    event_name: str
    event_message: dict
