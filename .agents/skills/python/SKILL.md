---
name: python
description: Modern Python development workflow using uv for project management, code formatting, docstring generation with numpy style, and code optimization. Use when creating new Python projects, formatting code, optimizing existing Python code, managing dependencies, or setting up development environments.
---

# Python Development with uv

## Overview

This skill provides a complete modern Python development workflow using uv for fast project management, code formatting with ruff, numpy-style docstring generation, and code quality assurance.

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
