import unittest
import boto3
import json
from datetime import datetime
from unittest.mock import patch, Mock, MagicMock, PropertyMock


def create_s3_text_file(bucket, key, file_text):
    s3 = boto3.resource("s3")
    file_text_binary = bytes(file_text, "utf-8")
    object = s3.Object(bucket, key)
    response = object.put(Body=file_text_binary)
    return response


def get_s3_bucket_from_stack(output_key):
    cloudformation = boto3.client("cloudformation")
    stacks = cloudformation.describe_stacks(StackName="lutils")
    stack_outputs = stacks["Stacks"][0]["Outputs"]
    s3_bucket = ""
    for output in stack_outputs:
        if output["OutputKey"] == output_key:
            s3_bucket = output["OutputValue"]
            break
    return s3_bucket.split(":")[-1:][0]


class EndToEndTests(unittest.TestCase):
    def test_upload_new_starting_file__given_upload_new_starting_file__then_new_html_pages_downloaded(
        self,
    ):
        # Arrange
        cf = boto3.client("cloudformation")
        stack = cf.describe_stacks(StackName="lutils")
        # print(json.dumps(stack, indent=3, default=str))
        bucket = get_s3_bucket_from_stack("S3ProcessingBucket")
        print(f"*** {bucket}")

        list = """https://www.icf.com
https://usa.gov"""
        now = datetime.now().isoformat().replace(":", "")
        create_s3_text_file(
            bucket,
            f"lutil_s3_text_lines_to_sns/lutil_s3_text_lines_output/test-end-to-end/folder2/test_{now}.txt",
            list,
        )

        # Act

        # Assert


if __name__ == "__main__":
    unittest.main()
