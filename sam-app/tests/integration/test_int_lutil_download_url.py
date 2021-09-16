import inspect
import json
import os
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/lutil_download_url"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

import json
import time
import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

import boto3
from lutil_download_url import app

cnn_event = {
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
                "Message": '{"line" : "https://www.cnn.com", "source" : "https://s3.amazonaws.com/lutils-processingbucket-ekhfo2czytqo/lutil_s3_text_lines_to_sns/lutil_s3_text_lines_output_selenium/step-1/step-2/zillow_urls.txt"}',
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

zillow_event = {
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
                "Message": '{"line" : "https://www.zillow.com/homedetails/104-Amberglen-Ln-Holly-Springs-NC-27540/81436400_zpid/", "source" : "https://s3.amazonaws.com/lutils-processingbucket-ekhfo2czytqo/lutil_s3_text_lines_to_sns/lutil_s3_text_lines_output_selenium/step-1/step-2/zillow_urls.txt"}',
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
    # def test_lambda_handler__given_valid_sns_data_for_cnn__file_is_downloaded_to_location(
    #     self,
    # ):
    #     # Arrange
    #     os.environ["s3_bucket"] = "lutils-processingbucket-ekhfo2czytqo"

    #     # Act
    #     results = app.lambda_handler(cnn_event, None)
    #     print(f"test results: {results}")

    #     # Arrange
    #     self.assertEqual(results["status_code"], 200)

    def test_lambda_handler__given_valid_sns_data_for_zillow__file_is_downloaded_to_location(
        self,
    ):
        # Arrange
        os.environ["s3_bucket"] = "lutils-processingbucket-ekhfo2czytqo"

        # Act
        results = app.lambda_handler(zillow_event, None)
        print(f"test results: {results}")

        # Arrange
        self.assertEqual(results["status_code"], 500)


if __name__ == "__main__":
    unittest.main()


if __name__ == "__main__":
    unittest.main()
