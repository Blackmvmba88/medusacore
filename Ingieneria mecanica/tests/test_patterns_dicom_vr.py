from medusa.learners import parse_ingenierias_markdown


def test_detect_patient_birthdate_and_accession():
    md = """
### DICOMVR
- Enfoque corto: datos sensibles
- Ojo de inteligencia: PatientBirthDate: 19900101
- Herramientas y recursos: PatientName: Doe^John, AccessionNumber: ABC-12345
- Notas: (0008,0050) AccessionNumber tag
"""
    res = parse_ingenierias_markdown(md)
    assert len(res) == 1
    entry = res[0]
    assert "_suspicious" in entry
    reasons = set()
    for v in entry["_suspicious"].values():
        reasons.update(v)
    assert "dicom_birthdate_DA" in reasons or "dicom_birthdate_iso" in reasons
    assert "dicom_patientname_value" in reasons
    assert "dicom_accession_value" in reasons or \
        "dicom_accession_tag_number" in reasons


def test_detect_dicom_tag_number_and_uid_formats():
    md = """
### DICOMUID
- Enfoque corto: UID y tags
- Ojo de inteligencia: StudyInstanceUID: 1.2.840.113619.2.55.3.604688403.784.141
- Herramientas y recursos: Tag (0010,0030) (birthdate)
"""
    res = parse_ingenierias_markdown(md)
    entry = res[0]
    assert "_suspicious" in entry
    reasons = set()
    for v in entry["_suspicious"].values():
        reasons.update(v)
    assert "dicom_uid_like" in reasons
    assert "dicom_tag_pattern" in reasons or \
        "dicom_birthdate_tag_number" in reasons
