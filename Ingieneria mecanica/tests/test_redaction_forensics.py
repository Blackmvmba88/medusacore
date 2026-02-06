from medusa.learners import parse_ingenierias_markdown
import hashlib


def _sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def test_redact_and_collect_forensics():
    md = """
### DICOMSensitive
- Enfoque corto: datos personales
- Ojo de inteligencia: PatientBirthDate: 19850705
- Herramientas y recursos: PatientName: Perez^Maria, AccessionNumber: ACC-999
- Notas: PatientAddress: Calle Falsa 123
"""
    res = parse_ingenierias_markdown(md, redact=True, collect_forensics=True)
    entry = res[0]
    # Redaction happened
    assert "_redacted" in entry
    # Specific fields redacted
    assert entry.get("PatientBirthDate") == "[REDACTED]"
    assert entry.get("PatientName") == "[REDACTED]"
    assert entry.get("AccessionNumber") == "[REDACTED]"
    assert entry.get("PatientAddress") == "[REDACTED]"
    # Forensics originals and hashes present
    assert "_forensics_originals" in entry
    assert "PatientName" in entry["_forensics_originals"]
    assert entry["_forensics_hashes"]["PatientName"] == _sha256(
        entry["_forensics_originals"]["PatientName"]
    )
