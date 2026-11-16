# ADR 0002: No automatic publishing

- **Status:** Accepted
- **Date:** 2026-11-16
- **Deciders:** Pilot, Risk Spotter

## Context

A generated meme can be funny, wrong, or defamatory. YouTube publishing is public and
difficult to undo at scale. The first version has no OAuth flow, no channel credentials,
and no upload client. The value is the review-ready package, not autonomous publishing.

## Decision

NewsMemeAI YouTube MUST NOT upload, schedule, or publish to YouTube in v0.1. Every
package MUST default to `privacy_status: private`. The manifest MUST record a review
status of `draft`. A human reviewer MUST complete `REVIEW.md` before any future upload
step. Any future publisher MUST require an explicit human action and MUST NOT be wired
to a feed trigger.

## Consequences

- The product cannot accidentally publish a hallucinated claim.
- The upload workflow remains manual and therefore slower.
- A future upload feature needs its own ADR, OAuth design, and risk review.
- The package format can stay platform-neutral.

## Related ADRs

- ADR-0004 (SVG-first storyboards)
- ADR-0003 (specs in repo)
