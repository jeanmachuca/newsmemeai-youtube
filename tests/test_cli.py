"""End-to-end CLI tests using local feed fixtures."""

from __future__ import annotations

import json
from pathlib import Path

from newsmemeai_youtube.cli import main

RSS = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Fixture News</title>
    <item>
      <title>Robots learn to garden</title>
      <link>https://example.com/garden</link>
      <pubDate>Mon, 16 Nov 2026 09:00:00 GMT</pubDate>
      <description>Tomatoes are involved.</description>
    </item>
    <item>
      <title>Moon gets a new parking lot</title>
      <link>https://example.com/moon</link>
    </item>
  </channel>
</rss>
"""


def _feed(tmp_path: Path) -> Path:
    feed = tmp_path / "fixture.xml"
    feed.write_text(RSS, encoding="utf-8")
    return feed


def test_headlines_json(tmp_path: Path, capsys) -> None:
    exit_code = main(["headlines", "--feed", str(_feed(tmp_path)), "--json"])
    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert [headline["title"] for headline in payload] == [
        "Robots learn to garden",
        "Moon gets a new parking lot",
    ]


def test_headlines_human_output(tmp_path: Path, capsys) -> None:
    exit_code = main(["headlines", "--feed", str(_feed(tmp_path))])
    assert exit_code == 0
    output = capsys.readouterr().out
    assert "1. Robots learn to garden" in output
    assert "2. Moon gets a new parking lot" in output


def test_build_and_validate(tmp_path: Path, capsys) -> None:
    package = tmp_path / "pkg"
    exit_code = main(
        [
            "build",
            "--feed",
            str(_feed(tmp_path)),
            "--index",
            "2",
            "--no-llm",
            "--out",
            str(package),
            "--json",
        ]
    )
    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["manifest"]["headline"]["title"] == "Moon gets a new parking lot"
    assert (package / "manifest.json").is_file()

    exit_code = main(["validate", str(package)])
    assert exit_code == 0
    assert "OK: 7 files verified" in capsys.readouterr().out


def test_build_human_output(tmp_path: Path, capsys) -> None:
    package = tmp_path / "pkg"
    exit_code = main(["build", "--feed", str(_feed(tmp_path)), "--no-llm", "--out", str(package)])
    assert exit_code == 0
    output = capsys.readouterr().out
    assert f"Wrote package: {package}" in output
    assert "Review required:" in output
    assert "Status: draft (nothing was published)" in output


def test_build_index_out_of_range(tmp_path: Path, capsys) -> None:
    exit_code = main(["build", "--feed", str(_feed(tmp_path)), "--index", "99", "--no-llm"])
    assert exit_code == 1
    assert "out of range" in capsys.readouterr().err


def test_validate_invalid_package(tmp_path: Path, capsys) -> None:
    package = tmp_path / "empty"
    package.mkdir()
    exit_code = main(["validate", str(package)])
    assert exit_code == 1
    assert "INVALID" in capsys.readouterr().err


def test_missing_feed(tmp_path: Path, capsys) -> None:
    exit_code = main(["headlines", "--feed", str(tmp_path / "missing.xml")])
    assert exit_code == 1
    assert "could not read feed" in capsys.readouterr().err
