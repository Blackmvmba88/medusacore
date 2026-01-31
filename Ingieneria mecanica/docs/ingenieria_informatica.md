# Ingeniería Informática / Software — Ojo de inteligencia 🔍

Enfoque corto:
Desarrollo de software, arquitecturas, sistemas distribuidos y prácticas de ingeniería de confiabilidad.

Ojo de inteligencia:
- Datos: logs, traces, métricas de rendimiento, repositorios de código, CI artifacts.
- Tareas IA: anomaly detection en logs, generación asistida de código, MLOps (pipelines reproducibles), automatización de pruebas.
- Quick wins: pipeline CI que incluye análisis estático y tests automáticos, detector de regresiones por ML sobre métricas.

Competencias clave:
Arquitectura de software, testing, seguridad, DevOps, modelado de datos.

Herramientas y recursos:
Git, Docker, Kubernetes, pytest, Prometheus, ELK, GitHub Actions/GitLab CI.

Ejemplos de proyecto:
1) Pipeline MLOps reproducible (train → evaluate → canary → promote) con versionado de datos y modelos.
2) Sistema de detección de anomalías en logs que dispara alertas y crea issues automáticos.

Métricas:
MTTR, cobertura de tests, tasa de regresiones, tiempo de despliegue.

Quick-start pipeline:
1. Versionado: código + datos + modelos con tags y metadatos.
2. CI: lint, tests unitarios, integración y pruebas de canary.
3. Observabilidad: dashboards y alertas con umbrales adaptativos (ML-driven).