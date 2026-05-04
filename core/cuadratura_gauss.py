"""Gaussian Quadrature (2-point Gauss-Legendre).

Approximates ∫f(x)dx on [a, b] by evaluating f at 2 strategically chosen
points (not equally spaced). Exact for polynomials of degree ≤ 3.
"""

from typing import Callable

Function = Callable[[float], float]


def gauss_quadrature_2(f: Function, a: float, b: float) -> float:
    """Approximate ∫f(x)dx on [a, b] using 2-point Gauss-Legendre quadrature.

    Does NOT require n — always evaluates exactly 2 points.
    Exact for polynomials of degree ≤ 3.

    Args:
        f: The function to integrate.
        a: Left endpoint of the interval.
        b: Right endpoint of the interval.

    Returns:
        Numerical approximation of the definite integral.
    """
    # Gauss-Legendre nodes and weights on [-1, 1]
    node_0 = -1.0 / (3 ** 0.5)
    node_1 =  1.0 / (3 ** 0.5)
    weight_0 = weight_1 = 1.0

    # Change of variable from [-1, 1] to [a, b]
    midpoint = (a + b) / 2.0
    half_length = (b - a) / 2.0

    return half_length * (
        weight_0 * f(midpoint + half_length * node_0) +
        weight_1 * f(midpoint + half_length * node_1)
    )