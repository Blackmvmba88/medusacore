"""Demostraciones simples de fórmulas universales (ejemplos numéricos).
Uso: python examples/formulas_demo.py
Requiere: numpy
"""

import math
import numpy as np

# Mecánica


def newton_second(mass, force):
    """Devuelve la aceleración a = F/m"""
    return force / mass


def hooke_force(k, x):
    """Fuerza elástica F = k * x"""
    return k * x


# Fluidos


def bernoulli_pressure(p_static, rho, v, h=0, g=9.81):
    """Calcula la constante de Bernoulli por unidad de volumen: p + 0.5 rho v^2 + rho g h"""
    return p_static + 0.5 * rho * v**2 + rho * g * h


def reynolds_number(rho, v, L, mu):
    return rho * v * L / mu


# Electricidad


def ohm_voltage(I, R):
    return I * R


def electric_power(V=None, I=None, R=None):
    if V is not None and I is not None:
        return V * I
    if I is not None and R is not None:
        return I**2 * R
    if V is not None and R is not None:
        return V**2 / R
    raise ValueError("Supply (V,I) or (I,R) or (V,R)")


# Gases


def ideal_gas_pressure(n, R, T, V):
    return n * R * T / V


# Transferencia de calor (conducción unidimensional simple)


def fourier_heat_flux(k, dTdx):
    """q = -k dT/dx"""
    return -k * dTdx


# PID (discreto simple)


def pid_control(e, e_prev, integral, Kp, Ki, Kd, dt):
    integral_new = integral + e * dt
    derivative = (e - e_prev) / dt if dt > 0 else 0.0
    u = Kp * e + Ki * integral_new + Kd * derivative
    return u, integral_new


def main():
    print("-- Mecánica --")
    print("Aceleración (F=10 N, m=2 kg):", newton_second(2.0, 10.0), "m/s^2")
    print("Fuerza Hooke (k=200 N/m, x=0.01 m):", hooke_force(200, 0.01), "N")

    print("\n-- Fluidos --")
    print(
        "Bernoulli (p=101325 Pa, rho=1.225 kg/m3, v=10 m/s):",
        bernoulli_pressure(101325, 1.225, 10.0),
    )
    print(
        "Reynolds (aire, v=10 m/s, L=0.1 m, mu=1.8e-5):",
        reynolds_number(1.225, 10.0, 0.1, 1.8e-5),
    )

    print("\n-- Electricidad --")
    print("V=I*R (I=2 A, R=10 ohm):", ohm_voltage(2.0, 10.0), "V")
    print("Potencia (V=20, I=2):", electric_power(V=20, I=2), "W")

    print("\n-- Gases --")
    # Ejemplo: 1 mol ideal en 0.022414 m3 a 273.15 K con R=8.314 J/mol/K
    print(
        "P (1 mol, V=0.022414 m3, T=273.15 K):",
        ideal_gas_pressure(1.0, 8.314, 273.15, 0.022414),
        "Pa",
    )

    print("\n-- Transferencia de calor --")
    print(
        "Flujo de calor (k=200 W/mK, dTdx=10 K/m):",
        fourier_heat_flux(200.0, 10.0),
        "W/m2",
    )

    print("\n-- PID (simulación de un paso) --")
    u, integ = pid_control(
        e=1.0, e_prev=0.5, integral=0.0, Kp=1.0, Ki=0.1, Kd=0.01, dt=0.1
    )
    print("Salida PID u=", u, "integral=", integ)


if __name__ == "__main__":
    main()
