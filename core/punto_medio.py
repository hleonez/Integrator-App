"""Midpoint Rule integration method."""

from typing import Callable

Function = Callable[[float], float]

def midpoint(f: Function, a: float, b: float, n: int) -> float:
    if n < 1:
        raise ValueError("n must be at least 1.")

    h = (b - a) / n
    return h * sum(f(a + (i + 0.5) * h) for i in range(n))