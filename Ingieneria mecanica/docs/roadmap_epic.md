# Roadmap Épico — Forensics & Ingest Pipeline (6–12 meses) 🚀

**Visión**
Convertir la ingesta en un proceso auditable, resistente y automatizado: detección precisa, redaction configurada, captura forense reproducible y persistencia segura con aprobaciones humanas y políticas de retención.

## Epics y milestones

### Epic: Detección & Corpus Adversarial 🔬
- Objetivo: cobertura completa de DICOM VRs y heurísticas PLC; corpus adversarial reproducible.
- Milestones:
  - 1.1 Expansión de reglas DICOM por VR (PatientBirthDate, AccessionNumber, PatientAddress, ReferringPhysicianName, SOPInstanceUID, etc.).
  - 1.2 Heurísticas PLC por vendor (Siemens SCL, Allen‑Bradley) + tests unitarios.
  - 1.3 Generador de corpus adversarial (determinístico, semilla controlada).
  - 1.4 Cobertura de tests objetivo: >95% en patrones críticos.

### Epic: Forensics Platform & Redaction Engine 🛡️
- Objetivo: captura reproducible y redaction configurable, metadatos inmutables y firmas opcionales.
- Milestones:
  - 2.1 `hydras/forensics`: persistencia raw + `.meta.json` (id, sha256, timestamp UTC, branch, source).
  - 2.2 Redaction engine extensible (rules, truncate vs redact vs mask).
  - 2.3 Firma de metadatos y verificación de integridad.
  - 2.4 API interna para consultas forenses y restauración de artefactos (si aplica).

### Epic: Governance & CI Approval Flow 🔐
- Objetivo: gate humano en CI, roles y playbooks auditables.
- Milestones:
  - 3.1 Job `persist-forensics` que usa GitHub Environment con approvers.
  - 3.2 `docs/ops_forensics.md` con checklist operativo y playbooks de incidentes.
  - 3.3 Registro de aprobaciones y meta-aprobaciones en `.meta.json`.

### Epic: Cloud Hardened Storage & Retention IaC ☁️
- Objetivo: uploads seguros, lifecycle (retención/expiración) y replicación.
- Milestones:
  - 4.1 `hydras/cloud.py` y `hydras/gcs.py` con KMS/CMEK y retries seguras.
  - 4.2 Terraform/CloudFormation para lifecycle rules (S3/GCS).
  - 4.3 Tests de políticas de retención (simulaciones + unit tests).

### Epic: Adversarial Resilience & Monitoring 🎯
- Objetivo: campañas continuas de fuzz, red-team, detección de regresiones.
- Milestones:
  - 5.1 Integración de fuzzing scheduled en CI.
  - 5.2 Dashboards SIEM/Alerting para detecciones nuevas.
  - 5.3 Playbook para respuesta y remediación.

### Epic: e2e CI, Compliance & Audit ✅
- Objetivo: e2e reproducible en CI que produce artefactos firmados y reportes de cumplimiento.
- Milestones:
  - 6.1 e2e pipeline con dry-run y approved → persist.
  - 6.2 Reportes automáticos de cumplimiento (PDF/JSON) y export para auditoría.
  - 6.3 Pruebas de penetración y revisión externa (opcional).

---

## Roles sugeridos
- Product Dev: mantiene backlog y prioridades.
- Security/Infra: revisa diseños KMS, IaC y runs de red-team.
- QA: pruebas fuzz + integración.
- Legal/Compliance: revisiones de retention y datos sensibles.
- SRE: despliegue y monitorización.

## KPIs / Criterios de éxito
- Tests unit + e2e pasan en CI en cada PR.
- Artefactos persistidos con `.meta.json` firmados y aprobaciones registradas.
- Policy lifecycle aplicada en Cloud.
- Tiempo medio a aprobación < X horas (configurable).

---

## Checklist inicial (para empezar el Epic)
- [ ] Crear Issue/Epic en GitHub con milestones (Backlog, In Progress, Done)
- [ ] Añadir `docs/roadmap_epic.md` (este archivo)
- [ ] Crear branch base `epic/forensics-roadmap` y PR inicial con propuesta
- [ ] Definir reviewers/approvers y configurar Environment en GitHub
- [ ] Implementar primer milestone: expansión DICOM + tests

---

## Plantilla de Issue (uso rápido)
**Título:** epic(forensics): roadmap & milestones
**Descripción corta:** Roadmap épico para la plataforma de forensics e ingest. Ver `docs/roadmap_epic.md`.
**Milestones propuestos:** Detección, Forensics, CI Approvals, Cloud, Adversarial, e2e/Compliance.
**Suggested labels:** epic, forensics, infra, security
**Suggested reviewers:** @security, @infra, @qa

---

*Generado automáticamente como primer borrador. Ajustes y prioridades a definir en la reunión de planificación.*
