# Implementation Plan

## Scope

This plan covers v0.1.0: the process-compliant repository, deterministic package builder,
optional AI script path, validation, and CI. Upload, video encoding, and a web UI are
future work.

## Normative Statements (RFC 2119)

- The release MUST NOT ship unless every FR in the traceability matrix has a passing test
  or a documented manual check.
- Milestone M0 MUST be merged before implementation work begins.
- Every milestone MUST include a rollback path and a verification command.
- The traceability matrix MUST link every FR to a milestone and a verification artifact.
- A milestone that changes a requirement MUST update the relevant spec folder first.

## Milestones

| Milestone | Scope | Estimate | Verification |
| --- | --- | --- | --- |
| M0 — Process bootstrap | Mission Script, specs, policy docs, repo bootstrap PR | 1 day | Spec audit PASS; release PR merged; v0.1.0 tagged |
| M1 — Core package builder | Feeds, template script, renderer, package writer | 1–2 days | Package tests and CLI build test |
| M2 — AI and validation | LLM path, response parser, validate command | 1 day | Script and validation tests |
| M3 — CI and operations | CI matrix, spec audit, benchmark, pre-commit | 0.5 day | Green CI; audit report |
| M4 — Manual upload (future) | OAuth, review gate, upload command | Not in v0.1 | Separate ADR and PR |

## Dependencies

- M0 depends on the user naming the repository and the no-auto-publish boundary.
- M1 depends on M0's schema and artifact list.
- M2 depends on M1's script and metadata contracts.
- M3 depends on M0's audit script and M1/M2's tests.
- M4 is blocked until a dedicated publishing ADR is accepted.

## Resource estimates

| Role | M0 | M1 | M2 | M3 |
| --- | --- | --- | --- | --- |
| Pilot | 0.5d | 0.25d | 0.25d | 0.25d |
| Ops Mechanic | 0.25d | 0.5d | 0.25d | 0.5d |
| Logic Navigator | 0.25d | 0.25d | 0.25d | 0.25d |
| Creative Pilot | 0.25d | 0.5d | 0.25d | 0d |
| Risk Spotter | 0.25d | 0.25d | 0.25d | 0.25d |

Single-owner model: one human MAY hold several roles, so the calendar estimate is 3–4
working days, not the sum of role columns.

## Rollback strategy

- **Spec regression:** revert the spec commit on `development`; the audit fails first.
- **Code regression:** revert the merge commit with `git revert`; never rebase.
- **Bad release:** tag a patch on `main` after a fix PR; do not move an existing tag.
- **Bad package:** delete the local package directory; the source feed is untouched.
- **Secret exposure:** rotate the secret, revoke the token, then rewrite the incident
  note outside the repository if it contains sensitive details.

## Traceability matrix

| Requirement | Milestone | Verification |
| --- | --- | --- |
| FR-001 | M1 | `test_cli.py::test_headlines_human_output` |
| FR-002 | M1 | `test_cli.py::test_build_and_validate` |
| FR-003 | M1 | `test_feeds.py::test_fetch_local_file` |
| FR-004 | M1 | `test_feeds.py::test_parse_rss`, `test_parse_atom` |
| FR-005 | M1 | `test_script.py::test_template_script_is_deterministic` |
| FR-006 | M2 | `test_script.py::test_generate_script_uses_model_when_configured` |
| FR-007 | M1 | `test_package.py::test_build_package_creates_all_artifacts` |
| FR-008 | M1 | `test_package.py::test_build_package_creates_all_artifacts` |
| FR-009 | M2 | `test_validate.py` |
| FR-010 | M1 | `test_package.py::test_youtube_metadata_limits` |
| FR-011 | M1 | `test_render.py::test_story_frame_dimensions_and_escaping` |
| FR-012 | M1 | `test_package.py::test_build_package_creates_all_artifacts` |
| FR-013 | M2 | `test_cli.py::test_missing_feed` |
| FR-014 | M1 | `test_package.py::test_youtube_metadata_limits` |
| FR-015 | M1 | `test_cli.py::test_headlines_json` |
| FR-016 | M2 | `test_script.py::test_parse_script_rejects_bad_payloads` |
| NFR-001 | M3 | `scripts/benchmark.py` |
| NFR-002 | M3 | secret scan and review |
| NFR-003 | M1 | `test_package.py::test_build_is_deterministic` |
| NFR-004 | M3 | `.github/workflows/ci.yml` |
| NFR-005 | M0 | `LICENSE` and review |
| NFR-006 | M1 | `requirements.txt` and review |
| NFR-007 | M1 | `test_render.py` |
| NFR-008 | M2 | `test_cli.py` |

## Drift backlog

No drift items at INIT. The audit script will append findings here if implementation and
specs diverge.

## Open Questions

- Should M4 be a separate repository to keep OAuth credentials out of the builder?
- Which channel should receive the first manual upload after v0.1?

## Change Log

| Date | Author | RFC 2119 level changed | Rationale |
| --- | --- | --- | --- |
| 2026-11-16 | Pilot | Initial | v0.1 milestones, estimates, rollback, traceability. |
