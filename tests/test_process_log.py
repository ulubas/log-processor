import unittest
from log_processor import LogProcessor


class TestProcessLogMethod(unittest.TestCase):
    def setUp(self):
        # Create a temporary test file
        self.test_file_path = "test_file.txt"
        with open(self.test_file_path, "w") as test_file:
            test_file.write("00:00:01 user start\n")

        self.log_processor = LogProcessor("test_file.txt")
        self.log_processor.update_earliest_latest_time = lambda timestamp: setattr(
            self.log_processor, "update_earliest_latest_time_called", True
        )
        self.log_processor.update_user_sessions = (
            lambda username, timestamp, action: setattr(
                self.log_processor, "update_user_sessions_called", True
            )
        )
        self.log_processor.adjust_overlapping_sessions = lambda: setattr(
            self.log_processor, "adjust_overlapping_sessions_called", True
        )
        self.log_processor.print_results = lambda: setattr(
            self.log_processor, "print_results_called", True
        )

    def tearDown(self):
        # Remove the temporary test file
        import os

        os.remove(self.test_file_path)
        pass

    def test_process_log_calls_all_methods(self):
        # Call the process_log method
        self.log_processor.process_log()

        # Assert that each method was called at least once
        self.assertTrue(
            getattr(self.log_processor, "update_earliest_latest_time_called", False)
        )
        self.assertTrue(
            getattr(self.log_processor, "update_user_sessions_called", False)
        )
        self.assertTrue(
            getattr(self.log_processor, "adjust_overlapping_sessions_called", False)
        )
        self.assertTrue(getattr(self.log_processor, "print_results_called", False))
