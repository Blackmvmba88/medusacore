#!/bin/bash
# Activa la capa ética en todo el sistema (incluye prueba smoke para staging)

echo "Activando Gobernanza Ética Distribuida..."

# 1. Instalar núcleo ético
pip install -e .[ethics] || true

# 2. Inicializar registro de consentimiento
python - <<'PY'
from src.blast_radius.ethical_governance import global_ethics
print('Motor ético inicializado en:', global_ethics.jurisdiction)
print('Principios activos:', list(global_ethics.ethical_frameworks.keys()))
PY

# 3. Integrar con CI/CD (staging smoke test)
echo "Integrando con CI/CD en entorno: staging..."
python - <<'PY'
from src.blast_radius.ethics_adapter import apply_ethics_to_scoring
from src.blast_radius.policy import load_policy
import json
sample_report = {
 "meta": {"version":"1.0","timestamp":"2026-02-03T00:00:00Z","policy_name":"staging-test"},
 "target": {"path":"./","sha256":"sha","size_bytes":0,"file_count":0},
 "blast_radius": {"score": 10, "classification": "LOW"}
}
capabilities = {"network":["outbound_unrestricted"], "persistence": ["local_file"], "obfuscation": []}
context = {"explicit_consent": False, "audit_capabilities": []}
policy, policy_hash = load_policy()
updated = apply_ethics_to_scoring(sample_report, capabilities, context, policy=policy, policy_hash=policy_hash)
print('Staging smoke test output:')
print(json.dumps(updated, indent=2))
PY

# 4. Primer manifiesto
python - <<'PY'
from src.blast_radius.ethical_governance import global_ethics
manifest = global_ethics.generate_ethical_manifest()
import json
print('Manifiesto Ético Inicial:')
print(json.dumps(manifest, indent=2))
PY

echo "✅ Capa ética activa en STAGING. La carga ahora es compartida."