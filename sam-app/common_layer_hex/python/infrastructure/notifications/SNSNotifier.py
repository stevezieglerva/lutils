from abc import ABC, abstractmethod

from infrastructure.notifications.INotifier import *
from domain.FanEventDTO import FanEventDTO

import boto3


class SNSNotifier(INotifier):
    def send_message(self, message: FanEventDTO):
        assert len(self.source.split(":")), f"source must be a valid AWS arn for SNS"

        print(f"Sending SNS message: {message}")

        sns = boto3.client("sns")
        result = sns.publish(
            TopicArn=self.source,
            Message=str(message.__dict__),
            MessageAttributes={
                "event_name": {"DataType": "String", "StringValue": message.event_name},
                "process_name": {
                    "DataType": "String",
                    "StringValue": message.event_message["process_name"],
                },
                "event_source": {
                    "DataType": "String",
                    "StringValue": message.event_source,
                },
            },
        )
        return result
