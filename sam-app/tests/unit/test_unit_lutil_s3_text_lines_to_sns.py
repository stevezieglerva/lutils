import os, sys, inspect, json


import unittest
from lutil_s3_text_lines_to_sns import app
from unittest.mock import patch, Mock, MagicMock, PropertyMock


class UnitTests(unittest.TestCase):
    def test_format_messages__given_simple_dict__then_messages_formatted(self):
        # Arrange
        input = {"file_1.txt": "line1", "file_2.txt": "line2"}

        # Act
        results = app.format_messages(input)

        # Assert
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["line"], "line1")


if __name__ == "__main__":
    unittest.main()
