from tools.generate_adversarial_corpus import generate
from medusa.learners import parse_ingenierias_markdown
from hydras.forensics import ForensicsHydra
from pathlib import Path
import json
import hashlib


def test_forensics_persistence_and_reproducibility(tmp_path):
    out_dir = tmp_path / "corpus"
    out_dir.mkdir()
    files = generate(out_dir, make_count=2, randomize=True)
    f = ForensicsHydra(artifacts_dir=tmp_path / "artifacts")
    assert (tmp_path / "artifacts").exists()
    saved_meta = None
    for p in files:
        txt = p.read_text(encoding="utf-8")
        parsed = parse_ingenierias_markdown(txt)
        for entry in parsed:
            if entry.get("_suspicious"):
                logs = {"file": str(p.name), "parsed": entry}
                rep = f.capture(branch="wip/genesis-pr", logs=logs)
                # metadata paths should exist
                meta_path = Path(rep["meta_path"])
                raw_path = Path(rep["raw_path"])
                assert meta_path.exists() and raw_path.exists()
                # verify sha matches raw content
                raw_bytes = raw_path.read_bytes()
                sha = hashlib.sha256(raw_bytes).hexdigest()
                assert sha == rep["sha256"]
                saved_meta = rep
    assert saved_meta is not None, "No suspicious artifacts found in corpus"
    # Reproduce: read meta and raw and verify
    meta = json.loads(Path(saved_meta["meta_path"]).read_text(encoding="utf-8"))
    raw = Path(meta["raw_path"]).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == meta["sha256"]
