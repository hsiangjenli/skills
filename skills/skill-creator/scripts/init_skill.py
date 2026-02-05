#!/usr/bin/env python3
"""
Skill Initializer - Creates a new skill from template

Usage:
    init_skill.py <skill-name> [--path <path>] [--non-interactive] [--python] [--uv]

Examples:
    init_skill.py my-new-skill                           # Interactive path choice (default: .agents/skills/)
    init_skill.py my-api-helper --path custom/location   # Custom path
    init_skill.py data-processor --non-interactive       # Use default .agents/skills/ without asking
    init_skill.py data-processor --python --uv          # With Python + uv setup
"""

import sys
import shutil
import subprocess
import os
from pathlib import Path
import argparse


def check_dependencies():
    """Check if required dependencies are available."""
    dependencies = {
        "python": "Python is required for skill development",
        "uv": "uv is recommended for Python dependency management. Install from https://docs.astral.sh/uv/",
        "git": "Git is used for version control. Install from https://git-scm.com/",
    }

    available = {}
    for dep, message in dependencies.items():
        try:
            result = subprocess.run(
                [dep, "--version"], capture_output=True, text=True, timeout=5
            )
            available[dep] = result.returncode == 0
            if dep == "uv" and available[dep]:
                print(f"✅ {dep} is available")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            available[dep] = False
            if dep != "uv":  # uv is optional
                print(f"⚠️ {dep} not found: {message}")

    return available


def setup_python_environment(skill_dir, use_uv=False):
    """Setup Python environment for the skill."""
    if use_uv and shutil.which("uv"):
        try:
            # Initialize uv project
            subprocess.run(
                ["uv", "init", "--name", skill_dir.name],
                cwd=skill_dir,
                check=True,
                capture_output=True,
            )
            # Add common dependencies
            common_deps = ["requests", "pathlib"]
            for dep in common_deps:
                subprocess.run(
                    ["uv", "add", dep], cwd=skill_dir, check=True, capture_output=True
                )
            print("✅ Python environment created with uv")
            return True
        except subprocess.CalledProcessError as e:
            print(f"⚠️ uv setup failed: {e}")
            return False
    else:
        print("🐍 uv not available, skipping Python environment setup")
        return False


def create_skill_template(skill_name, skill_title):
    """Create the main SKILL.md template."""
    return f"""---
name: {skill_name}
description: [TODO: Complete and informative explanation of what the skill does and when to use it. Include WHEN to use this skill - specific scenarios, file types, or tasks that trigger it.]
---

# {skill_title}

## Overview

[TODO: 1-2 sentences explaining what this skill enables]

## Structuring This Skill

[TODO: Choose the structure that best fits this skill's purpose. Common patterns:

**1. Workflow-Based** (best for sequential processes)
- Works well when there are clear step-by-step procedures
- Example: DOCX skill with "Workflow Decision Tree" → "Reading" → "Creating" → "Editing"
- Structure: ## Overview → ## Workflow Decision Tree → ## Step 1 → ## Step 2...

**2. Task-Based** (best for tool collections)
- Works well when the skill offers different operations/capabilities
- Example: PDF skill with "Quick Start" → "Merge PDFs" → "Split PDFs" → "Extract Text"
- Structure: ## Overview → ## Quick Start → ## Task Category 1 → ## Task Category 2...

**3. Reference/Guidelines** (best for standards or specifications)
- Works well for brand guidelines, coding standards, or requirements
- Example: Brand styling with "Brand Guidelines" → "Colors" → "Typography" → "Features"
- Structure: ## Overview → ## Guidelines → ## Specifications → ## Usage...

**4. Capabilities-Based** (best for integrated systems)
- Works well when the skill provides multiple interrelated features
- Example: Product Management with "Core Capabilities" → numbered capability list
- Structure: ## Overview → ## Core Capabilities → ### 1. Feature → ### 2. Feature...

Patterns can be mixed and matched as needed. Most skills combine patterns (e.g., start with task-based, add workflow for complex operations).

Delete this entire "Structuring This Skill" section when done - it's just guidance.]

## [TODO: Replace with the first main section based on chosen structure]

[TODO: Add content here. See examples in existing skills:
- Code samples for technical skills
- Decision trees for complex workflows
- Concrete examples with realistic user requests
- References to scripts/templates/references as needed]

## Resources

This skill includes example resource directories that demonstrate how to organize different types of bundled resources:

### scripts/
Executable code (Python/Bash/etc.) that can be run directly to perform specific operations.

**Examples from other skills:**
- PDF skill: `fill_fillable_fields.py`, `extract_form_field_info.py` - utilities for PDF manipulation
- DOCX skill: `document.py`, `utilities.py` - Python modules for document processing

**Appropriate for:** Python scripts, shell scripts, or any executable code that performs automation, data processing, or specific operations.

**Note:** Scripts may be executed without loading into context, but can still be read by Claude for patching or environment adjustments.

### references/
Documentation and reference material intended to be loaded into context to inform Claude's process and thinking.

**Examples from other skills:**
- Product management: `communication.md`, `context_building.md` - detailed workflow guides
- BigQuery: API reference documentation and query examples
- Finance: Schema documentation, company policies

**Appropriate for:** In-depth documentation, API references, database schemas, comprehensive guides, or any detailed information that Claude should reference while working.

### assets/
Files not intended to be loaded into context, but rather used within the output Claude produces.

**Examples from other skills:**
- Brand styling: PowerPoint template files (.pptx), logo files
- Frontend builder: HTML/React boilerplate project directories
- Typography: Font files (.ttf, .woff2)

**Appropriate for:** Templates, boilerplate code, document templates, images, icons, fonts, or any files meant to be copied or used in the final output.

---

**Any unneeded directories can be deleted.** Not every skill requires all three types of resources.
"""


