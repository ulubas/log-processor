import unittest
from log_processor import LogProcessor
from io import BytesIO as StringIO
import os


class TestLogProcessorScenarios(unittest.TestCase):
    def setUp(self):
        # Create a LogProcessor instance for testing
        self.log_processor = LogProcessor("file.txt")

    def test_single_user_single_session(self):
        # Scenario: One user, one session
        log_entries = [
            "12:00:00 user start\n",
            "12:30:00 user end\n",
        ]
        self.run_test(log_entries, "user 1 1800")

    def test_single_user_multiple_sessions(self):
        # Scenario: One user, multiple sessions
        log_entries = [
            "12:00:00 user start\n",
            "12:30:00 user end\n",
            "13:00:00 user start\n",
            "13:45:00 user end\n",
        ]
        self.run_test(log_entries, "user 2 4500")

    def test_multiple_users(self):
        # Scenario: Multiple users, single session each
        log_entries = [
            "12:00:00 user1 start\n",
            "12:30:00 user2 start\n",
            "13:00:00 user1 end\n",
            "13:15:00 user2 end\n",
        ]
        self.run_test(log_entries, "user2 1 2700\nuser1 1 3600")

    def test_overlapping_sessions(self):
        # Scenario: Overlapping sessions for a user
        log_entries = [
            "12:00:00 user start\n",
            "12:45:00 user start\n",
            "12:30:00 user end\n",
            "13:15:00 user end\n",
        ]
        self.run_test(log_entries, "user 2 3600")

    def test_given_scenario_in_the_test_pdf(self):
        log_entries = [
            "14:02:03 ALICE99 Start\n",
            "14:02:05 CHARLIE End\n",
            "14:02:34 ALICE99 End\n",
            "14:02:58 ALICE99 Start\n",
            "14:03:02 CHARLIE Start\n",
            "14:03:33 ALICE99 Start\n",
            "14:03:35 ALICE99 End\n",
            "14:03:37 CHARLIE End\n",
            "14:04:05 ALICE99 End\n",
            "14:04:23 ALICE99 End\n",
            "14:04:41 CHARLIE Start\n",
        ]
        self.run_test(log_entries, "CHARLIE 3 37\nALICE99 4 240")

    def run_test(self, log_entries, expected_result):
        # Create a temporary test file with provided log entries
        file_path = os.path.join(os.path.dirname(__file__), "test_file.txt")
        with open(file_path, "w") as test_file:
            test_file.writelines(log_entries)

        # Capture the printed output during process_log
        captured_output = StringIO()
        import sys

        sys.stdout = captured_output

        self.log_processor.file_path = file_path
        self.log_processor.process_log()

        sys.stdout = sys.__stdout__  # Reset redirect.

        # Compare the printed output with the expected result
        self.assertEqual(captured_output.getvalue().strip(), expected_result)

        # Remove the temporary test file
        os.remove(file_path)
