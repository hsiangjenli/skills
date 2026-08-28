---
name: python
description: Develop, run, test, and maintain Python projects with uv. Use when executing Python code or managing Python dependencies; do not use for non-Python tasks.
---

# Python Development with uv

Use `uv run` for Python tools and `uv add` or `uv remove` for dependencies.

| Task | Command |
| --- | --- |
| Run a script | `uv run script.py` |
| Run a module | `uv run python -m package.module` |
| Add or remove a dependency | `uv add <package>` / `uv remove <package>` |
| Add a development dependency | `uv add --dev <package>` |
| Local development | `uv sync`; commit intentional `uv.lock` changes. |
| CI | `uv sync --locked` |
| Production image | `uv sync --locked --no-dev --link-mode=copy` |
| Format / check formatting | `uv run ruff format .` / `uv run ruff format . --check` |
| Lint | `uv run ruff check .` |
| Type check | `uv run ty check` |
| Test | `uv run pytest` (full suite in CI); `uv run pytest tests/test_api.py`; `uv run pytest tests/test_api.py::test_login`; `uv run pytest -k "login or signup"` |
| Dependency audit | `uv audit` |
| Docstrings | Use NumPy-style docstrings for public APIs and non-obvious behavior. |

For image builds, copy `pyproject.toml` and `uv.lock` before application source. Use `uv run --with <package> ...` for a one-off dependency.

Add Ruff's `S` security rules; `extend-select` keeps the defaults:

```toml
[tool.ruff.lint]
extend-select = ["S"]
```

Run `uv audit` in CI for dependency changes and on a schedule, not on every commit. Document any security-rule or audit exception.

## Commit hooks

When a repository needs commit-time checks, use `prek`: it is compatible with the existing `.pre-commit-config.yaml` format.

```bash
uv tool install prek
prek install
prek run --all-files
```

Keep hooks fast: run Ruff formatting and linting, plus `ty check` when it is quick enough. Do not add full test suites to every commit; use CI for them.
