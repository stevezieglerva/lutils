import os, sys, inspect, json

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/lutil_s3_text_lines_to_sns"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))


import unittest
from lutil_s3_text_lines_to_sns import app
from unittest.mock import patch, Mock, MagicMock, PropertyMock
from lutil_s3_text_lines_to_sns import app


class IntegrationTests(unittest.TestCase):
    def test_lambda_handler__given_event__then_messages_sent(self):
        # Arrange
        event = {
            "Records": [
                {
                    "eventVersion": "2.0",
                    "eventSource": "aws:s3",
                    "awsRegion": "us-east-1",
                    "eventTime": "1970-01-01T00:00:00.000Z",
                    "eventName": "ObjectCreated:Put",
                    "userIdentity": {"principalId": "EXAMPLE"},
                    "requestParameters": {"sourceIPAddress": "127.0.0.1"},
                    "responseElements": {
                        "x-amz-request-id": "EXAMPLE123456789",
                        "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH",
                    },
                    "s3": {
                        "s3SchemaVersion": "1.0",
                        "configurationId": "testConfigRule",
                        "bucket": {
                            "name": "lutils-processing",
                            "ownerIdentity": {"principalId": "EXAMPLE"},
                            "arn": "arn:aws:s3:::lutils-processing",
                        },
                        "object": {
                            "key": "lutil_s3_text_lines_to_sns/lutil_s3_text_lines_output/url_list.txt",
                            "size": 1024,
                            "eTag": "0123456789abcdef0123456789abcdef",
                            "sequencer": "0A1B2C3D4E5F678901",
                        },
                    },
                }
            ]
        }
        os.environ["region"] = "us-east-1"

        # Act
        results = app.lambda_handler(event, "")

        # Assert
        self.assertEqual(len(results), 2)


if __name__ == "__main__":
    unittest.main()
