from medusa.learners import parse_ingenierias_markdown


def test_siemens_scl_block_detection():
    scl = """
### SiemensSCL
- Enfoque corto: SCL function block snippet
- Ojo de inteligencia: FUNCTION_BLOCK FB_Motor
- Herramientas y recursos: VAR_INPUT
    Speed: INT;
    Torque: INT;
END_VAR
BEGIN
    // simple assignment
    Speed := 100;
END_FUNCTION_BLOCK
"""
    res = parse_ingenierias_markdown(scl)
    entry = res[0]
    assert "_suspicious" in entry
    reasons = set()
    for v in entry["_suspicious"].values():
        reasons.update(v)
    assert any(
        r.startswith("plc_siemens") or r == "plc_structured_text" for r in reasons
    )


def test_allen_bradley_export_detection():
    export = """
### ABExport
- Enfoque corto: RSLogix export snippet
- Ojo de inteligencia: N7:0 B3:0/0 Local:1:I.Data.0 TON CTU MSG
- Herramientas y recursos: Program: MainRoutine
"""
    res = parse_ingenierias_markdown(export)
    entry = res[0]
    assert "_suspicious" in entry
    reasons = set()
    for v in entry["_suspicious"].values():
        reasons.update(v)
    assert any(r.startswith("plc_ab") or r == "plc_ab_tag_address" for r in reasons)
