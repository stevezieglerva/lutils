from dataclasses import dataclass


@dataclass(frozen=True)
class FanEventDTO:
    event_source: str
    event_name: str
    event_message: dict

    def get_formatted_line(self):
        line = f"{self.event_source:<40} {self.event_name:<40} "
        process_id = self.event_message.get("process_id", "")
        if process_id != "":
            line = line + f" {process_id:<40} "
        process_name = self.event_message.get("process_name", "")
        if process_name != "":
            line = line + f" {process_name:<40} "
        task_name = self.event_message.get("task_name", "")
        if task_name != "":
            line = line + f" {task_name:<40}"
        return line


def convert_json_to_fanevent(object_json: dict) -> FanEventDTO:
    dummy_for_fields = FanEventDTO("x", "y", "z")
    expected_fields = [field for field in dummy_for_fields.__dict__.keys()]
    constructor_arguments = []
    for field in expected_fields:
        try:
            field_value = object_json[field]
            constructor_arguments.append(field_value)
        except KeyError as e:
            # missing field might be optional so let it pass
            pass
    print(constructor_arguments)
    return FanEventDTO(*constructor_arguments)