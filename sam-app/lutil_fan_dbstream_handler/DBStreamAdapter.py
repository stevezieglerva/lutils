from IRepository import *
from INotifier import *
from FanManager import *
from TaskDTO import *


class DBStreamAdapter:
    def __init__(self, repository: IRepository, notifier: INotifier):
        self.repository = repository
        self.notifier = notifier
        self.fan_manager = FanManager(self.repository, self.notifier)

    def process_single_event(self, single_event):
        print("\n\nsingle_event:")
        print(json.dumps(single_event, indent=3, default=str))

        db_event = single_event["eventName"]
        pk = single_event["dynamodb"]["NewImage"]["pk"]["S"]
        sk = single_event["dynamodb"]["NewImage"]["sk"]["S"]
        task_status = ""
        if single_event["dynamodb"]["NewImage"]["sk"]["S"].startswith("TASK"):
            task_status = single_event["dynamodb"]["NewImage"]["status"]["S"]
        print(f"DEBUG single_event: {db_event:<10} {pk:<20} {sk:20} {task_status}")

        if self._is_newly_created_fan_out(
            single_event
        ) or self._is_newly_completed_task(single_event):
            task_db_json = single_event["dynamodb"]["NewImage"]
            task_json = self._convert_from_dict_format(task_db_json)
            print(json.dumps(task_json, indent=3, default=str))
            task = convert_json_to_task(task_json)
            print(f"task dto: {task}")
            results = self.fan_manager.fan_out([task])
            return results

    def _is_newly_created_fan_out(self, single_event):
        if single_event["eventName"] == "INSERT" and single_event["dynamodb"][
            "NewImage"
        ]["sk"]["S"].startswith("TASK"):
            if (
                single_event["dynamodb"]["NewImage"]["status"]["S"]
                == TASK_STATUS_FAN_OUT
            ):
                return True
        return False

    def _is_newly_completed_task(self, single_event):
        print("checking completed")
        if single_event["eventName"] == "MODIFY" and single_event["dynamodb"][
            "NewImage"
        ]["sk"]["S"].startswith("TASK"):
            print("is updated task")
            if (
                single_event["dynamodb"]["NewImage"]["status"]["S"]
                == TASK_STATUS_TASK_COMPLETED
            ):
                print("is task complete")
                return True
        return False

    def _convert_from_dict_format(self, dict):
        results = {}
        for k, v in dict.items():
            field_name = k
            for sub_k, sub_v in v.items():
                type = sub_k
                field_value = sub_v
                # try to convert to dict
                if type == "S":
                    if "{" in field_value:
                        try:
                            json_str = field_value.replace("'", '"')
                            json_str = json_str[1:]
                            json_str = json_str[:-1]
                            field_dict = json.loads(json_str)
                            field_value = field_dict
                        except json.decoder.JSONDecodeError:
                            # field is not JSON
                            pass
                if type == "N":
                    field_value = float(field_value)
            results[field_name] = field_value
        return results