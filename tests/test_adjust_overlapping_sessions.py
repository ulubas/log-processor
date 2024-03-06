import unittest
from datetime import datetime
from log_processor import LogProcessor, UserSession


class TestAdjustOverlappingSessions(unittest.TestCase):
    def setUp(self):
        # Sample data for testing
        self.log_processor = LogProcessor("file.txt")
        self.log_processor.earliest_time = datetime(2022, 1, 1, 12, 0, 0)
        self.log_processor.latest_time = datetime(2022, 1, 1, 14, 0, 0)
        self.log_processor.user_sessions = {
            "user1": [
                UserSession(
                    start=datetime(2022, 1, 1, 12, 30, 0),
                    end=datetime(2022, 1, 1, 13, 0, 0),
                )
            ],
            "user2": [UserSession(start=None, end=datetime(2022, 1, 1, 13, 45, 0))],
            "user3": [UserSession(start=datetime(2022, 1, 1, 12, 15, 0), end=None)],
        }

    def test_adjust_overlapping_sessions(self):
        self.log_processor.adjust_overlapping_sessions()

        # Check user1 session, user with start and end time
        user1_session = self.log_processor.user_sessions["user1"][0]
        self.assertEqual(user1_session.start, datetime(2022, 1, 1, 12, 30, 0))
        self.assertEqual(user1_session.end, datetime(2022, 1, 1, 13, 0, 0))

        # Check user2 session, user with only end time
        user2_session = self.log_processor.user_sessions["user2"][0]
        self.assertEqual(user2_session.start, self.log_processor.earliest_time)
        self.assertEqual(user2_session.end, datetime(2022, 1, 1, 13, 45, 0))

        # Check user3 session, user with only start time
        user3_session = self.log_processor.user_sessions["user3"][0]
        self.assertEqual(user3_session.start, datetime(2022, 1, 1, 12, 15, 0))
        self.assertEqual(user3_session.end, self.log_processor.latest_time)
