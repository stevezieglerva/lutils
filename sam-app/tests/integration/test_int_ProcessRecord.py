import inspect
import json
import os
import sys
import ulid

import boto3


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/common_layer/python"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

import unittest
from unittest import mock


from common_layer.python.TaskRecord import *
from common_layer.python.infrastructure.repository.DynamoDB import DynamoDB
from common_layer.python.FanEvent import *
from common_layer.python.ProcessRecord import *


def get_output_from_stack(output_key):
    cloudformation = boto3.client("cloudformation")
    stacks = cloudformation.describe_stacks(StackName="lutils2")
    stack_outputs = stacks["Stacks"][0]["Outputs"]
    s3_bucket = ""
    for output in stack_outputs:
        if output["OutputKey"] == output_key:
            output_value = output["OutputValue"]
            break
    return output_value


os.environ["TABLE_NAME"] = get_output_from_stack("FanProcessingPartTestTableName")


class ProcessRecordIntTests(unittest.TestCase):
    def test_update_process_record_based_on_completions__given_one_of_two_completed__then_update_complete(
        self,
    ):
        # Arrange
        id = str(ulid.ULID())
        db = DynamoDB(os.environ["TABLE_NAME"])
        task1 = TaskRecord(
            process_id=id,
            process_name="ProcessRecord Int Test",
            task_name="task_00",
            task_message={"go": "caps!"},
            db=db,
        )
        task1.fan_out()
        task1.complete()
        task2 = TaskRecord(
            process_id=id,
            process_name="ProcessRecord Int Test",
            task_name="task_01",
            task_message={"go": "caps!"},
            db=db,
        )
        task2.fan_out()

        process = ProcessRecord(
            process_id=id, process_name="ProcessRecord Int Test", db=db
        )
        process.save()

        # Act
        process.update_process_record_based_on_completions()

        # Assert
        latest_process_data = db.get_item({"pk": process.pk, "sk": process.pk})
        print(latest_process_data)
        self.assertEqual(latest_process_data["progress"], 0.5)

    def test_is_current_live_process_already_done__given_not_done__then_false(
        self,
    ):
        # Arrange
        id = str(ulid.ULID())
        db = DynamoDB(os.environ["TABLE_NAME"])

        process = ProcessRecord(
            process_id=id, process_name="ProcessRecord Int Test", db=db
        )
        process.save()

        task1 = TaskRecord(
            process_id=id,
            process_name="ProcessRecord Int Test",
            task_name="task_00",
            task_message={"go": "caps!"},
            db=db,
        )
        task1.fan_out()
        task1.complete()
        task2 = TaskRecord(
            process_id=id,
            process_name="ProcessRecord Int Test",
            task_name="task_01",
            task_message={"go": "caps!"},
            db=db,
        )
        task2.fan_out()

        data_set = db.query_table_begins({"pk": process.pk, "sk": "TASK"})
        print("tasks data set:")
        print(json.dumps(data_set, indent=3, default=str))

        data_set = db.query_table_begins({"pk": process.pk, "sk": "PROCESS"})
        print("process data set:")
        print(json.dumps(data_set, indent=3, default=str))

        # Act
        results = process.is_current_live_process_already_done()

        # Assert
        self.assertEqual(results, False)

    def test_is_current_live_process_already_done__given_done__then_true(
        self,
    ):
        # Arrange
        id = str(ulid.ULID())
        db = DynamoDB(os.environ["TABLE_NAME"])

        process = ProcessRecord(
            process_id=id, process_name="ProcessRecord Int Test", db=db
        )
        process.save()

        task1 = TaskRecord(
            process_id=id,
            process_name="ProcessRecord Int Test",
            task_name="task_00",
            task_message={"mow": "lawn!"},
            db=db,
        )
        task1.fan_out()
        task1.complete()
        task2 = TaskRecord(
            process_id=id,
            process_name="ProcessRecord Int Test",
            task_name="task_01",
            task_message={"mow": "lawn!"},
            db=db,
        )
        task2.fan_out()
        task2.complete()
        process.done()

        data_set = db.query_table_begins({"pk": process.pk, "sk": "TASK"})
        print("tasks data set:")
        print(json.dumps(data_set, indent=3, default=str))

        data_set = db.query_table_begins({"pk": process.pk, "sk": "PROCESS"})
        print("process data set:")
        print(json.dumps(data_set, indent=3, default=str))

        # Act
        results = process.is_current_live_process_already_done()

        # Assert
        self.assertEqual(results, True)


if __name__ == "__main__":
    unittest.main()