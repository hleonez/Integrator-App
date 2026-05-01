"""Gaussian Quadrature (2-point Gauss-Legendre)."""

from typing import Callable

Function = Callable[[float], float]

def gauss_quadrature_2(f: Function, a: float, b: float) -> float:
    # puntos y pesos para [-1,1]
    x0 = -1 / (3 ** 0.5)
    x1 =  1 / (3 ** 0.5)
    w0 = w1 = 1

    # cambio de variable a [a,b]
    mid = (a + b) / 2
    half = (b - a) / 2

    return half * (w0 * f(mid + half * x0) + w1 * f(mid + half * x1))