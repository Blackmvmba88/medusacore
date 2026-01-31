from tools.generate_adversarial_corpus import generate
from medusa.learners import parse_ingenierias_markdown
from hydras.forensics import ForensicsHydra
from pathlib import Path


def test_ingest_corpus_and_capture_forensics(tmp_path):
    out_dir = tmp_path / "corpus"
    out_dir.mkdir()
    files = generate(out_dir)
    assert len(files) > 0
    fhydra = ForensicsHydra()
    artifacts = {}
    for p in files:
        txt = p.read_text(encoding="utf-8")
        parsed = parse_ingenierias_markdown(txt)
        # parsed should be a list; at least one element
        assert isinstance(parsed, list)
        # if suspicious fields found in parsed entries, capture forensics
        for entry in parsed:
            if entry.get("_suspicious"):
                # create a minimal logs/artifacts dict and capture
                logs = {
                    "file": str(p.name),
                    "parsed": entry,
                }
                rep = fhydra.capture(branch="wip/genesis-pr", logs=logs)
                assert rep["branch"] == "wip/genesis-pr"
                assert "artifacts" in rep and rep["artifacts"] == logs
                artifacts[p.name] = True
    # ensure at least one adversarial file produced suspicious flags
    assert any(artifacts.values())
