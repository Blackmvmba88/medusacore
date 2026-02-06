# Nombre del proyecto — Descripción corta 🚀

**Resumen:** Una breve descripción (1–2 líneas) del propósito del proyecto y su público objetivo.

## 📌 Estado
- **Estado:** Iniciando / En desarrollo / Mantener (elige y actualiza)

## 🔒 Forensics & PII handling
- Parser optionally collects originals of detected sensitive fields (`_forensics_originals`).
- Use `tools/ingest_and_persist.py` to persist artifacts locally or upload to S3/GCS.
- CI contains a `persist-forensics` job that runs in the `forensics` GitHub Environment and requires manual approval before artifacts are persisted and (optionally) uploaded.
- See `docs/forensics.md` for full details and recommended retention/approval practices.

## 🚩 Epic: Forensics Roadmap (plan épico)
- **Resumen:** roadmap épico para convertir la ingesta y captura forense en un proceso auditable, automatizado y resistente (detección, redaction, capture, persistencia, retención y aprobaciones humanas).
- **Documento:** `docs/roadmap_epic.md` (milestones, roles, KPIs).
- **Issue / Epic:** https://github.com/Blackmvmba88/medusacore/issues/6
- **PRs relacionadas:** Automatización del Environment y reglas de approvers — PR #7 (incluye workflow dispatch, script y verificación automática).
- **Cómo usar:** instala el GitHub App según `docs/ops_forensics_env.md`, añade secrets `GITHUB_APP_ID` y `GITHUB_APP_PRIVATE_KEY`, y ejecuta la acción `Setup Forensics Environment` desde Actions (input: `reviewers`, `required_approving_review_count`).
- **Notas:** la automatización incluye `--dry-run` y `--verify` para pruebas seguras; ver `scripts/setup_forensics_env.py` y `tests/test_setup_forensics_env.py`.


## 🧭 Estructura del proyecto
- `src/` — Código fuente principal
- `tests/` — Pruebas unitarias e integración
- `docs/` — Documentación de diseño y decisiones arquitectónicas
- `.github/` — Configuración de CI y workflows (incluye `copilot-instructions.md`)

> Reemplaza o ajusta las rutas anteriores según la estructura real del repositorio.

## ⚙️ Requisitos
- Node >= X, Python >= Y, Go >= Z, etc. (rellenar según el stack)
- Docker (opcional) si se usan contenedores

## 🔧 Instalación
1. Clona el repositorio:

```bash
git clone <repo-url>
cd <repo-folder>
```

2. Instala dependencias (ejemplo):

```bash
# Node
npm install
# Python (recomendado: crear virtualenv)
python -m pip install --upgrade pip
python -m pip install pytest
# o si existe un requirements.txt
pip install -r requirements.txt
```

> Sustituye los comandos por los específicos del proyecto.

## ▶️ Cómo ejecutar
- Modo desarrollo:

```bash
npm run dev
# o
make run
```

- Ejecutar tests:

```bash
npm test
# o
pytest
```

### Ingestar índice de ingenierías (Medusa learning)
- Generar la base de conocimiento a partir de `docs/ingenierias.md`:

```bash
python scripts/ingest_ingenierias.py
# o explícitamente
python scripts/ingest_ingenierias.py docs/ingenierias.md data/ingenierias.json
```

El script parsea el documento y guarda `data/ingenierias.json` con la representación estructurada.

### Genesis (AXIOM_ZERO)
- Dry-run del núcleo Genesis:

```bash
python scripts/genesis_run.py
```

- Pruebas del núcleo:

```bash
pytest tests/test_genesis.py
```

## 🧪 Flujo de desarrollo y pruebas
- Ejecuta la suite de tests antes de abrir PRs.
- Incluye pruebas unitarias y, cuando aplique, pruebas de integración.
- Usa `pre-commit`/linters configurados en el repositorio.

## 🔁 Integraciones externas
- Bases de datos: (ej. Postgres en `docker-compose.yml`)
- Servicios 3ro: (ej. Stripe, S3, etc.) — documentar variables de entorno necesarias

## 🤝 Contribuir
- Abre issues para discutir cambios grandes.
- Crea PRs pequeños y descriptivos.
- Sigue el formato de commit (ej.: `feat(scope): descripción corta`).

## 📄 Licencia
- Añade aquí la licencia del proyecto (ej. MIT, Apache-2.0).

---

Si quieres, puedo rellenar este README usando archivos reales del proyecto (por ejemplo `package.json`, `Dockerfile`, `README` existente) o traducirlo a otro idioma. ¿Deseas que lo complete con más detalles ahora? ✨