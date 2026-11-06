# -*- coding: utf-8 -*-
"""
atterberg.py — Límites de Atterberg desde la curva de fluencia
==============================================================

Ajusta la curva de fluencia w = a·log10(x) + b por mínimos cuadrados y
obtiene el límite líquido LL, el índice de plasticidad IP y el índice de
liquidez IL, con la posición en la carta de plasticidad de Casagrande.

Versión Python del módulo JavaScript que ejecuta el calculador en:
    https://insarwatch.com/es/foundations/atterberg-limits

    Casagrande (copa):  x = golpes N,   LL = w(N=25)
    Cono (76 g):        x = penetración d (mm), LL = w(d=20)

Licencia: MIT. Solo biblioteca estándar.
"""

import math


def aline(ll):
    """Línea A: IP = 0,73·(LL−20)."""
    return 0.73 * (ll - 20)


def uline(ll):
    """Línea U: IP = 0,9·(LL−8)."""
    return 0.9 * (ll - 8)


def _clean_points(rows):
    points = []
    dropped = 0
    for r in rows:
        try:
            x = float(r[0])
            w = float(r[1])
        except (IndexError, TypeError, ValueError):
            dropped += 1
            continue
        if not (x > 0 and w > 0):
            dropped += 1
            continue
        points.append((x, w))
    return points, dropped


def fit_flow_curve(rows):
    """Ajusta w = a·log10(x) + b. Devuelve dict o None (puntos insuficientes)."""
    pts, dropped = _clean_points(rows)
    if len(pts) < 2:
        return None

    X = []
    sum_x = sum_y = sum_xx = sum_xy = sum_yy = 0.0
    for x, w in pts:
        lg = math.log10(x)
        X.append(lg)
        sum_x += lg
        sum_y += w
        sum_xx += lg * lg
        sum_xy += lg * w
        sum_yy += w * w
    n = len(pts)
    denom = n * sum_xx - sum_x * sum_x
    if abs(denom) <= 1e-12:
        return None  # todos los x iguales

    a = (n * sum_xy - sum_x * sum_y) / denom
    b = (sum_y - a * sum_x) / n

    mean_y = sum_y / n
    sst = sse = 0.0
    fitted = []
    residuals = []
    for i in range(n):
        y_hat = a * X[i] + b
        fitted.append(y_hat)
        residuals.append(pts[i][1] - y_hat)
        sst += (pts[i][1] - mean_y) ** 2
        sse += residuals[i] ** 2
    r2 = 1 - sse / sst if sst > 1e-12 else 1.0

    return {"a": a, "b": b, "r2": r2, "n": n, "dropped": dropped,
            "fitted": fitted, "residuals": residuals}


def liquid_limit(rows, mode):
    """LL sobre la curva en el golpe/penetración de referencia."""
    fit = fit_flow_curve(rows)
    if fit is None:
        return None
    target_x = 20 if mode == "cone" else 25
    LL = fit["a"] * math.log10(target_x) + fit["b"]
    return {"LL": LL, "targetX": target_x, "fit": fit}


def atterberg(rows, mode="casagrande", lp=0, wn=None):
    """Devuelve {"LL","IP","IL","fit","plasticity",...} o {"error"}."""
    r = liquid_limit(rows, mode)
    if r is None:
        return {"error": "insufficient_points"}
    LL = r["LL"]
    fit = r["fit"]

    if not (lp >= 0):
        return {"error": "invalid_lp"}
    IP = LL - lp
    if IP < 0:
        return {"error": "ip_negative", "LL": LL, "fit": fit, "IP": IP}

    IL = None
    if wn is not None and wn != "":
        try:
            w = float(wn)
            IL = (w - lp) / IP if IP > 1e-9 else None
        except (TypeError, ValueError):
            IL = None

    a = aline(LL)
    u = uline(LL)
    side = "above" if IP >= a else "below"
    anomaly = IP > u

    return {
        "LL": LL, "IP": IP, "IL": IL, "fit": fit,
        "targetX": r["targetX"], "mode": mode,
        "plasticity": {"aline": a, "uline": u, "side": side, "anomaly": anomaly},
    }


if __name__ == "__main__":
    # w = −10·log10(N) + b, con LL = 40 % en N=25 → b = 40 + 10·log10(25)
    b_target = 40 + 10 * math.log10(25)
    pts = [
        (10, -10 * math.log10(10) + b_target),
        (25, 40),
        (50, -10 * math.log10(50) + b_target),
    ]
    r = atterberg(pts, "casagrande", 18, 28)
    print("LL = %.1f %% · IP = %.1f %% · IL = %.3f" % (r["LL"], r["IP"], r["IL"]))
    print("R² = %.4f · posición: %s" % (r["fit"]["r2"], r["plasticity"]["side"]))
