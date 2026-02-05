#!/usr/bin/env python3
"""
Skill Packager - Creates distributable .skill files.

Usage:
    uv run package_skill.py <skill-folder> [output-directory]

Examples:
    uv run package_skill.py my-skill
    uv run package_skill.py my-skill ./dist
"""

import sys
import zipfile
from pathlib import Path
from typing import Optional

from quick_validate import SkillValidator


class PackageError(Exception):
    """Package creation error."""

    pass


class SkillPackager:
    """Handles skill packaging operations."""

    def __init__(self):
        self.validator = SkillValidator()

    def validate_skill_path(self, skill_path: Path) -> None:
        """Validate skill directory exists and has required files."""
        if not skill_path.exists():
            raise PackageError(f"Skill folder not found: {skill_path}")

        if not skill_path.is_dir():
            raise PackageError(f"Path is not a directory: {skill_path}")

        skill_md = skill_path / "SKILL.md"
        if not skill_md.exists():
            raise PackageError(f"SKILL.md not found in {skill_path}")

    def create_package(
        self, skill_path: Path, output_dir: Optional[Path] = None
    ) -> Path:
        """Create .skill package from skill directory."""
        skill_path = skill_path.resolve()
        self.validate_skill_path(skill_path)

        # Validate skill before packaging
        print("🔍 Validating skill...")
        if not self.validator.validate_skill(skill_path):
            raise PackageError("Skill validation failed")
        print("✅ Validation passed")

        # Determine output path
        if output_dir:
            output_path = output_dir.resolve()
            output_path.mkdir(parents=True, exist_ok=True)
        else:
            output_path = Path.cwd()

        skill_filename = output_path / f"{skill_path.name}.skill"

        # Create package
        try:
            with zipfile.ZipFile(skill_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
                for file_path in skill_path.rglob("*"):
                    if file_path.is_file():
                        arcname = file_path.relative_to(skill_path.parent)
                        zipf.write(file_path, arcname)
                        print(f"  Added: {arcname}")

            return skill_filename

        except Exception as e:
            raise PackageError(f"Failed to create package: {e}")


def main() -> None:
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: uv run package_skill.py <skill-folder> [output-directory]")
        print("\nExamples:")
        print("  uv run package_skill.py my-skill")
        print("  uv run package_skill.py my-skill ./dist")
        sys.exit(1)

    skill_path = Path(sys.argv[1])
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else None

    try:
        packager = SkillPackager()

        print(f"📦 Packaging skill: {skill_path}")
        if output_dir:
            print(f"   Output directory: {output_dir}")
        print()

        package_file = packager.create_package(skill_path, output_dir)
        print(f"\n✅ Successfully packaged: {package_file}")

    except PackageError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Cancelled")
        sys.exit(1)


if __name__ == "__main__":
    main()
