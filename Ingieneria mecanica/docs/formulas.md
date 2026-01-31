# Fórmulas universales para ingenierías — Resumen práctico ⚙️📐

Este documento recoge fórmulas conceptuales que aparecen en múltiples ramas de la ingeniería. No sustituye libros de texto; su objetivo es servir como índice de referencia rápida y base para implementaciones automatizadas.

---

## 1) Leyes de conservación (generales)
- Masa: d(rho)/dt + div(rho * v) = 0  (ecuación de continuidad)
- Momentum (Navier–Stokes, forma incompr.): rho (du/dt + u·∇u) = -∇p + mu ∇^2 u + f
- Energía: (balance energía interna + trabajo + calor)

*Por qué importa:* todas las disciplinas que modelan flujos, estructuras o procesos fisicoquímicos usan formas de estas ecuaciones.

---

## 2) Mecánica clásica
- Segunda ley de Newton: F = m a
- Ley de Hooke (elasticidad lineal): sigma = E * epsilon   (o F = k x para muelles)
- Energía cinética: KE = 1/2 m v^2

---

## 3) Fluidos
- Ecuación de Bernoulli (flujo incompresible, sin fricción): p + 1/2 rho v^2 + rho g h = cte
- Número de Reynolds: Re = (rho v L) / mu  (caracteriza flujo laminar/turbulento)

---

## 4) Transferencia de calor
- Ley de Fourier (conducción): q = -k ∇T  (tasa de flujo de calor)
- Ecuación de difusión / calor: dT/dt = alpha ∇^2 T

---

## 5) Electricidad y magnetismo
- Ley de Ohm: V = I R
- Potencia eléctrica: P = V I = I^2 R = V^2 / R
- Leyes de Kirchhoff (corrientes y tensiones)
- Ecuaciones de Maxwell (forma diferencial; resumen para electromagnetismo)

---

## 6) Termodinámica y gases
- Ley de los gases ideales: p V = n R T  (o p = rho R_spec T)
- Primera ley (conservación energía): dU = Q - W

---

## 7) Procesos y control
- Formas comunes: controlador PID (u(t) = Kp e + Ki ∫ e dt + Kd de/dt)
- Modelado lineal (sistemas LTI): dx/dt = A x + B u; y = C x + D u

---

## 8) Mecánica de materiales / fatiga
- Módulo de Young: E = stress / strain (elasticidad)
- Vida a fatiga (familias S-N) y criterios de fractura (p. ej. parámetro de intensidad de tensión K)

---

## 9) Dimensionalidad y escalado
- Teorema de Buckingham Pi: permite construir grupos adimensionales para reducir variables y comparar sistemas.

---

## 10) Estadística y optimización (transversales)
- Estimación por mínimos cuadrados: minimize ||Ax - b||^2
- PCA, regresión, clasificación: herramientas para modelado y reducción de variables
- Optimización multiobjetivo: trade-offs (ej. coste vs. rendimiento)

---

## Uso práctico y recomendaciones
- Empezar por identificar la ley de conservación relevante y las hipótesis (incompresible, estacionario, lineal, etc.).
- Usar números adimensionales (Re, Fr, Biot, etc.) para comparar y escalado.
- Comprobar unidades con librerías (p. ej. pint en Python) para evitar errores de escala.

---

Si quieres, puedo:
1) Crear `examples/formulas_demo.py` (Python) que implementa las fórmulas clave con funciones, ejemplos numéricos y comprobación de unidades. ✅
2) Generar un conjunto de notebooks (`notebooks/`) con visualizaciones y casos prácticos por disciplina. 📊
3) Preparar una plantilla YAML/JSON que documente, para cada ecuación, su dominio de validez, variables, unidades y referencias.

Elige la opción que prefieras y la implemento.