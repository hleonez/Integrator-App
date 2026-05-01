"""Romberg Integration method."""

from typing import Callable

Function = Callable[[float], float]

def romberg(f: Function, a: float, b: float, max_iter: int = 5) -> float:
    if max_iter < 1:
        raise ValueError("max_iter must be at least 1.")

    R = [[0.0] * (max_iter + 1) for _ in range(max_iter + 1)]

    # R[0][0] = trapecio básico
    R[0][0] = (b - a) * (f(a) + f(b)) / 2

    for i in range(1, max_iter + 1):
        n = 2 ** i
        h = (b - a) / n

        # suma de nuevos puntos (los impares)
        sum_new = sum(f(a + (2 * k - 1) * h) for k in range(1, 2**(i-1) + 1))

        # trapecio refinado
        R[i][0] = 0.5 * R[i-1][0] + h * sum_new

        # extrapolación de Richardson
        for j in range(1, i + 1):
            R[i][j] = R[i][j-1] + (R[i][j-1] - R[i-1][j-1]) / (4**j - 1)

    return R[max_iter][max_iter]