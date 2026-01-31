"""Tests for the Medusa learners ingestion of docs/ingenierias.md"""

from medusa.learners import load_markdown, parse_ingenierias_markdown


def test_parse_returns_many_disciplines():
    txt = load_markdown("docs/ingenierias.md")
    disciplines = parse_ingenierias_markdown(txt)
    # Debe detectar al menos 10 disciplinas en el documento base
    assert len(disciplines) >= 10


def test_civil_contains_expected_fields():
    txt = load_markdown("docs/ingenierias.md")
    disciplines = parse_ingenierias_markdown(txt)
    names = [d.get("name") for d in disciplines]
    assert any("Ingeniería Civil" in n for n in names)
    civil = next(d for d in disciplines if "Ingeniería Civil" in d.get("name"))
    # debe contener enfoque y ejemplos
    assert "Enfoque corto" in civil or any(
        k.lower().startswith("enfoque") for k in civil.keys()
    )
    assert "Ejemplos" in civil and len(civil["Ejemplos"]) >= 1
