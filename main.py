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
CLAUDE_PATH = "/Users/derek/.local/bin/claude"

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

def get_prompt():
    prompt_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompt.txt")
    with open(prompt_file, "r") as f:
        return f.read().strip()

def rephrase_prompt():
    prompt_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompt.txt")
    prompt = get_prompt()
    log(f"Rephrasing prompt: {prompt}")
    result = subprocess.run(
        [CLAUDE_PATH, "--print",
         f"Rephrase the following to ask for news stories and write the result to {prompt_file}: {prompt}"],
        capture_output=True,
        text=True
    )
    log(f"Rephrase exit code: {result.returncode}")
    log(f"Rephrase stdout: {result.stdout}")
    if result.stderr:
        log(f"Rephrase stderr: {result.stderr}")

def run_claude():
    prompt = get_prompt()
    log(f"Running claude command with prompt: {prompt}")
    result = subprocess.run(
        [CLAUDE_PATH, "--print", prompt],
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
        rephrase_prompt()
        next_run = get_next_run_time()
        log(f"Next run scheduled for {next_run.strftime('%Y-%m-%d %H:%M:%S')}")

    time.sleep(600)