def create_script_template(skill_name, skill_title):
    """Create a helper script template."""
    return f"""#!/usr/bin/env python3
\"\"\"
{skill_title} Helper Script

Utility script for {skill_name} operations.
Replace with actual implementation or delete if not needed.

Usage:
    uv run python {skill_name}_helper.py [options]
    
Examples from other skills:
- Image processing: resize, compress, convert formats
- Data processing: CSV to JSON, API data fetching
- File operations: batch rename, organize, validate
\"\"\"

import argparse
import sys
from pathlib import Path

def process_files(input_path, output_path=None):
    \"\"\"Example function - replace with actual logic.\"\"\"
    input_path = Path(input_path)
    
    if not input_path.exists():
        print(f"❌ Input path does not exist: {{input_path}}")
        return False
        
    print(f"📁 Processing: {{input_path}}")
    
    # TODO: Add your processing logic here
    # Examples:
    # - Process images: resize, compress, convert
    # - Transform data: CSV to JSON, clean data
    # - Generate content: templates, reports, documentation
    
    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"💾 Output will be saved to: {{output_path}}")
    
    print("✅ Processing completed successfully")
    return True

def main():
    parser = argparse.ArgumentParser(
        description="{skill_title} helper script"
    )
    parser.add_argument(
        "input", 
        help="Input file or directory to process"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file or directory (optional)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        print(f"🚀 Starting {skill_name} processing...")
        print(f"📄 Input: {{args.input}}")
        if args.output:
            print(f"💾 Output: {{args.output}}")
    
    success = process_files(args.input, args.output)
    
    if success:
        print("🎉 Task completed successfully!")
        sys.exit(0)
    else:
        print("❌ Task failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
"""


def create_reference_template(skill_title):
    """Create reference documentation template."""
    return f"""# Reference Documentation for {skill_title}

This is a placeholder for detailed reference documentation.
Replace with actual reference content or delete if not needed.

Example real reference docs from other skills:
- product-management/references/communication.md - Comprehensive guide for status updates
- product-management/references/context_building.md - Deep-dive on gathering context
- bigquery/references/ - API references and query examples

## When Reference Docs Are Useful

Reference docs are ideal for:
- Comprehensive API documentation
- Detailed workflow guides
- Complex multi-step processes
- Information too lengthy for main SKILL.md
- Content that's only needed for specific use cases

## Structure Suggestions

### API Reference Example
- Overview
- Authentication
- Endpoints with examples
- Error codes
- Rate limits

### Workflow Guide Example
- Prerequisites
- Step-by-step instructions
- Common patterns
- Troubleshooting
- Best practices
"""


def create_asset_template():
    """Create asset placeholder."""
    return """# Example Asset File

This placeholder represents where asset files would be stored.
Replace with actual asset files (templates, images, fonts, etc.) or delete if not needed.

Asset files are NOT intended to be loaded into context, but rather used within
the output Claude produces.

Example asset files from other skills:
- Brand guidelines: logo.png, slides_template.pptx
- Frontend builder: hello-world/ directory with HTML/React boilerplate
- Typography: custom-font.ttf, font-family.woff2
- Data: sample_data.csv, test_dataset.json

## Common Asset Types

- Templates: .pptx, .docx, boilerplate directories
- Images: .png, .jpg, .svg, .gif
- Fonts: .ttf, .otf, .woff, .woff2
- Boilerplate code: Project directories, starter files
- Icons: .ico, .svg
- Data files: .csv, .json, .xml, .yaml

Note: This is a text placeholder. Actual assets can be any file type.
"""


def title_case_skill_name(skill_name):
    """Convert hyphenated skill name to Title Case for display."""
    return " ".join(word.capitalize() for word in skill_name.split("-"))


