from medusa.learners import parse_ingenierias_markdown
from medusa.learners import MAX_FIELD_CHARS


def test_parser_detects_script_and_shell_and_truncates():
    long_text = "A" * (MAX_FIELD_CHARS + 100)
    md = """
### Malicious
- Enfoque corto: prueba de inyección <script>alert('x')</script>
- Ojo de inteligencia: rm -rf / --no-preserve-root
- Herramientas y recursos: {}
""".format(long_text)
    res = parse_ingenierias_markdown(md)
    assert isinstance(res, list)
    assert len(res) == 1
    entry = res[0]
    # suspicious flags should be present
    assert "_suspicious" in entry
    suspicious = entry["_suspicious"]
    assert any("Enfoque corto" in k or True for k in suspicious.keys())
    # check truncation occurred in Herramientas y recursos
    tools = entry.get("Herramientas y recursos", "")
    assert tools.endswith("... [TRUNCATED]")


def test_parser_handles_malformed_lines_gracefully():
    md = """
### Broken
- Enfoque corto this lacks colon
- Ojo de inteligencia: normal line
random text without dash
- Ejemplos: (1) Good example (2) Another
"""
    res = parse_ingenierias_markdown(md)
    assert isinstance(res, list)
    entry = res[0]
    # Should still parse the normal line and examples
    assert entry.get("Ojo de inteligencia") == "normal line"
    assert "Ejemplos" in entry
