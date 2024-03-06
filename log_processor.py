import os
from collections import defaultdict
from datetime import datetime

from user_session import UserSession


class LogProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.user_sessions = defaultdict(list)
        self.earliest_time, self.latest_time = None, None

    def is_valid_file(self):
        """
        Check if the file path is a valid text file that exists.

        Returns:
            bool: True if the file is valid, False otherwise.
        """
        # Check if the file exists
        if not os.path.isfile(self.file_path):
            return False

        # Check if the file is a text file
        _, file_extension = os.path.splitext(self.file_path)
        if file_extension.lower() != ".txt":
            return False

        return True

    @staticmethod
    def is_valid_line(line):
        """
        Check if a log file line adheres to the specified format.

        Returns:
            bool: True if the line is valid, False otherwise.
        """
        # Check for empty lines
        line = line.strip()
        if not line:
            return False

        # Check if the line has 3 parts
        parts = line.split(" ")
        if len(parts) != 3:
            return False
        timestamp_str, username, action = parts

        # Check if the timestamp is in the correct format
        try:
            datetime.strptime(timestamp_str, "%H:%M:%S")
        except ValueError:
            return False

        # Check if the username is alphanumeric
        if not username.isalnum():
            return False

        # Check if the action is either 'start' or 'end'
        if action.lower() not in {"start", "end"}:
            return False

        return True

    @staticmethod
    def parse_line(line):
        """
        Parse a log file line and extract timestamp, username, and action.

        Returns:
            tuple: Tuple containing timestamp (datetime object), username (str), and action (str).
        """
        parts = line.strip().split(" ")
        timestamp_str, username, action = parts
        timestamp = datetime.strptime(timestamp_str, "%H:%M:%S")
        action = action.lower()
        return timestamp, username, action

    def update_earliest_latest_time(self, timestamp):
        """
        Update the earliest and latest time based on the log entry timestamp.

        Args:
            timestamp (datetime): Timestamp of the log entry.
        """
        if self.earliest_time is None or timestamp < self.earliest_time:
            self.earliest_time = timestamp

        if self.latest_time is None or timestamp > self.latest_time:
            self.latest_time = timestamp

    def update_user_sessions(self, username, timestamp, action):
        """
        Update user sessions based on the log file entry.

        Args:
            username (str): User's username.
            timestamp (datetime): Timestamp of the log entry.
            action (str): Log entry action (start or end).
        """
        # Get the sessions for the user
        sessions = self.user_sessions.get(username, [])

        # Find the first open session (if any)
        last_open_session = next((s for s in sessions if s.end is None), None)

        # If the action is 'start', add a new session entry for the user
        if action == "start":
            self.user_sessions[username].append(UserSession(start=timestamp))

        # If the action is 'end'
        elif action == "end":
            # If there is a last open session, update its end time
            if last_open_session:
                last_open_session.end = timestamp

            # If there is no last open session, add a new session entry
            else:
                self.user_sessions[username].append(UserSession(end=timestamp))

    def adjust_overlapping_sessions(self):
        """
        Adjust star & end times for sessions that overlap the time boundaries.
        """
        for username, sessions in self.user_sessions.items():
            for session in sessions:
                if session.end is None:
                    session.end = self.latest_time

                if session.start is None:
                    session.start = self.earliest_time

    def print_results(self):
        """
        Print the user sessions and their total duration.
        """
        for username, sessions in self.user_sessions.items():
            total_duration = sum(
                (session.end - session.start).seconds for session in sessions
            )
            print(
                "{username} {session_count} {total_duration}".format(
                    username=username,
                    session_count=len(sessions),
                    total_duration=total_duration,
                )
            )

    def process_log(self):
        """
        Process the log file and update user sessions.
        """
        with open(self.file_path, "r") as file:
            for line in file:
                if not self.is_valid_line(line):
                    continue  # Skip invalid lines

                timestamp, username, action = self.parse_line(line)

                self.update_earliest_latest_time(timestamp)

                self.update_user_sessions(username, timestamp, action)

        self.adjust_overlapping_sessions()
        self.print_results()
