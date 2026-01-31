from pathlib import Path
import json
from tools.ingest_and_persist import main as ingest_main
import sys


def test_ingest_and_persist_cli(tmp_path, monkeypatch, capsys):
    # create sample md file
    md = tmp_path / "sample.md"
    md.write_text("""
### DICOM1
- Enfoque corto: prueba
- Enfoque: PatientName: Lopez^Ana
""")
    # run CLI
    argv = ["ingest_and_persist.py", "--src", str(tmp_path), "--branch", "ci-branch", "--out", str(tmp_path / "artifacts"), "--batch"]
    monkeypatch.setattr(sys, "argv", argv)
    ingest_main()
    # check artifacts dir
    artifacts = tmp_path / "artifacts"
    files = list(artifacts.glob("*"))
    assert any(f.suffix == ".json" for f in files)
    # find raw file and assert content
    raw = [f for f in files if f.name.startswith("artifact_") and f.suffix == ".json"][0]
    data = json.loads(raw.read_text(encoding="utf-8"))
    assert "items" in data and len(data["items"]) == 1
