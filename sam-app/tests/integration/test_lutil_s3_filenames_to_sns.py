import os, sys, inspect, json

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/lutil_s3_filenames_to_sns"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))


import unittest
from lutil_s3_filenames_to_sns import app
from unittest.mock import patch, Mock, MagicMock, PropertyMock


class IntegrationTests(unittest.TestCase):
    def test_lambda_handler__given_custom_json_input__then_messages_sent(self):
        # Arrange
        event = {
            "bucket": "zillow-and-schools-processingbucket-1pfwmakyhm307",
            "prefix": "glue/10-raw-homes-json",
            "sns_arn": "arn:aws:sns:us-east-1:112280397275:lutil_s3_filenames_output",
        }
        os.environ["region"] = "us-east-1"
        os.environ["accountid"] = "112280397275"

        # Act
        results = app.lambda_handler(event, "")

        # Assert
        self.assertEqual(len(results), 2)


if __name__ == "__main__":
    unittest.main()
