# Claude Run Service Setup

## Install and Start the Service

```bash
# Copy to LaunchAgents
# Load the service
cp /Users/derek/claude_run/com.derek.clauderun.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.derek.clauderun.plist
```

## Useful Commands

```bash
# Stop the service
launchctl unload ~/Library/LaunchAgents/com.derek.clauderun.plist

# Restart (unload then load)
launchctl unload ~/Library/LaunchAgents/com.derek.clauderun.plist
launchctl load ~/Library/LaunchAgents/com.derek.clauderun.plist

# Check status
launchctl list | grep clauderun

# View logs
tail -f /Users/derek/claude_run/claude_run.log
tail -f /Users/derek/claude_run/claude_run.error.log
```

## Service Behavior

- Starts automatically at login (`RunAtLoad`)
- Restarts automatically if it exits (`KeepAlive`)
- Logs output to `claude_run.log` and errors to `claude_run.error.log`
