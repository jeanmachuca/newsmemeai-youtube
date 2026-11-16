# NewsMemeAI YouTube

Turn one news headline into a **review-ready YouTube Shorts package** — three vertical
storyboard frames, a thumbnail, a three-beat script, YouTube metadata, a human review
checklist, and a checksummed manifest.

**No automatic publishing.** v0.1 builds a private, draft package and stops there.

[![CI](https://github.com/jeanmachuca/newsmemeai-youtube/actions/workflows/ci.yml/badge.svg?branch=development)](https://github.com/jeanmachuca/newsmemeai-youtube/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](pyproject.toml)

## Why

The blank page is the bottleneck, not the upload button. NewsMemeAI YouTube removes the
mechanical work — pick a headline, shape a hook, lay out the beats, prepare metadata —
and leaves the judgment call to a human. Every package carries its source and a SHA-256
manifest so review starts from evidence, not vibes.

## Quick start

```bash
git clone git@github.com:jeanmachuca/newsmemeai-youtube.git
cd newsmemeai-youtube
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

List headlines from the bundled offline fixture:

```bash
newsmemeai-youtube headlines --feed tests/fixtures/news.xml
```

Build a package without any model call:

```bash
newsmemeai-youtube build \
  --feed tests/fixtures/news.xml \
  --index 1 \
  --no-llm \
  --out out/robots-pizza
```

Validate it:

```bash
newsmemeai-youtube validate out/robots-pizza
# OK: 7 files verified in .../out/robots-pizza
```

No install needed for a smoke test:

```bash
PYTHONPATH=src python3 -m newsmemeai_youtube headlines --feed tests/fixtures/news.xml
```

## What the package contains

| File | Purpose |
| --- | --- |
| `frame-01-hook.svg` | 1080×1920 hook frame (0–3s) |
| `frame-02-context.svg` | 1080×1920 factual beat (3–8s) |
| `frame-03-punchline.svg` | 1080×1920 reaction + CTA (8–12s) |
| `thumbnail.svg` | 1280×720 YouTube thumbnail |
| `script.md` | Three-beat script, rationale, production notes |
| `metadata.json` | Title, description, tags, `privacy_status: private` |
| `REVIEW.md` | Human checklist; any unchecked item blocks release |
| `manifest.json` | Provenance, dimensions, SHA-256 and byte size per artifact |

## Commands

| Command | What it does |
| --- | --- |
| `newsmemeai-youtube headlines [--feed URL_OR_PATH] [--json]` | List numbered headlines with source and timestamp |
| `newsmemeai-youtube build [--feed ...] [--index N] [--style classic\|reaction\|headline] [--no-llm] [--out DIR] [--json]` | Build a complete package |
| `newsmemeai-youtube validate DIR [--json]` | Verify manifest, paths, sizes, checksums, and metadata limits |

Exit codes: `0` success, `1` expected failure (bad feed, invalid package, out-of-range
index), `2` usage error.

### Optional AI drafting

The deterministic template is the default fallback. To use an OpenAI-compatible chat
endpoint, set:

```bash
export NEWSMEMEAI_YOUTUBE_BASE_URL=http://localhost:11434/v1
export NEWSMEMEAI_YOUTUBE_MODEL=llama3.2
# export NEWSMEMEAI_YOUTUBE_API_KEY=...
# export NEWSMEMEAI_YOUTUBE_TIMEOUT=30
```

`--no-llm` overrides the configuration and makes the build deterministic. Invalid or
over-limit model output is rejected; it is never silently truncated.

## Guarantees

- **Private by default** — packages are drafts; there is no upload client or credential.
- **Fact-bounded** — the script engine uses only the headline and summary.
- **Escaped output** — feed and model text is HTML-escaped before entering SVG or JSON.
- **Tamper-evident** — `validate` rejects missing files, checksum mismatches, unsafe
  paths, and metadata limit violations.
- **Zero runtime dependencies** — Python 3.11+ standard library only.
- **Deterministic** — identical input, style, and version produce identical checksums.

## Process

This repository is run as a Vibe Leading project, not an ad-hoc code dump:

| Artifact | What it covers |
| --- | --- |
| [`MISSION.md`](MISSION.md) | Six-field Mission Script; Stealth/Precision frequency |
| [`HUD.md`](HUD.md) | IRA, Circuit Delta, Hallucination Debt, escalation triggers |
| [`specs/`](specs/README.md) | SPECv1 tree: vision, PRD, architecture, ADRs, FR/NFR, schemas, SDLC |
| [`docs/git-workflow.md`](docs/git-workflow.md) | Topic branches, no rebase, SemVer releases |
| [`docs/skills-compliance.md`](docs/skills-compliance.md) | Which skills apply and why some are N/A |
| [`docs/org-structure.md`](docs/org-structure.md) | Pilot + four specialists + NPC agents |
| [`docs/pit-stop.md`](docs/pit-stop.md) | Lap ritual, monthly Vibe Audit, Pilot's Final Checklist |
| [`docs/ira.md`](docs/ira.md) | Seven IRA techniques applied to this repo |
| [`docs/review-checklist.md`](docs/review-checklist.md) | Package and PR review gates |
| [`specs/AUDIT-REPORT.md`](specs/AUDIT-REPORT.md) | Latest strict spec audit |

## Development

```bash
ruff check .
ruff format --check .
mypy src/
pytest -v
python scripts/audit_specs.py --strict
bash scripts/verify.sh
```

CI runs the same checks on Python 3.11, 3.12, and 3.13.

### Repository layout

```
src/newsmemeai_youtube/   # feeds, script, render, package, validate, CLI
tests/                    # 73 offline tests and XML fixtures
specs/                    # SPECv1 folders 01–11 + audit report
scripts/                  # audit_specs.py, benchmark.py, verify.sh
docs/                     # process and workflow documentation
.github/workflows/        # CI, auto-PR, release-PR guard
```

## Contributing

1. Branch from `development` using `feature/`, `fix/`, `bugfix/`, `chore/`, `docs/`,
   `refactor/`, or `test/`.
2. Keep the change scoped; update the affected spec and test.
3. Run `bash scripts/verify.sh`.
4. Open a PR into `development` and complete the PR template.

Releases promote `development` → `main` via a release PR and an annotated SemVer tag.
Rebase is not used in this repository.

## License

MIT — see [LICENSE](LICENSE).
