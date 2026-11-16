# Git workflow

This repository follows GHW: topic branches, no rebase, PR review, SemVer tags.

## Branching and PRs (default)

- **Do not** commit new work **directly** on **`main`** or **`development`**. Use a
  **topic branch** from **`development`**:
  `git fetch origin` then `git checkout -b feature/<topic> development` (or
  `fix/<topic>`, `bugfix/<topic>`, `chore/<topic>`, `docs/<topic>`, `refactor/<topic>`,
  `test/<topic>`).
- **Push** the topic branch and open a PR into **`development`** via the GitHub UI or
  `gh pr create`. The bundled auto-PR workflow fires on exactly these prefixes and a
  branch named anything else pushes silently.
- Merge to **`development`** via **PR** after review.
- Promotion **`development` → `main`** uses a release PR.

**Exception:** If the user **explicitly** asks to commit or push **directly** to
**`development`** or **`main`** (e.g. maintainer emergency), follow their instruction and
remind them that it bypasses the usual topic-branch flow.

## Never use `git rebase`

Prefer plain **`git pull`** (merge) when updating from remote, unless the user specifies
otherwise. Do not use **`git pull --rebase`** or **`git rebase`** for this repository's
workflow.

## When the user says "sync git"

Meaning: **save local work and push the current branch** to the remote — **not** "skip
branching."

1. If the current branch is **`main`** or **`development`** and there are **new**
   changes, **prefer** moving work to a topic branch first (unless the user explicitly
   wants a direct push — see Exception above):
   `git fetch origin && git checkout -b feature/<short-description> development`, then
   bring commits across if needed.
2. Stage, commit with a clear message, push:

   ```bash
   git add .
   git commit -m "<concise message describing the changes>"
   git push -u origin HEAD
   ```

   Use `-u origin HEAD` when the branch has no upstream yet; otherwise `git push`. If
   there is nothing to commit, run `git push` if there are unpushed commits.
3. **Untracked files:** use `git add .` (or add paths explicitly); do not rely on
   `git commit -a` alone when new files exist.

Do not substitute stash/rebase flows for "sync git" unless the user asks for a
pull-only or merge-from-remote step.

## Opening a PR

Use the GitHub UI, `gh pr create`, or the auto-PR workflow. Complete
[`.github/PULL_REQUEST_TEMPLATE.md`](../.github/PULL_REQUEST_TEMPLATE.md).

## Releases and tags

1. Open a release PR from `development` to `main`. The `Main PR source` workflow rejects
   any other head branch.
2. Merge with a merge commit.
3. On `main`, create an annotated SemVer tag:

   ```bash
   git tag -a vMAJOR.MINOR.PATCH -m "<description>"
   git push origin vMAJOR.MINOR.PATCH
   ```

4. Record the release in the HUD Lap log and the Pit Stop log.

**Integration tags:** after a feature/fix PR merges into `development`, optionally tag
`vMAJOR.MINOR.PATCH-dev.N` on `development`.

## Release history

| Version | Date | Notes |
| --- | --- | --- |
| `v0.1.0` | 2026-11-16 | First process-compliant release: deterministic package builder, validation, CI, SPECv1 tree |
