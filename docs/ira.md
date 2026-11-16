# IRA Prompting in This Repository

IRA (Intent-Result Alignment) measures the gap between the Mission Script and the
machine's output. IRA 100% means the artifact is exactly what was intended. IRA 60% means
the machine guessed, drifted, or invented.

This document records how the seven techniques are applied to NewsMemeAI YouTube and how
to score a phase.

## The seven techniques

### 1. Phase Contract

One goal per prompt. The v0.1 bootstrap was split into explicit phases:

| Phase | Single goal | Close artifact |
| --- | --- | --- |
| P1 | Runtime package and tests | `pytest` green |
| P2 | SPECv1 tree | `specs/01`–`11` populated |
| P3 | Process documents | `MISSION.md`, `HUD.md`, `docs/` |
| P4 | CI and audit | `audit_specs.py --strict` green |
| P5 | Release flow | PR merged + `v0.1.0` tagged |

Do not mix "add a feature" with "rewrite the spec" and "fix CI" in one prompt. Split it.

### 2. Delta Prompt

After the first result, describe only the change:

> "Keep `newsmemeai` untouched. Only the new `newsmemeai-youtube` repo changes."

> "The package builds; now add validation only. Do not touch the renderer."

Re-wrapping the whole context invites drift and burns working memory.

### 3. Symptom Report

Describe what is observed; let the agent diagnose.

- **Bad:** "Change the `_clip` function to subtract three from the limit."
- **Good:** "A 100-character YouTube title is rejected by the validator even though the
  generator claims it fits. The failure is in the title path."

- **Bad:** "Rewrite `wrap_text` with a while loop."
- **Good:** "A long unbroken word overflows the SVG frame. The text should wrap inside
  the 1080 px canvas."

### 4. Constraint-First

State the must-nots in the first sentence. The opening line is the frame.

> "**No automatic publishing.** Build a CLI that turns one headline into a private,
> review-ready Shorts package; stop before upload."

> "**Stdlib only at runtime.** Add feed ingestion without adding `feedparser` or
> `requests`."

### 5. Design by Reference

Use the target technology's vocabulary and point at a working example.

> "Use the same auto-PR pattern as
> `.github/workflows/open-pr-to-development.yml`: trigger on `feature/**`, open a PR into
> `development` with `actions/github-script`, skip if an open PR exists."

> "Match the GHW release flow in `docs/git-workflow.md`: release PR, merge commit,
> annotated SemVer tag."

### 6. Pivot Prompt

When the machine is on the wrong track, prescribe the correct approach; skip the lecture.

- **Low:** "No, that's not what I meant. I wanted the specs in the same repo, not a
  second one. You keep creating extra repositories and the request was one repo."
- **High:** "Pivot: specs live in `specs/` in this repository. Do not create a second
  repo. Record the deviation in ADR-0003."

### 7. Checklist Close

Name the artifact and the exact check. Not "does it work?"

> "Run `python scripts/audit_specs.py --strict`. Paste the summary line. Confirm it says
> PASS with zero breaches."

> "Run `newsmemeai-youtube validate /tmp/pkg`. Confirm the output is exactly
> `OK: 7 files verified`."

## Scoring rubric

Score each criterion 0–2. Target **8–10** per phase; below 6 means rewrite the Vibe
instead of re-rolling the prompt.

| Criterion | 0 | 1 | 2 |
| --- | --- | --- | --- |
| **Scope** | Multiple goals, no boundary | One goal, fuzzy boundary | One goal, explicit in/out |
| **Constraints** | None stated | Some limits, late | Must-nots and limits first |
| **Refinement** | No delta; re-explains everything | Partial delta | Delta only, 2–3 sentences |
| **Bug report** | Prescribes code, no symptom | Symptom + guess | Symptom, reproduction, expected |
| **Verification** | "Does it work?" | Vague check | Named artifact + exact command |

### Worked score — v0.1 bootstrap

| Criterion | Score | Evidence |
| --- | --- | --- |
| Scope | 2 | One repo, one release, explicit no-upload boundary |
| Constraints | 2 | No auto-publish, stdlib-only, no direct commits, no rebase stated first |
| Refinement | 2 | Delta prompts kept `newsmemeai` untouched |
| Bug report | 2 | Symptoms named (title limit, wrap overflow, audit findings) before fixes |
| Verification | 2 | `bash scripts/verify.sh`, `validate`, strict audit, tag check |
| **Total** | **10/10** | Ship |

## Working memory

Assume roughly four files and eight turns of reliable recall. Re-reference the Mission
Script, the artifact contract, and the current branch instead of assuming they are still
in context. When a constraint matters, repeat it in the phase that can violate it.

## Change Log

| Date | Author | Change | Rationale |
| --- | --- | --- | --- |
| 2026-11-16 | Pilot | Initial IRA guide and bootstrap score | Apply ira-prompting to v0.1. |
