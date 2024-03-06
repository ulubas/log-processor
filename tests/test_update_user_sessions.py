import unittest
from log_processor import LogProcessor
from datetime import datetime

from user_session import UserSession


class TestUpdateUserSessions(unittest.TestCase):
    def setUp(self):
        self.log_processor = LogProcessor("file.txt")

    def test_start_action_adds_new_session(self):
        self.log_processor.update_user_sessions(
            "user1", datetime(1900, 1, 1, 12, 0, 0), "start"
        )
        expected = UserSession(start=datetime(1900, 1, 1, 12, 0, 0))
        self.assertEqual(
            self.log_processor.user_sessions["user1"][0].start, expected.start
        )
        self.assertIsNone(self.log_processor.user_sessions["user1"][0].end)

    def test_end_action_updates_first_open_session(self):
        self.log_processor.update_user_sessions(
            "user1", datetime(1900, 1, 1, 12, 0, 0), "start"
        )
        self.log_processor.update_user_sessions(
            "user1", datetime(1900, 1, 1, 12, 10, 0), "start"
        )
        self.log_processor.update_user_sessions(
            "user1", datetime(1900, 1, 1, 12, 30, 0), "end"
        )
        expected = UserSession(
            start=datetime(1900, 1, 1, 12, 0, 0), end=datetime(1900, 1, 1, 12, 30, 0)
        )

        self.assertEqual(
            self.log_processor.user_sessions["user1"][0].start, expected.start
        )
        self.assertEqual(self.log_processor.user_sessions["user1"][0].end, expected.end)

    def test_end_action_adds_new_session_if_no_last_open_session(self):
        self.log_processor.update_user_sessions(
            "user1", datetime(1900, 1, 1, 12, 30, 0), "end"
        )
        expected = UserSession(end=datetime(1900, 1, 1, 12, 30, 0))
        self.assertEqual(self.log_processor.user_sessions["user1"][0].end, expected.end)
        self.assertIsNone(self.log_processor.user_sessions["user1"][0].start)
