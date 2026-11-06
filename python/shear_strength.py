# -*- coding: utf-8 -*-
"""
shear_strength.py — Envolvente de resistencia al corte c, φ por mínimos cuadrados
=================================================================================

Ajusta la envolvente de Mohr-Coulomb a datos de corte directo (σn, τ) o de
triaxial (σ3, σ1), y entrega cohesión c, ángulo de fricción φ, R², residuos
por punto e intervalos de confianza al 95 %.

Versión Python del módulo JavaScript que ejecuta el calculador en:
    https://insarwatch.com/es/foundations/shear-strength

Corte directo:  τ = c + σn·tanφ     (regresión directa)
Triaxial:       p = (σ1+σ3)/2, q = (σ1−σ3)/2, q = c·cosφ + p·sinφ
    (el triaxial entrega un círculo de Mohr, no un punto; ajustar en p–q
     evita el error clásico de tratar σ1 como τ y σ3 como σn).

Licencia: MIT. Solo biblioteca estándar.
"""

import math

D2R = math.pi / 180
R2D = 180 / math.pi

# Cuantil 0.975 de la t de Student, grados de libertad 1..30 (df>30 → 1.96)
T975 = [12.706, 4.303, 3.182, 2.776, 2.571, 2.447, 2.365, 2.306, 2.262, 2.228,
        2.201, 2.179, 2.160, 2.145, 2.131, 2.120, 2.110, 2.101, 2.093, 2.086,
        2.080, 2.074, 2.069, 2.064, 2.060, 2.056, 2.052, 2.048, 2.045, 2.042]


def t975(df):
    if df < 1:
        return float("nan")
    if df <= 30:
        return T975[df - 1]
    return 1.96


def linreg(xs, ys):
    """Regresión lineal y = a + b·x (forma centrada). Devuelve dict o None."""
    n = len(xs)
    if n < 2:
        return None
    mx = sum(xs) / n
    my = sum(ys) / n
    sxx = sxy = syy = 0.0
    for x, y in zip(xs, ys):
        dx = x - mx
        dy = y - my
        sxx += dx * dx
        sxy += dx * dy
        syy += dy * dy
    if sxx < 1e-12:
        return None  # todos los x iguales
    b = sxy / sxx
    a = my - b * mx
    ssr = 0.0
    resid = []
    for x, y in zip(xs, ys):
        rr = y - (a + b * x)
        resid.append(rr)
        ssr += rr * rr
    df = n - 2
    s2 = ssr / df if df > 0 else 0.0
    se_b = math.sqrt(s2 / sxx) if df > 0 else float("nan")
    se_a = math.sqrt(s2 * (1 / n + mx * mx / sxx)) if df > 0 else float("nan")
    r2 = 1 - ssr / syy if syy >= 1e-12 else 1.0
    return {"a": a, "b": b, "r2": r2, "resid": resid, "seA": se_a, "seB": se_b,
            "df": df, "n": n, "s2": s2}


def fit_direct_shear(pts):
    """pts: lista de dicts {"sn", "tau", "label"?}. c en las mismas unidades que σ."""
    xs, ys = [], []
    for p in pts:
        if math.isfinite(p["sn"]) and math.isfinite(p["tau"]):
            xs.append(p["sn"])
            ys.append(p["tau"])
    fit = linreg(xs, ys)
    if fit is None:
        return None
    phi_rad = math.atan(fit["b"])
    t = t975(fit["df"])
    b_lo = fit["b"] - t * fit["seB"]
    b_hi = fit["b"] + t * fit["seB"]
    res = {
        "method": "direct", "n": fit["n"], "c": fit["a"],
        "phi": phi_rad * R2D, "r2": fit["r2"], "tanPhi": fit["b"],
        "cLo": fit["a"] - t * fit["seA"], "cHi": fit["a"] + t * fit["seA"],
        "phiLo": math.degrees(math.atan(b_lo)), "phiHi": math.degrees(math.atan(b_hi)),
        "points": [], "resid": fit["resid"], "df": fit["df"],
    }
    k = 0
    for p in pts:
        if not (math.isfinite(p["sn"]) and math.isfinite(p["tau"])):
            continue
        pred = res["c"] + p["sn"] * res["tanPhi"]
        res["points"].append({
            "x": p["sn"], "y": p["tau"], "pred": pred, "resid": p["tau"] - pred,
            "label": p.get("label") or ("S%d" % (k + 1)),
        })
        k += 1
    return res


