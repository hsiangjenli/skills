import argparse
import shutil
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent


def main() -> None:
    parser = argparse.ArgumentParser(description="Check or install skill dependencies.")
    parser.add_argument("--install", action="store_true", help="Install dependencies with uv sync")
    args = parser.parse_args()

    if shutil.which("uv") is None:
        print("uv not found. Install it first: curl -LsSf https://astral.sh/uv/install.sh | sh")
        sys.exit(1)

    command = ["uv", "sync"] if args.install else ["uv", "sync", "--check"]
    result = subprocess.run(command, cwd=SKILL_DIR)
    if result.returncode != 0:
        print("Dependencies are not satisfied. Run with --install.")
        sys.exit(result.returncode)
    print("Dependencies are satisfied.")


if __name__ == "__main__":
    main()
