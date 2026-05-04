"""Método de integración de la Regla de Boole."""

from typing import Callable

Function = Callable[[float], float]

def boole(f: Function, a: float, b: float, n: int) -> float:
    if n < 4 or n % 4 != 0:
        raise ValueError("n must be a positive multiple of 4 for Boole's rule.")

    h = (b - a) / n
    boole_coefficients = [7, 32, 12, 32, 7]
    total = 0.0

    # Iterar sobre cada grupo de 4 subintervalos
    for group in range(n // 4):
        base_index = group * 4
        group_sum = sum(
            boole_coefficients[j] * f(a + (base_index + j) * h)
            for j in range(5)
        )
        total += group_sum

    return (2 * h / 45) * total