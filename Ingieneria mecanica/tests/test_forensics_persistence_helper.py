from hydras.forensics import persist_forensics_entries, ForensicsHydra
import json
import os
from pathlib import Path


def test_persist_forensics_entries(tmp_path):
    # craft entries with _forensics_originals
    entries = [
        {
            "name": "DICOMSensitive",
            "_forensics_originals": {
                "PatientName": "Perez^Maria",
                "PatientBirthDate": "19850705",
            },
        },
        {"name": "NoForensics"},
    ]
    results = persist_forensics_entries(
        entries, branch="test-branch", artifacts_dir=tmp_path
    )
    # Should capture only one artifact
    assert len(results) == 1
    meta = results[0]
    assert os.path.exists(meta["raw_path"]) and os.path.exists(meta["meta_path"])
    # meta JSON has expected fields
    with open(meta["meta_path"], "r", encoding="utf-8") as fh:
        meta_contents = json.load(fh)
    assert meta_contents["branch"] == "test-branch"
    # raw file includes originals
    with open(meta["raw_path"], "r", encoding="utf-8") as fh:
        raw = json.load(fh)
    assert raw["items"][0]["originals"]["PatientName"] == "Perez^Maria"


def test_persist_forensics_entries_non_batch(tmp_path):
    entries = [
        {"name": "A", "_forensics_originals": {"k": "v1"}},
        {"name": "B", "_forensics_originals": {"k": "v2"}},
    ]
    results = persist_forensics_entries(entries, branch="b", artifacts_dir=tmp_path, batch=False)
    # Should create two artifacts (one per entry)
    assert len(results) == 2
    paths = [r["raw_path"] for r in results]
    assert all(Path(p).exists() for p in paths)
