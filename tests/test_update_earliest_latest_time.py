import unittest
from datetime import datetime
from log_processor import LogProcessor


class TestUpdateEarliestLatestTimeMethod(unittest.TestCase):
    def setUp(self):
        self.log_processor = LogProcessor("test_file.txt")

    def tearDown(self):
        pass

    def test_update_earliest_latest_time_initial_values(self):
        timestamp = datetime(2022, 1, 1, 12, 0, 0)
        self.log_processor.update_earliest_latest_time(timestamp)

        self.assertEqual(self.log_processor.earliest_time, timestamp)
        self.assertEqual(self.log_processor.latest_time, timestamp)

    def test_update_earliest_latest_time_earlier_timestamp(self):
        initial_timestamp = datetime(2022, 1, 1, 12, 0, 0)
        updated_timestamp = datetime(2022, 1, 1, 11, 0, 0)

        self.log_processor.earliest_time = initial_timestamp
        self.log_processor.latest_time = initial_timestamp

        self.log_processor.update_earliest_latest_time(updated_timestamp)

        self.assertEqual(self.log_processor.earliest_time, updated_timestamp)
        self.assertEqual(self.log_processor.latest_time, initial_timestamp)

    def test_update_earliest_latest_time_later_timestamp(self):
        initial_timestamp = datetime(2022, 1, 1, 12, 0, 0)
        updated_timestamp = datetime(2022, 1, 1, 13, 0, 0)

        self.log_processor.earliest_time = initial_timestamp
        self.log_processor.latest_time = initial_timestamp

        self.log_processor.update_earliest_latest_time(updated_timestamp)

        self.assertEqual(self.log_processor.earliest_time, initial_timestamp)
        self.assertEqual(self.log_processor.latest_time, updated_timestamp)
