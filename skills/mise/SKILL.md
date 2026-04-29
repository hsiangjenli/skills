---
name: mise
description: Use mise as the default workflow for installing programming language runtimes, CLIs, and switching tool versions. Trigger this whenever the user needs a new development environment, hits a version mismatch, wants to align local and global toolchains, or asks how to install a language or CLI without using nvm, pyenv, asdf, brew-only flows, or ad-hoc installers.
---

# Mise Environment Management

Use this skill whenever a task involves installing or switching versions of developer tools. Prefer `mise` unless the user explicitly requires another manager or the tool is not supported by mise.

## Core Rules

1. Prefer `mise` over tool-specific managers such as `nvm`, `pyenv`, `rbenv`, `sdkman`, or manual tarball installers.
2. When a command fails because of a version mismatch, treat the runtime or CLI version as part of the root cause and fix it with `mise`.
3. For Python workflows, use `mise` to choose the Python version but use `uv run ...` to execute Python commands whenever the project uses `uv`.
4. Prefer project-local versions for repository work and global versions for workstation defaults.
5. If `mise` is not activated in the shell, use `mise exec ... -- <command>` for one-off runs instead of assuming the PATH is already correct.
6. When a language or CLI is not already covered by local examples, check the official docs at https://mise.jdx.dev/getting-started.html and the registry/backends pages before falling back to another installer.

## Default Workflow

### 1. Verify `mise`

```bash
mise --version
mise doctor
```

If `mise` is not installed yet, use:

```bash
curl https://mise.run | sh
~/.local/bin/mise --version
```

If shell activation is needed for interactive use, add the snippet to the shell rc file and restart the shell:

```bash
# zsh
echo 'eval "$(~/.local/bin/mise activate zsh)"' >> ~/.zshrc

# bash
echo 'eval "$(~/.local/bin/mise activate bash)"' >> ~/.bashrc
```

Without activation, use `mise exec -- <command>` for every invocation or prefix all commands with `~/.local/bin/mise exec --`.

### 2. Decide scope

Use global scope for machine-wide defaults:

```bash
mise use --global node@22
```

Use local scope for a repository or project:

```bash
mise use node@22
mise install
```

This writes the tool version to the local `mise.toml` or the global config and makes the version choice explicit.

### 3. Run with the correct version

For one-off commands or shells that are not activated:

```bash
mise exec node@22 -- node -v
mise exec python@3.12 -- uv run python --version
```

For an already configured project:

```bash
mise exec -- node -v
mise exec -- uv run python --version
```

If the repository already uses `uv`, prefer `uv run pytest`, `uv run python -m ...`, and similar forms over raw `python` execution.

## Common Tasks

### Install a runtime or language

Check available versions first when precision matters:

```bash
mise latest node
mise latest bun
mise ls-remote python
```

Install globally:

```bash
mise use --global java@openjdk-21
mise use --global rust@latest
mise use --global bun@1.3.13
mise use --global node@22
```

After installation, verify with the real executable:

```bash
java --version
rustc --version
bun --version
node --version
which node
```

Rust may still resolve to binaries under `.cargo/bin`; that is expected for the Rust toolchain.

#### macOS: Java system integration (optional)

After installing Java, mise may suggest creating a symlink so that IDEs and `/usr/libexec/java_home` can discover the JDK:

```bash
sudo mkdir /Library/Java/JavaVirtualMachines/openjdk-21.0.2.jdk
sudo ln -s ~/.local/share/mise/installs/java/openjdk-21.0.2/Contents \
  /Library/Java/JavaVirtualMachines/openjdk-21.0.2.jdk/Contents
```

This is optional for command-line use but required for tools that rely on the system Java registry.

### Fix a version mismatch

When a project expects a different version than the current shell:

1. Identify the required version from the error, project files, CI config, or lockfiles.
2. Set the version with `mise use <tool>@<version>` inside the repository.
3. Run `mise install` if the tool is not already installed.
4. Re-run the failing command through `mise exec -- ...` if shell activation is uncertain.

Example:

```bash
mise use python@3.12
mise install
mise exec -- uv run python -m pytest
```

If the shell is already activated and the repository is using `uv`, the equivalent command is:

```bash
uv run python -m pytest
```

### Python-specific rule

For Python projects:

1. Use `mise` to pin the interpreter version.
2. Use `uv` to create and run the Python environment.
3. Prefer `uv run <command>` over calling `python`, `pip`, or `pytest` directly.
4. If packages need to be added, prefer `uv add` or the repository's existing `uv` workflow.

Example:

```bash
mise use python@3.12
mise install
uv run python --version
uv run pytest
```

### Install CLIs from non-core backends

Use the backend prefix when the tool is distributed through npm, pipx, GitHub releases, aqua, or another backend.

```bash
mise use --global npm:@anthropic-ai/claude-code
mise use --global pipx:black
mise use --global github:BurntSushi/ripgrep
```

If you are not sure which backend to use, check the mise docs and registry before proposing another installer.

## Troubleshooting

### `mise` command not found

Use the full path first:

```bash
~/.local/bin/mise --version
```

Then configure shell activation or PATH according to the official docs.

### Version still looks wrong

Run these checks:

```bash
mise current
mise which node
which node
mise exec -- node -v
```

If `which` and `mise which` disagree, the shell likely is not activated or another manager is earlier on `PATH`.

For Python, also verify through `uv`:

```bash
mise which python
uv run python --version
uv run which python
```

### Project config trust prompt

If a checked-in `mise.toml` prompts for trust, review it and then run:

```bash
mise trust
```

## Decision Guide

- Use `mise use --global ...` for personal machine defaults.
- Use `mise use ...` in a project when the repo needs a pinned version.
- Use `mise exec ... -- ...` for one-off commands, CI-like execution, or when PATH setup is uncertain.
- For Python projects that use `uv`, run Python commands with `uv run ...` after selecting the interpreter version with `mise`.
- Use `mise install` after editing or creating `mise.toml` manually.
- Use the official docs when a language, backend, activation flow, or plugin behavior is unclear.

## Response Pattern

When helping a user, prefer this order:

1. Confirm whether the need is install, upgrade, downgrade, or version alignment.
2. Choose global or local scope.
3. Use `mise` commands to install or switch versions.
4. For Python, route execution through `uv run ...` after the version is pinned.
5. Verify the active version with the real executable.
6. Re-run the original command with `mise exec -- ...` if activation is uncertain.

## Official References

- Getting started: https://mise.jdx.dev/getting-started.html
- Registry: https://mise.jdx.dev/registry.html
- Backends: https://mise.jdx.dev/dev-tools/backends/
- Tool versions index: https://mise-versions.jdx.dev/