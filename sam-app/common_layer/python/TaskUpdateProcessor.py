import json
from datetime import datetime

from TaskRecord import *


class TaskUpdateProcessor:
    def __init__(self, sns_topic_name, table_name):
        self.sns_topic_name = sns_topic_name
        self.table_name = table_name

    def process_task(self, task):
        results = {"process_record": {}, "event": {}}
        return results
