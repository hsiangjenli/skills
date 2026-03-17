#!/usr/bin/env python3
"""
Update README.md with skills list from .agents/skills directory.
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


def filter_skills_by_source(skills_data: dict, target_source: str) -> list[str]:
    """
    Filter skills by source.

    Parameters
    ----------
    skills_data : dict
        The skills dictionary from skills-lock.json
    target_source : str
        The source to filter by (e.g., "hsiangjenli/skills")

    Returns
    -------
    list[str]
        List of skill names that match the target source
    """
    filtered_skills = []
    skills = skills_data.get("skills", {})

    for skill_name, skill_info in skills.items():
        if skill_info.get("source") == target_source:
            filtered_skills.append(skill_name)

    return filtered_skills


def generate_skills_table(
    skills_dir: Path, allowed_skills: list[str] | None = None
) -> str:
    """
    Generate markdown table of skills.

    Parameters
    ----------
    skills_dir : Path
        Path to .agents/skills directory
    allowed_skills : list[str] | None
        If provided, only include skills whose directory name is in this list.

    Returns
    -------
    str
        Markdown table content
    """
    skills = []

    # Scan all subdirectories in .agents/skills
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
        default=".agents/skills",
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

    # Optionally filter by source
    allowed_skills = None
    if args.source:
        if not skills_lock_path.exists():
            print(f"Error: {skills_lock_path} does not exist")
            return
        skills_data = load_skills_lock(skills_lock_path)
        allowed_skills = filter_skills_by_source(skills_data, args.source)
        print(
            f"Filtering by source '{args.source}': {len(allowed_skills)} skills matched"
        )

    # Generate and update
    skills_table = generate_skills_table(skills_dir, allowed_skills)
    update_readme(readme_path, skills_table)

    print(f"Found {len(skills_table.split(chr(10))) - 2} skills")


if __name__ == "__main__":
    main()
