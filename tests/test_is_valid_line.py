import unittest
from log_processor import LogProcessor


class TestIsValidLine(unittest.TestCase):
    def test_valid_line(self):
        line = "12:34:56 user123 Start"
        result = LogProcessor.is_valid_line(line)
        self.assertTrue(result)

    def test_line_missing_empty_line(self):
        line = " "
        result = LogProcessor.is_valid_line(line)
        self.assertFalse(result)

    def test_line_missing_parts(self):
        line = "12:34:56 user123"
        result = LogProcessor.is_valid_line(line)
        self.assertFalse(result)

    def test_invalid_timestamp(self):
        line = "12:3456 user123 start"
        result = LogProcessor.is_valid_line(line)
        self.assertFalse(result)

    def test_non_alphanumeric_username(self):
        line = "12:34:56 user#123 start"
        result = LogProcessor.is_valid_line(line)
        self.assertFalse(result)

    def test_invalid_action(self):
        line = "12:34:56 user123 jump"
        result = LogProcessor.is_valid_line(line)
        self.assertFalse(result)
