# Changelog

All notable changes to NewsMemeAI YouTube are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] — 2026-11-16

### Added

- `newsmemeai-youtube headlines`: RSS 2.0 / Atom ingestion from HTTP(S) or local files,
  with deduplication and JSON output.
- `newsmemeai-youtube build`: one headline → three 1080×1920 SVG storyboard frames, a
  1280×720 thumbnail, a three-beat `script.md`, YouTube `metadata.json`, `REVIEW.md`, and
  a SHA-256 `manifest.json`.
- `newsmemeai-youtube validate`: manifest shape, path safety, byte sizes, checksums, and
  YouTube metadata limits.
- Deterministic `--no-llm` template path and an optional OpenAI-compatible drafting path
  with strict response validation.
- SPECv1 tree (`specs/01`–`11`), strict audit script, and generated audit report.
- Mission Script, HUD, squad model, Pit Stop ritual, IRA guide, review checklists.
- GitHub Actions CI on Python 3.11–3.13, auto-PR to `development`, and a release-PR
  source guard.
- 73 offline tests covering feeds, scripts, rendering, packages, validation, CLI, and
  the spec audit.

### Security

- No upload, scheduling, or publishing path exists in v0.1.
- Every package defaults to `privacy_status: private` and `review.status: draft`.
- Feed and model text is escaped before entering SVG or JSON.
- No runtime third-party dependencies.

[0.1.0]: https://github.com/jeanmachuca/newsmemeai-youtube/releases/tag/v0.1.0
