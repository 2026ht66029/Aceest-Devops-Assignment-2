#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install --requirement requirements-dev.txt
.venv/bin/ruff check .
.venv/bin/pytest --cov-report=xml:coverage.xml
.venv/bin/python ci/run_version_matrix.py --allow-expected-failure
