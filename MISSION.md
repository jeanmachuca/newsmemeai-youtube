# Mission Script — NewsMemeAI YouTube v0.1

> A Mission Script is a technical specification of intent: poetic enough that a human
> feels the Vibe, precise enough that an agent can execute it without guessing.

## 1. Mission Name

**One headline → one review-ready Shorts package.** The package is complete, traceable,
legible, and private until a human says otherwise.

## 2. Frequency

**Stealth / Precision.** This product touches published media, source attribution, and
public reputation. Correctness outranks volume. When the machine is unsure, it MUST
refuse or mark the package as draft rather than invent a fact.

## 3. Outcome

By the end of v0.1.0:

- `newsmemeai-youtube build` turns one selected headline into a package containing
  **3 vertical storyboard frames, 1 thumbnail, 1 script, 1 metadata file, 1 review
  checklist, and 1 checksummed manifest** — 7 required artifacts plus the manifest.
- `newsmemeai-youtube validate` exits `0` on an intact package and `1` on a tampered,
  missing, or unsafe artifact.
- The deterministic path (`--no-llm`) produces **byte-identical artifacts** for the same
  input, style, and version, with a median build time **under 2 seconds** on a 2-core
  runner, excluding feed network time.
- **Zero automatic publishes.** No YouTube credentials, no OAuth flow, no upload client.
- The repository is process-compliant: 11 SPECv1 folders, a passing strict audit, a
  Mission Script, a HUD, a named squad, and a Pit Stop ritual.

## 4. Constraints

These are stated first because they are the frame:

1. **MUST NOT upload, schedule, or publish to YouTube in v0.1.** Every package is
   `privacy_status: private` and every manifest records `review.status: draft`.
2. **MUST NOT invent facts, numbers, names, or quotes.** The script engine may use only
   the headline and summary as source material.
3. **MUST NOT add a runtime third-party dependency.** Python 3.11+ standard library only.
4. **MUST NOT require a database, server, cloud service, or secret for the default path.**
5. **MUST NOT commit directly to `main` or `development`.** Topic branch → PR →
   `development` → release PR → `main` → annotated `v0.1.0` tag.
6. **MUST NOT use rebase or force-push** on shared branches.
7. **MUST NOT embed remote content or scripts in generated SVG.**
8. **MUST treat feed and model text as untrusted data** and escape it before rendering.
9. **MUST keep the license MIT** and collect no PII or telemetry.

## 5. Acceptance

The mission is accepted when all of the following are true:

| Check | Bar |
| --- | --- |
| Package completeness | 7/7 required artifacts plus `manifest.json` |
| Determinism | Identical checksums across repeated `--no-llm` builds |
| Integrity | `validate` detects tampering, missing files, unsafe paths, bad sizes |
| Review gate | `REVIEW.md` is present and manifest status is `draft` |
| Privacy | `privacy_status: private`, `made_for_kids: false` |
| Spec audit | `python scripts/audit_specs.py --strict` passes |
| CI | ruff, format, mypy, pytest, audit green on Python 3.11, 3.12, 3.13 |
| Process | PR into `development` merged; release PR into `main` merged; `v0.1.0` tagged |
| Documentation | `MISSION.md`, `HUD.md`, `README.md`, `AGENTS.md`, `docs/` complete |

## 6. Verification

Run these commands from the repository root. Every one MUST pass before the release PR:

```bash
ruff check .
ruff format --check .
mypy src/
pytest -v
python scripts/audit_specs.py --strict
python scripts/benchmark.py --runs 5
bash scripts/verify.sh
```

Package-level smoke check:

```bash
PYTHONPATH=src python -m newsmemeai_youtube build \
  --feed tests/fixtures/news.xml --no-llm --out /tmp/newsmemeai-pkg
PYTHONPATH=src python -m newsmemeai_youtube validate /tmp/newsmemeai-pkg
```

The Checklist Close is explicit: **does the package contain all seven artifacts, does
`validate` return `OK: 7 files verified`, and did anything publish?** The answer to the
last question MUST be no.

## Prompt Ladder rung

This script is written at the **Behavioural** rung: it names the trigger, the sequence,
the fallbacks, and the refusal. The package contract and the test names are the
**Exemplar** anchor — the implementation is judged against them, not against taste.

## Change Log

| Date | Author | Change | Rationale |
| --- | --- | --- | --- |
| 2026-11-16 | Pilot | Initial Mission Script | Set Stealth/Precision frequency for v0.1. |
