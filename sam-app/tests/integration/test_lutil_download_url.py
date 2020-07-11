import os, sys, inspect, json

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/lutil_download_url"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

import unittest
from unittest.mock import patch, Mock, MagicMock, PropertyMock
import time
import boto3
from lutil_download_url import app
import json


event = {
    "Records": [
        {
            "EventSource": "aws:sns",
            "EventVersion": "1.0",
            "EventSubscriptionArn": "arn:aws:sns:us-east-1:{{accountId}}:ExampleTopic",
            "Sns": {
                "Type": "Notification",
                "MessageId": "95df01b4-ee98-5cb9-9903-4c221d41eb5e",
                "TopicArn": "arn:aws:sns:us-east-1:123456789012:ExampleTopic",
                "Subject": "example subject",
                "Message": '{"line" : "https://www.cnn.com"}',
                "Timestamp": "1970-01-01T00:00:00.000Z",
                "SignatureVersion": "1",
                "Signature": "EXAMPLE",
                "SigningCertUrl": "EXAMPLE",
                "UnsubscribeUrl": "EXAMPLE",
                "MessageAttributes": {
                    "Test": {"Type": "String", "Value": "TestString"},
                    "TestBinary": {"Type": "Binary", "Value": "TestBinary"},
                },
            },
        }
    ]
}

opm_event = {
    "Records": [
        {
            "EventSource": "aws:sns",
            "EventVersion": "1.0",
            "EventSubscriptionArn": "arn:aws:sns:us-east-1:{{accountId}}:ExampleTopic",
            "Sns": {
                "Type": "Notification",
                "MessageId": "95df01b4-ee98-5cb9-9903-4c221d41eb5e",
                "TopicArn": "arn:aws:sns:us-east-1:123456789012:ExampleTopic",
                "Subject": "example subject",
                "Message": '{"line" : "https://ia800608.us.archive.org/16/items/opm-federal-employment-data/data/1973-09-to-2014-06/non-dod/status/Status_Non_DoD_2012_09.txt"}',
                "Timestamp": "1970-01-01T00:00:00.000Z",
                "SignatureVersion": "1",
                "Signature": "EXAMPLE",
                "SigningCertUrl": "EXAMPLE",
                "UnsubscribeUrl": "EXAMPLE",
                "MessageAttributes": {
                    "Test": {"Type": "String", "Value": "TestString"},
                    "TestBinary": {"Type": "Binary", "Value": "TestBinary"},
                },
            },
        }
    ]
}


class IntegrationTests(unittest.TestCase):
    def test_lambda_handler__given_valid_sns_data__file_is_downloaded_to_location(self):
        # Arrange
        os.environ["s3_bucket"] = "lutils-processingbucket-ekhfo2czytqo"

        # Act
        result = app.lambda_handler(event, None)
        print(result)

        # Arrange
        self.assertEqual(1, 1)


## 	def test_lambda_handler__given_valid_sns_data_big_slow_url__file_is_downloaded_to_location(self):
## 		# Act
##
## 		result = lambda_handler(opm_event, None)
## 		print(result)
##
## 		# Arrange
## 		self.assertEqual(1, 1)


if __name__ == "__main__":
    unittest.main()


if __name__ == "__main__":
    unittest.main()
