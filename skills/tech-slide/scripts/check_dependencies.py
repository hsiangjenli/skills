#!/usr/bin/env python3
"""
Dependency Check Script for Tech Slide Skill

This script checks and installs required dependencies.
Run this before using any Python scripts in this skill.

Usage:
    uv run scripts/check_dependencies.py
    uv run scripts/check_dependencies.py --install
"""

import sys
import subprocess
from pathlib import Path


def check_uv_available():
    """Check if uv is available."""
    try:
        subprocess.run(["uv", "--version"], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def check_dependencies():
    """Check if dependencies are satisfied."""
    skill_dir = Path(__file__).parent.parent
    pyproject_file = skill_dir / "pyproject.toml"

    if not pyproject_file.exists():
        print("❌ No pyproject.toml found")
        return False

    if not check_uv_available():
        print("❌ uv not found. Please install uv first:")
        print("   curl -LsSf https://astral.sh/uv/install.sh | sh")
        return False

    try:
        # Check if dependencies are installed
        result = subprocess.run(
            ["uv", "sync", "--check"], cwd=skill_dir, capture_output=True, text=True
        )

        if result.returncode == 0:
            print("✅ All dependencies are satisfied")
            return True
        else:
            print("⚠️ Dependencies need to be installed")
            return False

    except subprocess.CalledProcessError as e:
        print(f"❌ Error checking dependencies: {e}")
        return False


def install_dependencies():
    """Install dependencies using uv."""
    skill_dir = Path(__file__).parent.parent

    try:
        print("📦 Installing dependencies...")
        result = subprocess.run(["uv", "sync"], cwd=skill_dir, check=True)
        print("✅ Dependencies installed successfully")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Check and install skill dependencies")
    parser.add_argument(
        "--install", action="store_true", help="Install dependencies if missing"
    )

    args = parser.parse_args()

    # Check dependencies
    deps_ok = check_dependencies()

    if not deps_ok and args.install:
        success = install_dependencies()
        if not success:
            sys.exit(1)
    elif not deps_ok:
        print("\n💡 Run with --install to install dependencies:")
        print(f"   uv run scripts/check_dependencies.py --install")
        sys.exit(1)

    print("\n🎉 Ready to use Tech Slide skill!")


if __name__ == "__main__":
    main()
