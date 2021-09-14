import os, sys, inspect, json


import unittest
from lutil_download_url import app
from unittest.mock import patch, Mock, MagicMock, PropertyMock


class UnitTests(unittest.TestCase):
    def test_get_s3_key_for_latest__given_just_direct_file__then_filename_formatted(
        self,
    ):
        # Arrange
        url = "http://www.cnn.com"
        source = "https://s3.amazonaws.com/lutils-processingbucket-ekhfo2czytqo/lutil_s3_text_lines_to_sns/lutil_s3_text_lines_output_selenium/zillow_urls.txt"

        # Act
        result = app.get_s3_key_for_latest(url, source)
        print(f"s3_key: {result}")

        # Assert
        self.assertEqual(
            result, "lutil-download-url/latest/www.cnn.com/http___www.cnn.com"
        )

    def test_get_s3_key_for_latest__given_prefix_folders_in_source__then_filename_formatted(
        self,
    ):
        # Arrange
        url = "http://www.cnn.com"
        source = "https://s3.amazonaws.com/lutils-processingbucket-ekhfo2czytqo/lutil_s3_text_lines_to_sns/lutil_s3_text_lines_output_selenium/step-1/step-2/zillow_urls.txt"

        # Act
        result = app.get_s3_key_for_latest(url, source)
        print(f"s3_key: {result}")

        # Assert
        self.assertEqual(
            result,
            "lutil-download-url/latest/step-1/step-2/www.cnn.com/http___www.cnn.com",
        )

    def test_get_s3_key_for_latest__given_use_guid__then_filename_formatted(
        self,
    ):
        # Arrange
        url = "http://www.cnn.com"
        source = "https://s3.amazonaws.com/lutils-processingbucket-ekhfo2czytqo/lutil_s3_text_lines_to_sns/lutil_s3_text_lines_output_selenium/step-1/step-2/zillow_urls.txt"

        # Act
        result = app.get_s3_key_for_latest(url, source, True)
        print(f"s3_key: {result}")

        # Assert
        self.assertEqual(
            result,
            "lutil-download-url/latest/step-1/step-2/www.cnn.com/13135319696474009996500139906251311974",
        )


if __name__ == "__main__":
    unittest.main()