def get_user_choice_path(skill_name):
    """
    Ask user for the skill installation path with interactive menu.

    Args:
        skill_name: Name of the skill being created

    Returns:
        Path object for the chosen directory
    """
    current_dir = Path.cwd()
    default_path = current_dir / ".agents" / "skills"

    print(f"\n📁 Where would you like to create the '{skill_name}' skill?")
    print(f"1. Default location: {default_path} (Recommended)")
    print(f"2. Current directory: {current_dir}")
    print(f"3. Custom path")

    while True:
        try:
            choice = input(
                "\nEnter your choice (1-3, or press Enter for default): "
            ).strip()

            if not choice or choice == "1":
                # Default: .agents/skills
                path = default_path
                break
            elif choice == "2":
                # Current directory
                path = current_dir
                break
            elif choice == "3":
                # Custom path
                custom_path = input("Enter custom path: ").strip()
                if custom_path:
                    path = Path(custom_path).expanduser().resolve()
                    # Confirm the custom path
                    print(f"\nUsing custom path: {path}")
                    confirm = input("Is this correct? (y/N): ").strip().lower()
                    if confirm in ("y", "yes"):
                        break
                    else:
                        print("Please choose again.")
                        continue
                else:
                    print("Please enter a valid path.")
                    continue
            else:
                print("Please enter 1, 2, or 3.")
                continue

        except KeyboardInterrupt:
            print("\n\n❌ Operation cancelled by user")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            continue

    return path


def init_skill(
    skill_name, path=None, setup_python=False, use_uv=False, interactive=True
):
    """
    Initialize a new skill directory with template SKILL.md.

    Args:
        skill_name: Name of the skill
        path: Path where the skill directory should be created (default: ask user)
        setup_python: Whether to setup Python environment
        use_uv: Whether to use uv for Python setup
        interactive: Whether to ask user for path choice (default: True)

    Returns:
        Path to created skill directory, or None if error
    """
    # Path handling with user interaction
    if path is None:
        if interactive:
            path = get_user_choice_path(skill_name)
            if path is None:  # User cancelled
                return None
        else:
            # Non-interactive mode: use default .agents/skills
            path = Path.cwd() / ".agents" / "skills"
    else:
        path = Path(path)

    skill_dir = path / skill_name
    skill_title = title_case_skill_name(skill_name)

    # Check if skill already exists
    if skill_dir.exists():
        print(f"❌ Skill already exists: {skill_dir}")
        return None

    try:
        # Create skill directory structure
        skill_dir.mkdir(parents=True)

        # Create SKILL.md
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text(create_skill_template(skill_name, skill_title))

        # Create optional directories with examples
        scripts_dir = skill_dir / "scripts"
        scripts_dir.mkdir(exist_ok=True)

        # Create example script
        example_script = scripts_dir / f"{skill_name}_helper.py"
        example_script.write_text(create_script_template(skill_name, skill_title))
        example_script.chmod(0o755)  # Make executable

        # Create references directory
        references_dir = skill_dir / "references"
        references_dir.mkdir(exist_ok=True)

        # Create example reference
        example_reference = references_dir / "api_reference.md"
        example_reference.write_text(create_reference_template(skill_title))

        # Create assets directory
        assets_dir = skill_dir / "assets"
        assets_dir.mkdir(exist_ok=True)

        # Create example asset placeholder
        example_asset = assets_dir / "README.md"
        example_asset.write_text(create_asset_template())

        print(f"✅ Created skill directory: {skill_dir}")
        print(f"📄 Main file: {skill_md}")
        print(f"🐍 Example script: {example_script}")
        print(f"📚 Reference docs: {example_reference}")
        print(f"🗂️ Assets: {example_asset}")

        # Setup Python environment if requested
        if setup_python or use_uv:
            setup_python_environment(skill_dir, use_uv=use_uv)

        return skill_dir

    except Exception as e:
        print(f"❌ Error creating skill: {e}")
        # Clean up on failure
        if skill_dir.exists():
            shutil.rmtree(skill_dir)
        return None


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Initialize a new skill from template")
    parser.add_argument(
        "skill_name", help="Name of the skill to create (use-hyphen-case)"
    )
    parser.add_argument(
        "--path",
        help="Directory where skill should be created (default: interactive choice)",
    )
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Skip interactive path selection and use default .agents/skills",
    )
    parser.add_argument(
        "--python", action="store_true", help="Setup Python environment"
    )
    parser.add_argument(
        "--uv",
        action="store_true",
        help="Use uv for Python dependency management (implies --python)",
    )

    args = parser.parse_args()

    # Check dependencies
    deps = check_dependencies()

    # If --uv is specified, enable python as well
    if args.uv:
        args.python = True

    # Determine interactive mode
    interactive = not args.non_interactive and args.path is None

    # Create skill
    result = init_skill(
        args.skill_name,
        path=args.path,
        setup_python=args.python,
        use_uv=args.uv,
        interactive=interactive,
    )

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
