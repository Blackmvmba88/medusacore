# MedusaCore 🌌

**Estado:** WIP / Genesis  
**Lenguajes principales:** Python, HTML, Shell  
**Propósito:** Núcleo modular de herramientas asistidas y automatización con un "HermeticCore" de gestión de semillas y procesos primordiales.

## 🔑 Concepto

MedusaCore es un framework experimental para la generación, control y optimización de entornos automatizados. Su corazón, **HermeticCore**, actúa como una semilla primordial (**AXIOM_ZERO PrimordialSeed**) que permite inicializar procesos, scripts y agentes de manera controlada y modular.

El objetivo es que el proyecto se autooptimice mediante la integración de scripts, herramientas y módulos que se ajustan dinámicamente a su entorno de ejecución.

## 🗂 Estructura del proyecto

```
medusacore/
│
├─ Ingieneria mecanica/        # Modelos, cálculos y simulaciones mecánicas
│
├─ herramientas_asistente/     # Scripts y UI para control de tareas
│   └─ Flask_webUI/            # Interfaz para gestión y monitoreo
│
├─ core/                       # Núcleo HermeticCore y AXIOM_ZERO
│   └─ seed.py                 # Inicialización de la semilla primordial
│   └─ optimizer.py            # Módulos de autooptimización
│
├─ tests/                      # Pruebas unitarias y de integración
│
└─ README.md
```

## ⚡ Funcionalidades clave

### HermeticCore
- Inicialización de PrimordialSeed (AXIOM_ZERO)
- Control de scripts y agentes
- Registro y monitoreo de procesos

### Herramientas asistente
- UI web (Flask) para gestión de scripts
- Automatización de tareas recurrentes
- Integración con módulos de simulación mecánica

### Optimización
- Módulos que analizan rendimiento y ajustan parámetros
- Capacidad de autoaprendizaje en función de logs y resultados
- Posibilidad de añadir agentes inteligentes en futuras versiones

## 🚀 Próximos pasos / Roadmap

- [ ] Documentación completa de HermeticCore y scripts
- [ ] Protección de ramas para evitar borrados accidentales
- [ ] Implementar módulos de autooptimización avanzados
- [ ] Añadir tests unitarios y de integración
- [ ] Crear un sistema de releases y paquetes PyPI

## 🧩 Contribución

### Clona el repositorio

```bash
git clone https://github.com/Blackmvmba88/medusacore.git
cd medusacore
```

### Instala dependencias

```bash
pip install -r requirements.txt
```

### Ejecuta la UI de herramientas asistente

```bash
cd herramientas_asistente
python app.py
```

### Para nuevas funciones, crea una rama desde wip/genesis

```bash
git checkout -b feature/nueva_funcion
```

## 📈 Autooptimización

MedusaCore puede evolucionar con:

- Monitoreo automático de logs y métricas
- Ajuste dinámico de scripts según el rendimiento
- Integración de "agentes" que propongan mejoras automáticamente
- Modularidad para añadir nuevos procesos sin romper el núcleo

## 🧪 Uso del Core

### Inicializar AXIOM_ZERO

```python
from core.seed import PrimordialSeed, HermeticCore, run_genesis_dry_run

# Inicializar la semilla primordial
seed = PrimordialSeed.initialize()
print(seed["statement"])

# Crear el núcleo hermético
core = HermeticCore()
print(f"Principios iniciales: {len(core.principles)}")

# Ejecutar dry-run de genesis
result = run_genesis_dry_run()
```

### Optimización automática

```python
from core.optimizer import Optimizer, PerformanceMonitor, run_optimization_cycle

# Crear monitor y optimizador
monitor = PerformanceMonitor(log_file="logs/performance.jsonl")
optimizer = Optimizer(monitor=monitor)

# Registrar operaciones
monitor.record_operation("process_data", duration=1.2, success=True)
monitor.record_operation("validate", duration=0.3, success=True)

# Ejecutar ciclo de optimización
result = run_optimization_cycle(optimizer, auto_adjust=True)
print(result["analysis"]["recommendations"])
```

### Decorador para medir rendimiento

```python
from core.optimizer import Optimizer

optimizer = Optimizer()

@optimizer.measure_operation("mi_funcion")
def mi_funcion_lenta():
    # Tu código aquí
    import time
    time.sleep(1)
    return "completado"

# La función será medida automáticamente
resultado = mi_funcion_lenta()

# Analizar rendimiento
analysis = optimizer.analyze_performance()
```

## 🧪 Ejecutar tests

```bash
# Ejecutar todos los tests
pytest

# Ejecutar tests específicos
pytest tests/test_seed.py
pytest tests/test_optimizer.py

# Con verbose
pytest -v

# Con cobertura
pytest --cov=core tests/
```

## 📝 Licencia

Este proyecto está en desarrollo activo. Consulta con el autor para detalles de licencia.

---

**Nota:** Este proyecto está en fase WIP/Genesis y evoluciona constantemente. Las APIs y estructuras pueden cambiar.
