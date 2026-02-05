#!/usr/bin/env python3
"""
Neversink Presentation Setup Script

Creates a new Slidev presentation with Neversink theme setup.
Includes theme installation, basic configuration, and template selection.
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path


def run_command(cmd, cwd=None, check=True):
    """Run shell command and return result."""
    try:
        result = subprocess.run(
            cmd, shell=True, cwd=cwd, capture_output=True, text=True, check=check
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{cmd}': {e}")
        print(f"stderr: {e.stderr}")
        if check:
            sys.exit(1)
        return None


def check_dependencies():
    """Check if required dependencies are available."""
    dependencies = {
        "node": "Node.js is required. Install from https://nodejs.org/",
        "npm": "npm is required (usually comes with Node.js)",
        "uv": "uv is required for Python dependency management. Install from https://docs.astral.sh/uv/getting-started/installation/",
    }

    for cmd, message in dependencies.items():
        if not shutil.which(cmd):
            print(f"❌ {cmd} not found. {message}")
            return False

    print("✅ Dependencies check passed")
    return True


def setup_slidev_project(project_name, template_type="academic"):
    """Create new Slidev project with Neversink theme."""

    if os.path.exists(project_name):
        print(f"❌ Directory '{project_name}' already exists")
        return False

    # Create project directory
    os.makedirs(project_name)
    print(f"📁 Created project directory: {project_name}")

    # Initialize npm project
    print("📦 Initializing npm project...")
    package_json = {
        "name": project_name,
        "private": True,
        "scripts": {
            "build": "slidev build",
            "dev": "slidev --open",
            "export": "slidev export",
        },
        "dependencies": {
            "@slidev/cli": "latest",
            "@slidev/theme-default": "latest",
            "slidev-theme-neversink": "latest",
        },
    }

    with open(f"{project_name}/package.json", "w") as f:
        json.dump(package_json, f, indent=2)

    # Create Python project structure if needed
    python_dir = f"{project_name}/scripts"
    os.makedirs(python_dir, exist_ok=True)

    # Initialize uv project in scripts directory
    print("🐍 Setting up Python environment with uv...")
    run_command("uv init --name presentation-tools", cwd=python_dir, check=False)

    # Install Python dependencies for presentation tools
    python_deps = ["requests", "pillow", "markdown"]
    for dep in python_deps:
        run_command(f"uv add {dep}", cwd=python_dir, check=False)

    # Install Node.js dependencies
    print("⬇️ Installing Slidev and Neversink theme...")
    install_cmd = "npm install"
    result = run_command(install_cmd, cwd=project_name, check=False)

    if result is None:
        print("⚠️ npm install failed, trying with --legacy-peer-deps")
        run_command("npm install --legacy-peer-deps", cwd=project_name)

    # Copy template
    template_files = {
        "academic": "academic-template.md",
        "technical": "technical-template.md",
        "business": "business-template.md",
    }

    if template_type in template_files:
        template_file = template_files[template_type]
        # In a real implementation, you'd copy from the skill's assets directory
        # For now, create a basic template
        create_basic_template(project_name, template_type)
    else:
        create_basic_template(project_name, "default")

    # Create additional files
    create_gitignore(project_name)
    create_readme(project_name, template_type)

    print(f"✅ Neversink presentation '{project_name}' created successfully!")
    print(f"")
    print(f"Next steps:")
    print(f"  cd {project_name}")
    print(f"  npm run dev")
    print(f"")
    print(f"Template type: {template_type}")
    print(f"Edit slides.md to customize your presentation")

    return True


def create_basic_template(project_name, template_type):
    """Create a basic slides.md template."""

    templates = {
        "academic": """---
theme: neversink
colorSchema: auto
title: Research Presentation
---

# Your Research Title

**Your Name**  
_Institution Name_

---
layout: default
---

# Research Question

What is the main question you're investigating?

- Background context
- Why this matters  
- Your hypothesis

---
layout: two-cols-title
columns: is-6
color: navy
---

:: title ::
# Methodology  

:: left ::
### Study Design
- Participants
- Procedure  
- Measures

:: right ::
### Analysis
- Statistical approach
- Expected outcomes
- Limitations

---
layout: section
color: emerald
---

# Results
<hr>
Your key findings

---
layout: end
---

# Thank You

Questions?
""",
        "technical": """---
theme: neversink
colorSchema: auto
title: Technical Presentation
---

# Project Name

**Your Name**  
_Company/Team_

---
layout: side-title
color: dark
align: rm-lm
---

:: title ::
# Problem

:: content ::
What technical challenge are you solving?

- User pain points
- Technical complexity
- Business impact

---
layout: two-cols-title
columns: is-6
color: slate-light
---

