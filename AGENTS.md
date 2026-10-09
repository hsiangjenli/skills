# AGENTS.md

Development conventions for this repository.

## Skill Location

All repository-managed skills live under `skills/`. This is the canonical source directory, is published to GitHub, and is what `npx skills add` consumes.

Do not create new skills under `.agents/skills/`. That directory is legacy and must not be used as a source.

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

`README.md` is auto-generated from skill frontmatter in `skills/**/SKILL.md` by the GitHub Actions workflow `.github/workflows/sync-to-skills.yaml`. No manual step needed.
