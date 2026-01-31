# Ingeniería Biomédica / Bioingeniería — Ojo de inteligencia 🔍

Enfoque corto:
Dispositivos médicos, imágenes médicas, bioinstrumentación y tecnologías clínicas.

Ojo de inteligencia:
- Datos: imágenes DICOM, señales fisiológicas, registros clínicos, ensayos preclínicos.
- Tareas IA: segmentación y detección en imágenes médicas, modelos de apoyo a diagnóstico, análisis de series fisiológicas, gemelos clínicos.
- Quick wins: pipeline de segmentación para cuantificación automática y reportes estructurados para radiólogos.

Competencias clave:
Bioinstrumentación, fisiología, regulaciones (FDA/CE), ética y validación clínica.

Herramientas y recursos:
ITK/VTK, MONAI, TensorFlow/PyTorch, herramientas DICOM, ambientes para validación clínica (sandbox).

Ejemplos de proyecto:
1) Segmentación automática de órganos y cuantificación para seguimiento de enfermedades.
2) Sistema de priorización de estudios radiológicos basado en detección de anomalías (triage).

Métricas:
Sensibilidad/especificidad, AUC, tiempo de reporte, impacto en flujo clínico.

Quick-start pipeline:
1. Ingesta DICOM y anonimización.
2. Anotación semiautomática con revisión humana y entrenamiento de modelos.
3. Despliegue en entorno clínico controlado (canary) y evaluación de impacto operativo.

Recursos:
- Guías regulatorias y checklist para validación clínica y gestión de datos de salud.