:: title ::
# Solution

:: left ::
### Architecture
```python
# Code example
def solve_problem():
    return "elegant_solution"
```

:: right ::  
### Benefits
- Performance improvement
- Scalability gains
- Maintainability

---
layout: default
color: emerald
---

# Results

## Performance Metrics

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Speed | 100ms | 10ms | 10x |
| Memory | 1GB | 100MB | 10x |

---
layout: end
---

# Let's Build Together

Questions? Let's discuss!
""",
        "business": """---
theme: neversink  
colorSchema: auto
title: Business Presentation
---

# Initiative Title

**Presenter Name**  
_Department_

---
layout: side-title
color: navy
align: rm-lm
---

:: title ::
# Executive Summary

:: content ::
## Key Points

- **Objective**: What we're proposing
- **Investment**: Required resources  
- **Timeline**: Implementation schedule
- **ROI**: Expected returns

---
layout: two-cols-title
columns: is-6
color: blue-light
---

:: title ::
# Business Case

:: left ::
### Opportunity
- Market size
- Growth potential
- Competitive position

:: right ::
### Solution
- Our approach
- Key differentiators  
- Success metrics

---
layout: default
color: emerald-light
---

# Financial Analysis

## Investment & Returns

| Year | Investment | Revenue | ROI |
|------|------------|---------|-----|
| 1 | $100K | $150K | 50% |
| 2 | $150K | $300K | 100% |
| 3 | $200K | $500K | 150% |

---
layout: end
---

# Next Steps

Questions & Discussion
""",
        "default": """---
theme: neversink
colorSchema: auto  
title: My Presentation
---

# Welcome to Slidev

Presentation slides for developers

---
layout: default
---

# What is Slidev?

Slidev is a slides maker and presenter designed for developers, consist of the following features

- 📝 **Text-based** - focus on the content with Markdown, and then style them later
- 🎨 **Themable** - theme can be shared and used with npm packages  
- 🧑‍💻 **Developer Friendly** - code highlighting, live coding with autocompletion
- 🤹 **Interactive** - embedding Vue components to enhance your expressions
- 🎥 **Recording** - built-in recording and camera view
- 📤 **Portable** - export into PDF, PNGs, or even a hostable SPA

---
layout: two-cols-title
columns: is-6
color: sky-light
---

:: title ::
# Neversink Features

:: left ::
### Layouts
- Multiple slide layouts
- Two-column layouts  
- Image layouts
- Custom positioning

:: right ::
### Components
- Sticky notes
- Speech bubbles  
- Admonitions
- Interactive elements

---
layout: end
---

# Learn More

[Documentation](https://sli.dev) · [GitHub](https://github.com/slidevjs/slidev)
""",
    }

    template = templates.get(template_type, templates["default"])

    with open(f"{project_name}/slides.md", "w") as f:
        f.write(template)

    print(f"📄 Created slides.md with {template_type} template")


def create_gitignore(project_name):
    """Create .gitignore file."""
    gitignore_content = """# Slidev
dist/
.slidev/

# Dependencies
node_modules/
.pnpm-debug.log*

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
"""

    with open(f"{project_name}/.gitignore", "w") as f:
        f.write(gitignore_content)


def create_readme(project_name, template_type):
    """Create README.md file."""
    readme_content = f"""# {project_name}

A presentation created with Slidev and the Neversink theme.

## Prerequisites

- Node.js and npm for Slidev
- Python and uv for additional tools

## Development

Start the slide show in development mode:

```bash
npm run dev
```

## Build

Build the slide show for production:

```bash
npm run build
```

## Export

Export slides to PDF:

```bash
npm run export
```

## Python Tools

The `scripts/` directory contains Python utilities managed with uv:

```bash
cd scripts
uv run python your_script.py
```

## Template

This presentation uses the **{template_type}** template from Neversink theme.

## Learn More

- [Slidev Documentation](https://sli.dev)
- [Neversink Theme](https://github.com/gureckis/slidev-theme-neversink)
- [uv Documentation](https://docs.astral.sh/uv/)
"""

    with open(f"{project_name}/README.md", "w") as f:
        f.write(readme_content)


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python setup_presentation.py <project-name> [template-type]")
        print("Template types: academic, technical, business")
        sys.exit(1)

    project_name = sys.argv[1]
    template_type = sys.argv[2] if len(sys.argv) > 2 else "academic"

    print("🚀 Setting up Neversink presentation...")
    print(f"Project: {project_name}")
    print(f"Template: {template_type}")
    print()

    if not check_dependencies():
        sys.exit(1)

    if setup_slidev_project(project_name, template_type):
        print("🎉 Setup complete! Happy presenting!")
    else:
        print("❌ Setup failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
