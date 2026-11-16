"""Validate a generated package: manifest shape, paths, sizes, and checksums."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import cast

from . import GENERATOR_NAME
from .package import (
    PACKAGE_SCHEMA_VERSION,
    REQUIRED_ARTIFACTS,
    YOUTUBE_CATEGORY,
    YOUTUBE_DESCRIPTION_LIMIT,
    YOUTUBE_TAG_BUDGET,
    YOUTUBE_TITLE_LIMIT,
)
from .render import THUMBNAIL_HEIGHT, THUMBNAIL_WIDTH, VERTICAL_HEIGHT, VERTICAL_WIDTH
from .script import STYLES

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
_REVIEW_CONTRACT = {"status": "draft", "required": True, "checklist": "REVIEW.md"}


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Outcome of validating one package directory."""

    package: Path
    files_checked: int
    issues: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.issues


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_json(path: Path, issues: list[str]) -> object | None:
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        issues.append(f"{path.name}: could not read ({exc})")
        return None
    try:
        return cast(object, json.loads(raw))
    except json.JSONDecodeError as exc:
        issues.append(f"{path.name}: invalid JSON ({exc})")
        return None


def _check_metadata(root: Path, issues: list[str]) -> None:
    path = root / "metadata.json"
    payload = _read_json(path, issues)
    if payload is None:
        return
    if not isinstance(payload, dict):
        issues.append("metadata.json: expected a JSON object")
        return

    if payload.get("schema_version") != PACKAGE_SCHEMA_VERSION:
        issues.append(f"metadata.json: schema_version must be {PACKAGE_SCHEMA_VERSION}")
    if payload.get("privacy_status") != "private":
        issues.append("metadata.json: privacy_status must be 'private'")
    if payload.get("made_for_kids") is not False:
        issues.append("metadata.json: made_for_kids must be false")
    if payload.get("shorts") is not True:
        issues.append("metadata.json: shorts must be true")
    if payload.get("category_id") != YOUTUBE_CATEGORY:
        issues.append(f"metadata.json: category_id must be {YOUTUBE_CATEGORY!r}")

    title = payload.get("title")
    if not isinstance(title, str) or not title.strip():
        issues.append("metadata.json: title must be a non-empty string")
    elif len(title) > YOUTUBE_TITLE_LIMIT:
        issues.append(f"metadata.json: title exceeds {YOUTUBE_TITLE_LIMIT} characters")

    description = payload.get("description")
    if not isinstance(description, str):
        issues.append("metadata.json: description must be a string")
    elif len(description) > YOUTUBE_DESCRIPTION_LIMIT:
        issues.append(f"metadata.json: description exceeds {YOUTUBE_DESCRIPTION_LIMIT} characters")

    tags = payload.get("tags")
    if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
        issues.append("metadata.json: tags must be a list of strings")
    else:
        budget = sum(len(tag) + 1 for tag in tags)
        if budget > YOUTUBE_TAG_BUDGET:
            issues.append(f"metadata.json: tag budget exceeds {YOUTUBE_TAG_BUDGET}")


