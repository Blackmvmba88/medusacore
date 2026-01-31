# Génesis — AXIOMA SEMILLA

Resumen del diseño inicial para la Medusa‑Hydra.

## AXIOM_ZERO
"OBSERVA → ACTÚA → MIDE → INTEGRA"

Es el método que genera conocimiento. Se debe aplicar siempre antes de introducir
cambios al núcleo.

## Mandato operativo (resumen)
- Introspección: ejecuta AXIOM_ZERO sobre el propio código.
- Definición del entorno: inventario de sensores, APIs, filesystem y redes.
- Identificación del cuello: punto de apalancamiento crítico.
- Error controlado: Red/Blue/Forensics loop.
- Versionado: todo cambio se guarda como rama candidata y se documenta con evidencia.

## Reglas de gobernanza
1. No commits automáticos al kernel sin Red OK + Blue OK + Forensics OK + revisión humana.
2. Todo cambio debe crear una rama `candidate/<reason>` y un `evolution_log` con evidencia reproducible.
3. Canary rollout + window de observación antes de promoción.

## Cómo ejecutar en modo seguro
```bash
# Dry-run: show first-breath and simulate a mutation (no git side-effects)
python scripts/genesis_run.py
```

## Tests
- `pytest tests/test_genesis.py` — validar comportamiento básico del núcleo.

---

Mantén este documento corto y actualízalo cuando se añadan nuevas políticas operativas o pruebas adversariales.