"""Método de integración de la Regla Trapezoidal."""

from typing import Callable

Function = Callable[[float], float]



def trapezoidal(f: Function, a: float, b: float, n: int) -> float:
    
    if n < 1:
        raise ValueError("n must be at least 1.")

    h = (b - a) / n
    interior_sum = sum(f(a + i * h) for i in range(1, n))
    return (h / 2) * (f(a) + 2 * interior_sum + f(b))