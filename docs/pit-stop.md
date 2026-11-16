# Pit Stop and Vibe Audit

Every Lap ends with a Pit Stop. Every month the Pit Stop deepens into a Vibe Audit. Both
are calibration rituals: they ask whether the right things are on the scoreboard, not
whether everyone is busy.

## The Pit Stop (end of every Lap)

### 1. Review

- Grade the Lap against `MISSION.md`: did the package, PR, or release hit the Vibe?
- Read the HUD: IRA, Circuit Delta, Hallucination Debt.
- Name one thing that drifted and one thing that compounded.

**Prompt:** *"Against the Mission Script, what did the machine deliver exactly, what did
it approximate, and what did it invent?"*

### 2. Refuel

- Was the drift a **data** problem, a **prompt/script** problem, or a **tooling** problem?
- The Vibe is the usual suspect. Rewrite the Mission Script or the affected spec before
  re-running the same prompt.
- Update the HUD baseline only when a deliberate process change lands.

### 3. Restart

- Launch the next Lap immediately with a scoped intent.
- Record the decision in the log below.
- If a red trigger fired, the named owner freezes the affected path first; the next Lap
  starts with the fix, not with new scope.

## Traction vs Velocity sanity check

| Question | Bad answer | Good answer |
| --- | --- | --- |
| Did we produce more packages? | "42 builds in a minute." | "Five packages reviewed and accepted." |
| Did the output move the goal? | "The model wrote 1,000 hooks." | "IRA ≥ 95% with zero open claims." |
| Did the process get faster? | "We skipped review to ship." | "Circuit Delta negative with debt 0." |

Volume is a speedometer; Traction is the compass. A fast Lap in the wrong direction is a
crash with better latency.

## The Monthly Vibe Audit

### Check 1 — The HUD

- Are IRA, Circuit Delta, and Hallucination Debt still predicting value?
- Is any metric now theater (measured because it is easy, not because it decides)?
- Is the HUD current and visible to observers?

### Check 2 — The Squad

- Are all four specialist seats assigned and covered?
- Is the Double Tenaza too tight — are reviews burning out the humans?
- Is the Bridge actually dead, or did a status meeting reappear?

### Check 3 — The Script

- Has the market or the channel moved?
- Does `MISSION.md` still describe the product we are building?
- Does the Frequency still match the risk (Stealth/Precision until publishing exists)?

## The Pilot's Final Checklist

Run at kickoff, quarter start, release, or after significant drift.

### 1. The Vibe Calibration

- [ ] `MISSION.md` has all six fields.
- [ ] The Frequency is explicit (Stealth/Precision for v0.1).
- [ ] Outcome and acceptance contain numbers or named artifacts.
- [ ] A human can feel the intent; an agent can execute it without guessing.

### 2. The Garage Inspection

- [ ] `bash scripts/verify.sh` passes.
- [ ] CI is green on Python 3.11, 3.12, and 3.13.
- [ ] `python scripts/audit_specs.py --strict` passes.
- [ ] `python scripts/benchmark.py --runs 5` is under the 2,000 ms guardrail.
- [ ] The HUD is visible to observers.
- [ ] Privacy Shield: **N/A in v0.1** — no PII, no telemetry, no audience data. Revisit
      before any analytics feature.

### 3. The Diamond Squad Roll Call

- [ ] Pilot, Ops Mechanic, Logic Navigator, Creative Pilot, and Risk Spotter are assigned.
- [ ] Each seat has a named decision right and evidence path.
- [ ] The Publisher NPC is dormant; no upload code or credential exists.
- [ ] The Bridge is dead: observers read the HUD, not a summary deck.

### 4. The Double Tenaza Grip

- [ ] **Let Go:** the deterministic path, tests, CI, and validator run without a human.
- [ ] **Grip:** IRA, Circuit Delta, and debt triggers name an owner and an action.
- [ ] The Risk Spotter veto is respected without a second vote.
- [ ] A red band freezes work before new scope is discussed.

### 5. The Circuit Delta Target

- [ ] The machine baseline is recorded (`median_ms` from the benchmark).
- [ ] The review-cycle baseline is recorded from the first three reviewed packages.
- [ ] The next-Lap target is a **negative** Circuit Delta, not more volume.
- [ ] The 2,000 ms build guardrail is unchanged or deliberately revised by ADR.

## Pit Stop log

| Lap | Date | Review | Refuel | Restart | Owner |
| --- | --- | --- | --- | --- | --- |
| L0 | 2026-11-16 | Bootstrap audit: specs, CI, package contract | Fixed drift found by strict audit | v0.1.0 release PR and tag | Pilot |

## Vibe Audit log

| Month | HUD check | Squad check | Script check | Verdict |
| --- | --- | --- | --- | --- |
| 2026-11 | Three signals defined; baseline pending | Five seats assigned; Bridge dead | v0.1 script matches scope | PASS (bootstrap) |

## Change Log

| Date | Author | Change | Rationale |
| --- | --- | --- | --- |
| 2026-11-16 | Pilot | Initial ritual and checklist | Apply pit-stop-audit to v0.1. |
