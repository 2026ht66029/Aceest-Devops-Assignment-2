"""Tests for the version manifest used by the staged build."""

import json
from pathlib import Path


def test_manifest_contains_all_supplied_versions():
    manifest_path = Path(__file__).parents[1] / "ci" / "version_manifest.json"
    entries = json.loads(manifest_path.read_text())
    versions = [entry["version"] for entry in entries]
    assert versions == [
        "1.0.0",
        "1.1.0",
        "1.1.2",
        "2.0.1",
        "2.1.2",
        "2.2.1",
        "2.2.4",
        "3.0.1",
        "3.1.2",
        "3.2.4",
    ]
    for entry in entries:
        assert (manifest_path.parents[1] / entry["source"]).is_file()
