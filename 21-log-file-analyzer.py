import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path


TIMESTAMP_PATTERN = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"
LEVEL_PATTERN = r"\b(ERROR|WARN|INFO|DEBUG)\b"


def parse_log_file(file_path):
    error_counts = defaultdict(int)
    time_buckets = defaultdict(int)
    skipped_lines = 0

    with open(file_path, "r", errors="ignore") as file:
        for line in file:
            timestamp_match = re.search(TIMESTAMP_PATTERN, line)
            level_match = re.search(LEVEL_PATTERN, line)

            if not timestamp_match or not level_match:
                skipped_lines += 1
                continue

            level = level_match.group()
            timestamp_str = timestamp_match.group()

            try:
                timestamp = datetime.strptime(
                    timestamp_str, "%Y-%m-%d %H:%M:%S"
                )
            except ValueError:
                skipped_lines += 1
                continue

            # Count error types
            error_counts[level] += 1

            # Group by hour
            hour_bucket = timestamp.strftime("%Y-%m-%d %H:00")
            time_buckets[hour_bucket] += 1

    return error_counts, time_buckets, skipped_lines


def main():
    file_path = input("Enter log file path: ").strip()
    path = Path(file_path)

    if not path.exists() or not path.is_file():
        print("Invalid file path.")
        return

    error_counts, time_buckets, skipped = parse_log_file(path)

    print("\n=== Log Summary ===")

    print("\nEvents by level:")
    for level, count in error_counts.items():
        print(f"{level}: {count}")

    print("\nEvents per hour:")
    for hour, count in sorted(time_buckets.items()):
        print(f"{hour} -> {count}")

    print(f"\nSkipped lines: {skipped}")


if __name__ == "__main__":
    main()
