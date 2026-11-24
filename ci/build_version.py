#!/usr/bin/env python3
"""Build one supplied ACEest milestone without starting its GUI."""

from __future__ import annotations

import argparse
import ast
import json
import py_compile
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "ci" / "version_manifest.json"
ARTIFACTS = ROOT / "artifacts" / "versions"


def load_entry(version: str) -> dict:
    entries = json.loads(MANIFEST.read_text())
    for entry in entries:
        if entry["version"] == version:
            return entry
    raise SystemExit(f"Unknown version: {version}")


def build(version: str) -> Path:
    entry = load_entry(version)
    source = ROOT / entry["source"]
    if not source.is_file():
        raise SystemExit(f"Missing source file: {source}")

    tree = ast.parse(source.read_text(), filename=str(source))
    if not any(isinstance(node, ast.ClassDef) and node.name == "ACEestApp" for node in tree.body):
        raise SystemExit(f"{version}: ACEestApp class was not found")

    py_compile.compile(str(source), doraise=True)
    target = ARTIFACTS / version
    target.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target / "app.py")
    metadata = {
        "application": "ACEest Fitness and Gym",
        "version": version,
        "source": entry["source"],
        "stage": entry["stage"],
        "syntax": "passed",
    }
    (target / "build-metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(f"BUILD PASSED {version}: {entry['stage']}")
    return target


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("version")
    args = parser.parse_args()
    build(args.version)
