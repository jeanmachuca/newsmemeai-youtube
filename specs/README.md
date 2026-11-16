# NewsMemeAI YouTube — Specification Index

This repository is the source of truth for **what** NewsMemeAI YouTube MUST do.
The application source is the source of truth for **how** it does it.

## WHAT

> Turn one news headline into a review-ready YouTube Shorts package: three vertical
> storyboard frames, a thumbnail, a three-beat script, YouTube metadata, a human review
> checklist, and a checksummed manifest — without publishing automatically.

## INIT

- **Status:** INIT executed 2026-11-16.
- **Product:** NewsMemeAI YouTube.
- **Owner model:** standalone single-owner model (see `01-product-vision/org-structure.md`).
- **Language and runtime:** Python 3.11+, standard library only at runtime.
- **Specs location:** in this repository under `specs/`. ADR-0003 records the deviation
  from the SPECv1 recommendation to use a dedicated specs repository.
- **Release target:** v0.1.0, private/draft packages only.

## RFC 2119 legend

| Keyword | Level | Meaning |
| --- | --- | --- |
| MUST / REQUIRED / SHALL | Absolute | The implementation is not conformant without it. |
| MUST NOT / SHALL NOT | Absolute | The implementation is not conformant if it does it. |
| SHOULD / RECOMMENDED | Strong | Default expectation; departures need a recorded reason. |
| SHOULD NOT / NOT RECOMMENDED | Strong | Default prohibition; departures need a recorded reason. |
| MAY / OPTIONAL | Discretionary | Genuine choice. |

Lowercase variants are not normative. Every requirement in `05-requirements/` uses a
capitalized keyword.

## Folder index

| # | Folder | Primary artifact |
| --- | --- | --- |
| 01 | [Product vision](01-product-vision/vision.md) | Problem, opportunity, personas, metrics |
| 02 | [PRD](02-prd/prd.md) | Goals, non-goals, user stories, acceptance |
| 03 | [Architecture](03-architecture/architecture.md) | Components, boundaries, data flow, deployment |
| 04 | [ADRs](04-adrs/README.md) | Durable architecture decisions |
| 05 | [Requirements](05-requirements/requirements.md) | FRs and NFRs with RFC 2119 levels |
| 06 | [Schemas](06-schemas/schemas.md) | Manifest and metadata contracts |
| 07 | [SDLC](07-sdlc/sdlc.md) | Phases, gates, branching, release |
| 08 | [Code conventions](08-code-conventions/conventions.md) | Naming, lint, types, review |
| 09 | [Housekeeping](09-housekeeping/housekeeping.md) | Dependencies, secrets, branches, spec review |
| 10 | [Script helpers](10-script-helpers/scripts.md) | Audit, benchmark, verify scripts |
| 11 | [Implementation plan](11-implementation-plan/plan.md) | Milestones, dependencies, rollback, traceability |

## Pre-INIT decisions

1. **Dedicated specs repository?** The user requested one repository named
   `newsmemeai-youtube`; therefore the specs live in `specs/`. ADR-0003 records this.
2. **Organization context?** The product is standalone. It uses the SPECv1 single-owner
   model: one human MAY hold all decision seats, but each seat's decision right is named
   in `01-product-vision/org-structure.md`.
3. **No assumptions hidden:** the product scope, runtime, and no-auto-publish boundary
   are written in `MISSION.md`, this index, and `05-requirements/requirements.md`.

## Audit

```bash
python scripts/audit_specs.py --strict
python scripts/audit_specs.py --strict --write-report
```

The audit checks folder integrity, the minimum schema, RFC 2119 usage, requirement IDs,
user-story traceability, ADR structure, schema validity, and implementation drift. The
latest report is `AUDIT-REPORT.md`.

## Change log

| Date | Author | Change | Rationale |
| --- | --- | --- | --- |
| 2026-11-16 | Pilot | Initial SPECv1 tree and INIT record | Start the process-compliant repository. |
