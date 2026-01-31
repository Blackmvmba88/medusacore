from medusa.learners import parse_ingenierias_markdown


def test_detect_dicom_uid_and_tags():
    md = """
### DICOMExample
- Enfoque corto: prueba UID
- Ojo de inteligencia: StudyInstanceUID: 1.2.840.113619.2.55.3.604688403.784.141
- Herramientas y recursos: PixelData present (7FE0,0010)
"""
    res = parse_ingenierias_markdown(md)
    assert len(res) == 1
    entry = res[0]
    assert "_suspicious" in entry
    # find suspicious reasons across fields
    reasons = set()
    for v in entry["_suspicious"].values():
        reasons.update(v)
    assert "dicom_uid_like" in reasons or "dicom_tag_name" in reasons
    assert "dicom_pixeldata_tag" in reasons


def test_detect_plc_patterns():
    md = """
### PLCExample
- Enfoque corto: sample PLC
- Ojo de inteligencia: MOV R1, R2
- Herramientas y recursos: DB1.DBW0 I0.0 Q1.2 %M100 VAR_speed FB MyFunction
"""
    res = parse_ingenierias_markdown(md)
    entry = res[0]
    assert "_suspicious" in entry
    reasons = set()
    for v in entry["_suspicious"].values():
        reasons.update(v)
    assert any(r.startswith("plc_") for r in reasons)
    assert (
        "plc_db_address" in reasons
        or "plc_input_address" in reasons
        or "plc_output_address" in reasons
    )
