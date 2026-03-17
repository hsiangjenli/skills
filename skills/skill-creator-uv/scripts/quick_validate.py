#!/usr/bin/env python3
"""
Skill Validator - Validates skill structure and content.

Usage:
    uv run quick_validate.py <skill-directory>
"""

import sys
import re
import yaml
from pathlib import Path
from typing import Tuple, Dict, Any


class ValidationError(Exception):
    """Skill validation error."""

    pass


class SkillValidator:
    """Validates skill structure and content."""

    ALLOWED_PROPERTIES = {"name", "description", "license", "allowed-tools", "metadata"}

    def validate_skill_file_exists(self, skill_path: Path) -> Path:
        """Check SKILL.md exists and return its path."""
        skill_md = skill_path / "SKILL.md"
        if not skill_md.exists():
            raise ValidationError("SKILL.md not found")
        return skill_md

    def extract_frontmatter(self, content: str) -> Dict[str, Any]:
        """Extract and parse YAML frontmatter."""
        if not content.startswith("---"):
            raise ValidationError("No YAML frontmatter found")

        match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        if not match:
            raise ValidationError("Invalid frontmatter format")

        frontmatter_text = match.group(1)

        try:
            frontmatter = yaml.safe_load(frontmatter_text)
            if not isinstance(frontmatter, dict):
                raise ValidationError("Frontmatter must be a YAML dictionary")
            return frontmatter
        except yaml.YAMLError as e:
            raise ValidationError(f"Invalid YAML in frontmatter: {e}")

    def validate_frontmatter_properties(self, frontmatter: Dict[str, Any]) -> None:
        """Validate frontmatter has required properties and no unexpected ones."""
        # Check for unexpected properties
        unexpected_keys = set(frontmatter.keys()) - self.ALLOWED_PROPERTIES
        if unexpected_keys:
            allowed = ", ".join(sorted(self.ALLOWED_PROPERTIES))
            unexpected = ", ".join(sorted(unexpected_keys))
            raise ValidationError(
                f"Unexpected frontmatter keys: {unexpected}. Allowed: {allowed}"
            )

        # Check required fields
        if "name" not in frontmatter:
            raise ValidationError("Missing 'name' in frontmatter")
        if "description" not in frontmatter:
            raise ValidationError("Missing 'description' in frontmatter")

    def validate_name(self, name: Any) -> None:
        """Validate skill name format."""
        if not isinstance(name, str):
            raise ValidationError(f"Name must be a string, got {type(name).__name__}")

        name = name.strip()
        if not name:
            return

        # Check naming convention
        if not re.match(r"^[a-z0-9-]+$", name):
            raise ValidationError(
                f"Name '{name}' must be lowercase letters, digits, and hyphens only"
            )

        if name.startswith("-") or name.endswith("-") or "--" in name:
            raise ValidationError(
                f"Name '{name}' cannot start/end with hyphen or have consecutive hyphens"
            )

        # Check length
        if len(name) > 64:
            raise ValidationError(f"Name too long ({len(name)} chars). Maximum: 64")

    def validate_description(self, description: Any) -> None:
        """Validate skill description format."""
        if not isinstance(description, str):
            raise ValidationError(
                f"Description must be a string, got {type(description).__name__}"
            )

        description = description.strip()
        if not description:
            return

        # Check for angle brackets
        if "<" in description or ">" in description:
            raise ValidationError("Description cannot contain angle brackets (< or >)")

        # Check length
        if len(description) > 1024:
            raise ValidationError(
                f"Description too long ({len(description)} chars). Maximum: 1024"
            )

    def validate_skill(self, skill_path: Path) -> bool:
        """Validate complete skill structure."""
        try:
            skill_path = Path(skill_path)

            # Check SKILL.md exists
            skill_md = self.validate_skill_file_exists(skill_path)

            # Read and parse content
            content = skill_md.read_text()
            frontmatter = self.extract_frontmatter(content)

            # Validate frontmatter
            self.validate_frontmatter_properties(frontmatter)
            self.validate_name(frontmatter.get("name", ""))
            self.validate_description(frontmatter.get("description", ""))

            return True

        except ValidationError as e:
            print(f"❌ Validation failed: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False


def validate_skill(skill_path: Path) -> Tuple[bool, str]:
    """Validate skill and return result with message."""
    validator = SkillValidator()

    try:
        if validator.validate_skill(skill_path):
            return True, "Skill is valid!"
    except Exception:
        pass

    return False, "Skill validation failed"


def main() -> None:
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: uv run quick_validate.py <skill-directory>")
        sys.exit(1)

    skill_path = Path(sys.argv[1])
    validator = SkillValidator()

    if validator.validate_skill(skill_path):
        print("✅ Skill is valid!")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
