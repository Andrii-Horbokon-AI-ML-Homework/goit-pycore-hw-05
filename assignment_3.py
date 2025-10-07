from typing import Dict, List
from collections import Counter
import sys
import re


# Return codes
TOO_FEW_ARGUMENTS = 1
FILE_NOT_FOUND = 2
OS_ERROR = 3


def parse_log_line(line: str) -> Dict[str, str] | None:
    """
    Parses one line of log into components

    Parameters:
        line: Line from log file

    Returns:
        Log entry as dictionary with components: timestamp, level, message
    """
    match = re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) ([A-Z]+) ([^\n]+)", line)
    if not match or len(match.groups()) != 3:
        return None

    return {
        "timestamp": match.group(1),
        "level": match.group(2),
        "message": match.group(3)
    }


def load_logs(path: str) -> List[Dict[str, str]]:
    """
    Loads log file and parses into components

    Parameters:
        path: Path to log file

    Returns:
        List of log entries as dictionary with following keys: timestamp, level, message
    """
    with open(path, mode="r", encoding="utf-8") as log:
        logs = []
        for line in log:
            item = parse_log_line(line)
            if item:
                logs.append(item)
        return logs
    

def filter_logs_by_level(logs: List[Dict[str, str]], level: str) -> List[Dict[str, str]]:
    """
    Filters log entries by log level

    Parameters:
        logs: List of log entries
        level: Log level to filter by

    Returns:
        List of log entries matching the specified level
    """
    return [item for item in logs if item["level"] == level]
    

def count_logs_by_level(logs: List[Dict[str, str]]) -> Counter[str]:
    """
    Counts the number of entries for each log level

    Parameters:
        logs: List of log entries

    Returns:
        Counter with the number of entries for each log level
    """
    return Counter([item["level"] for item in logs])


def display_logs(logs: List[Dict[str, str]], level: str) -> None:
    """
    Prints log details for the specified log level

    Parameters:
        logs: List of log entries
        level: Log level to display
    """
    level_normalized = level.upper()
    logs_by_level = filter_logs_by_level(logs, level_normalized)
    if len(logs_by_level) == 0:
        print(f"Записів для рівня '{level_normalized}' не знайдено.")
        return

    print(f"Деталі логів для рівня '{level_normalized}':")
    for log in logs_by_level:
        print(f"{log['timestamp']} - {log['message']}")


def display_log_counts(counts: Counter[str]) -> None:
    """
    Formats and displays statistics of entry counts by log levels

    Parameters:
        counts: Counter with the number of entries for each log level
    """
    level_header = "Рівень логування"
    level_header_len = len(level_header)
    count_header = "Кількість"
    count_header_len = len(count_header)
    print(f"{level_header} | {count_header}")
    print("-" * (level_header_len + 3 + count_header_len))
    for level, count in counts.most_common():
        print(f"{level:<{level_header_len}} | {count:<{count_header_len}}")


def main():
    """
    Accepts the log file path as the first command-line argument
    and an optional log level as the second argument.

    Displays statistics by log levels and, if a level is specified, lists entries for this level
    """
    if len(sys.argv) < 2:
        print("Замало аргументів.")
        print(f"Використання: python {sys.argv[0]} path [level]")
        sys.exit(TOO_FEW_ARGUMENTS)

    try:
        path = sys.argv[1]
        logs = load_logs(path)
        counts = count_logs_by_level(logs)
        display_log_counts(counts)

        if len(sys.argv) > 2:
            level = sys.argv[2]
            print()
            display_logs(logs, level)

    except FileNotFoundError:
        print(f"Файл не знайдено: '{path}'")
        sys.exit(FILE_NOT_FOUND)

    except OSError:
        print(f"Виникла помилка при читанні файлу: '{path}'")
        sys.exit(OS_ERROR)


if __name__ == "__main__":
    main()
