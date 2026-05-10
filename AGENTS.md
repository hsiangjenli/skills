# AGENTS.md

Development conventions for this repository.

## Skill Location

All skills are developed **directly** under `skills/`. Do not use `.agents/skills` as a source — that sync workflow has been retired.

```
skills/
└── my-skill/
    ├── SKILL.md         ← required
    ├── scripts/         ← optional Python scripts
    ├── references/      ← optional reference docs
    └── assets/          ← optional templates / output files
```

## Creating a New Skill

Follow the **`skill-creator-uv`** skill for all creation steps. If the skill involves Python scripts, also follow the **`python`** skill.

### Exceptions

- If the skill explicitly does not need Python, skip the `python` skill conventions.
- "Free-form" skills with no tooling need only `SKILL.md`.

## Updating skills-lock.json

`skills-lock.json` is managed by `npx skills add`. Do not edit it manually after creating a new skill.

## Updating the README

`README.md` is auto-generated from skill frontmatter by the GitHub Actions workflow on every push that modifies `skills/**/SKILL.md`. No manual step needed.
