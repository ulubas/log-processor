import sys

from log_processor import LogProcessor


def run_app():
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    processor = LogProcessor(file_path)

    if not processor.is_valid_file():
        print("Invalid log file format. Please check the file and try again.")
        sys.exit(1)

    processor.process_log()


if __name__ == "__main__":
    run_app()
