# Ingeniería Electrónica — Ojo de inteligencia 🔍

Enfoque corto:
Diseño de circuitos, sistemas embebidos, comunicaciones y test de PCBs.

Ojo de inteligencia:
- Datos: imágenes de PCB, logs de pruebas, medidas eléctricas (IV), señales RF.
- Tareas IA: visión para inspección de soldaduras, diagnosis automática de fallos, TinyML en dispositivos embebidos.
- Quick wins: detector automático de soldaduras defectuosas que reduzca el muestreo manual.

Competencias clave:
Diseño PCB, RF, programación embebida, testing.

Herramientas y recursos:
KiCad, Altium, osciloscopios, FPGAs, TensorFlow Lite.

Ejemplos:
1) Detector automático de soldaduras defectuosas (visión + heurísticas de inspección).
2) Modelo TinyML para clasificación de señales de sensores en dispositivo embebido.

Métricas:
Tasa de fallos en campo, tiempo de diagnóstico, consumo de energía.

Quick-start pipeline:
1. Captura imágenes y pruebas eléctricas en banco → dataset etiquetado.
2. Entrenar modelo de detección + quantización para TFLite.
3. Desplegar en lote de prueba y evaluar rendimiento en campo.