#!/usr/bin/env bash
# Checklist Close for a Lap. Runs the full local verification sequence.
# Preconditions: run from the repository root with dev tools installed.
# Postconditions: exits non-zero on the first failed check.

set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

echo "==> ruff check ."
ruff check .

echo "==> ruff format --check ."
ruff format --check .

echo "==> mypy src/"
mypy src/

echo "==> pytest -v"
pytest -v

echo "==> spec audit (strict)"
python scripts/audit_specs.py --strict

echo "All checks passed."
