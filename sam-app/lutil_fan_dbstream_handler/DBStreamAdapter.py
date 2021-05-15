from botocore.retryhandler import _create_single_checker
from TaskRecord import TaskRecord
from DynamoDB import DynamoDB
from FanEvent import *
from TaskUpdateProcessor import TaskUpdateProcessor
from FanEventPublisher import FanEventPublisher


class DBStreamAdapter:
    def __init__(self, db, publisher):
        self.db = db
        self.publisher = publisher
        self.task_update_processor = TaskUpdateProcessor(self.publisher)

    def __str__(self):
        text = ""
        return text

    def __repr__(self):
        return str(self)

    def process_single_event(self, single_event):
        if self._is_newly_created_fan_out(
            single_event
        ) or self._is_newly_completed_task(single_event):
            task_db_json = single_event["dynamodb"]["NewImage"]
            task_json = self.db.convert_from_dict_format(task_db_json)
            task = TaskRecord(
                record_string=json.dumps(task_json, indent=3, default=str), db=self.db
            )
            results = self.task_update_processor.process_task(task)
            return results

    def _is_newly_created_fan_out(self, single_event):
        if single_event["eventName"] == "INSERT" and single_event["dynamodb"][
            "NewImage"
        ]["sk"]["S"].startswith("TASK"):
            if single_event["dynamodb"]["NewImage"]["status"]["S"] == FAN_OUT:
                return True
        return False

    def _is_newly_completed_task(self, single_event):
        print("checking completed")
        if single_event["eventName"] == "MODIFY" and single_event["dynamodb"][
            "NewImage"
        ]["sk"]["S"].startswith("TASK"):
            print("is updated task")
            if single_event["dynamodb"]["NewImage"]["status"]["S"] == TASK_COMPLETED:
                print("is task complete")
                return True
        return False
