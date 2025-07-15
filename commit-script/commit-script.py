import subprocess
import importlib
from datetime import datetime

LOG_DIR = "logs"

pattern_name = "smiley"
pattern_module = importlib.import_module(f"commit-patterns.{pattern_name}")

PATTERN = pattern_module.PATTERN
START_DATE = datetime.strptime(pattern_module.START_DATE, "%Y-%m-%d")

def should_commit(today):
    days_since_start = (today - START_DATE).days
    if days_since_start < 0:
        print("Date is before pattern start date— you should double check the config.")
        return False

    week = days_since_start // 7
    day = today.weekday()
    day = (day + 1) % 7

    if week >= len(PATTERN[0]):
        print("Date is beyond the defined pattern grid— time to update the pattern!")
        return False

    cell_value = PATTERN[day][week]
    print(f"Grid value for today: {cell_value} (Week {week}, Day {day})")

    return cell_value == "1"

def git_commit(today):
    date_str = today.strftime("%Y-%m-%d")
    commit_message = f"Log for {date_str}"
    commit_date = f"{date_str}T12:00:00"

    print(f"Committing new logs...")

    subprocess.run(["git", "add", LOG_DIR], check=True)
    subprocess.run([
        "git", "commit",
        "--date", commit_date,
        "-m", commit_message
    ], check=True)

def git_push():
    print("Pushing to GitHub...")
    subprocess.run(["git", "push"], check=True)

if __name__ == "__main__":
    today = datetime.today()
    date_str = today.strftime("%Y-%m-%d")

    if should_commit(today):
        git_commit(today)
        git_push()
    else:
        print("Today’s cell is 0 — skipping commit.")
