# AGENTS.md

Development conventions for this repository.

## Skill Location

All repository-managed skills are developed under `.agents/skills/`.

Use `.agents/skills` as the canonical source directory for this repo. If a workflow or user has a special path requirement, treat that as an explicit override rather than the default convention.

```
.agents/skills/
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

`README.md` is auto-generated from skill frontmatter in `.agents/skills/**/SKILL.md` by the GitHub Actions workflow. No manual step needed.
