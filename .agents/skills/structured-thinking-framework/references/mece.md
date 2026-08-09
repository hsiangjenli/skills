# MECE problem decomposition

## Use when

Use MECE when the question is broad, the scope is unclear, or the user needs a problem tree. Do not force strict MECE onto inherently overlapping human or social categories; state the chosen organizing principle instead.

## Method

1. Write one root question that can be answered.
2. Choose one decomposition rule for the first level, such as process stage, customer segment, cause, or time period.
3. Create branches that do not overlap under that rule.
4. Check coverage: every material part of the root question should have a branch.
5. Continue only until branches become actionable or answerable.
6. Mark uncertain or estimated branches explicitly.

## Framework data

```json
{
  "root_question": "How can delivery reliability improve?",
  "branches": [
    {"label": "Planning", "children": ["scope clarity", "capacity forecast"]},
    {"label": "Execution", "children": ["work in progress", "handoffs"]}
  ],
  "coverage_check": "All observed delay stages are represented.",
  "overlap_check": "Branches use delivery lifecycle stage as the single rule."
}
```

## Quality checks

- The root question is specific enough to answer.
- Each level uses one consistent decomposition rule.
- Branches are mutually exclusive under that rule.
- Missing information is listed rather than silently filled.
- Stop before the tree becomes unreadable.
