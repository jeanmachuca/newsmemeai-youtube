#!/usr/bin/env python3
"""SPECv1 audit for NewsMemeAI YouTube.

Checks four dimensions: integrity, reliability, consistency, and implementation
drift. The script is stdlib-only so it can run before the package is installed.

Exit codes:
    0  PASS (warnings do not fail unless --strict is set)
    1  FAIL (integrity/reliability/consistency breach, or strict warnings)
    2  usage or environment error
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path

FOLDERS: dict[str, str] = {
    "01-product-vision": "Product Vision",
    "02-prd": "Product Requirement Document",
    "03-architecture": "Architecture",
    "04-adrs": "Architecture Decision Records",
    "05-requirements": "Requirements",
    "06-schemas": "Schemas",
    "07-sdlc": "Software Development Life Cycle",
    "08-code-conventions": "Code Conventions",
    "09-housekeeping": "Housekeeping",
    "10-script-helpers": "Script Helpers",
    "11-implementation-plan": "Implementation Plan",
}

REQUIRED_HEADINGS = (
    "## Scope",
    "## Normative Statements (RFC 2119)",
    "## Open Questions",
    "## Change Log",
)

ADR_HEADINGS = ("## Context", "## Decision", "## Consequences", "## Related ADRs")

RFC_KEYWORD_RE = re.compile(
    r"\b(MUST NOT|SHALL NOT|SHOULD NOT|NOT RECOMMENDED|MUST|SHALL|SHOULD|"
    r"REQUIRED|RECOMMENDED|MAY|OPTIONAL)\b"
)
REQUIREMENT_ROW_RE = re.compile(
    r"^\|\s*((?:FR|NFR)-\d{3})\s*\|\s*([^|]+?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|$"
)
USER_STORY_RE = re.compile(r"^###\s+(US-\d{3})\b")
MAPS_TO_RE = re.compile(r"\*\*Maps to:\*\*\s*(.+)")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
MODULE_RE = re.compile(r"`([a-z_]+\.py)`")
VERSION_RE = re.compile(r'__version__\s*=\s*"([^"]+)"')
PYPROJECT_VERSION_RE = re.compile(r'^version\s*=\s*"([^"]+)"', re.MULTILINE)

VALID_LEVELS = {
    "MUST",
    "MUST NOT",
    "SHALL",
    "SHALL NOT",
    "SHOULD",
    "SHOULD NOT",
    "MAY",
    "REQUIRED",
    "RECOMMENDED",
    "NOT RECOMMENDED",
    "OPTIONAL",
}

CI_COMMANDS = (
    "ruff check",
    "ruff format --check",
    "mypy src/",
    "pytest",
    "audit_specs.py --strict",
)

PROCESS_ARTIFACTS = (
    "MISSION.md",
    "HUD.md",
    "LICENSE",
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "docs/git-workflow.md",
    "docs/skills-compliance.md",
    "docs/org-structure.md",
    "docs/pit-stop.md",
    "docs/ira.md",
    "docs/review-checklist.md",
    ".opencode/instructions/git-workflow.md",
    ".pre-commit-config.yaml",
    "opencode.json",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/ci.yml",
    "scripts/benchmark.py",
    "scripts/verify.sh",
)

DIMENSIONS = ("integrity", "reliability", "consistency", "drift")


@dataclass(frozen=True, slots=True)
class Finding:
    """One audit observation."""

    dimension: str
    severity: str  # Breach | Warning | Advisory
    location: str
    message: str


@dataclass(slots=True)
class AuditResult:
    """Collected findings for one run."""

    root: Path
    strict: bool
    dimensions: tuple[str, ...] = DIMENSIONS
    findings: list[Finding] = field(default_factory=list)

    def add(self, dimension: str, severity: str, location: str, message: str) -> None:
        self.findings.append(Finding(dimension, severity, location, message))

    @property
    def breaches(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "Breach"]

    @property
    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "Warning"]

    @property
    def advisories(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "Advisory"]

    @property
    def passed(self) -> bool:
        if self.breaches:
            return False
        return not (self.strict and self.warnings)

    def dimension_status(self, dimension: str) -> str:
        if dimension not in self.dimensions:
            return "SKIPPED"
        relevant = [f for f in self.findings if f.dimension == dimension]
        if any(f.severity == "Breach" for f in relevant):
            return "FAIL"
        if self.strict and any(f.severity == "Warning" for f in relevant):
            return "FAIL"
        if relevant:
            return "PASS (with notes)"
        return "PASS"


def _read(path: Path, result: AuditResult, dimension: str) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        result.add(dimension, "Breach", str(path), f"could not read file: {exc}")
        return ""


def _markdown_files(folder: Path) -> list[Path]:
    return sorted(path for path in folder.glob("*.md") if not path.name.startswith(("._", ".")))


def check_integrity(root: Path, result: AuditResult) -> None:
    specs = root / "specs"
    if not specs.is_dir():
        result.add("integrity", "Breach", "specs/", "specs/ directory is missing")
        return

    for folder, title in FOLDERS.items():
        folder_path = specs / folder
        if not folder_path.is_dir():
            result.add("integrity", "Breach", f"specs/{folder}/", "folder is missing")
            continue
        documents = _markdown_files(folder_path)
        if not documents:
            result.add(
                "integrity",
                "Breach",
                f"specs/{folder}/",
                "folder contains no markdown document",
            )
            continue

        schema_ok = False
        for document in documents:
            text = _read(document, result, "integrity")
            if not text:
                continue
            if not text.startswith("# "):
                result.add(
                    "integrity",
                    "Breach",
                    str(document.relative_to(root)),
                    "document must start with a level-1 title",
                )
            if folder == "04-adrs" and document.name != "README.md":
                # ADRs use the Context/Decision/Consequences schema, checked under
                # consistency. The folder README carries the minimum schema.
                continue
            missing = [heading for heading in REQUIRED_HEADINGS if heading not in text]
            if missing:
                result.add(
                    "integrity",
                    "Breach",
                    str(document.relative_to(root)),
                    f"missing minimum-schema headings: {', '.join(missing)}",
                )
                continue
            if not schema_ok:
                schema_ok = True
            _check_normative_bullets(document, text, root, result)

        if not schema_ok:
            result.add(
                "integrity",
                "Breach",
                f"specs/{folder}/",
                f"no document follows the minimum schema for {title!r}",
            )


def _check_normative_bullets(document: Path, text: str, root: Path, result: AuditResult) -> None:
    lines = text.splitlines()
    try:
        start = lines.index("## Normative Statements (RFC 2119)")
    except ValueError:
        return
    bullets = 0
    for line in lines[start + 1 :]:
        if line.startswith("## "):
            break
        if not line.startswith("- "):
            continue
        bullets += 1
        if not RFC_KEYWORD_RE.search(line):
            result.add(
                "integrity",
                "Breach",
                str(document.relative_to(root)),
                f"normative bullet lacks a capitalized RFC 2119 keyword: {line.strip()[:120]}",
            )
    if bullets == 0:
        result.add(
            "integrity",
            "Breach",
            str(document.relative_to(root)),
            "RFC 2119 section has no normative statements",
        )


def _parse_requirements(root: Path, result: AuditResult) -> dict[str, tuple[str, str, str]]:
    path = root / "specs" / "05-requirements" / "requirements.md"
    text = _read(path, result, "reliability")
    requirements: dict[str, tuple[str, str, str]] = {}
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = REQUIREMENT_ROW_RE.match(line)
        if not match:
            continue
        requirement_id, level, statement, verification = match.groups()
        level = level.strip().strip("*`")
        statement = statement.strip()
        verification = verification.strip()
        if level not in VALID_LEVELS:
            result.add(
                "reliability",
                "Breach",
                f"specs/05-requirements/requirements.md:{line_number}",
                f"{requirement_id} has invalid RFC 2119 level {level!r}",
            )
        if not statement:
            result.add(
                "reliability",
                "Breach",
                f"specs/05-requirements/requirements.md:{line_number}",
                f"{requirement_id} has no statement",
            )
        if not verification or verification in {"-", "TBD", "n/a"}:
            result.add(
                "reliability",
                "Breach",
                f"specs/05-requirements/requirements.md:{line_number}",
                f"{requirement_id} has no verification method",
            )
        if requirement_id in requirements:
            result.add(
                "reliability",
                "Breach",
                f"specs/05-requirements/requirements.md:{line_number}",
                f"duplicate requirement id {requirement_id}",
            )
            continue
        requirements[requirement_id] = (level, statement, verification)

    if not requirements:
        result.add(
            "reliability",
            "Breach",
            "specs/05-requirements/requirements.md",
            "no FR/NFR rows found",
        )
    return requirements


def _check_user_stories(
    root: Path, requirements: dict[str, tuple[str, str, str]], result: AuditResult
) -> set[str]:
    path = root / "specs" / "02-prd" / "prd.md"
    text = _read(path, result, "reliability")
    stories: dict[str, set[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        header = USER_STORY_RE.match(line)
        if header:
            current = header.group(1)
            stories[current] = set()
            continue
        if line.startswith("## ") or line.startswith("### "):
            current = None
            continue
        if current is None:
            continue
        mapping = MAPS_TO_RE.search(line)
        if mapping:
            stories[current].update(re.findall(r"(?:FR|NFR)-\d{3}", mapping.group(1)))

    if not stories:
        result.add("reliability", "Breach", "specs/02-prd/prd.md", "no user stories found")
        return set()

    for story, mapped in stories.items():
        if not mapped:
            result.add(
                "reliability",
                "Breach",
                "specs/02-prd/prd.md",
                f"{story} has no 'Maps to' requirement",
            )
            continue
        if not any(requirement.startswith("FR-") for requirement in mapped):
            result.add(
                "reliability",
                "Breach",
                "specs/02-prd/prd.md",
                f"{story} maps to no functional requirement",
            )
        for requirement in sorted(mapped):
            if requirement not in requirements:
                result.add(
                    "reliability",
                    "Breach",
                    "specs/02-prd/prd.md",
                    f"{story} references unknown requirement {requirement}",
                )
    return set(stories)


def _check_plan_traceability(
    root: Path, requirements: dict[str, tuple[str, str, str]], result: AuditResult
) -> None:
    path = root / "specs" / "11-implementation-plan" / "plan.md"
    text = _read(path, result, "reliability")
    planned = set(re.findall(r"^\|\s*((?:FR|NFR)-\d{3})\s*\|", text, re.MULTILINE))
    for requirement in sorted(set(requirements) - planned):
        result.add(
            "reliability",
            "Breach",
            "specs/11-implementation-plan/plan.md",
            f"{requirement} is missing from the traceability matrix",
        )


def check_reliability(root: Path, result: AuditResult) -> None:
    requirements = _parse_requirements(root, result)
    _check_user_stories(root, requirements, result)
    _check_plan_traceability(root, requirements, result)


def _check_adrs(root: Path, result: AuditResult) -> None:
    folder = root / "specs" / "04-adrs"
    if not folder.is_dir():
        return
    adrs = [document for document in _markdown_files(folder) if document.name != "README.md"]
    if not adrs:
        result.add("consistency", "Breach", "specs/04-adrs/", "no ADR documents found")
        return
    for adr in adrs:
        text = _read(adr, result, "consistency")
        if not text:
            continue
        if "**Status:**" not in text:
            result.add(
                "consistency",
                "Breach",
                str(adr.relative_to(root)),
                "ADR has no Status line",
            )
        for heading in ADR_HEADINGS:
            if heading not in text:
                result.add(
                    "consistency",
                    "Breach",
                    str(adr.relative_to(root)),
                    f"ADR is missing {heading!r}",
                )
        decision = text.split("## Decision", 1)[-1]
        if not RFC_KEYWORD_RE.search(decision):
            result.add(
                "consistency",
                "Breach",
                str(adr.relative_to(root)),
                "ADR Decision section uses no RFC 2119 keyword",
            )


def _check_schemas(root: Path, result: AuditResult) -> None:
    folder = root / "specs" / "06-schemas"
    if not folder.is_dir():
        return
    documents = sorted(
        path for path in folder.glob("*.json") if not path.name.startswith(("._", "."))
    )
    if not documents:
        result.add("consistency", "Breach", "specs/06-schemas/", "no JSON schema found")
        return
    for document in documents:
        relative = str(document.relative_to(root))
        try:
            payload = json.loads(document.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            result.add("consistency", "Breach", relative, f"invalid JSON: {exc}")
            continue
        if not isinstance(payload, dict):
            result.add("consistency", "Breach", relative, "schema must be a JSON object")
            continue
        if "$schema" not in payload:
            result.add(
                "consistency",
                "Breach",
                relative,
                "schema does not declare a $schema dialect",
            )
        properties = payload.get("properties")
        if not isinstance(properties, dict) or "schema_version" not in properties:
            result.add(
                "consistency",
                "Breach",
                relative,
                "schema does not declare a schema_version property",
            )


def _check_index_links(root: Path, result: AuditResult) -> None:
    index = root / "specs" / "README.md"
    text = _read(index, result, "consistency")
    if not text:
        return
    for target in LINK_RE.findall(text):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        candidate = (index.parent / target).resolve()
        if not candidate.exists():
            result.add(
                "consistency",
                "Breach",
                "specs/README.md",
                f"broken relative link {target!r}",
            )


def _check_requirements_match_schemas(root: Path, result: AuditResult) -> None:
    schemas_text = _read(root / "specs" / "06-schemas" / "schemas.md", result, "consistency")
    requirements_text = _read(
        root / "specs" / "05-requirements" / "requirements.md", result, "consistency"
    )
    if "manifest.json" not in schemas_text or "metadata.json" not in schemas_text:
        result.add(
            "consistency",
            "Breach",
            "specs/06-schemas/schemas.md",
            "schema document must cover manifest.json and metadata.json",
        )
    if "manifest.json" not in requirements_text:
        result.add(
            "consistency",
            "Breach",
            "specs/05-requirements/requirements.md",
            "requirements do not mention the manifest contract",
        )


def _check_nfr_coverage(root: Path, result: AuditResult) -> None:
    path = root / "specs" / "05-requirements" / "requirements.md"
    text = _read(path, result, "consistency")
    if not text:
        return
    for category in ("Performance", "Security", "Reliability", "Operability", "Compliance"):
        match = re.search(
            rf"^\|\s*{category}\s*\|\s*([^|]+?)\s*\|$", text, re.MULTILINE | re.IGNORECASE
        )
        if not match:
            result.add(
                "consistency",
                "Breach",
                "specs/05-requirements/requirements.md",
                f"NFR coverage is missing the {category} category",
            )
        elif "NFR-" not in match.group(1):
            result.add(
                "consistency",
                "Breach",
                "specs/05-requirements/requirements.md",
                f"NFR coverage for {category} names no NFR id",
            )


def _check_sdlc_gates(root: Path, result: AuditResult) -> None:
    path = root / "specs" / "07-sdlc" / "sdlc.md"
    text = _read(path, result, "consistency")
    if not text:
        return
    for folder in FOLDERS:
        if folder not in text:
            result.add(
                "consistency",
                "Breach",
                "specs/07-sdlc/sdlc.md",
                f"approval gates do not name {folder}",
            )


def _check_script_helpers(root: Path, result: AuditResult) -> None:
    path = root / "specs" / "10-script-helpers" / "scripts.md"
    text = _read(path, result, "consistency")
    if not text:
        return
    for heading in ("**Purpose:**", "**Preconditions:**", "**Postconditions:**"):
        if text.count(heading) < 3:
            result.add(
                "consistency",
                "Breach",
                "specs/10-script-helpers/scripts.md",
                f"each helper must declare {heading}; found {text.count(heading)} of 3",
            )
    if "--strict" not in text:
        result.add(
            "consistency",
            "Breach",
            "specs/10-script-helpers/scripts.md",
            "the audit helper must document the --strict flag",
        )


def check_consistency(root: Path, result: AuditResult) -> None:
    _check_adrs(root, result)
    _check_schemas(root, result)
    _check_index_links(root, result)
    _check_requirements_match_schemas(root, result)
    _check_nfr_coverage(root, result)
    _check_sdlc_gates(root, result)
    _check_script_helpers(root, result)


def _package_source(root: Path, source: Path | None) -> Path:
    base = source if source is not None else root / "src"
    return base / "newsmemeai_youtube"


def _check_modules(root: Path, result: AuditResult, source: Path | None = None) -> None:
    architecture = _read(root / "specs" / "03-architecture" / "architecture.md", result, "drift")
    package_source = _package_source(root, source)
    modules = sorted(set(MODULE_RE.findall(architecture)))
    if not modules:
        result.add(
            "drift",
            "Warning",
            "specs/03-architecture/architecture.md",
            "no backticked modules found; drift check is weak",
        )
        return
    for module in modules:
        if not (package_source / module).is_file():
            result.add(
                "drift",
                "Breach",
                str(package_source / module),
                "module is declared in the architecture but missing from source",
            )


def _check_version(root: Path, result: AuditResult, source: Path | None = None) -> None:
    init_path = _package_source(root, source) / "__init__.py"
    init = _read(init_path, result, "drift")
    pyproject = _read(root / "pyproject.toml", result, "drift")
    if not init or not pyproject:
        return
    init_match = VERSION_RE.search(init)
    pyproject_match = PYPROJECT_VERSION_RE.search(pyproject)
    if not init_match or not pyproject_match:
        result.add(
            "drift",
            "Breach",
            str(init_path),
            "could not read a version from __init__.py and pyproject.toml",
        )
        return
    if init_match.group(1) != pyproject_match.group(1):
        result.add(
            "drift",
            "Breach",
            str(init_path),
            f"__version__ {init_match.group(1)!r} does not match "
            f"pyproject version {pyproject_match.group(1)!r}",
        )


def _check_ci(root: Path, result: AuditResult) -> None:
    workflow = _read(root / ".github" / "workflows" / "ci.yml", result, "drift")
    if not workflow:
        return
    for command in CI_COMMANDS:
        if command not in workflow:
            result.add(
                "drift",
                "Breach",
                ".github/workflows/ci.yml",
                f"CI does not contain required command {command!r}",
            )


def _check_process_artifacts(root: Path, result: AuditResult) -> None:
    for relative in PROCESS_ARTIFACTS:
        path = root / relative
        if not path.is_file():
            result.add(
                "drift",
                "Breach",
                relative,
                "required process artifact is missing",
            )
            continue
        try:
            content = path.read_text(encoding="utf-8").strip()
        except (OSError, UnicodeDecodeError) as exc:
            result.add("drift", "Breach", relative, f"could not read process artifact: {exc}")
            continue
        if not content:
            result.add("drift", "Breach", relative, "required process artifact is empty")


def _check_artifact_contract(root: Path, result: AuditResult, source: Path | None = None) -> None:
    package_path = _package_source(root, source) / "package.py"
    package_source = _read(package_path, result, "drift")
    architecture = _read(root / "specs" / "03-architecture" / "architecture.md", result, "drift")
    schemas = _read(root / "specs" / "06-schemas" / "schemas.md", result, "drift")
    artifacts = sorted(
        set(re.findall(r'"((?:frame|thumbnail|script|metadata|REVIEW)[^"]*)"', package_source))
    )
    if len(artifacts) < 7:
        result.add(
            "drift",
            "Warning",
            str(package_path),
            f"expected at least 7 artifact names, found {len(artifacts)}",
        )
    for artifact in artifacts:
        if artifact not in architecture:
            result.add(
                "drift",
                "Warning",
                "specs/03-architecture/architecture.md",
                f"artifact {artifact!r} is not documented in the architecture",
            )
        if artifact not in schemas:
            result.add(
                "drift",
                "Warning",
                "specs/06-schemas/schemas.md",
                f"artifact {artifact!r} is not documented in the schemas",
            )


def check_drift(root: Path, result: AuditResult, source: Path | None = None) -> None:
    _check_modules(root, result, source)
    _check_version(root, result, source)
    _check_ci(root, result)
    _check_process_artifacts(root, result)
    _check_artifact_contract(root, result, source)


def run_audit(
    root: Path,
    *,
    strict: bool,
    source: Path | None = None,
    dimensions: set[str] | None = None,
) -> AuditResult:
    selected = tuple(
        dimension for dimension in DIMENSIONS if dimensions is None or dimension in dimensions
    )
    result = AuditResult(root=root, strict=strict, dimensions=selected)
    checkers = {
        "integrity": check_integrity,
        "reliability": check_reliability,
        "consistency": check_consistency,
    }
    for dimension in selected:
        if dimension == "drift":
            check_drift(root, result, source)
            continue
        checkers[dimension](root, result)
    return result


def _render_report(result: AuditResult) -> str:
    generated = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    mode = "strict" if result.strict else "standard"
    if result.dimensions != DIMENSIONS:
        mode += f", scoped to {', '.join(result.dimensions)}"
    lines = [
        "# Specification Audit Report",
        "",
        f"- **Generated:** {generated}",
        f"- **Root:** `{result.root.name or result.root}`",
        f"- **Mode:** {mode}",
        f"- **Result:** {'PASS' if result.passed else 'FAIL'}",
        f"- **Findings:** {len(result.breaches)} breach(es), "
        f"{len(result.warnings)} warning(s), {len(result.advisories)} advisory(ies)",
        "",
    ]

    for dimension in DIMENSIONS:
        relevant = [f for f in result.findings if f.dimension == dimension]
        lines.append(f"## {dimension.capitalize()} — {result.dimension_status(dimension)}")
        lines.append("")
        if not relevant:
            lines.extend(["No findings.", ""])
            continue
        lines.append("| Severity | Location | Finding |")
        lines.append("| --- | --- | --- |")
        for finding in relevant:
            location = finding.location.replace("|", "\\|")
            message = finding.message.replace("|", "\\|")
            lines.append(f"| {finding.severity} | `{location}` | {message} |")
        lines.append("")

    lines.extend(
        [
            "## Remediation",
            "",
            "Breaches MUST be fixed before a release PR can merge. Warnings MUST be fixed "
            "when `--strict` is enabled; advisories are informational. Drift items are "
            "tracked against the milestones in `11-implementation-plan/plan.md`.",
            "",
            "## Change Log",
            "",
            "| Date | Author | Result | Note |",
            "| --- | --- | --- | --- |",
            f"| {generated[:10]} | Spec audit | {'PASS' if result.passed else 'FAIL'} | "
            "Generated by `scripts/audit_specs.py`. |",
            "",
        ]
    )
    return "\n".join(lines)


def _render_json(result: AuditResult) -> str:
    payload = {
        "generated": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "root": str(result.root),
        "strict": result.strict,
        "passed": result.passed,
        "summary": {
            "breaches": len(result.breaches),
            "warnings": len(result.warnings),
            "advisories": len(result.advisories),
        },
        "dimensions": {dimension: result.dimension_status(dimension) for dimension in DIMENSIONS},
        "findings": [asdict(finding) for finding in result.findings],
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def _positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="audit_specs.py",
        description="Audit the SPECv1 tree and implementation drift.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        metavar="PATH",
        help="repository root (default: current directory)",
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=None,
        metavar="PATH",
        help="source tree to compare against (default: ROOT/src)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="treat warnings as failures",
    )
    parser.add_argument(
        "--write-report",
        action="store_true",
        help="write specs/AUDIT-REPORT.md",
    )
    parser.add_argument("--json", action="store_true", help="emit JSON instead of text")
    parser.add_argument(
        "--dimension",
        action="append",
        choices=DIMENSIONS,
        help="limit the run to one or more dimensions (default: all)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        print(f"audit_specs: error: {root} is not a directory", file=sys.stderr)
        return 2
    source = args.source.expanduser().resolve() if args.source else None
    selected = set(args.dimension) if args.dimension else None

    result = run_audit(root, strict=args.strict, source=source, dimensions=selected)

    if args.write_report:
        report_path = root / "specs" / "AUDIT-REPORT.md"
        try:
            report_path.parent.mkdir(parents=True, exist_ok=True)
            report_path.write_text(_render_report(result), encoding="utf-8")
        except OSError as exc:
            print(f"audit_specs: error: could not write report: {exc}", file=sys.stderr)
            return 2

    if args.json:
        print(_render_json(result))
    else:
        for finding in result.findings:
            print(
                f"[{finding.severity}] {finding.dimension}: {finding.location}: {finding.message}"
            )
        print(
            f"Spec audit: {'PASS' if result.passed else 'FAIL'} "
            f"({len(result.breaches)} breach(es), {len(result.warnings)} warning(s), "
            f"{len(result.advisories)} advisory(ies))"
        )
        if args.write_report:
            print(f"Report: {root / 'specs' / 'AUDIT-REPORT.md'}")

    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
