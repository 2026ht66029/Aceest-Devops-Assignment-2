#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

python3 -m compileall -q app.py aceest ci tests
python3 ci/run_version_matrix.py --allow-expected-failure
python3 - <<'PY'
import json
from pathlib import Path

entries = json.loads(Path('ci/version_manifest.json').read_text())
assert len(entries) == 10
assert sum(bool(e.get('expected_failure')) for e in entries) == 1
print('manifest validation passed: 10 versions and 1 expected failure')
PY

echo "Package validation passed. Install requirements-dev.txt before running pytest and ruff."
