# Product Requirement Document

## Scope

This PRD covers the v0.1 CLI: headline ingestion, deterministic and optional AI scripts,
package assembly, metadata preparation, and local validation. Public publishing, video
encoding, and channel analytics are out of scope.

## Normative Statements (RFC 2119)

- The PRD MUST define goals, non-goals, user stories, and acceptance criteria for v0.1.
- Every user story MUST map to at least one functional requirement in `05-requirements/`.
- The product MUST keep public publishing behind a human review gate.
- The product MUST expose machine-readable output for automation.
- The product SHOULD be usable offline with `--no-llm`.

## Goals

1. Generate a complete Shorts package from a headline in one command.
2. Keep the source and claim boundary visible in every artifact.
3. Make validation cheap enough to run in CI and before every upload.
4. Support a deterministic path for demos, tests, and low-connectivity environments.
5. Preserve a clean upgrade path to optional AI scripts and future manual upload.

## Non-goals

- Rendering MP4 video or burning captions.
- Uploading to YouTube, OAuth flows, or channel management.
- Automatic fact-checking against the open web.
- Trend prediction, audience analytics, or monetization advice.
- A web UI or multi-tenant service.

## User stories

### US-001 — List headlines

As a creator, I want to list current headlines from one or more feeds so that I can
choose the story worth turning into a Short.

**Acceptance criteria:** the command prints numbered headlines with source and timestamp;
`--json` returns a JSON array; an unreachable feed exits non-zero.

**Maps to:** FR-001, FR-003, FR-004, FR-013, FR-015

### US-002 — Build a package

As a creator, I want to build a package from one headline so that I have a script,
storyboard, thumbnail, and metadata ready for review.

**Acceptance criteria:** the output directory contains all seven required artifacts and
a manifest with SHA-256 checksums; no upload occurs.

**Maps to:** FR-002, FR-007, FR-008, FR-010, FR-012

### US-003 — Work offline

As an operator, I want a deterministic template path so that demos, tests, and CI do not
depend on a model endpoint.

**Acceptance criteria:** `--no-llm` produces byte-identical artifacts for the same input
and version; no network call is made.

**Maps to:** FR-005, FR-013, FR-015

### US-004 — Validate before upload

As a reviewer, I want to validate a package and its checksums so that a corrupted or
incomplete package never reaches a channel.

**Acceptance criteria:** `validate` exits 0 for a valid package; it exits 1 and names
the issue for a tampered, missing, or unsafe artifact.

**Maps to:** FR-009, FR-011, FR-013

### US-005 — Use AI drafting

As a creative lead, I want an optional OpenAI-compatible script path so that I can
improve hooks without changing the package contract.

**Acceptance criteria:** the endpoint is used only when base URL and model are set;
invalid model output is rejected; `--no-llm` overrides the configuration.

**Maps to:** FR-006, FR-013, FR-016

### US-006 — Stay private by default

As a risk owner, I want every generated package to be private and draft-only so that a
model or operator error cannot publish to YouTube.

**Acceptance criteria:** metadata contains `privacy_status: private`; no upload code or
credential requirement exists in v0.1; `REVIEW.md` blocks release until checked.

**Maps to:** FR-010, FR-012, NFR-002, NFR-005

## Stakeholder register

| Seat | Accountable for |
| --- | --- |
| Pilot | Scope, release approval, mission alignment |
| Ops Mechanic | CLI operability, CI, dependency surface |
| Logic Navigator | Requirement IDs, acceptance criteria, traceability |
| Creative Pilot | Hook, context, punchline, thumbnail readability |
| Risk Spotter | Privacy, no-auto-publish, hallucination debt |

## Open Questions

- Should the package include an optional `video.mp4` placeholder in v0.2?
- Which acceptance threshold defines "accepted without caption edits" for the HUD?
- Does the channel need multiple languages in v0.1? Currently out of scope.

## Change Log

| Date | Author | RFC 2119 level changed | Rationale |
| --- | --- | --- | --- |
| 2026-11-16 | Pilot | Initial | v0.1 PRD and user-story traceability. |
