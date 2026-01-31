# Ingeniería Civil — Ojo de inteligencia 🔍

Enfoque corto:
Diseño, construcción y operación de infraestructuras (puentes, carreteras, edificaciones, obras hidráulicas).

Ojo de inteligencia:
- Datos típicos: inspecciones fotográficas, sensores estructurales (strain, acelerómetros), GIS, históriales de mantenimiento.
- Tareas ML/IA útiles: detección de fisuras por visión, predicción de degradación, optimización logística de obra, modelos surrogate para FEA.
- Quick wins: pipeline de clasificación de daños en fotos y dashboard de priorización de inspecciones.

Competencias clave:
FEA, geotecnia, normativa, gestión de proyectos, GIS.

Herramientas y recursos:
OpenSees, ABAQUS, QGIS, Python (scikit-learn, PyTorch), BIM (Revit).

Ejemplos de proyecto:
1) Predicción de corrosión y vida útil de elementos de puentes a partir de series temporales y sensores.
2) Clasificador de daños en imágenes de inspección (con modelo de visión + métricas de confianza para human-in-loop).

Métricas / KPIs:
- Reducción de tiempo de inspección (%).
- Precisión en detección de daños.
- Coste de mantenimiento por km.

Quick-start pipeline (datos → modelo → despliegue):
1. Ingesta: fotos geolocalizadas + telemetría de sensores → S3/Archivo.
2. ETL: etiquetado semi-automático, augmentación, extracción de features (textura, fractal).
3. Modelado: CNN + calibración bayesiana de umbral.
4. Despliegue: API de inferencia, dashboard GIS y regla de priorización.

Recursos útiles:
- Manuales BIM y guías de inspección de infraestructuras.
- Datasets públicos de inspección (cuando existan) y plantillas de QGIS.