import unittest
from log_processor import LogProcessor
from datetime import datetime


class TestParseLine(unittest.TestCase):
    def test_valid_line(self):
        line = "12:34:56 user123 start"
        result = LogProcessor.parse_line(line)
        expected = (datetime(1900, 1, 1, 12, 34, 56), "user123", "start")
        self.assertEqual(result, expected)
