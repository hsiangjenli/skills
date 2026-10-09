#!/usr/bin/env python3
"""
Update README.md with skills list from the skills directory.
"""

import argparse
import json
import re
from pathlib import Path


def parse_skill_frontmatter(skill_md_path: Path) -> dict:
    """
    Parse SKILL.md frontmatter to extract name and description.

    Parameters
    ----------
    skill_md_path : Path
        Path to SKILL.md file

    Returns
    -------
    dict
        Dictionary with 'name' and 'description' keys
    """
    try:
        content = skill_md_path.read_text(encoding="utf-8")

        # Extract frontmatter between --- markers
        frontmatter_match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if not frontmatter_match:
            return {"name": "", "description": ""}

        frontmatter = frontmatter_match.group(1)

        # Extract name and description
        name_match = re.search(r"^name:\s*(.+)$", frontmatter, re.MULTILINE)
        desc_match = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)

        return {
            "name": name_match.group(1).strip() if name_match else "",
            "description": desc_match.group(1).strip() if desc_match else "",
        }
    except Exception as e:
        print(f"Error parsing {skill_md_path}: {e}")
        return {"name": "", "description": ""}


def load_skills_lock(skills_lock_path: Path) -> dict:
    """
    Load skills-lock.json file.

    Parameters
    ----------
    skills_lock_path : Path
        Path to skills-lock.json file

    Returns
    -------
    dict
        The parsed skills-lock data
    """
    with open(skills_lock_path, encoding="utf-8") as f:
        return json.load(f)


def filter_skills_by_source(
    skills_data: dict, target_source: str, skill_names: list[str]
) -> list[str]:
    """
    Filter skills by source, keeping locally created skills not tracked in the lock file.

    Parameters
    ----------
    skills_data : dict
        The skills dictionary from skills-lock.json
    target_source : str
        The source to filter by (e.g., "hsiangjenli/skills")
    skill_names : list[str]
        Skill directory names to filter

    Returns
    -------
    list[str]
        List of skill names that match the target source or are not in the lock file
    """
    skills = skills_data.get("skills", {})
    return [
        skill_name
        for skill_name in skill_names
        if skill_name not in skills or skills[skill_name].get("source") == target_source
    ]


def generate_skills_table(
    skills_dir: Path, allowed_skills: list[str] | None = None
) -> str:
    """
    Generate markdown table of skills.

    Parameters
    ----------
    skills_dir : Path
        Path to the skills directory
    allowed_skills : list[str] | None
        If provided, only include skills whose directory name is in this list.

    Returns
    -------
    str
        Markdown table content
    """
    skills = []

    # Scan all subdirectories in skills
    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue

        if allowed_skills is not None and skill_dir.name not in allowed_skills:
            continue

        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue

        info = parse_skill_frontmatter(skill_md)
        if info["name"]:
            skills.append(info)

    # Generate table
    table = "| Skill Name | Description |\n"
    table += "|------------|-------------|\n"

    for skill in skills:
        name = skill["name"]
        description = skill["description"]
        table += f"| `{name}` | {description} |\n"

    return table


def update_readme(readme_path: Path, skills_table: str):
    """
    Update README.md with skills table.

    Parameters
    ----------
    readme_path : Path
        Path to README.md file
    skills_table : str
        Generated skills table content
    """
    # Overwrite README with skills table
    content = f"# Skills\n\n{skills_table}\n"

    readme_path.write_text(content, encoding="utf-8")
    print(f"✓ Updated {readme_path}")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Update README.md with skills table, optionally filtered by source"
    )
    parser.add_argument(
        "--source",
        default=None,
        help="Source to filter by (e.g., hsiangjenli/skills). If omitted, all skills are included.",
    )
    parser.add_argument(
        "--skills-lock",
        default="skills-lock.json",
        help="Path to skills-lock.json",
    )
    parser.add_argument(
        "--source-dir",
        default="skills",
        help="Source directory path",
    )
    args = parser.parse_args()

    # Get repository root
    repo_root = Path(__file__).parent.parent

    # Paths
    skills_dir = repo_root / args.source_dir
    readme_path = repo_root / "README.md"
    skills_lock_path = repo_root / args.skills_lock

    if not skills_dir.exists():
        print(f"Error: {skills_dir} does not exist")
        return

    allowed_skills = None
    if args.source:
        if not skills_lock_path.exists():
            print(f"Error: {skills_lock_path} does not exist")
            return
        skills_data = load_skills_lock(skills_lock_path)
        skill_names = [path.name for path in skills_dir.iterdir() if path.is_dir()]
        allowed_skills = filter_skills_by_source(skills_data, args.source, skill_names)
        print(
            f"Filtering by source '{args.source}': {len(allowed_skills)} skills matched"
        )

    # Generate and update
    skills_table = generate_skills_table(skills_dir, allowed_skills)
    update_readme(readme_path, skills_table)

    print(f"Found {len(skills_table.split(chr(10))) - 2} skills")


if __name__ == "__main__":
    main()
