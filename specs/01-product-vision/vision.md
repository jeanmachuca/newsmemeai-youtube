# Product Vision

## Scope

NewsMemeAI YouTube turns a single news headline into a review-ready YouTube Shorts
package. The product covers ingestion, a three-beat script, storyboard frames, a
thumbnail, metadata, and a checksummed manifest. It does not render video, upload to
YouTube, or publish on its own.

## Normative Statements (RFC 2119)

- The product MUST produce a complete package from one selected headline in one command.
- The product MUST record the source headline and feed location in the package manifest.
- The product MUST require an explicit human review before any public publishing.
- The product MUST NOT upload to YouTube in v0.1.
- The product MUST NOT invent facts that are absent from the headline and summary.
- The product SHOULD produce deterministic artifacts when AI captions are disabled.
- The product SHOULD keep the runtime dependency set empty.
- The product MAY use an OpenAI-compatible endpoint for script drafting when configured.

## Problem

News desks and meme channels see more headlines than they can turn into short-form
video. The repetitive work — choosing a headline, shaping a hook, writing the context,
laying out frames, preparing metadata — is mechanical, but a bad automated package can
publish a false claim or an unreadable frame. The gap is not "more content"; it is a
**review-ready draft** with provenance and a checksum.

## Opportunity

- Shorts are a repeatable publishing surface for news commentary.
- A CLI plus a deterministic package format fits a solo creator, a small squad, and CI.
- Keeping the artifact set text/SVG makes the pipeline auditable and cheap to run.
- A human-gated upload step removes the largest platform and reputational risk.

## Target personas

| Persona | Need | Success signal |
| --- | --- | --- |
| Creator / Pilot | Turn one headline into a package in under two minutes | Package built and reviewed without editing the script |
| Reviewer / Risk Spotter | Verify provenance, claims, metadata, and checksums | Zero hallucination debt; validate exits 0 |
| Ops Mechanic | Run the pipeline in CI or a cron job | Deterministic build, no secrets, clear exit codes |
| Channel editor | Receive a storyboard and script ready for editing | All seven artifacts present and legible |

## Value proposition

NewsMemeAI YouTube removes the blank-page problem while keeping the risky step — public
publishing — under human control. The package is portable: SVG frames, Markdown, and
JSON, with no platform lock-in at build time.

## Success metrics

| Metric | Baseline | Target |
| --- | --- | --- |
| Package completeness | 0 | 100% of builds contain all seven required artifacts |
| Deterministic build time | not measured | median < 2 seconds with `--no-llm` |
| Hallucination debt | 0 | 0 open unsupported claims per reviewed package |
| Review acceptance (IRA) | not measured | ≥ 95% of packages accepted without caption edits |
| Auto-publish incidents | 0 | 0 |

## Open Questions

- Should v0.2 add a manual upload command, or remain an export-only pipeline?
- Which feed categories are in scope for the first channel: general news, tech, or both?
- Should the package include a rendered MP4 preview, or is SVG storyboard enough?

## Change Log

| Date | Author | RFC 2119 level changed | Rationale |
| --- | --- | --- | --- |
| 2026-11-16 | Pilot | Initial | v0.1 vision, metrics, and no-auto-publish boundary. |
