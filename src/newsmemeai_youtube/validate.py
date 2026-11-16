"""Validate a generated package: manifest shape, paths, sizes, and checksums."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import cast

from .package import (
    PACKAGE_SCHEMA_VERSION,
    REQUIRED_ARTIFACTS,
    YOUTUBE_DESCRIPTION_LIMIT,
    YOUTUBE_TAG_BUDGET,
    YOUTUBE_TITLE_LIMIT,
)

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


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

    generator = payload.get("generator")
    if not isinstance(generator, dict) or not isinstance(generator.get("name"), str):
        issues.append("manifest.json: generator.name is required")
    if not isinstance(payload.get("headline"), dict):
        issues.append("manifest.json: headline must be an object")
    if not isinstance(payload.get("script"), dict):
        issues.append("manifest.json: script must be an object")
    if not isinstance(payload.get("review"), dict):
        issues.append("manifest.json: review must be an object")

    files = payload.get("files")
    if not isinstance(files, dict) or not files:
        issues.append("manifest.json: files must be a non-empty object")
        _check_metadata(root, issues)
        return ValidationResult(root, files_checked, tuple(issues))

    missing = sorted(set(REQUIRED_ARTIFACTS) - set(files))
    for name in missing:
        issues.append(f"manifest.json: missing required artifact {name}")

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
