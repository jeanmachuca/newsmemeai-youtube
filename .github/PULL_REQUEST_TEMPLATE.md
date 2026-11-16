## Summary

<!-- One paragraph: what changed and why. Link the issue or spec section. -->

## Change type

- [ ] Feature (`feature/`)
- [ ] Fix (`fix/` or `bugfix/`)
- [ ] Documentation (`docs/`)
- [ ] Refactor (`refactor/`)
- [ ] Test (`test/`)
- [ ] Chore (`chore/`)

## Spec impact

- [ ] No normative change.
- [ ] Updated the owning spec folder (list it): `specs/__/`
- [ ] Updated `05-requirements/` and the traceability matrix.
- [ ] Added or superseded an ADR.
- [ ] This change alters a MUST requirement (requires Risk Spotter review).

## What changed

<!-- Bullet the important files and behaviours. -->

## Verification

Paste the commands and their results. Every box must be checked.

- [ ] `ruff check .`
- [ ] `ruff format --check .`
- [ ] `mypy src/`
- [ ] `pytest -v` — __ passed
- [ ] `python scripts/audit_specs.py --strict` — PASS
- [ ] `bash scripts/verify.sh`
- [ ] Package smoke test (if the build path changed):
      `newsmemeai-youtube validate /tmp/pkg` → `OK: 7 files verified`

## Risk and hallucination debt

- [ ] No new unsupported claims, facts, numbers, names, or quotes.
- [ ] No upload, scheduling, or publishing path was added.
- [ ] No secret, credential, `out/` artifact, or cache file is committed.
- [ ] Untrusted feed/model text is escaped before SVG or JSON.
- [ ] Rollback: revert this PR with `git revert`; no rebase.

## Release notes

<!-- One or two lines for the release PR and tag annotation. -->
