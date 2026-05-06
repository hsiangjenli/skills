---
name: ics-manager
description: Manage local or remote ICS calendar sources to inspect upcoming meetings, summarize work hours, and add, update, or delete calendar events when users need a quick operational view of their schedule.
---

# ICS Manager

Use this skill when the task involves reading or editing `.ics` calendar files from a local path or an HTTP(S) URL.

## When to Use

- Review meetings in the next few days or weeks
- Summarize work hours by day or by ISO week
- Build a quick schedule overview from a calendar feed
- Add, update, or delete events in a local `.ics` file
- Inspect calendar metadata such as attendees, locations, and categories

## Quick Start

### Dependency Setup

This skill includes Python scripts managed by `uv`.

```bash
uv run scripts/check_dependencies.py --install
```

### Configuration

Copy `.env.example` to `.env` in the directory where you run commands and fill in your calendar source.

```bash
cp .env.example .env
```

`.env` contents:

```
ICS_SOURCE=~/calendar/work.ics
```

Once set, every command picks up the source automatically without `--source`:

```bash
# No --source needed
uv run scripts/ics_manager.py list-events
uv run scripts/ics_manager.py overview
```

You can also place `.env` at `~/.config/ics-manager/.env` for a user-level default shared across projects.

Priority order: shell environment variable > `.env` in current directory > `~/.config/ics-manager/.env`.

### Main Script

All operations go through `scripts/ics_manager.py`.

```bash
# List events in the next two weeks from a local file
uv run scripts/ics_manager.py list-events --source ~/calendar/work.ics

# Read a remote ICS feed
uv run scripts/ics_manager.py list-events --source https://example.com/calendar.ics

# Summarize hours by week
uv run scripts/ics_manager.py summarize-hours --source ~/calendar/work.ics --group-by week

# Produce a compact operational summary
uv run scripts/ics_manager.py overview --source ~/calendar/work.ics

# Add an event to a local ICS file
uv run scripts/ics_manager.py add-event \
  --source ~/calendar/work.ics \
  --summary "Project review" \
  --start 2026-05-08T14:00:00+08:00 \
  --end 2026-05-08T15:00:00+08:00
```

## Supported Workflows

### Inspect Upcoming Meetings

Use `list-events` with the default 14-day window or provide `--start` and `--end` explicitly.

```bash
uv run scripts/ics_manager.py list-events \
  --source ~/calendar/work.ics \
  --start 2026-05-06 \
  --end 2026-05-20 \
  --contains review
```

Use `--format json` when the result needs to feed another tool or follow-up script.

### Summarize Work Hours

Use `summarize-hours` to aggregate event durations by day or week.

```bash
uv run scripts/ics_manager.py summarize-hours \
  --source ~/calendar/work.ics \
  --group-by week \
  --contains project
```

### Quick Operational Overview

Use `overview` when the user asks for a fast understanding of current workload.

This command reports:

- total event count in range
- total scheduled hours
- busiest day
- top summaries by frequency

### Edit Local Calendars

Mutation commands only support local files. Remote URLs are treated as read-only sources.

```bash
uv run scripts/ics_manager.py update-event --source ~/calendar/work.ics --uid abc123 --summary "Weekly sync"
uv run scripts/ics_manager.py delete-event --source ~/calendar/work.ics --uid abc123
```

By default the script writes a `.bak` backup before modifying the file. Use `--no-backup` only when the user explicitly wants in-place writes without a backup.

## Source Rules

- Accept local filesystem paths and HTTP(S) URLs through `--source`
- Treat remote sources as read-only
- Prefer explicit time windows for analysis tasks
- Prefer `UID` for update and delete operations

## Additional Requirements To Clarify

When the user is shaping the workflow, verify these points if they matter:

- whether recurring events must be expanded
- whether all-day events should count toward work hours
- whether transparent or tentative events should be excluded
- whether summaries should filter by project tag, attendee, or category
- whether edits should preserve alarms, attendees, and organizer metadata
- whether output should be text only or structured JSON
- whether calendar conflicts should be highlighted
- whether multiple ICS sources should be merged before analysis

## Resources

- `scripts/ics_manager.py` - Parse, summarize, and modify ICS files
- `scripts/check_dependencies.py` - Verify and install dependencies
- `.env.example` - Template for environment configuration
- `references/workflows.md` - Prompt patterns, supported commands, and caveats