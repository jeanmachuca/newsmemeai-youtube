# Requirements

## Scope

This document defines the v0.1 functional and non-functional requirements for the
NewsMemeAI YouTube CLI and package format. Each requirement has a unique ID, an RFC 2119
level, and a verification method.

## Normative Statements (RFC 2119)

- Every functional requirement MUST have a unique `FR-NNN` identifier.
- Every non-functional requirement MUST have a unique `NFR-NNN` identifier.
- Every requirement MUST declare an RFC 2119 level and a verification method.
- Every user story in `02-prd/` MUST map to at least one FR.
- The implementation MUST NOT claim a requirement is met without a test or documented
  manual check.

## Functional requirements

| ID | Level | Requirement | Verification |
| --- | --- | --- | --- |
| FR-001 | MUST | The CLI MUST provide a `headlines` command that lists numbered headlines with source and timestamp. | `test_cli.py::test_headlines_human_output` |
| FR-002 | MUST | The CLI MUST provide a `build` command that turns one selected headline into a package directory. | `test_cli.py::test_build_and_validate` |
| FR-003 | MUST | Feed input MUST accept HTTP(S) URLs and local file paths. | `test_feeds.py::test_fetch_local_file`, `test_fetch_bad_url` |
| FR-004 | MUST | The parser MUST support RSS 2.0 and Atom 1.0 and MUST deduplicate by case-folded title. | `test_feeds.py::test_parse_rss`, `test_parse_atom` |
| FR-005 | MUST | The script engine MUST provide a deterministic template path when AI is disabled. | `test_script.py::test_template_script_is_deterministic` |
| FR-006 | MAY | The script engine MAY call an OpenAI-compatible endpoint when base URL and model are configured. | `test_script.py::test_generate_script_uses_model_when_configured` |
| FR-007 | MUST | A package MUST contain three vertical frames, one thumbnail, `script.md`, `metadata.json`, `REVIEW.md`, and `manifest.json`. | `test_package.py::test_build_package_creates_all_artifacts` |
| FR-008 | MUST | The manifest MUST include a SHA-256 digest and byte size for every required artifact. | `test_package.py::test_build_package_creates_all_artifacts` |
| FR-009 | MUST | The CLI MUST provide a `validate` command that rejects missing, unexpected, or renamed manifest artifacts, checksum or size mismatches, unsafe paths, invalid manifest identity, non-private metadata, and a non-draft review status. | `test_validate.py::test_tampered_artifact_is_detected`, `test_missing_artifact_is_detected`, `test_extra_manifest_artifact_is_detected`, `test_public_metadata_is_detected`, `test_approved_review_is_detected`, `test_wrong_dimensions_are_detected` |
| FR-010 | MUST | The system MUST NOT upload, schedule, or publish to YouTube in v0.1; packages MUST default to private and `validate` MUST reject metadata that is not private. | `test_package.py::test_youtube_metadata_limits`, `test_validate.py::test_public_metadata_is_detected` |
| FR-011 | MUST | Untrusted headline, summary, and model text MUST be escaped before entering SVG or JSON. | `test_render.py::test_story_frame_dimensions_and_escaping` |
| FR-012 | MUST | The manifest MUST record the source headline, link, feed location, and publication timestamp. | `test_package.py::test_build_package_creates_all_artifacts` |
| FR-013 | MUST | Feed, model, package, and validation errors MUST produce a non-zero exit code and a human-readable message. | `test_cli.py::test_missing_feed`, `test_build_index_out_of_range` |
| FR-014 | MUST | Generated metadata MUST respect YouTube limits: title ≤100, description ≤5000, tag budget ≤500 characters. | `test_package.py::test_youtube_metadata_limits` |
| FR-015 | SHOULD | `headlines` and `build` SHOULD support `--json` for machine-readable automation. | `test_cli.py::test_headlines_json`, `test_build_and_validate` |
| FR-016 | MUST | Invalid or over-limit model output MUST be rejected rather than silently truncated. | `test_script.py::test_parse_script_rejects_bad_payloads` |

## Non-functional requirements

| ID | Level | Requirement | Verification |
| --- | --- | --- | --- |
| NFR-001 | SHOULD | `build --no-llm` SHOULD complete in under 2 seconds for one headline on a 2-core runner, excluding feed network time. | `scripts/benchmark.py` |
| NFR-002 | MUST | The repository MUST NOT contain credentials; LLM secrets MUST come from environment variables. | secret scan, `.env.example`, review |
| NFR-003 | MUST | The same input, style, and version MUST produce identical artifact checksums. | `test_package.py::test_build_is_deterministic` |
| NFR-004 | MUST | CI MUST run ruff, mypy, pytest, and the spec audit on Python 3.11–3.13. | `.github/workflows/ci.yml` |
| NFR-005 | MUST | The product MUST remain MIT-licensed and MUST NOT collect PII or telemetry. | `LICENSE`, code review |
| NFR-006 | MUST | The runtime MUST have zero third-party dependencies and no native build step. | `requirements.txt`, `pyproject.toml` |
| NFR-007 | SHOULD | SVG artifacts SHOULD include accessible `<title>` and `<desc>` elements and readable contrast. | `test_render.py` |
| NFR-008 | SHOULD | The CLI SHOULD expose structured JSON output and documented exit codes. | `test_cli.py` |

## NFR coverage

| Category | Requirements |
| --- | --- |
| Performance | NFR-001 |
| Security | NFR-002 |
| Reliability | NFR-003 |
| Operability | NFR-004, NFR-008 |
| Compliance | NFR-005 |

## User-story traceability

| User story | Functional requirements |
| --- | --- |
| US-001 | FR-001, FR-003, FR-004, FR-013, FR-015 |
| US-002 | FR-002, FR-007, FR-008, FR-010, FR-012 |
| US-003 | FR-005, FR-013, FR-015 |
| US-004 | FR-009, FR-011, FR-013 |
| US-005 | FR-006, FR-013, FR-016 |
| US-006 | FR-010, FR-012, NFR-002, NFR-005 |

## Open Questions

- Is the 2-second NFR measured on GitHub's standard runner or on a reference laptop?
- Should `validate` check the editorial review checklist state, or only file integrity?
- Should a future upload path be a separate package or an extra command?

## Change Log

| Date | Author | RFC 2119 level changed | Rationale |
| --- | --- | --- | --- |
| 2026-11-16 | Pilot | Initial | v0.1 FR/NFR baseline with test-level verification. |
| 2026-11-16 | Pilot | FR-009, FR-010 tightened | v0.1.1 closes the exact-seven-artifact and private/draft validation gap. |
