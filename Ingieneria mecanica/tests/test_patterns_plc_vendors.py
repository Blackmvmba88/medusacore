from medusa.learners import parse_ingenierias_markdown


def test_detect_siemens_patterns():
    md = """
### PLC_Siemens
- Enfoque corto: Siemens snippet
- Ojo de inteligencia: DB100.DBW0 FC 123 OB1 Siemens S7-300
- Herramientas y recursos: DB1.DBX0.0 DB2.DBD4
"""
    res = parse_ingenierias_markdown(md)
    entry = res[0]
    assert "_suspicious" in entry
    reasons = set()
    for v in entry["_suspicious"].values():
        reasons.update(v)
    assert any(
        r.startswith("plc_siemens") or r == "plc_db_address"
        for r in reasons
    )


def test_detect_allen_bradley_patterns():
    md = """
### PLC_AB
- Enfoque corto: Allen-Bradley snippet
- Ojo de inteligencia: N7:0 B3:0/0 I:1/0 O:2/1 TON CTU MSG Allen-Bradley
- Herramientas y recursos: Local:1:I.Data.0
"""
    res = parse_ingenierias_markdown(md)
    entry = res[0]
    assert "_suspicious" in entry
    reasons = set()
    for v in entry["_suspicious"].values():
        reasons.update(v)
    assert any(
        r.startswith("plc_ab") or r == "plc_ab_tag_address" or r == "plc_ab_opcodes"
        for r in reasons
    )
