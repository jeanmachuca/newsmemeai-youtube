# Housekeeping

## Scope

Housekeeping keeps the repository small, secret-free, and reviewable between Laps. It
covers dependency cadence, secret rotation, log retention, branch pruning, spec review,
and the HUD/Pit Stop cadence.

## Normative Statements (RFC 2119)

- The Ops Mechanic MUST review dependencies monthly and record the result in the Pit Stop log.
- The project MUST NOT commit API keys, tokens, cookies, or private feed URLs.
- Secrets introduced in a future release MUST be rotated at most every 90 days and
  immediately after any suspected exposure.
- Merged topic branches MUST be deleted; unmerged branches older than 30 days MUST be
  reviewed and either merged, closed, or deleted.
- CI logs SHOULD be retained for 90 days using the GitHub default.
- The spec tree MUST be reviewed at every monthly Vibe Audit and before every release.
- The HUD MUST be reviewed whenever a metric crosses a threshold band.
- Artifacts under `out/` MUST remain untracked.

## Cadence

| Area | Cadence | Owner | Evidence |
| --- | --- | --- | --- |
| Dependency review | Monthly | Ops Mechanic | Pit Stop log entry |
| Secret rotation | 90 days or on incident | Risk Spotter | Secret inventory note |
| Stale branch pruning | Monthly | Ops Mechanic | `git branch -r` review |
| Spec review | Monthly and pre-release | Logic Navigator | `AUDIT-REPORT.md` |
| HUD review | On threshold crossing | Pilot | `HUD.md` update |
| Pit Stop | End of every Lap | Pilot | `docs/pit-stop.md` |
| Vibe Audit | Monthly | Pilot | Audit notes |

## Dependency policy

- Runtime dependencies MUST remain empty for v0.1.
- Developer tools MAY use minimum-version ranges in `dev-requirements.txt`.
- A new runtime dependency MUST be justified by an ADR and a measured benefit.
- Automated dependency bots MAY be enabled with monthly grouped updates; if enabled,
  they MUST open PRs against `development`, never `main`.

## Secret policy

- No secrets exist in v0.1.
- LLM credentials MUST be read from `NEWSMEMEAI_YOUTUBE_API_KEY` and MUST NOT be logged.
- A future YouTube OAuth token MUST live outside the repository and MUST be scoped to
  the minimum channel permissions.
- A secret found in git history MUST be rotated before any other remediation.

## Logs and artifacts

- CI logs use the GitHub default retention; the project does not ship logs to a third party.
- Package artifacts are local and untracked; a package MAY be attached to a release only
  after review.
- The repository MUST NOT contain generated `out/` directories or `.venv/` snapshots.

## Branch hygiene

- Merged branches are deleted automatically when the GitHub setting is enabled.
- The default branch is `development`; `main` is release-only.
- A stale branch MUST be closed with a note before deletion if it contains unmerged work.
- Force-pushing shared branches is prohibited by the SDLC.

## Open Questions

- Should package artifacts be retained for 30 or 90 days after a review?
- Should the secret inventory live in this repo or in the squad's private vault?

## Change Log

| Date | Author | RFC 2119 level changed | Rationale |
| --- | --- | --- | --- |
| 2026-11-16 | Pilot | Initial | Dependency, secret, log, and branch hygiene. |
