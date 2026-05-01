"""Simpson's Rule integration method."""

from typing import Callable

Function = Callable[[float], float]


def simpson(f: Function, a: float, b: float, n: int) -> float:
    if n < 2 or n % 2 != 0:
        raise ValueError("n must be a positive even integer for Simpson's rule.")

    h = (b - a) / n
    nodes = [f(a + i * h) for i in range(n + 1)]

    weighted = nodes[0] + nodes[-1]
    for i in range(1, n):
        weight = 4 if i % 2 != 0 else 2
        weighted += weight * nodes[i]

    return (h / 3) * weighted