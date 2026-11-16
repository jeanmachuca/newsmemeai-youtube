"""Tests for the SPECv1 audit engine."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "audit_specs.py"


def _load_audit() -> ModuleType:
    spec = importlib.util.spec_from_file_location("audit_specs", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


audit = _load_audit()
REPO_ROOT = Path(__file__).resolve().parent.parent


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_repository_passes_strict_audit() -> None:
    result = audit.run_audit(REPO_ROOT, strict=True)
    messages = [
        f"{finding.severity} {finding.dimension} {finding.location}: {finding.message}"
        for finding in result.findings
    ]
    assert result.passed, "\n".join(messages)


def test_report_rendering_contains_verdict() -> None:
    result = audit.run_audit(REPO_ROOT, strict=True)
    report = audit._render_report(result)
    assert "# Specification Audit Report" in report
    assert "**Result:** PASS" in report
    assert "## Integrity — PASS" in report


def test_scoped_audit_marks_other_dimensions_skipped() -> None:
    result = audit.run_audit(REPO_ROOT, strict=True, dimensions={"integrity"})
    assert result.passed
    assert result.dimension_status("integrity") == "PASS"
    assert result.dimension_status("drift") == "SKIPPED"


def test_empty_root_fails(capsys) -> None:
    exit_code = audit.main(["--root", str(REPO_ROOT / "does-not-exist"), "--json"])
    assert exit_code == 2
    assert "not a directory" in capsys.readouterr().err


def test_missing_folder_is_detected(tmp_path: Path) -> None:
    (tmp_path / "specs").mkdir()
    result = audit.AuditResult(root=tmp_path, strict=True)
    audit.check_integrity(tmp_path, result)
    assert any("folder is missing" in finding.message for finding in result.findings)


def test_normative_bullet_without_keyword_is_detected(tmp_path: Path) -> None:
    _write(
        tmp_path / "specs" / "01-product-vision" / "vision.md",
        "# Vision\n\n## Scope\n\nx\n\n## Normative Statements (RFC 2119)\n\n"
        "- The product will probably work.\n\n## Open Questions\n\nx\n\n## Change Log\n\nx\n",
    )
    result = audit.AuditResult(root=tmp_path, strict=True)
    audit.check_integrity(tmp_path, result)
    assert any("RFC 2119 keyword" in finding.message for finding in result.findings)


def _requirements(text: str) -> str:
    return (
        "# Requirements\n\n## Scope\n\nx\n\n## Normative Statements (RFC 2119)\n\n"
        "- The product MUST work.\n\n"
        "| ID | Level | Requirement | Verification |\n"
        "| --- | --- | --- | --- |\n"
        f"{text}\n\n## Open Questions\n\nx\n\n## Change Log\n\nx\n"
    )


def test_duplicate_requirement_and_bad_level_are_detected(tmp_path: Path) -> None:
    _write(
        tmp_path / "specs" / "05-requirements" / "requirements.md",
        _requirements("| FR-001 | MUST | One | test_one |\n| FR-001 | MIGHT | Two | test_two |\n"),
    )
    result = audit.AuditResult(root=tmp_path, strict=True)
    requirements = audit._parse_requirements(tmp_path, result)
    messages = [finding.message for finding in result.findings]
    assert "duplicate requirement id FR-001" in messages
    assert any("invalid RFC 2119 level" in message for message in messages)
    assert "FR-001" in requirements


def test_requirement_without_verification_is_detected(tmp_path: Path) -> None:
    _write(
        tmp_path / "specs" / "05-requirements" / "requirements.md",
        _requirements("| NFR-001 | MUST | One | TBD |"),
    )
    result = audit.AuditResult(root=tmp_path, strict=True)
    audit._parse_requirements(tmp_path, result)
    assert any("no verification method" in finding.message for finding in result.findings)


def test_user_story_mapping_is_checked(tmp_path: Path) -> None:
    _write(
        tmp_path / "specs" / "05-requirements" / "requirements.md",
        _requirements("| FR-001 | MUST | One | test_one |"),
    )
    _write(
        tmp_path / "specs" / "02-prd" / "prd.md",
        "# PRD\n\n## Scope\n\nx\n\n## Normative Statements (RFC 2119)\n\n"
        "- The PRD MUST map stories.\n\n## Open Questions\n\nx\n\n## Change Log\n\nx\n\n"
        "### US-001 — One\n\n**Maps to:** FR-999\n",
    )
    _write(
        tmp_path / "specs" / "11-implementation-plan" / "plan.md",
        "# Plan\n\n## Scope\n\nx\n\n## Normative Statements (RFC 2119)\n\n"
        "- The plan MUST trace.\n\n| Requirement | Milestone | Verification |\n"
        "| --- | --- | --- |\n| FR-001 | M1 | test_one |\n\n"
        "## Open Questions\n\nx\n\n## Change Log\n\nx\n",
    )
    result = audit.AuditResult(root=tmp_path, strict=True)
    audit.check_reliability(tmp_path, result)
    messages = [finding.message for finding in result.findings]
    assert any("unknown requirement FR-999" in message for message in messages)


def test_plan_traceability_gap_is_detected(tmp_path: Path) -> None:
    _write(
        tmp_path / "specs" / "05-requirements" / "requirements.md",
        _requirements("| FR-001 | MUST | One | test_one |\n| FR-002 | MUST | Two | test_two |"),
    )
    _write(
        tmp_path / "specs" / "02-prd" / "prd.md",
        "# PRD\n\n## Scope\n\nx\n\n## Normative Statements (RFC 2119)\n\n"
        "- The PRD MUST map stories.\n\n## Open Questions\n\nx\n\n## Change Log\n\nx\n\n"
        "### US-001 — One\n\n**Maps to:** FR-001\n",
    )
    _write(
        tmp_path / "specs" / "11-implementation-plan" / "plan.md",
        "# Plan\n\n## Scope\n\nx\n\n## Normative Statements (RFC 2119)\n\n"
        "- The plan MUST trace.\n\n| Requirement | Milestone | Verification |\n"
        "| --- | --- | --- |\n| FR-001 | M1 | test_one |\n\n"
        "## Open Questions\n\nx\n\n## Change Log\n\nx\n",
    )
    result = audit.AuditResult(root=tmp_path, strict=True)
    audit.check_reliability(tmp_path, result)
    assert any("FR-002 is missing" in finding.message for finding in result.findings)


def test_invalid_schema_json_is_detected(tmp_path: Path) -> None:
    _write(tmp_path / "specs" / "06-schemas" / "bad.schema.json", "{not json")
    result = audit.AuditResult(root=tmp_path, strict=True)
    audit.check_consistency(tmp_path, result)
    assert any("invalid JSON" in finding.message for finding in result.findings)


def test_schema_without_schema_version_is_detected(tmp_path: Path) -> None:
    _write(
        tmp_path / "specs" / "06-schemas" / "empty.schema.json",
        json.dumps({"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object"}),
    )
    result = audit.AuditResult(root=tmp_path, strict=True)
    audit.check_consistency(tmp_path, result)
    assert any("schema_version" in finding.message for finding in result.findings)


def test_adr_missing_structure_is_detected(tmp_path: Path) -> None:
    _write(
        tmp_path / "specs" / "04-adrs" / "0001-test.md",
        "# ADR 0001\n\n- **Status:** Accepted\n\n## Context\n\nx\n",
    )
    result = audit.AuditResult(root=tmp_path, strict=True)
    audit.check_consistency(tmp_path, result)
    assert any("ADR is missing" in finding.message for finding in result.findings)


def test_version_mismatch_is_detected(tmp_path: Path) -> None:
    _write(
        tmp_path / "src" / "newsmemeai_youtube" / "__init__.py",
        '__version__ = "9.9.9"\n',
    )
    _write(tmp_path / "pyproject.toml", 'version = "0.1.0"\n')
    result = audit.AuditResult(root=tmp_path, strict=True)
    audit._check_version(tmp_path, result)
    assert any("does not match" in finding.message for finding in result.findings)


def test_missing_ci_command_is_detected(tmp_path: Path) -> None:
    _write(
        tmp_path / ".github" / "workflows" / "ci.yml",
        "jobs:\n  verify:\n    steps:\n      - run: ruff check .\n",
    )
    result = audit.AuditResult(root=tmp_path, strict=True)
    audit._check_ci(tmp_path, result)
    assert any("ruff format --check" in finding.message for finding in result.findings)


def test_cli_json_output_on_empty_tree(tmp_path: Path, capsys) -> None:
    exit_code = audit.main(["--root", str(tmp_path), "--json"])
    assert exit_code == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["passed"] is False
    assert payload["dimensions"]["integrity"] == "FAIL"
