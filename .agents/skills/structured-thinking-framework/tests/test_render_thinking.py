import json
from pathlib import Path

import pytest

from scripts import render_thinking

ROOT = Path(__file__).parents[1]
EXAMPLES = ROOT / "examples"


def test_render_index_contains_all_frameworks(tmp_path: Path) -> None:
    output = tmp_path / "index.html"

    render_thinking.render_index(output)

    content = output.read_text(encoding="utf-8")
    assert "MECE problem decomposition" in content
    assert "SWOT and scenario analysis" in content
    assert "Prioritization analysis" in content
    assert "1600px" in content


def test_render_result_escapes_user_content_and_applies_theme(tmp_path: Path) -> None:
    source = tmp_path / "input.json"
    source.write_text(
        json.dumps(
            {
                "framework": "mece",
                "title": "Unsafe <script>alert(1)</script>",
                "problem": "A problem",
                "framework_data": {"root_question": "Question"},
                "theme": {"primary": "#123456"},
                "preset": "social-square",
            }
        ),
        encoding="utf-8",
    )
    output = tmp_path / "result.html"

    render_thinking.render_result(source, output)

    content = output.read_text(encoding="utf-8")
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in content
    assert "<script>alert(1)</script>" not in content
    assert "--primary: #123456" in content
    assert "1200px" in content
    assert "Roboto" in content


def test_render_examples(tmp_path: Path) -> None:
    for example in EXAMPLES.glob("*.json"):
        output = tmp_path / f"{example.stem}.html"
        render_thinking.render_result(example, output)
        assert output.exists()
        assert "Framework analysis" in output.read_text(encoding="utf-8")


def test_unknown_framework_fails(tmp_path: Path) -> None:
    source = tmp_path / "input.json"
    source.write_text('{"framework": "unknown"}', encoding="utf-8")

    with pytest.raises(render_thinking.RenderError, match="Unknown framework"):
        render_thinking.render_result(source, tmp_path / "result.html")


def test_invalid_theme_color_fails(tmp_path: Path) -> None:
    source = tmp_path / "input.json"
    source.write_text(
        json.dumps(
            {
                "framework": "mece",
                "theme": {"primary": "blue"},
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(render_thinking.RenderError, match="Invalid HEX color"):
        render_thinking.render_result(source, tmp_path / "result.html")
