# HUD — NewsMemeAI YouTube

> The scoreboard replaces the status meeting. When telemetry is green, the meeting is
> cancelled. When it drifts, adjust the Vibe and re-run the Lap — do not explain.

## The three signals

| Signal | Question it answers | Source of truth |
| --- | --- | --- |
| **Traction (IRA)** | Did the package match the intent without edits? | `REVIEW.md` decisions per package |
| **Circuit Delta** | Are we producing reviewed packages faster than last Lap? | Lap log + `scripts/benchmark.py` |
| **Hallucination Debt** | Is the machine inventing claims or facts? | `REVIEW.md` claim check + Risk Spotter log |

## 1. Traction — Intent-Result Alignment (IRA)

**Formula**

```
IRA = (artifacts accepted without editorial edits / artifacts reviewed) × 100
```

An artifact is one of the seven required package files. An edit to a caption, frame,
title, description, tag, or checklist counts as a miss for that artifact. A package
rejected outright counts every artifact as a miss.

**Bands**

| Band | IRA | Action | Owner |
| --- | --- | --- | --- |
| Green | ≥ 95% | Stay quiet; hold the Double Tenaza. | Pilot |
| Yellow | 70–94.9% | Investigate the Mission Script before blaming the model. Rewrite the Vibe and re-run. | Pilot + Creative Pilot |
| Red | < 70% | Freeze the affected style or prompt; no new packages until the script is recalibrated. | Creative Pilot |

**Guardrail:** a Lap with zero reviewed packages reports `N/A`, never 100%.

## 2. Circuit Delta

**Primary formula (end-to-end Lap time)**

```
Circuit Delta % = (median current-Lap review minutes − median previous-Lap review minutes)
                  / median previous-Lap review minutes × 100
```

Negative is winning: the same quality of reviewed package in less time.

**Machine guardrail (deterministic build)**

`python scripts/benchmark.py --runs 5` reports `median_ms` for `build --no-llm`. The
v0.1.0 reference is **1.77 ms** on the build container (NFR-001 allows up to 2 s
excluding feed network time). A regression above **2,000 ms** is a red guardrail
regardless of review time.

**Bands**

| Band | Circuit Delta | Action | Owner |
| --- | --- | --- | --- |
| Green | ≤ −10% | Hold; the Lap is compounding. | Pilot |
| Yellow | −10% to +10% | Inspect the bottleneck: feed selection, review checklist, or package legibility. | Ops Mechanic |
| Red | > +10% | Stop adding scope. Remove one step from the Lap before the next run. | Pilot |

**Baseline:** recorded from the first three reviewed packages. Until then the metric is
`UNBASELINED` and MUST NOT be displayed as green.

## 3. Hallucination Debt

**Formula**

```
Hallucination Debt = open unsupported-claim alerts across all drafts
```

An alert is any claim in a hook, context beat, punchline, title, description, or tag
that is not supported by the headline or summary. The `REVIEW.md` line
`**Hallucination debt:**` is the per-package ledger; the HUD aggregates open alerts.

**Bands**

| Band | Open alerts | Action | Owner |
| --- | --- | --- | --- |
| Green | 0 | Ship the review decision. | Risk Spotter |
| Yellow | 1–3 | Fix the claim or drop it; do not publish. | Risk Spotter |
| Red | ≥ 4 | Freeze the Drafter NPC and the affected style; audit the last five packages. | Risk Spotter (veto) |

**Compounding rule:** an alert open for more than one Lap doubles in weight for the
release decision. Debt is never "accepted"; it is fixed or the package is rejected.

## Escalation triggers

| Trigger | Automatic action | Named owner |
| --- | --- | --- |
| IRA < 70% | Freeze new packages for the affected style | Creative Pilot |
| Circuit Delta > +10% | Scope freeze until one step is removed | Pilot |
| Hallucination Debt ≥ 4 | Freeze the Drafter NPC; audit last five packages | Risk Spotter |
| `validate` fails on a reviewed package | Block release; open a `fix/` branch | Ops Mechanic |
| Strict spec audit fails | Block merge and release | Logic Navigator |
| Any upload code or credential appears | Stop the Lap; revert; security review | Risk Spotter |

Escalation is a named action, not a meeting. The owner acts the moment the band is
crossed.

## View-only observer access

- The HUD lives in this file and is updated at every Pit Stop.
- Anyone who used to receive a status summary gets read access to this file and the CI
  run history instead.
- No vertical reporting. Display the telemetry; do not narrate it.

## Update cadence

| Event | HUD update |
| --- | --- |
| Package reviewed | Append to the Lap log; recompute IRA and debt |
| End of Lap | Record review minutes and Circuit Delta |
| Monthly Vibe Audit | Re-check that the three signals still predict value |
| Release | Record the benchmark baseline and tag |

## Lap log

| Lap | Date | Packages reviewed | IRA % | Median review min | Circuit Delta % | Open debt | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | 2026-11-16 | 0 | N/A | UNBASELINED | UNBASELINED | 0 | Bootstrap; no packages reviewed yet |

## Change Log

| Date | Author | Change | Rationale |
| --- | --- | --- | --- |
| 2026-11-16 | Pilot | Initial HUD | Three signals, bands, and escalation triggers for v0.1. |
