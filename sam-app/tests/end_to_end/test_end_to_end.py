import unittest
import boto3
from datetime import datetime
from unittest.mock import patch, Mock, MagicMock, PropertyMock


def create_s3_text_file(bucket, key, file_text):
    s3 = boto3.resource("s3")
    file_text_binary = bytes(file_text, "utf-8")
    object = s3.Object(bucket, key)
    response = object.put(Body=file_text_binary)
    return response


class EndToEndTests(unittest.TestCase):
    def test_upload_new_starting_file__given_upload_new_starting_file__then_new_html_pages_downloaded(
        self,
    ):
        # Arrange
        list = """https://www.twitter.com
https://www.facebook.com
https://instagram.com"""
        now = datetime.now().isoformat()
        create_s3_text_file(
            "lutils-processing",
            f"lutil_s3_text_lines_to_sns/lutil_s3_text_lines_output/test_{now}.txt",
            list,
        )

        # Act

        # Assert


if __name__ == "__main__":
    unittest.main()
