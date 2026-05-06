---
name: ics-manager
description: Manage local or remote ICS calendar sources to inspect upcoming meetings, summarize work hours, and add, update, or delete calendar events when users need a quick operational view of their schedule.
---

# ICS Manager

Read or edit `.ics` files from a local path or HTTP(S) URL.

## Setup (one-time only)

```bash
uv run scripts/check_dependencies.py --install
# Set ICS_SOURCE in .env or ~/.config/ics-manager/.env to skip --source each time
```

> **Do NOT run `check_dependencies.py` on every invocation.** `uv run` resolves dependencies automatically. Only run it once during initial setup or when the environment may be broken.

## Commands

All operations go through `scripts/ics_manager.py`:

| Command | Key flags | Notes |
|---|---|---|
| `list-events` | `--source`, `--start`, `--end`, `--contains`, `--format json` | Default window: 14 days |
| `summarize-hours` | `--source`, `--group-by day\|week`, `--contains` | Aggregates event durations |
| `overview` | `--source`, `--start`, `--end` | Count, total hours, busiest day — **use this instead of combining list-events + summarize-hours** |
| `add-event` | `--source`, `--summary`, `--start`, `--end` | Local files only |
| `update-event` | `--source`, `--uid`, `--summary` | Local files only |
| `delete-event` | `--source`, `--uid` | Local files only; `.bak` backup written by default |

Remote URLs are read-only. Use `--uid` for update/delete.

## Efficiency rules

- **One command per task**: use `overview` when the user asks for a schedule summary or total hours; only call `list-events` when full event details are needed.
- **Never run the same command twice**: do not call `list-events --format json` followed by `list-events` in plain format; pick one.
- **Skip setup**: do not call `check_dependencies.py` before each command.

## Resources

- `scripts/ics_manager.py` - Parse, summarize, and modify ICS files
- `references/workflows.md` - Prompt patterns and caveats
- `.env.example` - Environment configuration template