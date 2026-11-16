# Organizational Geometry

NewsMemeAI YouTube is run as a **5-person racing squad**: one Pilot, four specialist
seats, and a swarm of NPC agents. In v0.1 one human MAY hold several seats; the decision
rights are still named so nothing is orphaned.

## The squad

| Seat | Duty in this product | Decision right | Evidence |
| --- | --- | --- | --- |
| **Pilot** | Sets the Vibe, reads the HUD, runs the Laps, approves releases | Scope, frequency, release | `MISSION.md`, `HUD.md`, release PR |
| **Ops Mechanic** | Maintains the Garage: CLI, CI, dependencies, pre-commit, benchmark | Runtime, CI, dependency surface | `pyproject.toml`, `.github/workflows/`, `scripts/` |
| **Logic Navigator** | Maps intent into specs and measures: FR/NFR IDs, traceability, audit | Specs, requirements, audit verdict | `specs/`, `scripts/audit_specs.py` |
| **Creative Pilot** | Writes the voice: hook, context, punchline, frame and thumbnail legibility | Caption and visual voice | `src/newsmemeai_youtube/script.py`, `render.py` |
| **Risk Spotter** | Watches Hallucination Debt, privacy, secrets, and the no-publish gate | Veto on unsupported claims and any upload path | `REVIEW.md`, `validate.py`, housekeeping policy |

The full normative seat definitions live in
[`specs/01-product-vision/org-structure.md`](../specs/01-product-vision/org-structure.md).

## NPC agents

| Agent | Workload | Feed | Guardrail |
| --- | --- | --- | --- |
| **Researcher NPC** | Fetch, clean, and deduplicate headlines | RSS/Atom via `feeds.py` | Only operator-supplied feeds; no arbitrary XML uploads |
| **Drafter NPC** | Draft the three beats from headline + summary | `script.py` template or OpenAI-compatible endpoint | Must not invent facts; invalid output is rejected |
| **Auditor NPC** | Check checksums, paths, metadata limits, spec drift | `validate.py`, `audit_specs.py` | Any failure blocks release |
| **Publisher NPC** | Future manual upload only | Human-approved package | Dormant in v0.1; no credentials, no code path |

The Publisher NPC is deliberately **not built**. ADR-0002 records the prohibition; a
future upload feature needs its own ADR, OAuth design, and Risk Spotter sign-off.

## The Double Tenaza

Two grips hold the aircraft steady:

- **Grip 1 — Human intuition.** The reviewer feels when a hook is misleading, a frame is
  unreadable, or a joke punches down. That judgment is a sensor, not a meeting agenda.
- **Grip 2 — Machine precision.** The checksum, the validator, the strict audit, and the
  HUD outrank a good feeling. A green vibe with a red validator is red.

**Quiet Grip:** at IRA ≥ 95% and debt 0, hold steady and let the machine run.
**The Snap:** the moment a band turns red, the named owner acts — freeze the style, fix
the claim, or block the release.

## Killing the Bridge

There is no middle-management translator between the Pilot's intent and the machine:

- The Mission Script is handed directly to the agent.
- The HUD is view-only for anyone who used to receive a status summary.
- Work is displayed out, not reported up.
- A status meeting that restates the HUD is cancelled.

## Operating cadence

| Ritual | Cadence | Output |
| --- | --- | --- |
| Lap | 4 hours to 4 days | One scoped change or package batch |
| Pit Stop | End of every Lap | Review, Refuel, Restart note in `docs/pit-stop.md` |
| Vibe Audit | Monthly / release | HUD, squad, and Mission Script check |
| Release | On accepted scope | Release PR + annotated tag |

## Escalation path

1. A normative conflict is recorded in the owning spec folder's **Open Questions**.
2. The Logic Navigator classifies it as a MUST or SHOULD disagreement.
3. The Pilot resolves scope or priority.
4. The Risk Spotter can veto a release without a second vote.

## Change Log

| Date | Author | Change | Rationale |
| --- | --- | --- | --- |
| 2026-11-16 | Pilot | Initial squad and NPC map | Apply org-geometry to v0.1. |
