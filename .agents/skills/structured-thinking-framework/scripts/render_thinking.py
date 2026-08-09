#!/usr/bin/env python3
"""Render structured thinking JSON as an HTML index or analysis page."""

from __future__ import annotations

import argparse
import json
import re
import sys
from html import escape
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "references" / "framework-index.json"
TEMPLATE_PATH = ROOT / "assets" / "templates"
STYLESHEET_PATH = ROOT / "assets" / "styles" / "theme.css"
DEFAULT_THEME = {
    "primary": "#2563eb",
    "secondary": "#0f172a",
    "accent": "#f59e0b",
    "text": "#172033",
    "muted": "#64748b",
    "background": "#f8fafc",
    "surface": "#ffffff",
    "border": "#dbe3ef",
}
PRESETS = {
    "web-16x9": (1600, 900, "Web 16:9"),
    "presentation-16x9": (1920, 1080, "Presentation 16:9"),
    "social-square": (1200, 1200, "Social square"),
}
HEX_COLOR = re.compile(r"^#[0-9a-fA-F]{6}$")


class RenderError(ValueError):
    """Raised when input cannot be rendered safely."""


def load_json(path: Path) -> dict[str, Any]:
    """Load a JSON object from a file."""
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RenderError(f"Unable to read JSON input: {path}: {error}") from error
    if not isinstance(value, dict):
        raise RenderError(f"JSON input must be an object: {path}")
    return value


def load_registry() -> dict[str, Any]:
    """Load the framework registry."""
    return load_json(REGISTRY_PATH)


def find_framework(registry: dict[str, Any], framework_id: str) -> dict[str, Any]:
    """Find a framework by identifier."""
    for framework in registry.get("frameworks", []):
        if framework.get("id") == framework_id:
            return framework
    raise RenderError(f"Unknown framework: {framework_id}")


def resolve_theme(data: dict[str, Any]) -> dict[str, str]:
    """Validate and merge the requested theme with defaults."""
    theme = dict(DEFAULT_THEME)
    supplied = data.get("theme", {})
    if not isinstance(supplied, dict):
        raise RenderError("theme must be a JSON object")
    for name, value in supplied.items():
        if name not in theme:
            raise RenderError(f"Unknown theme color: {name}")
        if not isinstance(value, str) or not HEX_COLOR.fullmatch(value):
            raise RenderError(f"Invalid HEX color for theme.{name}: {value!r}")
        theme[name] = value
    return theme


def resolve_preset(data: dict[str, Any]) -> tuple[int, int, str]:
    """Resolve a named canvas preset."""
    preset = data.get("preset", "web-16x9")
    if preset not in PRESETS:
        valid = ", ".join(PRESETS)
        raise RenderError(f"Unknown preset: {preset!r}. Choose one of: {valid}")
    return PRESETS[preset]


def theme_css(theme: dict[str, str], width: int, height: int) -> str:
    """Build CSS variable overrides for the selected theme and canvas."""
    variables = [f"--{name}: {value};" for name, value in theme.items()]
    variables.extend([f"--canvas-width: {width}px;", f"--canvas-height: {height}px;"])
    return ":root { " + " ".join(variables) + " }"


def render_template(template_name: str, values: dict[str, str]) -> str:
    """Replace simple template placeholders."""
    template = (TEMPLATE_PATH / template_name).read_text(encoding="utf-8")
    for key, value in values.items():
        template = template.replace("{{ " + key + " }}", value)
    return template


def html_list(values: Any) -> str:
    """Render a safe HTML list from strings or simple objects."""
    if not isinstance(values, list) or not values:
        return '<p class="meta">None provided.</p>'
    items = []
    for value in values:
        if isinstance(value, dict):
            text = str(
                value.get(
                    "text", value.get("name", json.dumps(value, ensure_ascii=False))
                )
            )
            label = value.get("evidence_type")
            if label:
                text = f"[{label}] {text}"
        else:
            text = str(value)
        items.append(f"<li>{escape(text)}</li>")
    return '<ul class="list">' + "".join(items) + "</ul>"


