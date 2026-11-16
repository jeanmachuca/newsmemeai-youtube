# Organization Structure

## Scope

NewsMemeAI YouTube is a standalone product. This document records the single-owner
model and the four specialist decision seats. A seat is a **decision right**, not a
headcount requirement; one human MAY hold several seats in v0.1.

## Normative Statements (RFC 2119)

- The Pilot MUST own the Mission Script, the HUD, and the final release decision.
- The Ops Mechanic MUST own CI, local tooling, dependency hygiene, and the Garage.
- The Logic Navigator MUST own the specification tree, requirement IDs, and traceability.
- The Creative Pilot MUST own the caption voice, storyboard language, and thumbnail style.
- The Risk Spotter MUST own the hallucination-debt check, privacy review, and secret policy.
- The Risk Spotter MUST block a release when hallucination debt is greater than zero.
- The Pilot MAY delegate a seat but MUST NOT leave a seat unassigned.
- The team SHOULD record seat changes in the Pit Stop log.

## Seats and decision rights

| Seat | Decision right | Evidence |
| --- | --- | --- |
| Pilot | Vibe, scope, release | `MISSION.md`, `HUD.md`, release PR |
| Ops Mechanic | Runtime, CI, dependencies | `.github/workflows/`, `pyproject.toml` |
| Logic Navigator | Specs, requirements, audit | `specs/`, `scripts/audit_specs.py` |
| Creative Pilot | Script and visual voice | `src/newsmemeai_youtube/script.py`, `render.py` |
| Risk Spotter | Hallucination debt, security | `REVIEW.md`, validation, secret policy |

## NPC agents

| Agent | Workload | Feed |
| --- | --- | --- |
| Researcher NPC | Fetch and rank headlines | RSS/Atom feeds |
| Drafter NPC | Draft script beats and frames | Headline + summary |
| Auditor NPC | Checksums, spec audit, review checklist | Package manifest, spec tree |
| Publisher NPC | Future manual upload, never autonomous | Human-approved package only |

## Escalation path

1. A normative conflict is recorded in the relevant spec folder's **Open Questions**.
2. The Logic Navigator decides whether the conflict is a MUST or SHOULD disagreement.
3. The Pilot resolves scope or priority conflicts.
4. The Risk Spotter can veto a release without a second vote.

## Open Questions

- Will the four seats remain one human through v0.1, or will a second reviewer be added?
- Which seat owns channel analytics once publishing begins?

## Change Log

| Date | Author | RFC 2119 level changed | Rationale |
| --- | --- | --- | --- |
| 2026-11-16 | Pilot | Initial | Standalone single-owner model for v0.1. |
