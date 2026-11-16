# ADR 0004: SVG-first storyboards

- **Status:** Accepted
- **Date:** 2026-11-16
- **Deciders:** Creative Pilot, Ops Mechanic

## Context

The package needs visual beats without a video encoder or a native image library. PNG
would require Pillow or a system tool. MP4 would require ffmpeg. Both add runtime and CI
surface before the package contract is stable. SVG is text, diffable, scalable, and
renderable in every browser.

## Decision

The v0.1 renderer MUST produce SVG at 1080×1920 for storyboard frames and 1280×720 for
the thumbnail. The renderer MUST embed all text and styles in the document and MUST NOT
reference remote images or scripts. The package writer MUST treat the SVGs as the
canonical visual artifacts. A future raster or MP4 renderer MUST consume the package
without changing the SVG contract.

## Consequences

- Visual artifacts are testable by parsing XML and asserting escaped text.
- There is no native dependency and no font binary in the repository.
- YouTube upload needs a separate conversion step.
- Fonts depend on the viewer's environment; the design MUST remain legible with generic
  fallbacks such as Impact, Arial Black, and sans-serif.

## Related ADRs

- ADR-0001 (stdlib-first runtime)
- ADR-0002 (no automatic publishing)
