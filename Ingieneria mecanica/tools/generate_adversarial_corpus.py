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
    "latex_injection.md": r"""
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


def generate(output_dir: str | Path, make_count: int = 1, sample_size: int = 0, randomize: bool = True):
    """Generate an adversarial corpus with options.

    Args:
        output_dir: path to write files
        make_count: number of random noise files to add
        sample_size: if >0, copy first N files to `tests/adversarial_corpus/sample_set`
        randomize: whether to add small random variants
    Returns:
        list of generated Path objects
    """
    from random import randint, choice

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    created = []
    for name, content in SAMPLES.items():
        c = content
        if "{}" in c:
            long_text = "A" * 6000
            c = c.format(long_text)
        if randomize:
            c = c + "\n- NOTE: variant-id: {}\n".format(randint(1, 999999))
        p = out / name
        p.write_text(c, encoding="utf-8")
        created.append(p)
    # create additional randomized noisy files if requested
    for i in range(make_count):
        p = out / f"noise_{i}.md"
        content = "### Noise\n- Enfoque corto: random\n- Ojo de inteligencia: {}\n".format(
            ''.join(choice('abcdef0123456789') for _ in range(40))
        )
        p.write_text(content, encoding="utf-8")
        created.append(p)
    # optionally create a sample-set folder with a limited number of files to commit
    if sample_size > 0:
        sample_dir = Path("tests/adversarial_corpus/sample_set")
        sample_dir.mkdir(parents=True, exist_ok=True)
        for idx, p in enumerate(created[:sample_size]):
            dest = sample_dir / p.name
            dest.write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
    return created


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generar corpus adversarial para tests"
    )
    parser.add_argument("--out", default="tests/adversarial_corpus")
    args = parser.parse_args()
    files = generate(args.out)
    print(f"Generated {len(files)} files in {args.out}")
