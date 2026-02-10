#!/usr/bin/env python3
"""
Update README.md with skills list from .agents/skills directory.
"""

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


def generate_skills_table(skills_dir: Path) -> str:
    """
    Generate markdown table of skills.

    Parameters
    ----------
    skills_dir : Path
        Path to .agents/skills directory

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
    # Get repository root
    repo_root = Path(__file__).parent.parent

    # Paths
    skills_dir = repo_root / ".agents" / "skills"
    readme_path = repo_root / "README.md"

    if not skills_dir.exists():
        print(f"Error: {skills_dir} does not exist")
        return

    # Generate and update
    skills_table = generate_skills_table(skills_dir)
    update_readme(readme_path, skills_table)

    print(f"Found {len(skills_table.split(chr(10))) - 2} skills")


if __name__ == "__main__":
    main()
