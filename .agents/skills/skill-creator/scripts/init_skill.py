#!/usr/bin/env python3
"""
Skill Initializer - Creates skills from templates using KISS principles.

Usage:
    uv run init_skill.py <skill-name> [--path <path>] [--non-interactive]

Examples:
    uv run init_skill.py my-new-skill
    uv run init_skill.py my-skill --path ./custom
    uv run init_skill.py my-skill --non-interactive
"""

import sys
from pathlib import Path
import argparse
from typing import Optional


class SkillError(Exception):
    """Skill creation error."""

    pass


class SkillTemplate:
    """Handles skill template generation."""

    def __init__(self):
        """Initialize with template directory path."""
        self.template_dir = Path(__file__).parent.parent / "templates"

    def load_template(self, template_name: str) -> str:
        """Load template from file."""
        template_file = self.template_dir / template_name
        if not template_file.exists():
            raise SkillError(f"Template not found: {template_file}")
        return template_file.read_text()

    def create_skill_markdown(self, skill_name: str) -> str:
        """Generate main SKILL.md content."""
        title = skill_name.replace("-", " ").title()
        template = self.load_template("skill.md.template")
        return template.format(skill_name=skill_name, title=title)

    def create_helper_script(self, skill_name: str) -> str:
        """Generate example helper script."""
        title = skill_name.replace("-", " ").title()
        template = self.load_template("helper_script.py.template")
        return template.format(skill_name=skill_name, title=title)

    def create_reference_doc(self) -> str:
        """Generate reference documentation template."""
        return self.load_template("reference.md.template")

    def create_asset_readme(self) -> str:
        """Generate asset directory explanation."""
        return self.load_template("asset_readme.md.template")

    def create_pyproject_toml(self, skill_name: str) -> str:
        """Generate pyproject.toml for dependency management."""
        template = self.load_template("pyproject.toml.template")
        return template.format(skill_name=skill_name)

    def create_dependency_check_script(self, skill_name: str) -> str:
        """Generate dependency check script."""
        title = skill_name.replace("-", " ").title()
        template = self.load_template("check_dependencies.py.template")
        return template.format(title=title, skill_name=skill_name)


class PathSelector:
    """Handles path selection for skill creation."""

    @staticmethod
    def get_default_path() -> Path:
        """Get default skill creation path."""
        return Path.cwd() / ".agents" / "skills"

    @staticmethod
    def prompt_for_path(skill_name: str) -> Optional[Path]:
        """Prompt user for skill creation path."""
        default_path = PathSelector.get_default_path()
        current_dir = Path.cwd()

        print(f"\n📁 Where to create '{skill_name}' skill?")
        print(f"1. Default: {default_path}")
        print(f"2. Current: {current_dir}")
        print(f"3. Custom path")

        while True:
            try:
                choice = input("\nChoice (1-3, Enter for default): ").strip()

                if not choice or choice == "1":
                    return default_path
                elif choice == "2":
                    return current_dir
                elif choice == "3":
                    custom = input("Enter path: ").strip()
                    if custom:
                        path = Path(custom).expanduser().resolve()
                        return path
                    print("Please enter a valid path.")
                else:
                    print("Please enter 1, 2, or 3.")

            except KeyboardInterrupt:
                print("\n❌ Cancelled")
                return None


class SkillCreator:
    """Creates skill directories and files."""

    def __init__(self, skill_name: str):
        self.skill_name = skill_name
        self.template = SkillTemplate()

    def validate_name(self) -> None:
        """Validate skill name format."""
        if not self.skill_name.replace("-", "").replace("_", "").isalnum():
            raise SkillError(f"Invalid skill name: {self.skill_name}")

        if self.skill_name != self.skill_name.lower():
            raise SkillError(f"Skill name must be lowercase: {self.skill_name}")

    def create_directories(self, skill_dir: Path) -> None:
        """Create skill directory structure."""
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "scripts").mkdir(exist_ok=True)
        (skill_dir / "references").mkdir(exist_ok=True)
        (skill_dir / "assets").mkdir(exist_ok=True)

    def create_files(self, skill_dir: Path) -> None:
        """Create skill files."""
        # Main skill file
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text(self.template.create_skill_markdown(self.skill_name))

        # Python project configuration
        pyproject_file = skill_dir / "pyproject.toml"
        pyproject_file.write_text(self.template.create_pyproject_toml(self.skill_name))

        # Dependency check script
        deps_script = skill_dir / "scripts" / "check_dependencies.py"
        deps_script.write_text(
            self.template.create_dependency_check_script(self.skill_name)
        )
        deps_script.chmod(0o755)

        # Example helper script
        script_file = skill_dir / "scripts" / f"{self.skill_name}_helper.py"
        script_file.write_text(self.template.create_helper_script(self.skill_name))
        script_file.chmod(0o755)

        # Reference documentation
        ref_file = skill_dir / "references" / "api_reference.md"
        ref_file.write_text(self.template.create_reference_doc())

        # Asset readme
        asset_readme = skill_dir / "assets" / "README.md"
        asset_readme.write_text(self.template.create_asset_readme())

    def create_skill(self, base_path: Path) -> Path:
        """Create complete skill structure."""
        self.validate_name()

        skill_dir = base_path / self.skill_name

        if skill_dir.exists():
            raise SkillError(f"Skill already exists: {skill_dir}")

        try:
            self.create_directories(skill_dir)
            self.create_files(skill_dir)
            return skill_dir
        except Exception as e:
            # Cleanup on failure
            if skill_dir.exists():
                import shutil

                shutil.rmtree(skill_dir)
            raise SkillError(f"Failed to create skill: {e}")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Initialize a new skill")
    parser.add_argument("skill_name", help="Name of skill (use-hyphen-case)")
    parser.add_argument("--path", help="Custom creation path")
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Use default path without prompting",
    )

    args = parser.parse_args()

    try:
        # Determine path
        if args.path:
            base_path = Path(args.path)
        elif args.non_interactive:
            base_path = PathSelector.get_default_path()
        else:
            base_path = PathSelector.prompt_for_path(args.skill_name)
            if base_path is None:
                sys.exit(1)

        # Create skill
        creator = SkillCreator(args.skill_name)
        skill_dir = creator.create_skill(base_path)

        print(f"✅ Created skill at: {skill_dir}")
        print(f"📄 Edit: {skill_dir / 'SKILL.md'}")

    except SkillError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Cancelled")
        sys.exit(1)


if __name__ == "__main__":
    main()
