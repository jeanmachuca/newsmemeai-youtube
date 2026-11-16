"""Package assembly tests."""

from __future__ import annotations

import json
from pathlib import Path

from newsmemeai_youtube.feeds import Headline
from newsmemeai_youtube.package import (
    REQUIRED_ARTIFACTS,
    build_package,
    slugify,
    youtube_description,
    youtube_metadata,
    youtube_tags,
    youtube_title,
)
from newsmemeai_youtube.script import template_script

HEADLINE = Headline(
    title="Scientists teach robots to smell pizza",
    link="https://example.com/robots",
    source="https://example.com/feed.xml",
    published="Mon, 16 Nov 2026 09:00:00 GMT",
    summary="A lab says the sensor could help future kitchen robots.",
)


def test_build_package_creates_all_artifacts(tmp_path: Path) -> None:
    package = build_package(HEADLINE, template_script(HEADLINE), tmp_path / "pkg")

    for name in REQUIRED_ARTIFACTS:
        assert (package / name).is_file(), name
    assert (package / "manifest.json").is_file()

    manifest = json.loads((package / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["schema_version"] == 1
    assert manifest["generator"]["name"] == "newsmemeai-youtube"
    assert manifest["style"] == "classic"
    assert manifest["headline"]["title"] == HEADLINE.title
    assert manifest["script"]["context"]
    assert manifest["review"] == {
        "status": "draft",
        "required": True,
        "checklist": "REVIEW.md",
    }
    assert set(manifest["files"]) == set(REQUIRED_ARTIFACTS)
    assert "manifest.json" not in manifest["files"]
    for entry in manifest["files"].values():
        assert len(entry["sha256"]) == 64
        assert entry["bytes"] > 0


def test_build_is_deterministic(tmp_path: Path) -> None:
    first = build_package(HEADLINE, template_script(HEADLINE), tmp_path / "one")
    second = build_package(HEADLINE, template_script(HEADLINE), tmp_path / "two")
    first_manifest = json.loads((first / "manifest.json").read_text(encoding="utf-8"))
    second_manifest = json.loads((second / "manifest.json").read_text(encoding="utf-8"))
    assert first_manifest["files"] == second_manifest["files"]
    assert first_manifest["script"] == second_manifest["script"]


def test_build_records_style(tmp_path: Path) -> None:
    script = template_script(HEADLINE, style="reaction")
    package = build_package(HEADLINE, script, tmp_path / "pkg", style="reaction")
    manifest = json.loads((package / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["style"] == "reaction"
    assert manifest["script"]["style"] == "reaction"


def test_slugify() -> None:
    assert slugify("Hello, World!") == "hello-world"
    assert slugify("  ***  ") == "package"
    assert len(slugify("x" * 100)) <= 60


def test_youtube_title_fits_limit() -> None:
    headline = Headline(title="A very long headline " * 20)
    title = youtube_title(headline)
    assert len(title) <= 100
    assert title.endswith("#Shorts")


def test_youtube_metadata_limits() -> None:
    metadata = youtube_metadata(HEADLINE)
    assert len(str(metadata["title"])) <= 100
    assert len(str(metadata["description"])) <= 5000
    tags = metadata["tags"]
    assert isinstance(tags, list)
    assert sum(len(str(tag)) + 1 for tag in tags) <= 500
    assert metadata["privacy_status"] == "private"


def test_youtube_description_attributes_source() -> None:
    description = youtube_description(HEADLINE)
    assert "Source: https://example.com/feed.xml" in description
    assert "not published automatically" in description


def test_youtube_tags_without_url() -> None:
    tags = youtube_tags(Headline(title="Local story", source="tests/fixtures/news.xml"))
    assert "local news" in tags
