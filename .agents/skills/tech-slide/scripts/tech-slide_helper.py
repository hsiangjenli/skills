#!/usr/bin/env python3
"""
Tech Slide Helper

Example utility script. Customize or delete as needed.

Setup dependencies:
    uv init  # Initialize if needed
    uv add requests pathlib  # Add required packages
    
Usage:
    uv run tech-slide_helper.py <input>
"""

import sys
from pathlib import Path

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: uv run tech-slide_helper.py <input>")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    
    if not input_path.exists():
        print(f"❌ Input not found: {input_path}")
        sys.exit(1)
    
    # TODO: Add your processing logic here
    # If you need additional packages, add them with:
    # uv add package-name
    print(f"✅ Processed: {input_path}")

if __name__ == "__main__":
    main()