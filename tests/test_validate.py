"""Package validation and tamper-detection tests."""

from __future__ import annotations

import json
from pathlib import Path

from newsmemeai_youtube.feeds import Headline
from newsmemeai_youtube.package import build_package
from newsmemeai_youtube.script import template_script
from newsmemeai_youtube.validate import validate_package

HEADLINE = Headline(
    title="Robots learn to garden",
    source="https://example.com/feed.xml",
    summary="Tomatoes are involved.",
)


def _build(tmp_path: Path) -> Path:
    return build_package(HEADLINE, template_script(HEADLINE), tmp_path / "pkg")


def test_valid_package(tmp_path: Path) -> None:
    package = _build(tmp_path)
    result = validate_package(package)
    assert result.ok, result.issues
    assert result.files_checked == 7


def test_tampered_artifact_is_detected(tmp_path: Path) -> None:
    package = _build(tmp_path)
    frame = package / "frame-01-hook.svg"
    frame.write_text(frame.read_text(encoding="utf-8") + "<!-- tampered -->", encoding="utf-8")
    result = validate_package(package)
    assert not result.ok
    assert any("sha256 mismatch" in issue for issue in result.issues)


def test_missing_artifact_is_detected(tmp_path: Path) -> None:
    package = _build(tmp_path)
    (package / "thumbnail.svg").unlink()
    result = validate_package(package)
    assert not result.ok
    assert any("missing artifact" in issue for issue in result.issues)


def test_unsafe_manifest_path_is_detected(tmp_path: Path) -> None:
    package = _build(tmp_path)
    manifest_path = package / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["files"]["../escape.svg"] = {"sha256": "0" * 64, "bytes": 0}
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    result = validate_package(package)
    assert not result.ok
    assert any("unsafe path" in issue for issue in result.issues)


def test_invalid_metadata_title_is_detected(tmp_path: Path) -> None:
    package = _build(tmp_path)
    metadata_path = package / "metadata.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    metadata["title"] = "x" * 101
    metadata_path.write_text(json.dumps(metadata), encoding="utf-8")

    result = validate_package(package)
    assert not result.ok
    assert any("title exceeds" in issue for issue in result.issues)


def test_invalid_manifest_json_is_detected(tmp_path: Path) -> None:
    package = _build(tmp_path)
    (package / "manifest.json").write_text("{not json", encoding="utf-8")
    result = validate_package(package)
    assert not result.ok
    assert any("invalid JSON" in issue for issue in result.issues)


def test_missing_directory_is_detected(tmp_path: Path) -> None:
    result = validate_package(tmp_path / "nope")
    assert not result.ok
    assert any("not a directory" in issue for issue in result.issues)


def test_extra_files_are_allowed(tmp_path: Path) -> None:
    package = _build(tmp_path)
    (package / "notes.txt").write_text("producer notes", encoding="utf-8")
    result = validate_package(package)
    assert result.ok, result.issues
