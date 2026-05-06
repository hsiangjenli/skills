#!/usr/bin/env python3
"""
ICS Manager CLI.

Provides read and write operations for ICS files using icalendar.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse
from urllib.request import urlopen
from uuid import uuid4

from dateutil.rrule import rrulestr
from dotenv import load_dotenv
from icalendar import Calendar, Event


DEFAULT_RANGE_DAYS = 14


def load_env() -> None:
    """Load .env files from the current directory, then from ~/.config/ics-manager/.env.

    Priority (highest to lowest): shell env > cwd .env > user config .env.
    """
    load_dotenv()  # cwd .env; override=False so shell vars are never overwritten
    user_env = Path.home() / ".config" / "ics-manager" / ".env"
    if user_env.exists():
        load_dotenv(user_env)  # fallback for vars not yet set


class IcsManagerError(Exception):
    """Domain error for ICS operations."""


@dataclass(slots=True)
class EventOccurrence:
    """Normalized event occurrence data."""

    uid: str
    summary: str
    start: datetime
    end: datetime
    recurring: bool
    all_day: bool
    location: str
    status: str
    categories: list[str]
    description: str
    organizer: str
    attendees: list[str]

    @property
    def duration_hours(self) -> float:
        """Return event duration in fractional hours."""
        seconds = max((self.end - self.start).total_seconds(), 0.0)
        return seconds / 3600.0

    def to_dict(self) -> dict[str, Any]:
        """Serialize the occurrence to a JSON-safe dictionary."""
        return {
            "uid": self.uid,
            "summary": self.summary,
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
            "duration_hours": round(self.duration_hours, 2),
            "recurring": self.recurring,
            "all_day": self.all_day,
            "location": self.location,
            "status": self.status,
            "categories": self.categories,
            "description": self.description,
            "organizer": self.organizer,
            "attendees": self.attendees,
        }


def is_url(source: str) -> bool:
    """Return True when source is an HTTP(S) URL."""
    parsed = urlparse(source)
    return parsed.scheme in {"http", "https"}


def normalize_datetime(value: Any) -> datetime:
    """Convert a date or datetime-like value into an aware datetime."""
    if hasattr(value, "dt"):
        value = value.dt

    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value

    if isinstance(value, date):
        return datetime.combine(value, time.min, tzinfo=timezone.utc)

    raise IcsManagerError(f"Unsupported temporal value: {value!r}")


def parse_user_temporal(value: str) -> date | datetime:
    """Parse user input as ISO date or datetime."""
    if len(value) == 10:
        return date.fromisoformat(value)
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def parse_range_boundary(value: str | None, fallback: datetime) -> datetime:
    """Parse a range boundary or return the fallback."""
    if value is None:
        return fallback
    return normalize_datetime(parse_user_temporal(value))


def stringify(value: Any) -> str:
    """Return a readable string value."""
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode()
    return str(value)


def parse_categories(value: Any) -> list[str]:
    """Return normalized category values."""
    if value is None:
        return []
    if isinstance(value, list):
        return [stringify(item).strip() for item in value if stringify(item).strip()]
    text = stringify(value)
    if "," not in text:
        return [text.strip()] if text.strip() else []
    return [item.strip() for item in text.split(",") if item.strip()]


def parse_attendees(value: Any) -> list[str]:
    """Normalize attendee property values."""
    if value is None:
        return []
    if isinstance(value, list):
        return [stringify(item) for item in value]
    return [stringify(value)]


def event_duration(
    component: Event, start_value: Any, end_value: Any | None
) -> timedelta:
    """Compute duration for a VEVENT component."""
    start_dt = normalize_datetime(start_value)

    if end_value is not None:
        return max(normalize_datetime(end_value) - start_dt, timedelta(0))

    duration_value = component.decoded("DURATION", None)
    if isinstance(duration_value, timedelta):
        return max(duration_value, timedelta(0))

    if isinstance(start_value, date) and not isinstance(start_value, datetime):
        return timedelta(days=1)

    return timedelta(0)


def load_calendar(source: str) -> Calendar:
    """Load an ICS calendar from a local path or remote URL."""
    if is_url(source):
        with urlopen(source) as response:
            raw_data = response.read()
    else:
        raw_data = Path(source).expanduser().read_bytes()

    return Calendar.from_ical(raw_data)


def require_local_path(source: str) -> Path:
    """Return a local path or raise when source is remote."""
    if is_url(source):
        raise IcsManagerError("Mutating commands require a local .ics file path.")
    return Path(source).expanduser().resolve()


def extract_exdates(component: Event) -> set[datetime]:
    """Return excluded recurrence datetimes for a VEVENT."""
    values = component.get("EXDATE")
    if values is None:
        return set()

    excluded: set[datetime] = set()
    exdate_values = values if isinstance(values, list) else [values]

    for exdate_value in exdate_values:
        dts = getattr(exdate_value, "dts", [])
        for dt_value in dts:
            excluded.add(normalize_datetime(dt_value.dt))

    return excluded


def build_occurrence(
    component: Event,
    occurrence_start: datetime,
    occurrence_end: datetime,
    recurring: bool,
) -> EventOccurrence:
    """Build a normalized occurrence from a VEVENT."""
    start_value = component.decoded("DTSTART")
    categories = parse_categories(component.get("CATEGORIES"))
    organizer = stringify(component.get("ORGANIZER"))
    attendees = parse_attendees(component.get("ATTENDEE"))

    return EventOccurrence(
        uid=stringify(component.get("UID")),
        summary=stringify(component.get("SUMMARY")) or "(untitled)",
        start=occurrence_start,
        end=occurrence_end,
        recurring=recurring,
        all_day=isinstance(start_value, date) and not isinstance(start_value, datetime),
        location=stringify(component.get("LOCATION")),
        status=stringify(component.get("STATUS")),
        categories=categories,
        description=stringify(component.get("DESCRIPTION")),
        organizer=organizer,
        attendees=attendees,
    )


def iter_occurrences(
    calendar: Calendar,
    range_start: datetime,
    range_end: datetime,
) -> list[EventOccurrence]:
    """Expand VEVENTs into normalized occurrences in the given range."""
    overrides: dict[tuple[str, datetime], Event] = {}
    master_events: list[Event] = []
    explicit_events: list[Event] = []

    for component in calendar.walk("VEVENT"):
        uid = stringify(component.get("UID"))
        recurrence_id = component.get("RECURRENCE-ID")
        if recurrence_id is not None:
            overrides[(uid, normalize_datetime(recurrence_id))] = component
            explicit_events.append(component)
        else:
            master_events.append(component)

    occurrences: list[EventOccurrence] = []

    for component in master_events:
        uid = stringify(component.get("UID"))
        start_value = component.decoded("DTSTART", None)
        if start_value is None:
            continue

        end_value = component.decoded("DTEND", None)
        duration = event_duration(component, start_value, end_value)
        base_start = normalize_datetime(start_value)
        excluded_dates = extract_exdates(component)
        overridden_dates = {
            recurrence_start
            for override_uid, recurrence_start in overrides
            if override_uid == uid
        }

        rrule_value = component.get("RRULE")
        if rrule_value is None:
            candidate_starts = [base_start]
        else:
            rule = rrulestr(rrule_value.to_ical().decode(), dtstart=base_start)
            candidate_starts = list(
                rule.between(range_start - duration, range_end, inc=True)
            )

        for occurrence_start in candidate_starts:
            if (
                occurrence_start in excluded_dates
                or occurrence_start in overridden_dates
            ):
                continue

            occurrence_end = occurrence_start + duration
            if occurrence_end <= range_start or occurrence_start >= range_end:
                continue

            occurrences.append(
                build_occurrence(
                    component,
                    occurrence_start,
                    occurrence_end,
                    recurring=rrule_value is not None,
                )
            )

    for component in explicit_events:
        start_value = component.decoded("DTSTART", None)
        if start_value is None:
            continue

        end_value = component.decoded("DTEND", None)
        start_dt = normalize_datetime(start_value)
        end_dt = start_dt + event_duration(component, start_value, end_value)
        if end_dt <= range_start or start_dt >= range_end:
            continue

        occurrences.append(
            build_occurrence(component, start_dt, end_dt, recurring=False)
        )

    return sorted(occurrences, key=lambda item: (item.start, item.summary, item.uid))


def matches_contains(occurrence: EventOccurrence, needle: str | None) -> bool:
    """Return True when the occurrence matches the free-text filter."""
    if not needle:
        return True
    target = needle.lower()
    haystack = " ".join(
        [
            occurrence.summary,
            occurrence.location,
            occurrence.description,
            " ".join(occurrence.categories),
        ]
    ).lower()
    return target in haystack


def clip_duration_hours(
    occurrence: EventOccurrence,
    range_start: datetime,
    range_end: datetime,
) -> float:
    """Return clipped duration in hours within the requested range."""
    clipped_start = max(occurrence.start, range_start)
    clipped_end = min(occurrence.end, range_end)
    if clipped_end <= clipped_start:
        return 0.0
    return (clipped_end - clipped_start).total_seconds() / 3600.0


def print_json(payload: Any) -> None:
    """Print JSON output."""
    print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True))


def format_event_line(occurrence: EventOccurrence) -> str:
    """Return a one-line text representation of an occurrence."""
    duration = round(occurrence.duration_hours, 2)
    parts = [
        occurrence.start.isoformat(),
        occurrence.end.isoformat(),
        occurrence.summary,
        f"uid={occurrence.uid}",
        f"hours={duration}",
    ]
    if occurrence.location:
        parts.append(f"location={occurrence.location}")
    if occurrence.categories:
        parts.append(f"categories={','.join(occurrence.categories)}")
    if occurrence.recurring:
        parts.append("recurring=true")
    return " | ".join(parts)


def list_events(args: argparse.Namespace) -> int:
    """Handle the list-events subcommand."""
    now = datetime.now(timezone.utc)
    range_start = parse_range_boundary(args.start, now)
    range_end = parse_range_boundary(
        args.end, range_start + timedelta(days=DEFAULT_RANGE_DAYS)
    )

    calendar = load_calendar(args.source)
    occurrences = [
        occurrence
        for occurrence in iter_occurrences(calendar, range_start, range_end)
        if matches_contains(occurrence, args.contains)
    ]

    if args.format == "json":
        print_json([occurrence.to_dict() for occurrence in occurrences])
        return 0

    if not occurrences:
        print("No events found in the requested range.")
        return 0

    for occurrence in occurrences:
        print(format_event_line(occurrence))
    return 0


def overview(args: argparse.Namespace) -> int:
    """Handle the overview subcommand."""
    now = datetime.now(timezone.utc)
    range_start = parse_range_boundary(args.start, now)
    range_end = parse_range_boundary(
        args.end, range_start + timedelta(days=DEFAULT_RANGE_DAYS)
    )

    calendar = load_calendar(args.source)
    occurrences = [
        occurrence
        for occurrence in iter_occurrences(calendar, range_start, range_end)
        if matches_contains(occurrence, args.contains)
    ]

    total_hours = round(
        sum(
            clip_duration_hours(occurrence, range_start, range_end)
            for occurrence in occurrences
        ),
        2,
    )
    per_day_counts: dict[str, int] = defaultdict(int)
    summary_counts: Counter[str] = Counter()

    for occurrence in occurrences:
        per_day_counts[occurrence.start.date().isoformat()] += 1
        summary_counts[occurrence.summary] += 1

    busiest_day = None
    if per_day_counts:
        busiest_day = max(per_day_counts.items(), key=lambda item: (item[1], item[0]))

    payload = {
        "range_start": range_start.isoformat(),
        "range_end": range_end.isoformat(),
        "event_count": len(occurrences),
        "total_hours": total_hours,
        "busiest_day": {
            "date": busiest_day[0],
            "event_count": busiest_day[1],
        }
        if busiest_day
        else None,
        "top_summaries": [
            {"summary": summary, "count": count}
            for summary, count in summary_counts.most_common(5)
        ],
    }

    if args.format == "json":
        print_json(payload)
        return 0

    print(f"Range: {payload['range_start']} -> {payload['range_end']}")
    print(f"Events: {payload['event_count']}")
    print(f"Total scheduled hours: {payload['total_hours']}")
    if payload["busiest_day"]:
        print(
            "Busiest day: "
            f"{payload['busiest_day']['date']} ({payload['busiest_day']['event_count']} events)"
        )
    if payload["top_summaries"]:
        print("Top summaries:")
        for item in payload["top_summaries"]:
            print(f"- {item['summary']}: {item['count']}")
    return 0


def summarize_hours(args: argparse.Namespace) -> int:
    """Handle the summarize-hours subcommand."""
    now = datetime.now(timezone.utc)
    range_start = parse_range_boundary(args.start, now)
    range_end = parse_range_boundary(
        args.end, range_start + timedelta(days=DEFAULT_RANGE_DAYS)
    )

    calendar = load_calendar(args.source)
    occurrences = [
        occurrence
        for occurrence in iter_occurrences(calendar, range_start, range_end)
        if matches_contains(occurrence, args.contains)
    ]

    totals: dict[str, float] = defaultdict(float)
    for occurrence in occurrences:
        hours = clip_duration_hours(occurrence, range_start, range_end)
        if args.group_by == "day":
            bucket = occurrence.start.date().isoformat()
        else:
            iso_year, iso_week, _ = occurrence.start.isocalendar()
            bucket = f"{iso_year}-W{iso_week:02d}"
        totals[bucket] += hours

    payload = {
        "range_start": range_start.isoformat(),
        "range_end": range_end.isoformat(),
        "group_by": args.group_by,
        "totals": [
            {"bucket": bucket, "hours": round(hours, 2)}
            for bucket, hours in sorted(totals.items())
        ],
    }

    if args.format == "json":
        print_json(payload)
        return 0

    if not payload["totals"]:
        print("No scheduled hours found in the requested range.")
        return 0

    for item in payload["totals"]:
        print(f"{item['bucket']}: {item['hours']} hours")
    return 0


def backup_file(path: Path) -> Path:
    """Create a backup file and return its path."""
    backup_path = path.with_suffix(path.suffix + ".bak")
    shutil.copy2(path, backup_path)
    return backup_path


def write_calendar(calendar: Calendar, path: Path, backup: bool) -> None:
    """Write the updated calendar to disk."""
    if backup and path.exists():
        backup_file(path)
    path.write_bytes(calendar.to_ical())


def find_event_by_uid(calendar: Calendar, uid: str) -> Event:
    """Return the first VEVENT with the given UID."""
    for component in calendar.walk("VEVENT"):
        if stringify(component.get("UID")) == uid:
            return component
    raise IcsManagerError(f"No event found for UID: {uid}")


def set_component_field(component: Event, key: str, value: Any) -> None:
    """Replace a component field while preserving a single property entry."""
    if key in component:
        del component[key]
    component.add(key, value)


def add_event(args: argparse.Namespace) -> int:
    """Handle the add-event subcommand."""
    path = require_local_path(args.source)
    calendar = load_calendar(str(path))

    start_value = parse_user_temporal(args.start)
    end_value = parse_user_temporal(args.end)

    event = Event()
    event.add("UID", args.uid or str(uuid4()))
    event.add("SUMMARY", args.summary)
    event.add("DTSTART", start_value)
    event.add("DTEND", end_value)
    event.add("DTSTAMP", datetime.now(timezone.utc))

    if args.location:
        event.add("LOCATION", args.location)
    if args.description:
        event.add("DESCRIPTION", args.description)
    if args.status:
        event.add("STATUS", args.status)
    if args.categories:
        event.add(
            "CATEGORIES",
            [item.strip() for item in args.categories.split(",") if item.strip()],
        )

    calendar.add_component(event)

    if args.dry_run:
        print(f"Would add event UID={stringify(event.get('UID'))} to {path}")
        return 0

    write_calendar(calendar, path, backup=not args.no_backup)
    print(f"Added event UID={stringify(event.get('UID'))} to {path}")
    return 0


def update_event(args: argparse.Namespace) -> int:
    """Handle the update-event subcommand."""
    path = require_local_path(args.source)
    calendar = load_calendar(str(path))
    event = find_event_by_uid(calendar, args.uid)

    original_start = event.decoded("DTSTART", None)
    original_end = event.decoded("DTEND", None)

    if args.summary:
        set_component_field(event, "SUMMARY", args.summary)
    if args.location is not None:
        set_component_field(event, "LOCATION", args.location)
    if args.description is not None:
        set_component_field(event, "DESCRIPTION", args.description)
    if args.status is not None:
        set_component_field(event, "STATUS", args.status)
    if args.categories is not None:
        categories = [
            item.strip() for item in args.categories.split(",") if item.strip()
        ]
        set_component_field(event, "CATEGORIES", categories)

    if args.start:
        new_start = parse_user_temporal(args.start)
        set_component_field(event, "DTSTART", new_start)
        if args.end is None and original_start is not None and original_end is not None:
            shifted_end = parse_user_temporal(args.start)
            delta = normalize_datetime(original_end) - normalize_datetime(
                original_start
            )
            shifted_end = normalize_datetime(shifted_end) + delta
            set_component_field(event, "DTEND", shifted_end)

    if args.end:
        set_component_field(event, "DTEND", parse_user_temporal(args.end))

    set_component_field(event, "DTSTAMP", datetime.now(timezone.utc))

    if args.dry_run:
        print(f"Would update event UID={args.uid} in {path}")
        return 0

    write_calendar(calendar, path, backup=not args.no_backup)
    print(f"Updated event UID={args.uid} in {path}")
    return 0


def delete_event(args: argparse.Namespace) -> int:
    """Handle the delete-event subcommand."""
    path = require_local_path(args.source)
    calendar = load_calendar(str(path))
    target_event = find_event_by_uid(calendar, args.uid)

    if args.dry_run:
        print(f"Would delete event UID={args.uid} from {path}")
        return 0

    calendar.subcomponents.remove(target_event)
    write_calendar(calendar, path, backup=not args.no_backup)
    print(f"Deleted event UID={args.uid} from {path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(description="Inspect and edit ICS calendar files")
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_common_range_arguments(command_parser: argparse.ArgumentParser) -> None:
        command_parser.add_argument(
            "--source",
            default=os.environ.get("ICS_SOURCE"),
            help="Local .ics path or HTTP(S) URL (default: $ICS_SOURCE)",
        )
        command_parser.add_argument(
            "--start", help="ISO date or datetime for range start"
        )
        command_parser.add_argument("--end", help="ISO date or datetime for range end")
        command_parser.add_argument("--contains", help="Case-insensitive text filter")
        command_parser.add_argument(
            "--format",
            choices=["text", "json"],
            default="text",
            help="Output format",
        )

    list_parser = subparsers.add_parser(
        "list-events", help="List events in a time range"
    )
    add_common_range_arguments(list_parser)
    list_parser.set_defaults(handler=list_events)

    overview_parser = subparsers.add_parser(
        "overview", help="Summarize workload in a time range"
    )
    add_common_range_arguments(overview_parser)
    overview_parser.set_defaults(handler=overview)

    summarize_parser = subparsers.add_parser(
        "summarize-hours", help="Aggregate scheduled hours by day or week"
    )
    add_common_range_arguments(summarize_parser)
    summarize_parser.add_argument(
        "--group-by",
        choices=["day", "week"],
        default="week",
        help="Aggregation bucket",
    )
    summarize_parser.set_defaults(handler=summarize_hours)

    add_parser = subparsers.add_parser("add-event", help="Add a VEVENT to a local file")
    add_parser.add_argument(
        "--source",
        default=os.environ.get("ICS_SOURCE"),
        help="Local .ics file path (default: $ICS_SOURCE)",
    )
    add_parser.add_argument("--summary", required=True, help="Event summary")
    add_parser.add_argument("--start", required=True, help="ISO date or datetime")
    add_parser.add_argument("--end", required=True, help="ISO date or datetime")
    add_parser.add_argument("--location", help="Event location")
    add_parser.add_argument("--description", help="Event description")
    add_parser.add_argument("--status", help="Event status")
    add_parser.add_argument("--categories", help="Comma-separated categories")
    add_parser.add_argument("--uid", help="Explicit UID, otherwise a UUID is generated")
    add_parser.add_argument(
        "--dry-run", action="store_true", help="Report without writing"
    )
    add_parser.add_argument(
        "--no-backup", action="store_true", help="Disable backup creation"
    )
    add_parser.set_defaults(handler=add_event)

    update_parser = subparsers.add_parser("update-event", help="Update a VEVENT by UID")
    update_parser.add_argument(
        "--source",
        default=os.environ.get("ICS_SOURCE"),
        help="Local .ics file path (default: $ICS_SOURCE)",
    )
    update_parser.add_argument("--uid", required=True, help="Event UID")
    update_parser.add_argument("--summary", help="Updated summary")
    update_parser.add_argument("--start", help="Updated start")
    update_parser.add_argument("--end", help="Updated end")
    update_parser.add_argument(
        "--location", help="Updated location; empty string clears it"
    )
    update_parser.add_argument(
        "--description", help="Updated description; empty string clears it"
    )
    update_parser.add_argument(
        "--status", help="Updated status; empty string clears it"
    )
    update_parser.add_argument(
        "--categories", help="Updated comma-separated categories"
    )
    update_parser.add_argument(
        "--dry-run", action="store_true", help="Report without writing"
    )
    update_parser.add_argument(
        "--no-backup", action="store_true", help="Disable backup creation"
    )
    update_parser.set_defaults(handler=update_event)

    delete_parser = subparsers.add_parser("delete-event", help="Delete a VEVENT by UID")
    delete_parser.add_argument(
        "--source",
        default=os.environ.get("ICS_SOURCE"),
        help="Local .ics file path (default: $ICS_SOURCE)",
    )
    delete_parser.add_argument("--uid", required=True, help="Event UID")
    delete_parser.add_argument(
        "--dry-run", action="store_true", help="Report without writing"
    )
    delete_parser.add_argument(
        "--no-backup", action="store_true", help="Disable backup creation"
    )
    delete_parser.set_defaults(handler=delete_event)

    return parser


def main(argv: Iterable[str] | None = None) -> int:
    """Run the CLI."""
    load_env()
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    if getattr(args, "source", None) is None:
        print(
            "Error: --source is required. Set ICS_SOURCE in .env or pass --source explicitly.",
            file=sys.stderr,
        )
        return 1

    try:
        return args.handler(args)
    except IcsManagerError as error:
        print(str(error), file=sys.stderr)
        return 1
    except FileNotFoundError as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
