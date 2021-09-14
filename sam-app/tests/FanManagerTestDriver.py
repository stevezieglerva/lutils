from unittest.case import expectedFailure
from common_layer_hex.python.domain.FanManager import *
from common_layer_hex.python.infrastructure.repository.InMemoryRepository import (
    InMemoryRepository,
)
from common_layer_hex.python.infrastructure.notifications.TestNotifier import (
    TestNotifier,
)
from common_layer_hex.python.infrastructure.repository.DynamoDB import (
    DynamoDB,
)


class FanManagerTestDriver:
    def __init__(self):
        self._repository = InMemoryRepository("fake-table")
        self._fan_manager = FanManager(self._repository, TestNotifier("fake-sns"))

    def create_task_array(self, task_dict_list: list) -> list:
        task_dto_list = [TaskDTO(t["task_name"], t["message"]) for t in task_dict_list]
        return task_dto_list

    def create_task_completed_dynamodb_change_stream(
        self, process: ProcessDTO, task: TaskDTO
    ) -> dict:
        stream = {
            "Records": [
                {
                    "eventID": "f1c2fa59c0b128193cf9575ed54811d2",
                    "eventName": "MODIFY",
                    "eventVersion": "1.1",
                    "eventSource": "aws:dynamodb",
                    "awsRegion": "us-east-1",
                    "dynamodb": {
                        "ApproximateCreationDateTime": 1621025176.0,
                        "Keys": {
                            "sk": {"S": f"TASK#{task.task_name}"},
                            "pk": {"S": f"PROCESS#{process.process_id}"},
                        },
                        "NewImage": {
                            "task_name": {"S": task.task_name},
                            "process_id": {"S": process.process_id},
                            "status_changed_timestamp": {
                                "S": "2021-05-14T16:46:16.627334"
                            },
                            "task_message": {"S": "\"{'go': 'caps!'}\""},
                            "created": {"S": "2021-05-14T16:46:16.627306"},
                            "process_name": {"S": "ProcessRecord Int Test"},
                            "sk": {"S": f"TASK#{task.task_name}"},
                            "gs1_pk": {"S": "-"},
                            "pk": {"S": f"PROCESS#{process.process_id}"},
                            "gs1_sk": {"S": "-"},
                            "status": {"S": "completed"},
                        },
                        "OldImage": {
                            "task_name": {"S": task.task_name},
                            "process_id": {"S": process.process_id},
                            "status_changed_timestamp": {
                                "S": "2021-05-14T16:46:16.627334"
                            },
                            "task_message": {"S": "\"{'go': 'caps!'}\""},
                            "created": {"S": "2021-05-14T16:46:16.627306"},
                            "process_name": {"S": "ProcessRecord Int Test"},
                            "sk": {"S": f"TASK#{task.task_name}"},
                            "gs1_pk": {"S": "-"},
                            "pk": {"S": f"PROCESS#{process.process_id}"},
                            "gs1_sk": {"S": "-"},
                            "status": {"S": "created"},
                        },
                        "SequenceNumber": "875400000000009959396144",
                        "SizeBytes": 325,
                        "StreamViewType": "NEW_AND_OLD_IMAGES",
                    },
                    "eventSourceARN": "arn:aws:dynamodb:us-east-1:112280397275:table/lutils2-FanProcessingPartTestTable-Q3PVEB6MO2AJ/stream/2021-05-14T13:21:33.706",
                },
            ]
        }
        return stream

    def when_start_process(
        self, process_name: str, task_list: list
    ) -> FanManagerResults:
        process = ProcessDTO(
            process_name="fan manager test", information="special info"
        )
        results = self._fan_manager.start_process(process, task_list)
        return results

    def when_fan_out(self, task_list: list) -> FanManagerResults:
        results = self._fan_manager.fan_out(task_list)
        return results

    def when_complete_task(self, task: TaskDTO):
        results = self._fan_manager.complete_task(task)
        return results

    def when_complete_process_if_needed(self, process: ProcessDTO):
        results = self._fan_manager.complete_process_if_needed(process)
        return results

    def get_tasks_for_process(self, process: ProcessDTO) -> list:
        tasks = self._repository.get_tasks_for_process(process)
        return tasks

    def then_process_in_repo(self, process_id):
        db = DynamoDB("fake-table")
        process_json = db.get_item(
            {"pk": f"PROCESS#{process_id}", "sk": f"PROCESS#{process_id}"}
        )
        assert "pk" in process_json, f"'pk' not in {process_json}"

    def then_progress_is(self, actual_progress: float, expected_progress: float):
        assert (
            actual_progress == expected_progress
        ), f"Unexpected progress: {actual_progress} != {expected_progress}"

    def then_count_of_tasks_in_status(
        self, process: ProcessDTO, status: str, expected_count: int
    ):
        tasks = self.get_tasks_for_process(process)

        tasks_in_status = [t for t in tasks if t.status == status]
        assert (
            len(tasks_in_status) == expected_count
        ), f"{len(tasks_in_status)} != {expected_count}"

    def then_event_created_for(self, event: FanEventDTO, event_name):
        assert (
            event.event_name == event_name
        ), f"Unexpected event {event.event_name} != {event_name}"

    def then_tasks_linked_to_process(self, process: ProcessDTO, task: TaskDTO):
        assert (
            process.process_id == task.process_id
        ), f"{process.process_id} != {task.process_id}"
        assert (
            process.process_name == task.process_name
        ), f"{process.process_name} != {task.process_name}"
