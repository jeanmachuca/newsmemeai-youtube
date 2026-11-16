# ADR 0003: Specs live in this repository

- **Status:** Accepted
- **Date:** 2026-11-16
- **Deciders:** Pilot

## Context

SPECv1 recommends a dedicated specifications repository so specs can evolve separately
from code. The user requested one repository named `newsmemeai-youtube`. Creating a
second repository would add coordination overhead before the product has a team or a
release cadence.

## Decision

The specifications MUST live in `specs/` inside this repository for v0.1. The audit
script MUST treat this tree as the source of truth for requirements. The Pilot SHOULD
revisit this decision when a second contributor or an independent spec review cadence
appears. If the specs move, the existing folders MUST be archived with a superseding
ADR and the README MUST link to the new repository.

## Consequences

- One clone gives a contributor both the process and the implementation.
- Spec changes and code changes can be reviewed in one PR.
- The repository is larger and mixes normative and implementation history.
- The audit script becomes the guardrail that a separate specs repo would otherwise
  provide through repository boundaries.

## Related ADRs

- ADR-0001 (stdlib-first runtime)
- ADR-0002 (no automatic publishing)