def fit_triaxial(pts):
    """pts: lista de dicts {"s3", "s1", "label"?}. Exige σ1 ≥ σ3."""
    xs, ys, keep = [], [], []
    for p in pts:
        if not (math.isfinite(p["s3"]) and math.isfinite(p["s1"])):
            continue
        if not p["s1"] >= p["s3"]:
            continue
        xs.append((p["s1"] + p["s3"]) / 2)
        ys.append((p["s1"] - p["s3"]) / 2)
        keep.append(p)
    fit = linreg(xs, ys)
    if fit is None:
        return None
    sin_phi = fit["b"]
    if sin_phi <= -1 or sin_phi >= 1:
        return None
    phi_rad = math.asin(sin_phi)
    cos_phi = math.cos(phi_rad)
    c = fit["a"] / cos_phi if cos_phi > 1e-9 else float("nan")
    t = t975(fit["df"])
    b_lo = max(-0.999999, min(0.999999, fit["b"] - t * fit["seB"]))
    b_hi = max(-0.999999, min(0.999999, fit["b"] + t * fit["seB"]))
    a_lo = fit["a"] - t * fit["seA"]
    a_hi = fit["a"] + t * fit["seA"]
    c1 = a_lo / math.cos(math.asin(b_hi))
    c2 = a_hi / math.cos(math.asin(b_lo))
    res = {
        "method": "triaxial", "n": fit["n"], "c": c,
        "phi": phi_rad * R2D, "r2": fit["r2"], "sinPhi": sin_phi,
        "cLo": min(c1, c2), "cHi": max(c1, c2),
        "phiLo": math.degrees(math.asin(b_lo)), "phiHi": math.degrees(math.asin(b_hi)),
        "points": [], "resid": fit["resid"], "df": fit["df"],
    }
    for i, q in enumerate(keep):
        pp = (q["s1"] + q["s3"]) / 2
        qq = (q["s1"] - q["s3"]) / 2
        pred = res["c"] * cos_phi + pp * sin_phi
        res["points"].append({
            "x": pp, "y": qq, "pred": pred, "resid": qq - pred,
            "label": q.get("label") or ("T%d" % (i + 1)),
            "s3": q["s3"], "s1": q["s1"],
        })
    return res


def strength_at(res, sigma):
    """Resistencia al corte en (σ, τ) para una tensión normal dada."""
    if not res:
        return float("nan")
    if res["method"] == "direct":
        return res["c"] + sigma * res["tanPhi"]
    return res["c"] + sigma * math.tan(res["phi"] * D2R)


if __name__ == "__main__":
    # Corte directo: (100, 55), (200, 90), (300, 130), (400, 175)
    # → c ≈ 15 kPa, φ ≈ 21,8° (tanφ = 0,40)
    pts = [{"sn": 100, "tau": 55}, {"sn": 200, "tau": 90},
           {"sn": 300, "tau": 130}, {"sn": 400, "tau": 175}]
    r = fit_direct_shear(pts)
    print("c = %.1f kPa · φ = %.1f° · R² = %.4f" % (r["c"], r["phi"], r["r2"]))

    # Triaxial: (σ3, σ1) = (100, 300), (200, 500), (300, 780), (400, 1080)
    pts3 = [{"s3": 100, "s1": 300}, {"s3": 200, "s1": 500},
            {"s3": 300, "s1": 780}, {"s3": 400, "s1": 1080}]
    t = fit_triaxial(pts3)
    print("triaxial: c = %.1f kPa · φ = %.1f° · R² = %.4f" % (t["c"], t["phi"], t["r2"]))
