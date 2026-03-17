#!/usr/bin/env python3
"""
Sync skills from .agents/skills to skills directory based on source filter.
Only syncs skills that match the specified source in configuration.
"""

import argparse
import json
import shutil
from pathlib import Path


def load_skills_lock(skills_lock_path: str) -> dict:
    """Load skills-lock.json file."""
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


def sync_skills(
    source_dir: Path,
    target_dir: Path,
    skill_names: list[str],
) -> tuple[list[str], list[str]]:
    """
    Sync specified skills from source to target directory.

    Parameters
    ----------
    source_dir : Path
        Source directory path (.agents/skills)
    target_dir : Path
        Target directory path (skills)
    skill_names : list[str]
        List of skill names to sync

    Returns
    -------
    tuple[list[str], list[str]]
        Tuple of (synced_skills, skipped_skills)
    """
    synced = []
    skipped = []

    # Remove old skills directory completely
    if target_dir.exists():
        print(f"Removing old {target_dir} directory...")
        shutil.rmtree(target_dir)

    # Create fresh target directory
    target_dir.mkdir(parents=True, exist_ok=True)

    # Copy filtered skills
    for skill_name in skill_names:
        source_skill_path = source_dir / skill_name
        target_skill_path = target_dir / skill_name

        if source_skill_path.exists():
            shutil.copytree(source_skill_path, target_skill_path)
            synced.append(skill_name)
            print(f"[OK] Synced: {skill_name}")
        else:
            skipped.append(skill_name)
            print(f"[SKIP] Not found: {skill_name}")

    return synced, skipped


def main():
    """Main function to sync skills based on configuration."""
    parser = argparse.ArgumentParser(
        description="Sync skills from source to target directory based on source filter"
    )
    parser.add_argument(
        "--source",
        default="hsiangjenli/skills",
        help="Source to filter by (e.g., hsiangjenli/skills)",
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
    parser.add_argument(
        "--target-dir",
        default="skills",
        help="Target directory path",
    )

    args = parser.parse_args()

    target_source = args.source
    skills_lock_path = args.skills_lock
    source_dir = Path(args.source_dir)
    target_dir = Path(args.target_dir)

    print(f"Filtering skills from source: {target_source}")
    print(f"Source directory: {source_dir}")
    print(f"Target directory: {target_dir}")
    print()

    # Load and filter skills
    skills_data = load_skills_lock(skills_lock_path)
    filtered_skills = filter_skills_by_source(skills_data, target_source)

    print(f"Found {len(filtered_skills)} skills to sync:")
    for skill in filtered_skills:
        print(f"  • {skill}")
    print()

    # Sync skills
    synced, skipped = sync_skills(source_dir, target_dir, filtered_skills)

    # Summary
    print()
    print("=" * 50)
    print(f"Successfully synced: {len(synced)} skills")
    if skipped:
        print(f"Skipped: {len(skipped)} skills")
    print("=" * 50)


if __name__ == "__main__":
    main()
