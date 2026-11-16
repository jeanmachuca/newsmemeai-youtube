# Git workflow (agent instruction)

Canonical document: [`docs/git-workflow.md`](../../docs/git-workflow.md).

## Rules

1. Never commit directly to `main` or `development`; branch from `development` with a
   `feature/`, `fix/`, `bugfix/`, `chore/`, `docs/`, `refactor/`, or `test/` prefix.
2. Open a PR into `development`; merge only after CI, the strict spec audit, and human
   review.
3. Promotion to `main` uses a release PR from `development`.
4. Never rebase or force-push shared branches. Use merge commits or squash merges.
5. Tag releases on `main` with annotated SemVer tags:
   `git tag -a vMAJOR.MINOR.PATCH -m "<description>"`.
6. Run `bash scripts/verify.sh` before pushing.
