import unittest
from datetime import datetime
from log_processor import LogProcessor, UserSession


class TestPrintResults(unittest.TestCase):
    def setUp(self):
        # Sample data for testing
        self.log_processor = LogProcessor("file.txt")
        self.log_processor.user_sessions = {
            "user1": [
                UserSession(
                    start=datetime(2022, 1, 1, 12, 30, 0),
                    end=datetime(2022, 1, 1, 13, 0, 0),
                )
            ],
            "user2": [
                UserSession(
                    start=datetime(2022, 1, 1, 11, 0, 0),
                    end=datetime(2022, 1, 1, 11, 45, 0),
                )
            ],
        }

    def test_print_results(self):
        # Redirect print output for testing
        from io import BytesIO as StringIO
        import sys

        original_stdout = sys.stdout
        sys.stdout = StringIO()

        self.log_processor.print_results()

        # Get the printed content
        printed_content = sys.stdout.getvalue()

        # Reset redirect.
        sys.stdout = original_stdout

        # Check the printed content
        expected_output = "user2 1 2700\n" "user1 1 1800\n"
        self.assertEqual(printed_content, expected_output)
