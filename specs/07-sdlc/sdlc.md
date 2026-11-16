# Software Development Life Cycle

## Scope

This SDLC defines how NewsMemeAI YouTube moves from a Vibe to a released package. It
uses Laps, Pit Stops, topic branches, PR gates, and SemVer releases. Status meetings are
replaced by the HUD and the spec audit.

## Normative Statements (RFC 2119)

- Every change MUST start from a topic branch created from `development`.
- No contributor SHALL commit new work directly to `main` or `development`.
- Pull requests into `development` MUST pass CI, the spec audit, and a human review.
- Promotion to `main` MUST use a release PR from `development`.
- Releases MUST use annotated SemVer tags on `main`.
- The project MUST NOT use rebase or force-push to rewrite shared history.
- Every sprint or Lap MUST end with a Pit Stop: Review, Refuel, Restart.
- A monthly Vibe Audit MUST check the HUD, the squad, and the Mission Script.

## Phases and gates

| Phase | Entry | Exit gate |
| --- | --- | --- |
| 0. Pre-INIT | User names the product | `WHAT`, scope, owner model, and specs location recorded |
| 1. INIT | Specs location confirmed | All 11 SPECv1 folders and `AUDIT-REPORT.md` exist |
| 2. Build | Specs baseline accepted | Feature branch pushed, tests and lint green |
| 3. Review | PR open against `development` | CI green, spec audit PASS, reviewer approves |
| 4. Release | Development tested | Release PR merged to `main`, annotated tag pushed |

## Branching model

- `main` — release history only.
- `development` — default integration branch.
- `feature/<topic>` — new capability.
- `fix/<topic>` and `bugfix/<topic>` — corrections.
- `chore/<topic>`, `docs/<topic>`, `refactor/<topic>`, `test/<topic>` — supporting work.
- Topic branches MUST be pushed and opened as PRs into `development`.
- The auto-PR workflow MAY open the PR when a topic branch is pushed, but a human MUST
  review it.
- Merges into `development` MUST use a merge commit or squash commit; rebase is forbidden.
- Promotion to `main` MUST use a release PR. Direct pushes to `main` MUST NOT happen.

## Approval gates per specification folder

| Folder | Required approver | Gate |
| --- | --- | --- |
| 01-product-vision | Pilot | Scope and metrics unchanged or explicitly accepted |
| 02-prd | Logic Navigator + Pilot | Every user story maps to an FR |
| 03-architecture | Ops Mechanic + Pilot | Components and deployment remain accurate |
| 04-adrs | Pilot | Status and consequences recorded |
| 05-requirements | Logic Navigator + Risk Spotter | IDs unique, levels valid, tests named |
| 06-schemas | Logic Navigator + Ops Mechanic | Schema version and validator agree |
| 07-sdlc | Pilot | Branching and release gates match GHW |
| 08-code-conventions | Ops Mechanic | Rules enforceable in CI |
| 09-housekeeping | Risk Spotter | Secret, dependency, and branch policies current |
| 10-script-helpers | Ops Mechanic | Scripts have pre/postconditions and flags |
| 11-implementation-plan | Pilot | Every FR appears in the traceability matrix |

## Pull request gate

A PR MUST satisfy all of the following before merge:

1. `ruff check .`
2. `ruff format --check .`
3. `mypy src/`
4. `pytest -v`
5. `python scripts/audit_specs.py --strict`
6. A human review that checks the PR against `MISSION.md` and the affected specs.
7. No secrets, no generated cache files, and no accidental large binaries.

## Release process

1. Open a release PR from `development` to `main`.
2. Ensure the `Main PR source` workflow allows only `development` as the head branch.
3. Merge the release PR with a merge commit.
4. Tag on `main` with an annotated SemVer tag:
   `git tag -a vMAJOR.MINOR.PATCH -m "<description>"`.
5. Push the tag: `git push origin vMAJOR.MINOR.PATCH`.
6. Record the release in the Pit Stop log and update the HUD baseline if needed.

## Pit Stop and Vibe Audit

- Each Lap ends with Review (score against the Mission Script), Refuel (data or prompt
  changes), and Restart (next Lap).
- The monthly Vibe Audit checks the HUD metrics, the specialist seats, and whether the
  Mission Script still matches the market.
- The Pilot's Final Checklist is recorded in `docs/pit-stop.md`.

## Open Questions

- Should releases also publish a Python wheel to GitHub Packages?
- Should the release PR require a signed tag or a GitHub release note?

## Change Log

| Date | Author | RFC 2119 level changed | Rationale |
| --- | --- | --- | --- |
| 2026-11-16 | Pilot | Initial | GHW-compatible phase, gate, and release process. |
