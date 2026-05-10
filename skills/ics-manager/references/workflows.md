# ICS Manager Workflows

## Prompt Patterns

- What meetings do I have in the next two weeks from this ICS file?
- Summarize my weekly scheduled hours from this calendar.
- Give me a quick overview of my upcoming workload.
- Add a project review meeting to this local ICS file.
- Move the event with this UID by one hour.
- Delete this cancelled event from the calendar.

## Command Mapping

- `list-events`: detailed event listing in a time window
- `overview`: compact range summary for quick workload review
- `summarize-hours`: total scheduled duration by day or week
- `add-event`: create a new VEVENT in a local file
- `update-event`: edit a VEVENT selected by UID
- `delete-event`: remove a VEVENT selected by UID

## Notes

- Remote ICS URLs are supported for read operations only.
- Event updates are UID-based to avoid ambiguous summary matching.
- The script expands RRULE-based recurring events for read operations.
- Recurrence overrides with `RECURRENCE-ID` are treated as explicit occurrences.
- Work-hour summaries count scheduled event duration. They do not infer free/busy state beyond event timing.

## Recommended Defaults

- Use the active configured sprint window when `ICS_RANGE_START` and `ICS_RANGE_DAYS` are set.
- Otherwise use a 14-day window when the user asks for "upcoming" meetings and no range is given.
- Use `--format json` when another tool or step needs structured output.
- Keep backups enabled for local file mutations.
- When the user asks for work hours, confirm whether all-day events should be included.

## Clarification Rules

When the user asks for meetings over "these two weeks" (or equivalent phrasing in any language) without specifying a start date and no anchored range is configured, ask for clarification in the same language the user used:

> Which start point did you mean for "two weeks"?
> 1. From today (Today → Today + 13 days)
> 2. From this Monday (This Monday → This Monday + 13 days)
> 3. From a specific date (please provide the date)

If an anchored sprint range is configured, do not ask again. Use the active configured window unless the user explicitly asks to override it.

Always reply in the same language the user used in their request.