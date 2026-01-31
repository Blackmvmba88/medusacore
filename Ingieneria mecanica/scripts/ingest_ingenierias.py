#!/usr/bin/env python3
"""CLI to ingest engineering index into structured JSON for Medusa."""

from medusa.learners import load_markdown, parse_ingenierias_markdown, save_json
import sys


def main(argv=None):
    argv = argv or sys.argv[1:]
    src = argv[0] if len(argv) > 0 else "docs/ingenierias.md"
    out = argv[1] if len(argv) > 1 else "data/ingenierias.json"
    txt = load_markdown(src)
    data = parse_ingenierias_markdown(txt)
    save_json(data, out)
    print(f"Ingested {len(data)} disciplines from {src} → {out}")


if __name__ == "__main__":
    main()
