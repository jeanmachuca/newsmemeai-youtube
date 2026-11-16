"""SVG rendering tests."""

from __future__ import annotations

from pathlib import Path

from newsmemeai_youtube.render import (
    THUMBNAIL_HEIGHT,
    THUMBNAIL_WIDTH,
    VERTICAL_HEIGHT,
    VERTICAL_WIDTH,
    render_story_frame,
    render_thumbnail,
    wrap_text,
    write_svg,
)


def test_wrap_text_on_words() -> None:
    assert wrap_text("one two three four", max_chars=7) == ["one two", "three", "four"]


def test_wrap_text_preserves_explicit_lines() -> None:
    assert wrap_text("first line\nsecond line", max_chars=20) == ["first line", "second line"]


def test_wrap_text_hard_breaks_long_words() -> None:
    assert wrap_text("abcdefghij", max_chars=4) == ["abcd", "efgh", "ij"]


def test_wrap_text_empty() -> None:
    assert wrap_text("") == []


def test_story_frame_dimensions_and_escaping() -> None:
    svg = render_story_frame(
        kicker="hook",
        title="<script>alert(1)</script>",
        footer="https://example.com/?a=1&b=2",
        index=1,
    )
    assert "<script>" not in svg
    assert "&lt;script&gt;" in svg
    assert "https://example.com/?a=1&amp;b=2" in svg
    assert f'width="{VERTICAL_WIDTH}"' in svg
    assert f'height="{VERTICAL_HEIGHT}"' in svg
    assert "01 / 03" in svg


def test_thumbnail_dimensions_and_text() -> None:
    svg = render_thumbnail(title="A headline & a punchline")
    assert "A headline &amp; a punchline" in svg
    assert f'width="{THUMBNAIL_WIDTH}"' in svg
    assert f'height="{THUMBNAIL_HEIGHT}"' in svg
    assert "NEWS MEME" in svg


def test_write_svg_creates_parent_directory(tmp_path: Path) -> None:
    destination = tmp_path / "nested" / "frame.svg"
    written = write_svg(destination, render_thumbnail(title="TOP"))
    assert written == destination
    assert destination.read_text(encoding="utf-8").startswith("<svg")
