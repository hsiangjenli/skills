#!/usr/bin/env python3
"""
Dependency check script for the ICS Manager skill.

Usage
-----
uv run scripts/check_dependencies.py
uv run scripts/check_dependencies.py --install
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def check_uv_available() -> bool:
    """Return True when uv is available."""
    try:
        subprocess.run(["uv", "--version"], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False
    return True


def check_dependencies() -> bool:
    """Return True when the skill dependencies are already installed."""
    skill_dir = Path(__file__).resolve().parent.parent
    pyproject_file = skill_dir / "pyproject.toml"

    if not pyproject_file.exists():
        print("No pyproject.toml found.")
        return False

    if not check_uv_available():
        print("uv not found. Install uv before using this skill.")
        return False

    result = subprocess.run(
        ["uv", "sync", "--check"],
        cwd=skill_dir,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode == 0:
        print("Dependencies are satisfied.")
        return True

    print("Dependencies need to be installed.")
    return False


def install_dependencies() -> bool:
    """Install dependencies with uv sync."""
    skill_dir = Path(__file__).resolve().parent.parent
    result = subprocess.run(["uv", "sync"], cwd=skill_dir, check=False)
    if result.returncode == 0:
        print("Dependencies installed successfully.")
        return True
    print("Failed to install dependencies.")
    return False


def main() -> None:
    """Entry point for dependency checking."""
    parser = argparse.ArgumentParser(description="Check ICS Manager dependencies")
    parser.add_argument(
        "--install",
        action="store_true",
        help="Install dependencies when they are missing.",
    )
    args = parser.parse_args()

    dependencies_ok = check_dependencies()

    if dependencies_ok:
        print("ICS Manager is ready to use.")
        return

    if args.install:
        if install_dependencies():
            print("ICS Manager is ready to use.")
            return
        sys.exit(1)

    print("Run 'uv run scripts/check_dependencies.py --install' to install them.")
    sys.exit(1)


if __name__ == "__main__":
    main()
