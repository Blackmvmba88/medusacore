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
# Security / robustness constants
MAX_FIELD_CHARS = 5000
# DICOM common tag names and simple patterns to flag
DICOM_TAGS = [
    "PatientName",
    "PatientID",
    "PatientBirthDate",
    "AccessionNumber",
    "StudyInstanceUID",
    "SeriesInstanceUID",
    "SOPInstanceUID",
    "StudyDate",
    "Modality",
]

# PLC opcodes commonly seen in ladder/text representations
PLC_OPCODES = [
    "MOV", "LD", "ST", "OUT", "IN", "JMP", "CALL", "RET", "AND", "OR", "XOR", "SET", "RST"
]

SUSPICIOUS_PATTERNS = [
    (re.compile(r"<script", re.I), "html_script_tag"),
    (re.compile(r"rm\s+-rf", re.I), "dangerous_shell"),
    (re.compile(r"DROP\s+TABLE", re.I), "sql_injection"),
    (re.compile(r"OR\s+'1'='1", re.I), "sql_boolean_injection"),
    (re.compile(r"javascript:", re.I), "javascript_uri"),
    # LaTeX / TeX injections
    (re.compile(r"\\begin\{[^\}]+\}", re.I), "latex_begin_environment"),
    (re.compile(r"\$[^\$]+\$"), "latex_inline_math"),
    # DICOM-like tags or header marker
    (re.compile(r"\bDICM\b", re.I), "dicom_marker"),
    (re.compile(r"\(\s*\d{4}\s*,\s*\d{4}\s*\)", re.I), "dicom_tag_pattern"),
    (re.compile(r"\b(?:" + "|".join([re.escape(t) for t in DICOM_TAGS]) + r")\b", re.I), "dicom_tag_name"),
    # DICOM VR / value heuristics (sensitive metadata)
    (re.compile(r"\bPatientBirthDate\s*[:=]\s*\d{8}\b"), "dicom_birthdate_DA"),
    (re.compile(r"\bPatientBirthDate\s*[:=]\s*\d{4}-\d{2}-\d{2}\b"), "dicom_birthdate_iso"),
    (re.compile(r"\bDOB\s*[:=]\s*\d{8}\b", re.I), "dicom_birthdate_DA_alt"),
    (re.compile(r"\bAccessionNumber\s*[:=]\s*[A-Za-z0-9_\/\-]{3,}\b", re.I), "dicom_accession_value"),
    (re.compile(r"\bPatientName\s*[:=]\s*[A-Za-z0-9\^,\.\- ]{3,}\b"), "dicom_patientname_value"),
    (re.compile(r"\b(0008,0050)\b"), "dicom_accession_tag_number"),
    (re.compile(r"\b(0010,0030)\b"), "dicom_birthdate_tag_number"),
    # DICOM UID-like heuristic (dotted numerics)
    (re.compile(r"\b\d{1,6}(?:\.\d{1,10}){2,}\b"), "dicom_uid_like"),
    (re.compile(r"\b7FE0,0010\b", re.I), "dicom_pixeldata_tag"),
    # PLC commands / patterns (opcodes and memory addresses)
    (re.compile(r"\b(?:" + "|".join(PLC_OPCODES) + r")\b", re.I), "plc_opcode"),
    (re.compile(r"%M\d+", re.I), "plc_memory_address"),
    (re.compile(r"\bR\d+\b", re.I), "plc_register"),
    (re.compile(r"\bDB\d+(?:\.[A-Za-z0-9]+)?\b", re.I), "plc_db_address"),
    (re.compile(r"\bI\d+\.\d+\b", re.I), "plc_input_address"),
    (re.compile(r"\bQ\d+\.\d+\b", re.I), "plc_output_address"),
    (re.compile(r"\bVAR_\w+\b|\bFB\b|\bFC\b", re.I), "plc_structured_text"),
    # Siemens S7 / STEP7 patterns
    (re.compile(r"\bDB\d+\.(?:DBB|DBW|DBD|DBX)\d+\b", re.I), "plc_siemens_db_field"),
    (re.compile(r"\b(?:FC|FB)\s*\d+\b", re.I), "plc_siemens_function_block"),
    (re.compile(r"\bOB\d+\b", re.I), "plc_siemens_organization_block"),
    (re.compile(r"\bS7(?:[-\s])?(?:300|400|1200|1500)\b", re.I), "plc_siemens_model"),
    (re.compile(r"\bSiemens\b", re.I), "plc_siemens_vendor"),
    # Allen-Bradley / Rockwell patterns (RSLogix / ControlLogix)
    (re.compile(r"\b[NBIL]\d+:\d+(?:/\d+)?\b", re.I), "plc_ab_tag_address"),
    (re.compile(r"\bMSG\b|\bTON\b|\bCTU\b|\bCOP\b", re.I), "plc_ab_opcodes"),
    (re.compile(r"\bLocal:\d+:I\.Data\.\d+\b", re.I), "plc_ab_local_tag"),
    (re.compile(r"\bAllen[- ]?Bradley\b|\bRSLogix\b|\bControlLogix\b", re.I), "plc_allen_bradley_vendor"),
    # Modbus-like terms
    (re.compile(r"\bCoil\b|\bHoldingRegister\b|\bInputRegister\b", re.I), "modbus_keywords"),
    # long base64-like blobs detection
    (re.compile(r"[A-Za-z0-9+/]{100,}={0,2}"), "base64_blob"),
]


def load_markdown(path: str) -> str:
    p = Path(path)
    return p.read_text(encoding="utf-8")


def _detect_suspicious(val: str) -> List[str]:
    reasons = []
    for pat, name in SUSPICIOUS_PATTERNS:
        if pat.search(val):
            reasons.append(name)
    return reasons


def _truncate_if_needed(val: str) -> tuple[str, bool]:
    if len(val) > MAX_FIELD_CHARS:
        return val[:MAX_FIELD_CHARS] + "... [TRUNCATED]", True
    return val, False


def parse_block_lines(lines: List[str]) -> Dict[str, object]:
    """Parsea las líneas dentro de una sección de disciplina a campos estructurados.

    Añade detección sencilla de contenidos sospechosos y truncamiento para
    evitar entradas excesivamente grandes.
    """
    out: Dict[str, object] = {}
    ejemplos: List[str] = []
    suspicious: Dict[str, List[str]] = {}

    for ln in lines:
        m = FIELD_RE.match(ln.strip())
        if m:
            key = m.group("key").strip()
            val = m.group("value").strip()
            # truncar si es necesario
            val, _ = _truncate_if_needed(val)
            # detectar contenido sospechoso
            reasons = _detect_suspicious(val)
            if reasons:
                suspicious[key] = reasons
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
    if suspicious:
        out["_suspicious"] = suspicious
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
