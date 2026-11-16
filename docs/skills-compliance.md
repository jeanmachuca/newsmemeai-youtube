# Skills Compliance Matrix

This document records how each loaded process skill applies to NewsMemeAI YouTube. A
skill is either **Applied** with evidence, **N/A** with a rationale and a revisit
trigger, or **Reference** (support material, not a project gate).

## Matrix

| Skill | Status | Evidence | Why / why not |
| --- | --- | --- | --- |
| **SPECv1** | Applied | `specs/01`–`11`, `specs/AUDIT-REPORT.md`, `scripts/audit_specs.py` | Full normative tree, RFC 2119 requirements, ADRs, schemas, SDLC, traceability, strict audit. |
| **Mission Script** | Applied | `MISSION.md` | Six fields: name, frequency, outcome, constraints, acceptance, verification. Frequency is Stealth/Precision. |
| **GHW** | Applied | `docs/git-workflow.md`, topic branch → PR → release PR → annotated tag | No direct commits to `main`/`development`; no rebase; SemVer `v0.1.0`. |
| **HUD Setup** | Applied | `HUD.md` | Three signals, formulas, bands, named escalation owners, view-only observer access. |
| **Org Geometry** | Applied | `specs/01-product-vision/org-structure.md`, `docs/org-structure.md` | Pilot + four specialist seats + four NPC agents; Double Tenaza and Bridge rules. |
| **Pit Stop Audit** | Applied | `docs/pit-stop.md` | Per-Lap Review/Refuel/Restart; monthly Vibe Audit; Pilot's Final Checklist. |
| **IRA Prompting** | Applied | `docs/ira.md`, PR template, test names | Seven techniques mapped to actual repository prompts and review gates. |
| **AESEv2** | N/A | Rationale in `specs/03-architecture/architecture.md` | AESEv2 synthesizes an Astro application for Cloudflare edge. This product is a local Python CLI with no web surface. Revisit if a web front end is added. |
| **OSMv6** | N/A | Rationale in `specs/03-architecture/architecture.md` | OSMv6 routes ambiguous user intent through a synonym graph and external fallbacks. This pipeline is a fixed feed → script → render → package flow. Revisit if a multi-channel request router is added. |
| **Report** | Reference | n/a | Used only to report an OpenCode bug; it is not a product delivery gate. |
| **OpenCode** | Reference | `AGENTS.md`, `.opencode/instructions/git-workflow.md` | Harness configuration and workflow instructions; no runtime dependency. |

## Why N/A is not a gap

SPECv1 requires every folder to exist and every requirement to be testable. It does not
require every optional skill to be used. AESEv2 and OSMv6 target different compute and
intent shapes, so applying them here would add architecture the product does not need.
The decision is recorded in the architecture spec and revisited when the trigger named
above occurs.

## Verification

```bash
python scripts/audit_specs.py --strict
bash scripts/verify.sh
```

The audit checks the spec tree and implementation drift. The verification script checks
lint, format, types, tests, and the strict audit. A release PR also requires the HUD and
Pit Stop checklist in `docs/pit-stop.md`.

## Change Log

| Date | Author | Change | Rationale |
| --- | --- | --- | --- |
| 2026-11-16 | Pilot | Initial matrix | Record applied and N/A skills for v0.1.0. |
