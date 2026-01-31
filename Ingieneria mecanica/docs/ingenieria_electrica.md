# Ingeniería Eléctrica — Ojo de inteligencia 🔍

Enfoque corto:
Generación, transmisión y distribución de energía; electrónica de potencia.

Ojo de inteligencia:
- Datos: series temporales de consumo, registros SCADA, eventos de protecciones, telemetría.
- Tareas IA: predicción de demanda, detección de anomalías, optimización de despacho en microgrids.
- Quick wins: modelo de predicción de carga a corto plazo y alertas tempranas de anomalías.

Competencias clave:
Teoría de circuitos, protección, electrónica de potencia, control.

Herramientas y recursos:
PSCAD, MATLAB/Simulink, OpenDSS, Python, herramientas SCADA.

Ejemplos de proyecto:
1) Predicción de demanda/consumo con modelos de series temporales (Prophet/NN).
2) Detección temprana de fallos en transformadores vía análisis de vibración y series temporales.

Métricas:
SAIDI/SAIFI, precisión de predicción, coste operativo.

Quick-start pipeline:
1. Centralizar telemetría SCADA → time-series DB.
2. Engineer features (lags, ventanas, variables exógenas) y entrenar modelos forecasting.
3. Despliegue en canary con alarmas y pruebas de backtest continuas.