def _check_manifest_identity(payload: dict[str, object], issues: list[str]) -> None:
    generator = payload.get("generator")
    if not isinstance(generator, dict):
        issues.append("manifest.json: generator must be an object")
    else:
        if generator.get("name") != GENERATOR_NAME:
            issues.append(f"manifest.json: generator.name must be {GENERATOR_NAME!r}")
        version = generator.get("version")
        if not isinstance(version, str) or not _SEMVER_RE.fullmatch(version):
            issues.append("manifest.json: generator.version must be SemVer")

    style = payload.get("style")
    if style not in STYLES:
        issues.append(f"manifest.json: style must be one of {', '.join(STYLES)}")

    dimensions = payload.get("dimensions")
    expected_dimensions = {
        "frame": [VERTICAL_WIDTH, VERTICAL_HEIGHT],
        "thumbnail": [THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT],
    }
    if not isinstance(dimensions, dict):
        issues.append("manifest.json: dimensions must be an object")
    else:
        for name, expected in expected_dimensions.items():
            if dimensions.get(name) != expected:
                issues.append(f"manifest.json: dimensions.{name} must be {expected}")

    review = payload.get("review")
    if not isinstance(review, dict):
        issues.append("manifest.json: review must be an object")
    else:
        for key, expected_review in _REVIEW_CONTRACT.items():
            if review.get(key) != expected_review:
                issues.append(f"manifest.json: review.{key} must be {expected_review!r}")

    headline = payload.get("headline")
    if not isinstance(headline, dict) or not isinstance(headline.get("title"), str):
        issues.append("manifest.json: headline.title must be a string")
    elif not str(headline["title"]).strip():
        issues.append("manifest.json: headline.title must not be empty")

    script = payload.get("script")
    if not isinstance(script, dict):
        issues.append("manifest.json: script must be an object")
    else:
        for key in ("hook", "context", "punchline"):
            value = script.get(key)
            if not isinstance(value, str) or not value.strip():
                issues.append(f"manifest.json: script.{key} must be a non-empty string")


def validate_package(package_dir: str | Path) -> ValidationResult:
    """Validate the manifest and every artifact in ``package_dir``."""

    root = Path(package_dir).expanduser().resolve()
    issues: list[str] = []
    files_checked = 0

    if not root.is_dir():
        return ValidationResult(root, 0, (f"{root}: not a directory",))

    payload = _read_json(root / "manifest.json", issues)
    if payload is None:
        return ValidationResult(root, 0, tuple(issues))
    if not isinstance(payload, dict):
        return ValidationResult(root, 0, ("manifest.json: expected a JSON object",))

    if payload.get("schema_version") != PACKAGE_SCHEMA_VERSION:
        issues.append(f"manifest.json: schema_version must be {PACKAGE_SCHEMA_VERSION}")

    _check_manifest_identity(payload, issues)

    files = payload.get("files")
    if not isinstance(files, dict) or not files:
        issues.append("manifest.json: files must be a non-empty object")
        _check_metadata(root, issues)
        return ValidationResult(root, files_checked, tuple(issues))

    missing = sorted(set(REQUIRED_ARTIFACTS) - set(files))
    for name in missing:
        issues.append(f"manifest.json: missing required artifact {name}")
    unexpected = sorted(set(files) - set(REQUIRED_ARTIFACTS))
    for name in unexpected:
        issues.append(f"manifest.json: unexpected artifact {name}")

    for name, entry in files.items():
        if not isinstance(name, str) or not isinstance(entry, dict):
            issues.append("manifest.json: each files entry must be name -> object")
            continue
        relative = PurePosixPath(name)
        if relative.is_absolute() or ".." in relative.parts:
            issues.append(f"manifest.json: unsafe path {name!r}")
            continue
        target = (root / relative).resolve()
        if target == root or root not in target.parents:
            issues.append(f"manifest.json: path escapes package: {name!r}")
            continue
        if not target.is_file():
            issues.append(f"{name}: missing artifact")
            continue

        expected_sha = entry.get("sha256")
        if not isinstance(expected_sha, str) or not _SHA256_RE.fullmatch(expected_sha):
            issues.append(f"{name}: sha256 must be 64 lowercase hex characters")
        elif _sha256(target) != expected_sha:
            issues.append(f"{name}: sha256 mismatch")

        expected_bytes = entry.get("bytes")
        if (
            not isinstance(expected_bytes, int)
            or isinstance(expected_bytes, bool)
            or expected_bytes < 0
        ):
            issues.append(f"{name}: bytes must be a non-negative integer")
        elif target.stat().st_size != expected_bytes:
            issues.append(f"{name}: byte size mismatch")

        files_checked += 1

    _check_metadata(root, issues)
    return ValidationResult(root, files_checked, tuple(issues))
