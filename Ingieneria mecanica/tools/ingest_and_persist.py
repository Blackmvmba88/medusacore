"""Ingest markdown files from a directory and persist forensics artifacts.

Usage: python tools/ingest_and_persist.py --src tests/adversarial_corpus --branch mybranch --out tests/adversarial_artifacts --batch
"""
from __future__ import annotations
import argparse
from pathlib import Path
import json
from medusa.learners import parse_ingenierias_markdown
from hydras.forensics import persist_forensics_entries


def main():
    p = argparse.ArgumentParser(description="Ingest markdown files and persist forensics")
    p.add_argument("--src", required=True, help="Directory with .md files (or a single file)")
    p.add_argument("--branch", required=True, help="Branch name/context")
    p.add_argument("--out", default=None, help="Artifacts output dir (optional)")
    p.add_argument("--batch", action="store_true", help="Batch entries into a single artifact")
    args = p.parse_args()

    src = Path(args.src)
    files = []
    if src.is_file():
        files = [src]
    else:
        files = sorted(src.glob("**/*.md"))
    all_entries = []
    for f in files:
        txt = f.read_text(encoding="utf-8")
        parsed = parse_ingenierias_markdown(txt, redact=False, collect_forensics=True)
        # attach source
        for ent in parsed:
            ent["_source_file"] = str(f)
        all_entries.extend(parsed)

    results = persist_forensics_entries(all_entries, branch=args.branch, artifacts_dir=args.out, batch=args.batch)
    print(f"Persisted {len(results)} artifacts")
    for r in results:
        print(json.dumps(r, ensure_ascii=False))


if __name__ == "__main__":
    main()
