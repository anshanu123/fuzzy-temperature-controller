"""Membership functions used by the fuzzy inference system."""

def triangular(x: float, a: float, b: float, c: float) -> float:
    """Triangular membership function with support [a, c] and peak b."""
    x, a, b, c = float(x), float(a), float(b), float(c)
    if not a <= b <= c:
        raise ValueError("Expected a <= b <= c")
    if x < a or x > c:
        return 0.0
    if x == b:
        return 1.0
    if x < b:
        return 1.0 if a == b else (x - a) / (b - a)
    return 1.0 if b == c else (c - x) / (c - b)


def trapezoidal(x: float, a: float, b: float, c: float, d: float) -> float:
    """Trapezoidal membership function with plateau [b, c]."""
    x, a, b, c, d = map(float, (x, a, b, c, d))
    if not a <= b <= c <= d:
        raise ValueError("Expected a <= b <= c <= d")
    if x < a or x > d:
        return 0.0
    if b <= x <= c:
        return 1.0
    if x < b:
        return 1.0 if a == b else (x - a) / (b - a)
    return 1.0 if c == d else (d - x) / (d - c)
