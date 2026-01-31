"""Utilities to learn engineering index documents into structured knowledge.

Functions:
- parse_ingenierias_markdown(text) -> list[dict]
- load_markdown(path) -> str
- save_json(data, path)
"""

from __future__ import annotations
import json
import re
from pathlib import Path
from typing import List, Dict

HEADING_RE = re.compile(r"^###\s+(?P<name>.+)$", re.MULTILINE)
FIELD_RE = re.compile(r"^-\s*(?P<key>[^:]+):\s*(?P<value>.+)$")


def load_markdown(path: str) -> str:
    p = Path(path)
    return p.read_text(encoding="utf-8")


def parse_block_lines(lines: List[str]) -> Dict[str, object]:
    """Parsea las líneas dentro de una sección de disciplina a campos estructurados."""
    out = {}
    ejemplos = []
    for ln in lines:
        m = FIELD_RE.match(ln.strip())
        if m:
            key = m.group("key").strip()
            val = m.group("value").strip()
            # Normalizar claves a nombres cortos (en español)
            key_norm = key.lower()
            if key_norm.startswith("ejemplos"):
                # ejemplos pueden estar en la misma línea o en líneas siguientes numeradas
                # separar por (1) (2) si existen
                parts = re.split(r"\(\d+\)\s*", val)
                parts = [p.strip(" -;.\n") for p in parts if p.strip()]
                if parts:
                    ejemplos.extend(parts)
                else:
                    ejemplos.append(val)
            else:
                out[key] = val
        else:
            # líneas extra (p. ej. items numerados) -> buscar (1) (2)
            s = ln.strip().lstrip("- ")
            if s.startswith("(") and ")" in s:
                # formato (1) texto
                t = re.sub(r"^\(\d+\)\s*", "", s)
                if t:
                    ejemplos.append(t)
    if ejemplos:
        out["Ejemplos"] = ejemplos
    return out


def parse_ingenierias_markdown(text: str) -> List[Dict[str, object]]:
    """Extrae las secciones '### <Disciplina>' y parsea campos internos."""
    disciplines: List[Dict[str, object]] = []
    headings = list(HEADING_RE.finditer(text))
    for i, h in enumerate(headings):
        name = h.group("name").strip()
        start = h.end()
        end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
        block = text[start:end].strip()
        # split by lines and parse
        lines = [ln for ln in block.splitlines() if ln.strip()]
        parsed = parse_block_lines(lines)
        parsed["name"] = name
        disciplines.append(parsed)
    return disciplines


def save_json(data: object, path: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Ingest docs/ingenierias.md to structured JSON"
    )
    parser.add_argument("--src", default="docs/ingenierias.md")
    parser.add_argument("--out", default="data/ingenierias.json")
    args = parser.parse_args()
    txt = load_markdown(args.src)
    data = parse_ingenierias_markdown(txt)
    save_json(data, args.out)
    print(f"Saved {len(data)} disciplines to {args.out}")
