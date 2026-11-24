#!/usr/bin/env python3
"""Run every supplied version in order and write a matrix report."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "ci" / "version_manifest.json"
REPORT = ROOT / "artifacts" / "version-matrix.json"


def run(command: list[str]) -> tuple[int, str]:
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    output = (completed.stdout + completed.stderr).strip()
    return completed.returncode, output


def main(allow_expected_failure: bool) -> int:
    entries = json.loads(MANIFEST.read_text())
    results = []
    unexpected_failure = False
    for entry in entries:
        version = entry["version"]
        build_rc, build_output = run([sys.executable, "ci/build_version.py", version])
        test_rc, test_output = run([sys.executable, "ci/test_version.py", version])
        expected = bool(entry.get("expected_failure"))
        accepted = build_rc == 0 and (
            (test_rc == 2 and expected) or (test_rc == 0 and not expected)
        )
        if not accepted:
            unexpected_failure = True
        results.append(
            {
                "version": version,
                "stage": entry["stage"],
                "build_returncode": build_rc,
                "test_returncode": test_rc,
                "expected_failure": expected,
                "accepted": accepted,
                "build_output": build_output,
                "test_output": test_output,
            }
        )
        print(f"{version}: build={build_rc} test={test_rc} accepted={accepted}")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(results, indent=2) + "\n")
    print(f"Matrix report: {REPORT}")
    if unexpected_failure:
        return 1
    if not allow_expected_failure and any(item["expected_failure"] for item in results):
        print(
            "Expected failed version was observed; use --allow-expected-failure "
            "for a green local matrix."
        )
        return 2
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--allow-expected-failure", action="store_true")
    args = parser.parse_args()
    raise SystemExit(main(args.allow_expected_failure))
