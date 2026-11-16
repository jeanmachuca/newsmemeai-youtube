# Changelog

All notable changes to NewsMemeAI YouTube are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] — 2026-11-16

### Fixed

- `validate` now enforces the exact seven-artifact manifest contract: missing,
  unexpected, and renamed artifacts are rejected, along with checksum and byte-size
  mismatches.
- `validate` now rejects metadata that is not `privacy_status: private`,
  `made_for_kids: false`, `shorts: true`, and `category_id: "24"`.
- `validate` now rejects a manifest whose review status is anything other than `draft`,
  whose generator identity is wrong, or whose frame/thumbnail dimensions are wrong.
- `manifest.schema.json` now caps `files` at seven properties, requires all seven names,
  and restricts property names to the artifact enum.
- Added four validator tests (77 total) covering public metadata, approved review,
  extra manifest artifacts, and wrong dimensions.

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

[0.1.1]: https://github.com/jeanmachuca/newsmemeai-youtube/releases/tag/v0.1.1
[0.1.0]: https://github.com/jeanmachuca/newsmemeai-youtube/releases/tag/v0.1.0
