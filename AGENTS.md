# AGENTS.md — NewsMemeAI YouTube

Instructions for AI coding agents working in this repository. Read this file first, then
`MISSION.md`, `specs/README.md`, and the spec folder that owns the area you will touch.

## Project

NewsMemeAI YouTube turns one news headline into a review-ready YouTube Shorts package.
Runtime is Python 3.11+ standard library only. Specs are in-repo under `specs/`
(ADR-0003). There is no upload path in v0.1.

## Hard boundaries

- Do **not** add automatic publishing, OAuth, or YouTube API calls.
- Do **not** add a runtime third-party dependency without an ADR.
- Do **not** invent facts in generated scripts; only the headline and summary are source.
- Do **not** commit to `main` or `development` directly.
- Do **not** use rebase or force-push on shared branches.
- Do **not** commit secrets, generated packages, or `out/` artifacts.
- Do **not** weaken the spec audit, tests, or validation to make a change pass.

## Git workflow

See [`docs/git-workflow.md`](docs/git-workflow.md) and
[`.opencode/instructions/git-workflow.md`](.opencode/instructions/git-workflow.md).

```bash
git fetch origin
git checkout -b feature/<topic> development
# ... work ...
git add .
git commit -m "feat(scope): imperative summary"
git push -u origin HEAD
gh pr create --base development --fill
```

Topic prefixes: `feature/`, `fix/`, `bugfix/`, `chore/`, `docs/`, `refactor/`, `test/`.
Promotion to `main` uses a release PR. Releases use annotated SemVer tags on `main`.

## Commands

| Action | Command |
| --- | --- |
| Install (editable + dev) | `pip install -e '.[dev]'` |
| Install dev tools only | `pip install -r dev-requirements.txt` |
| Install hooks | `pre-commit install` |
| Lint | `ruff check .` |
| Format | `ruff format .` |
| Format check | `ruff format --check .` |
| Type check | `mypy src/` |
| Tests | `pytest -v` |
| Spec audit | `python scripts/audit_specs.py --strict` |
| Benchmark | `python scripts/benchmark.py --runs 5` |
| Full verification | `bash scripts/verify.sh` |
| Smoke build | `PYTHONPATH=src python -m newsmemeai_youtube build --feed tests/fixtures/news.xml --no-llm --out /tmp/pkg` |

## Conventions

- `from __future__ import annotations` in every Python module.
- Full type annotations on public functions; mypy strict over `src/`.
- Ruff line length 100; imports grouped future / stdlib / third-party / local.
- Tests use local XML fixtures; no network in the test suite.
- Public behaviour changes require a spec update and a test.
- Commit subjects: `type(scope): imperative summary`.
- Keep PRs under ~400 changed lines excluding specs and tests.

## Process

- Every Lap ends with a Pit Stop: Review, Refuel, Restart — see `docs/pit-stop.md`.
- The HUD (`HUD.md`) is the scoreboard; do not replace it with a status report.
- A change that alters a MUST requirement updates the matching spec and test together.
- The strict spec audit must pass before a PR can merge.
- Package-level review uses `docs/review-checklist.md` and the generated `REVIEW.md`.

## Where things live

| Path | Contents |
| --- | --- |
| `src/newsmemeai_youtube/` | Runtime package |
| `tests/` | Offline test suite and fixtures |
| `specs/01-product-vision/` … `specs/11-implementation-plan/` | Normative specs |
| `scripts/` | Audit, benchmark, verification helpers |
| `docs/` | Process, workflow, HUD-adjacent documentation |
| `.github/workflows/` | CI, auto-PR, release guard |
