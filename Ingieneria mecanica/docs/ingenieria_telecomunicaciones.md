# Ingeniería de Telecomunicaciones — Ojo de inteligencia 🔍

Enfoque corto:
Diseño y operación de redes y sistemas de transmisión (móviles, fijas, satélites).

Ojo de inteligencia:
- Datos: contadores de tráfico, KPIs de red (throughput, latency), mediciones RF, registros de fallos.
- Tareas IA: predicción de congestión, optimización de asignación de recursos, diagnóstico automático de fallos por correlación de eventos.
- Quick wins: modelo de predicción de congestión en celdas y ajuste dinámico de parámetros para evitar degradación.

Competencias clave:
Redes, RF, protocolos, gestión de espectro, seguridad de red.

Herramientas y recursos:
Wireshark, NS-3, plataformas OSS/BSS, Python, frameworks de streaming (Kafka).

Ejemplos de proyecto:
1) Predicción de degradación de servicio por tráfico y rerouting automático.
2) Diagnóstico automático de fallos en red por correlación temporal y topológica de eventos.

Métricas:
Latencia, pérdida de paquetes, disponibilidad, tasa de reclamos.

Quick-start pipeline:
1. Stream de métricas a time-series DB.
2. Feature engineering y modelos de forecasting/anomaly detection.
3. Orquestación de acciones (playbooks) con supervisión humana por defecto.