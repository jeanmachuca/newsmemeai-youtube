# Script Helpers

## Scope

This folder defines the normative helper scripts used by developers and CI. The helpers
are deliberately stdlib-only so they run before the package is installed.

## Normative Statements (RFC 2119)

- Every helper MUST declare its purpose, preconditions, postconditions, and flags.
- `audit_specs.py --strict` MUST fail on integrity errors and warnings.
- `verify.sh` MUST run lint, format, type, test, and spec audit in that order.
- `benchmark.py` MUST measure only the deterministic `--no-llm` path.
- Helpers MUST NOT write outside the repository except for temporary benchmark output.
- CI MUST run `audit_specs.py --strict` before a PR can merge.

## `scripts/audit_specs.py`

**Purpose:** Validate the SPECv1 tree and compare declared architecture to the source.

**Preconditions:** Python 3.11+; run from the repository root.

**Postconditions:** Prints findings; exits 0 when clean; with `--write-report`, rewrites
`specs/AUDIT-REPORT.md`.

| Flag | Meaning |
| --- | --- |
| `--root PATH` | Repository root (default: current directory) |
| `--source PATH` | Source tree containing `newsmemeai_youtube/` (default: `ROOT/src`) |
| `--dimension NAME` | Limit the run to `integrity`, `reliability`, `consistency`, or `drift`; repeatable |
| `--strict` | Treat warnings as failures |
| `--write-report` | Write `specs/AUDIT-REPORT.md` |
| `--json` | Emit machine-readable findings |

Checks:

1. Integrity: all 11 folders exist and each has the minimum schema.
2. Reliability: RFC 2119 usage, unique requirement IDs, user-story mapping.
3. Consistency: ADR structure, schema validity, index links.
4. Drift: named modules exist, version matches, CI contains the required commands.

## `scripts/benchmark.py`

**Purpose:** Measure the median deterministic build time for the HUD Circuit Delta.

**Preconditions:** Package is importable from `src/`; fixture feed exists.

**Postconditions:** Prints JSON with `runs`, `median_ms`, and `samples_ms`; leaves no
artifacts outside a temporary directory.

| Flag | Meaning |
| --- | --- |
| `--runs N` | Number of builds (default: 5) |
| `--feed PATH` | Feed fixture (default: `tests/fixtures/news.xml`) |
| `--index N` | Headline index (default: 1) |

## `scripts/verify.sh`

**Purpose:** The Checklist Close for a Lap.

**Preconditions:** Developer tools installed; run from the repository root.

**Postconditions:** Exits non-zero on the first failed check.

Sequence:

1. `ruff check .`
2. `ruff format --check .`
3. `mypy src/`
4. `pytest -v`
5. `python scripts/audit_specs.py --strict`

## Open Questions

- Should `verify.sh` also build a wheel to catch packaging regressions?
- Should the audit run as a pre-push hook as well as a pre-commit hook?

## Change Log

| Date | Author | RFC 2119 level changed | Rationale |
| --- | --- | --- | --- |
| 2026-11-16 | Pilot | Initial | Audit, benchmark, and verification helpers. |
