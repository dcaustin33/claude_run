import os
import subprocess
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

INTERVAL_HOURS = 5
START_HOUR = 4
START_MINUTE = 1
LOG_FILE = "claude_output.log"
EST = ZoneInfo("America/New_York")

def log(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def get_next_run_time():
    """Calculate the next scheduled run time: 4:01 AM EST or every 5 hours after that."""
    now = datetime.now(EST)
    today_start = now.replace(hour=START_HOUR, minute=START_MINUTE, second=0, microsecond=0)

    if now < today_start:
        return today_start

    hours_since_start = (now - today_start).total_seconds() / 3600
    intervals_passed = int(hours_since_start // INTERVAL_HOURS)
    next_run = today_start + timedelta(hours=(intervals_passed + 1) * INTERVAL_HOURS)

    tomorrow_start = today_start + timedelta(days=1)
    if next_run >= tomorrow_start:
        return tomorrow_start

    return next_run

def run_claude():
    log("Running claude command...")
    result = subprocess.run(
        ["/opt/homebrew/bin/claude", "hello"],
        capture_output=True,
        text=True
    )
    log(f"Exit code: {result.returncode}")
    log(f"Stdout: {result.stdout}")
    if result.stderr:
        log(f"Stderr: {result.stderr}")

log("Service started")

next_run = get_next_run_time()
log(f"Next run scheduled for {next_run.strftime('%Y-%m-%d %H:%M:%S')}")

while True:
    now = datetime.now(EST)

    if now >= next_run:
        run_claude()
        next_run = get_next_run_time()
        log(f"Next run scheduled for {next_run.strftime('%Y-%m-%d %H:%M:%S')}")

    time.sleep(600)
