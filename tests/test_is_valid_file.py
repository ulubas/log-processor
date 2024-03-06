import os
import unittest

from log_processor import LogProcessor


class TestIsValidFile(unittest.TestCase):
    def setUp(self):
        # Save the original isfile function to restore it after the test
        self.original_isfile = os.path.isfile
        self.log_processor = LogProcessor("file.txt")

    def tearDown(self):
        # Restore the original isfile function
        os.path.isfile = self.original_isfile

    def test_is_valid_file_checks_file_exists(self):
        # Mock the isfile function for this test case
        os.path.isfile = lambda x: True

        result = self.log_processor.is_valid_file()
        self.assertTrue(result)

    def test_is_valid_file_checks_file_exists_false(self):
        # Mock the isfile function for this test case
        os.path.isfile = lambda x: False

        result = self.log_processor.is_valid_file()
        self.assertFalse(result)

    def test_is_valid_file_checks_file_extension(self):
        # Mock the isfile function for this test case
        os.path.isfile = lambda x: True

        result = self.log_processor.is_valid_file()
        self.assertTrue(result)

    def test_is_valid_file_checks_file_extension_false(self):
        # Mock the isfile function for this test case
        os.path.isfile = lambda x: True

        self.log_processor.file_path = "file.csv"

        result = self.log_processor.is_valid_file()
        self.assertFalse(result)
