# Review Checklist

Three review gates exist: the package review, the pull request review, and the release
review. Any unchecked item blocks the gate.

## 1. Package review (human publishing gate)

Run before a package is used for any upload. Record the decision in the generated
`REVIEW.md`.

### Provenance

- [ ] The headline in `manifest.json` matches the source feed item.
- [ ] `headline.source` names the feed or file the item came from.
- [ ] `headline.link` and `headline.published` are present when the feed provides them.
- [ ] `manifest.json` lists all seven required artifacts.

### Claims

- [ ] The hook does not assert a fact that is absent from the headline or summary.
- [ ] The context beat matches the headline and summary.
- [ ] No numbers, names, dates, or quotes were invented.
- [ ] The punchline is clearly a reaction, not a false factual claim.
- [ ] `**Hallucination debt:**` is `0 open claims`, or every open claim is resolved.

### Metadata

- [ ] Title ≤ 100 characters and ends with `#Shorts`.
- [ ] Description ≤ 5,000 characters and attributes the source.
- [ ] Tags stay within the 500-character budget.
- [ ] `privacy_status` is `private`.
- [ ] `made_for_kids` is `false` unless the content is genuinely child-directed.
- [ ] Category `24` (Entertainment) is appropriate.

### Visuals and script

- [ ] All three 1080×1920 frames are legible on a phone.
- [ ] The 1280×720 thumbnail is legible at small size.
- [ ] Text does not overflow the canvas; no line is clipped.
- [ ] SVG text is escaped; no raw HTML, script, or remote resource is embedded.
- [ ] The script's three beats fit the 0–3s / 3–8s / 8–12s timing.
- [ ] The export is handled by a human editor; no auto-render claims are made.

### Integrity

- [ ] `newsmemeai-youtube validate <dir>` returns `OK: 7 files verified`.
- [ ] The package was not edited after validation; if it was, re-run `build` and
      `validate`.
- [ ] Nothing was uploaded, scheduled, or published by the tool.

**Decision:** draft / approved / rejected. An approved package may proceed to a manual
upload step outside this tool.

## 2. Pull request review

- [ ] The branch name uses an allowed prefix and targets `development`.
- [ ] CI is green (ruff, format, mypy, pytest, spec audit).
- [ ] `bash scripts/verify.sh` passes locally.
- [ ] New public behaviour has a test and a spec update.
- [ ] A MUST requirement change updates `05-requirements/` and the traceability matrix.
- [ ] No secrets, `out/` artifacts, caches, or large binaries are committed.
- [ ] Error paths return non-zero and a human-readable message.
- [ ] Untrusted text is escaped before SVG/JSON.
- [ ] The change does not add an upload path or a runtime dependency.
- [ ] The PR template's verification block is complete.

## 3. Release review

- [ ] The release PR is `development` → `main`; the `Main PR source` workflow passes.
- [ ] `specs/AUDIT-REPORT.md` is current and says PASS.
- [ ] `python scripts/benchmark.py --runs 5` is under the 2,000 ms guardrail.
- [ ] `MISSION.md`, `HUD.md`, and `docs/pit-stop.md` are current.
- [ ] The annotated tag matches `pyproject.toml` and `__init__.py`.
- [ ] The tag is created on `main` and pushed.
- [ ] The HUD Lap log and Pit Stop log record the release.

## Escalation

| Finding | Action | Owner |
| --- | --- | --- |
| Unsupported claim | Reject or fix; do not publish | Risk Spotter |
| Checksum mismatch | Rebuild the package; investigate tampering | Ops Mechanic |
| Metadata over limit | Fix the generator, not the JSON by hand | Creative Pilot |
| Spec drift | Fix the spec or code before merge | Logic Navigator |
| Upload code or credential | Stop, revert, security review | Risk Spotter |

## Change Log

| Date | Author | Change | Rationale |
| --- | --- | --- | --- |
| 2026-11-16 | Pilot | Initial package, PR, and release gates | Make the human review gate explicit. |