def common_sections(data: dict[str, Any]) -> str:
    """Render sections shared by every framework."""
    sections = []
    for title, key in [
        ("Problem", "problem"),
        ("Objective", "objective"),
        ("Facts and evidence", "facts"),
        ("Assumptions", "assumptions"),
        ("Constraints", "constraints"),
        ("Risks and counterarguments", "risks"),
        ("Open questions", "open_questions"),
        ("Next actions", "next_actions"),
    ]:
        value = data.get(key)
        if not value:
            continue
        content = escape(str(value)) if isinstance(value, str) else html_list(value)
        sections.append(f'<section class="section"><h2>{title}</h2>{content}</section>')
    return "".join(sections)


def framework_sections(data: dict[str, Any]) -> str:
    """Render framework-specific data as readable cards."""
    framework_data = data.get("framework_data", {})
    if not isinstance(framework_data, dict):
        raise RenderError("framework_data must be a JSON object")
    blocks = []
    for key, value in framework_data.items():
        title = escape(key.replace("_", " ").title())
        if isinstance(value, list):
            content = html_list(value)
        elif isinstance(value, dict):
            content = html_list([f"{name}: {item}" for name, item in value.items()])
        else:
            content = f"<p>{escape(str(value))}</p>"
        blocks.append(f'<article class="card"><h2>{title}</h2>{content}</article>')
    if not blocks:
        return '<p class="meta">No framework-specific analysis supplied.</p>'
    return '<div class="grid">' + "".join(blocks) + "</div>"


def render_index(output: Path) -> None:
    """Render the framework registry index."""
    registry = load_registry()
    cards = []
    for framework in registry.get("frameworks", []):
        keywords = "".join(
            f'<span class="pill">{escape(str(word))}</span>'
            for word in framework.get("keywords", [])
        )
        cards.append(
            '<article class="card">'
            f"<h2>{escape(str(framework['name']))}</h2>"
            f"<p>{escape(str(framework['summary']))}</p>"
            f'<p class="meta">Use for: {escape(", ".join(framework.get("problem_types", [])))}</p>'
            f"<div>{keywords}</div>"
            "</article>"
        )
    width, height, _ = PRESETS["web-16x9"]
    result = render_template(
        "index.html",
        {
            "title": "Choose a thinking framework",
            "stylesheet": "",
            "theme_css": STYLESHEET_PATH.read_text(encoding="utf-8")
            + theme_css(DEFAULT_THEME, width, height),
            "framework_cards": "".join(cards),
        },
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(result, encoding="utf-8")


def render_result(input_path: Path, output: Path) -> None:
    """Render one structured thinking result."""
    data = load_json(input_path)
    registry = load_registry()
    framework_id = data.get("framework")
    if not isinstance(framework_id, str):
        raise RenderError("framework is required and must be a string")
    framework = find_framework(registry, framework_id)
    width, height, preset_name = resolve_preset(data)
    result = render_template(
        "framework.html",
        {
            "title": escape(str(data.get("title", framework["name"]))),
            "framework_name": escape(str(framework["name"])),
            "preset_name": escape(preset_name),
            "canvas_width": str(width),
            "canvas_height": str(height),
            "stylesheet": "",
            "theme_css": STYLESHEET_PATH.read_text(encoding="utf-8")
            + theme_css(resolve_theme(data), width, height),
            "common_sections": common_sections(data),
            "framework_sections": framework_sections(data),
        },
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(result, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    index_parser = subparsers.add_parser("index", help="Render the framework index")
    index_parser.add_argument("--output", type=Path, required=True)
    render_parser = subparsers.add_parser("render", help="Render a thinking result")
    render_parser.add_argument("--input", type=Path, required=True)
    render_parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    """Run the renderer and report user-facing errors."""
    arguments = parse_args()
    try:
        if arguments.command == "index":
            render_index(arguments.output)
        else:
            render_result(arguments.input, arguments.output)
    except RenderError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    except OSError as error:
        print(f"Error writing output: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
