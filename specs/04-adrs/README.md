# Architecture Decision Records

## Scope

This folder records durable decisions that shape NewsMemeAI YouTube. Each ADR follows
the SPECv1 structure: Title, Status, Context, Decision, Consequences, Related ADRs.

## Normative Statements (RFC 2119)

- Every architecture decision MUST be recorded as an ADR before implementation.
- Every ADR MUST declare a status from Proposed, Accepted, Deprecated, or Superseded.
- Every accepted ADR MUST use RFC 2119 language in its Decision section.
- A superseded ADR MUST remain in the repository with a link to its replacement.

## Index

| ADR | Title | Status |
| --- | --- | --- |
| [0001](0001-stdlib-first-runtime.md) | Stdlib-first runtime | Accepted |
| [0002](0002-no-auto-publish.md) | No automatic publishing | Accepted |
| [0003](0003-specs-in-repo.md) | Specs live in this repository | Accepted |
| [0004](0004-svg-first-storyboards.md) | SVG-first storyboards | Accepted |

## Open Questions

- Which ADR format tool, if any, should render this folder as a website?
- Should future ADRs be signed by the Risk Spotter when they change data handling?

## Change Log

| Date | Author | RFC 2119 level changed | Rationale |
| --- | --- | --- | --- |
| 2026-11-16 | Pilot | Initial | Four decisions for the v0.1 architecture. |
