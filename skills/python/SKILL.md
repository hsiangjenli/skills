---
name: python
description: Modern Python development workflow where ALL Python execution goes through uv run — never call python, pip, or pytest directly. Use this skill whenever the user writes, runs, formats, tests, or packages Python code, sets up a Python project, or asks how to execute any Python script or command. Always enforce uv run for execution and uv add/remove for dependency management.
---

# Python Development with uv

## Non-Negotiable Rule

Never call `python`, `pip`, `pytest`, `ruff`, or `mypy` directly. Always prefix with `uv run`.

| Wrong | Correct |
|-------|---------|
| `python script.py` | `uv run python script.py` |
| `python -m pytest` | `uv run pytest` |
| `pip install requests` | `uv add requests` |
| `pytest` | `uv run pytest` |
| `ruff format .` | `uv run ruff format .` |
| `mypy src/` | `uv run mypy src/` |

## Overview

This skill provides a complete modern Python development workflow using uv. Every Python command runs through `uv run`; every package change goes through `uv add` or `uv remove`.

## Project Initialization

### Create New Project
```bash
uv init my-project
cd my-project
```

### Enhanced Project Setup
```bash
# Initialize with specific Python version
uv init my-project --python 3.11

# Create library structure
uv init my-library --lib

# Add common development dependencies
uv add --dev pytest ruff mypy black coverage pre-commit

# Add production dependencies
uv add requests pandas fastapi
```

## Code Quality Workflow

### 1. Code Formatting
```bash
# Format all code (replaces black)
uv run ruff format .

# Check formatting without changes
uv run ruff format . --check

# Sort imports
uv run ruff check . --select I --fix
```

### 2. Code Linting and Quality
```bash
# Run all linting checks
uv run ruff check .

# Auto-fix issues where possible
uv run ruff check . --fix

# Check specific rules (e.g., imports)
uv run ruff check . --select I,E,W,F
```

### 3. Type Checking
```bash
# Run type checking
uv run mypy src/

# Type check with specific config
uv run mypy . --strict
```

### 4. Testing
```bash
# Run tests
uv run pytest

# Run with coverage
uv run coverage run -m pytest
uv run coverage report
uv run coverage html
```

## Documentation with Numpy Style

### Docstring Format
Use numpy-style docstrings for all functions and classes:

```python
def process_data(data: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
    """
    Process dataframe by filtering and transforming values.
    
    Parameters
    ----------
    data : pd.DataFrame
        Input dataframe to process
    threshold : float, default 0.5
        Filtering threshold value
        
    Returns
    -------
    pd.DataFrame
        Processed dataframe
        
    Examples
    --------
    >>> df = pd.DataFrame({'values': [0.1, 0.7, 0.3]})
    >>> result = process_data(df, threshold=0.4)
    >>> len(result)
    2
    """
```

### Class Documentation
```python
class DataProcessor:
    """
    Data processing utility class.
    
    Provides methods for cleaning, transforming, and analyzing
    pandas DataFrames with configurable parameters.
    
    Parameters
    ----------
    config : dict
        Configuration parameters for processing
        
    Attributes
    ----------
    threshold : float
        Processing threshold value
    processed_count : int
        Number of processed items
        
    Examples
    --------
    >>> processor = DataProcessor({'threshold': 0.5})
    >>> result = processor.process(data)
    """
```

## Project Configuration

## Complete Development Workflow

### Daily Workflow Commands
```bash
# 1. Start development
uv sync  # Install/update dependencies

# 2. During development
uv run ruff format .          # Format code
uv run ruff check . --fix     # Fix linting issues
uv run mypy src/              # Type check

# 3. Before commit
uv run pytest                 # Run tests
uv run coverage run -m pytest && uv run coverage report

# 4. Run application
uv run -m mymodule
uv run src/main.py
```

### Project Structure Best Practices
```
my-project/
├── pyproject.toml
├── README.md  
├── .gitignore
├── src/
│   └── my_project/
│       ├── __init__.py
│       ├── main.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
└── docs/
    └── README.md
```

## uv Command Reference

### Package Management
```bash
# Add dependencies
uv add package-name
uv add --dev dev-package

# Remove packages  
uv remove package-name

# Update dependencies
uv sync --upgrade

# Show dependency tree
uv tree
```

### Environment Management
```bash
# Create virtual environment
uv venv

# Activate environment
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Run in environment
uv run script.py
uv run pytest
```

### Code Quality Integration
```bash
# One-command quality check
uv run ruff format . && uv run ruff check . --fix && uv run mypy src/ && uv run pytest
```

## Executing Python Code

Always use `uv run` to execute Python scripts, modules, and REPL:

```bash
# Run a script
uv run script.py
uv run src/main.py

# Run a module
uv run python -m mymodule

# Pass arguments
uv run script.py --input data.csv

# One-off execution without changing project deps
uv run --with httpx python fetch.py
```

Never use bare `python script.py` — this bypasses the project environment managed by uv.

## Common Patterns

### Fast Project Setup
```bash
uv init my-app --python 3.11
cd my-app
uv add --dev pytest ruff mypy coverage
uv add requests fastapi uvicorn
echo "pytest\nruff\ncoverage" > requirements-dev.txt
```

### Pre-commit Integration
```bash
# Install pre-commit
uv add --dev pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
EOF

# Install hooks
uv run pre-commit install
```
