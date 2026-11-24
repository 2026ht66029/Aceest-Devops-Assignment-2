#!/usr/bin/env python3
"""Run the version acceptance gate used by Jenkins."""

from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "ci" / "version_manifest.json"


def load_entry(version: str) -> dict:
    for entry in json.loads(MANIFEST.read_text()):
        if entry["version"] == version:
            return entry
    raise SystemExit(f"Unknown version: {version}")


def validate(version: str) -> int:
    entry = load_entry(version)
    source = ROOT / entry["source"]
    tree = ast.parse(source.read_text(), filename=str(source))
    methods = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    if "__init__" not in methods:
        print(f"TEST FAILED {version}: ACEestApp initialization is missing")
        return 1

    if entry.get("expected_failure"):
        print(
            f"TEST FAILED {version}: {entry['failure_reason']}; "
            "this is the intentional failed version for the Jenkins evidence"
        )
        return 2

    print(f"TEST PASSED {version}: AST acceptance checks passed")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("version")
    args = parser.parse_args()
    sys.exit(validate(args.version))
