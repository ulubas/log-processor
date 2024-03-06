# Log Processor

The Log Processor is a Python command-line tool designed to process log files containing user sessions and calculate their total duration. The tool is built with simplicity and modularity in mind.

## Prerequisites
- Python 2.7

## Getting Started
- Clone the repository:

```bash
git clone <repository_url>
cd LogProcessor
````

## Usage

To use the Log Processor, run the following command in your terminal:

```bash
python2.7 app.py <file_path>
```

Where `<file_path>` is the path to the log file you want to process.

## Features

- **File Validation**: Checks if the provided file is a valid text file.
  
- **Line Validation**: Verifies if each line in the log file adheres to the specified format.
  
- **Session Processing**: Updates user sessions based on the log file entries.
  
- **Time Adjustment**: Adjusts start and end times for sessions that overlap the time boundaries.
  
- **Results Printing**: Prints user sessions and their total duration.

## Structure

- `log_processor.py`: Contains the `LogProcessor` class responsible for processing log files.
  
- `user_session.py`: Defines the `UserSession` class representing a user session.
  
- `app.py`: The main application script that runs the Log Processor from the command line.
  
- `tests/`: Contains unit tests for the Log Processor.

## Running Tests

Execute the following command in your terminal to run the unit tests:

```bash
python2.7 -m unittest discover -p 'test_*.py' -s tests
```

## Example

Suppose you have a log file named example_log.txt with entries like:

```text
14:02:03 ALICE99 Start
14:02:05 CHARLIE End
14:02:34 ALICE99 End
14:02:58 ALICE99 Start
14:03:02 CHARLIE Start
14:03:33 ALICE99 Start
14:03:35 ALICE99 End
14:03:37 CHARLIE End
14:04:05 ALICE99 End
14:04:23 ALICE99 End
14:04:41 CHARLIE Start
```

Running the Log Processor with the following command:

```bash
python2.7 app.py example_log.txt
```

Would produce the following output:

```text
CHARLIE 3 37
ALICE99 4 240
```

This indicates the user sessions, session counts, and total durations.

## License

This project is licensed under the MIT License.