# ADR 0001: Stdlib-first runtime

- **Status:** Accepted
- **Date:** 2026-11-16
- **Deciders:** Pilot, Ops Mechanic

## Context

The package needs to fetch feeds, draft text, render SVG, and validate checksums. A
conventional stack would add `feedparser`, `requests`, `Pillow`, and a JSON-schema
library. Those are useful, but each expands the install surface and the supply-chain
risk for a tool that must run in a small CI job and on a creator's laptop.

## Decision

The runtime package MUST depend only on the Python standard library on Python 3.11+.
The implementation MUST use `urllib.request`, `xml.etree.ElementTree`, `json`,
`hashlib`, and text/SVG rendering. Developer tools MAY be declared as extras. A future
raster or video renderer MUST be introduced as an optional extra, not a core dependency.

## Consequences

- Installation is fast and has no native build step.
- Feed edge cases remain our responsibility.
- SVG is the primary visual format; PNG/MP4 require an external tool.
- `xml.etree` is not hardened against every entity-expansion attack. The product only
  reads feeds chosen by the operator and MUST NOT accept arbitrary XML uploads.

## Related ADRs

- ADR-0004 (SVG-first storyboards)
- ADR-0003 (specs in repo)
