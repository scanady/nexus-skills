"""Shared distribution math for the statistical-methods scripts.

Standard library only. Accuracy is about 1e-9 for the p-values and critical
values these scripts report, which is far inside any rounding they print.
"""

import math

_EPS = 1e-14
_MAX_ITER = 500


def normal_cdf(z: float) -> float:
    return 0.5 * math.erfc(-z / math.sqrt(2))


def normal_ppf(p: float) -> float:
    """Inverse standard normal CDF by bisection."""
    if not 0 < p < 1:
        raise ValueError("probability must be between 0 and 1 (exclusive)")
    lo, hi = -12.0, 12.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if normal_cdf(mid) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def z_critical(alpha: float) -> float:
    """Two-sided critical z for significance level alpha."""
    return normal_ppf(1 - alpha / 2)


def _beta_cf(a: float, b: float, x: float) -> float:
    """Continued fraction for the incomplete beta function (modified Lentz)."""
    tiny = 1e-300
    qab, qap, qam = a + b, a + 1, a - 1
    c = 1.0
    d = 1 - qab * x / qap
    d = 1 / (d if abs(d) > tiny else tiny)
    h = d
    for m in range(1, _MAX_ITER):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1 + aa * d
        d = 1 / (d if abs(d) > tiny else tiny)
        c = 1 + aa / c
        c = c if abs(c) > tiny else tiny
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1 + aa * d
        d = 1 / (d if abs(d) > tiny else tiny)
        c = 1 + aa / c
        c = c if abs(c) > tiny else tiny
        delta = d * c
        h *= delta
        if abs(delta - 1) < _EPS:
            break
    return h


def reg_inc_beta(a: float, b: float, x: float) -> float:
    """Regularized incomplete beta I_x(a, b)."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    log_front = (
        math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
        + a * math.log(x) + b * math.log(1 - x)
    )
    front = math.exp(log_front)
    if x < (a + 1) / (a + b + 2):
        return front * _beta_cf(a, b, x) / a
    return 1 - front * _beta_cf(b, a, 1 - x) / b


def t_two_sided_p(t: float, df: float) -> float:
    """Two-sided p-value for a t statistic."""
    return reg_inc_beta(df / 2, 0.5, df / (df + t * t))


def t_critical(alpha: float, df: float) -> float:
    """Two-sided critical t for significance level alpha."""
    lo, hi = 0.0, 1e4
    for _ in range(200):
        mid = (lo + hi) / 2
        if t_two_sided_p(mid, df) > alpha:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def _reg_gamma_lower(a: float, x: float) -> float:
    """Regularized lower incomplete gamma P(a, x)."""
    if x <= 0:
        return 0.0
    log_front = -x + a * math.log(x) - math.lgamma(a)
    if x < a + 1:
        term = total = 1 / a
        n = a
        for _ in range(_MAX_ITER):
            n += 1
            term *= x / n
            total += term
            if abs(term) < abs(total) * _EPS:
                break
        return total * math.exp(log_front)
    tiny = 1e-300
    b = x + 1 - a
    c = 1 / tiny
    d = 1 / b
    h = d
    for i in range(1, _MAX_ITER):
        an = -i * (i - a)
        b += 2
        d = an * d + b
        d = d if abs(d) > tiny else tiny
        c = b + an / c
        c = c if abs(c) > tiny else tiny
        d = 1 / d
        delta = d * c
        h *= delta
        if abs(delta - 1) < _EPS:
            break
    return 1 - math.exp(log_front) * h


def chi2_p(stat: float, df: int) -> float:
    """Upper-tail p-value for a chi-squared statistic."""
    return 1 - _reg_gamma_lower(df / 2, stat / 2)


def effect_label(value: float, kind: str) -> str:
    """Cohen's conventional bands. Cramer's V bands are for df = 1."""
    cuts = (0.1, 0.3, 0.5) if kind == "v" else (0.2, 0.5, 0.8)
    v = abs(value)
    if v < cuts[0]:
        return "negligible"
    if v < cuts[1]:
        return "small"
    if v < cuts[2]:
        return "medium"
    return "large"
