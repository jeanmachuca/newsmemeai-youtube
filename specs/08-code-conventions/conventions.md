# Code Conventions

## Scope

These conventions cover the Python package, tests, scripts, workflows, and documentation.
They are enforceable in CI where possible; review covers the rest.

## Normative Statements (RFC 2119)

- Runtime code MUST use Python 3.11+ syntax and `from __future__ import annotations`.
- Public functions and methods MUST have complete type annotations.
- Runtime code MUST NOT import third-party packages.
- The package MUST use a `src/` layout with the importable name `newsmemeai_youtube`.
- Ruff MUST be the linter and formatter; line length MUST be 100.
- Mypy MUST run in strict mode over `src/`.
- Pytest MUST cover every required artifact and error path named in the requirements.
- Commit subjects MUST use one of `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, or
  `perf`, followed by an optional scope and a colon.
- A pull request SHOULD stay under 400 changed lines excluding generated specs and tests.
- Reviewers MUST reject code that feeds untrusted text into SVG, shell, or `eval`.

## Naming

| Kind | Rule | Example |
| --- | --- | --- |
| Package | snake_case | `newsmemeai_youtube` |
| Module | snake_case | `package.py`, `validate.py` |
| Class | PascalCase | `ValidationResult` |
| Function | snake_case | `build_package` |
| Constant | UPPER_SNAKE | `REQUIRED_ARTIFACTS` |
| CLI command | kebab-case | `newsmemeai-youtube` |
| Branch | type/kebab-topic | `feature/spec-bootstrap` |

## Formatting and linting

- `ruff check .` MUST pass.
- `ruff format --check .` MUST pass.
- `mypy src/` MUST pass without ignores except documented third-party stubs.
- No wildcard imports, no mutable default arguments, no bare `except`.
- Imports MUST be grouped: future, standard library, third party (tests only), local.

## Testing

- Tests MUST use local XML fixtures and MUST NOT require network access.
- Tests MUST assert behaviour, not implementation details where a public contract exists.
- A bug fix MUST add a regression test.
- Test names MUST describe the behaviour, e.g. `test_tampered_artifact_is_detected`.

## Commit and review conventions

- Commit subject: `type(scope): imperative summary`.
- Commit body SHOULD explain why, not restate the diff.
- PRs MUST include the verification checklist from the PR template.
- Reviewers MUST check spec drift when a public behaviour changes.
- A PR that changes a MUST requirement MUST update the matching spec folder and test.

## Security rules

- Secrets MUST come from environment variables and MUST NOT be committed.
- Feed and model text MUST be treated as untrusted data.
- SVG MUST be generated locally and MUST NOT embed remote resources or scripts.
- Validation MUST reject absolute paths and parent traversal before reading artifacts.
- `eval`, `exec`, and shell interpolation of feed text are prohibited.

## Open Questions

- Should the project adopt a commit-msg hook for the Conventional Commit prefix?
- Should coverage be enforced, and if so at what threshold?

## Change Log

| Date | Author | RFC 2119 level changed | Rationale |
| --- | --- | --- | --- |
| 2026-11-16 | Pilot | Initial | Python, lint, type, test, and review conventions. |
