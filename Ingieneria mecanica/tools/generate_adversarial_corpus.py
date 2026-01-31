"""Generador de corpus adversarial para tests.
Genera archivos Markdown en una carpeta destino con diferentes vectores de ataque.
"""

from pathlib import Path

SAMPLES = {
    "script_injection.md": """
### Safety Test
- Enfoque corto: prueba de inyección <script>alert('xss')</script>
- Ojo de inteligencia: normal line
- Herramientas y recursos: simple
""",
    "shell_injection.md": """
### Shell Test
- Enfoque corto: prueba comando peligroso
- Ojo de inteligencia: rm -rf / --no-preserve-root
- Herramientas y recursos: sudo rm -rf /
""",
    "latex_injection.md": """
### LaTeX Test
- Enfoque corto: prueba LaTeX
- Ojo de inteligencia: \begin{equation}E=mc^2\end{equation}
- Herramientas y recursos: $ a + b $
""",
    "dicom_like.md": """
### DICOM Test
- Enfoque corto: prueba DICOM
- Ojo de inteligencia: DICM header present (0010,0020)
- Herramientas y recursos: (0010,0010) PatientName
""",
    "plc_commands.md": """
### PLC Test
- Enfoque corto: comandos PLC visibles
- Ojo de inteligencia: MOV R1, R2\nLD %M100
- Herramientas y recursos: ladder program snippet
""",
    "big_blob.md": """
### Big Blob Test
- Enfoque corto: campo muy largo
- Ojo de inteligencia: {}
- Herramientas y recursos: nothing
""",
}


def generate(output_dir: str | Path, make_count: int = 1):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    for name, content in SAMPLES.items():
        if "{}" in content:
            # generate a very long string to force truncation
            long_text = "A" * 6000
            content = content.format(long_text)
        p = out / name
        p.write_text(content, encoding="utf-8")
    # create additional randomized noisy files if requested
    for i in range(make_count):
        p = out / f"noise_{i}.md"
        p.write_text(
            "### Noise\n- Enfoque corto: random\n- Ojo de inteligencia: xyz\n",
            encoding="utf-8",
        )
    return list(out.iterdir())


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generar corpus adversarial para tests"
    )
    parser.add_argument("--out", default="tests/adversarial_corpus")
    args = parser.parse_args()
    files = generate(args.out)
    print(f"Generated {len(files)} files in {args.out}")
