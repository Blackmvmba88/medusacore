"""CLI helper: persist forensics from a JSON file of parsed entries.

Usage: python tools/save_forensics.py --src parsed.json --branch mybranch --out artifacts/
"""

from __future__ import annotations
import argparse
import json
from pathlib import Path
from hydras.forensics import persist_forensics_entries


def main():
    p = argparse.ArgumentParser(description="Persist forensics originals to artifacts")
    p.add_argument("--src", required=True, help="JSON file with parsed entries (list)")
    p.add_argument("--branch", required=True, help="Branch name/context")
    p.add_argument("--out", default=None, help="Artifacts output dir (optional)")
    args = p.parse_args()
    path = Path(args.src)
    data = json.loads(path.read_text(encoding="utf-8"))
    artifacts_dir = args.out if args.out else None
    results = persist_forensics_entries(data, args.branch, artifacts_dir=artifacts_dir)
    print(f"Persisted {len(results)} artifacts")


if __name__ == "__main__":
    main()
