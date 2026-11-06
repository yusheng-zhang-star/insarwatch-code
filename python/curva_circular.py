# -*- coding: utf-8 -*-
"""
curva_circular.py — Elementos y replanteo de una curva circular simple
======================================================================

Dados la deflexión Δ (grados) y el radio R (m), calcula los seis elementos
de la curva y genera la tabla de replanteo por deflexiones.

Versión Python del módulo JavaScript que ejecuta el calculador en:
    https://insarwatch.com/es/medicion/curva-circular

    Tangente     T = R·tan(Δ/2)
    Externa      E = R·(sec(Δ/2) − 1)
    Longitud     L = R·Δ      (Δ en radianes)
    Cuerda larga C = 2R·sin(Δ/2)
    Ordenada media M = R·(1 − cos(Δ/2))
    Grado        D = 1145,9156/R   (° por cuerda de 20 m)

Replanteo por deflexiones: cada estación a distancia de arco l lleva una
deflexión δ = l/(2R) y se marca con la cuerda c = 2R·sin(δ).

Licencia: MIT. Solo biblioteca estándar.
"""

import math


def curva_circular(delta_deg, R):
    """Devuelve {"T","E","L","C","M","degree","delta"} o {"error"}."""
    try:
        d = float(delta_deg)
        r = float(R)
    except (TypeError, ValueError):
        return {"error": "invalid_input"}
    if not (0 < d < 180) or not r > 0:
        return {"error": "invalid_input"}
    delta = math.radians(d)
    T = r * math.tan(delta / 2)
    E = r * (1 / math.cos(delta / 2) - 1)
    L = r * delta
    C = 2 * r * math.sin(delta / 2)
    M = r * (1 - math.cos(delta / 2))
    degree = 1145.9156 / r
    return {"T": T, "E": E, "L": L, "C": C, "M": M, "degree": degree, "delta": delta}


def replanteo(delta_deg, R, chord_step):
    """Devuelve {"stations": [{"dist","deltaDeg","chord"}, ...], "L"} o {"error"}."""
    c = curva_circular(delta_deg, R)
    if "error" in c:
        return c
    step = float(chord_step)
    if not step > 0:
        return {"error": "invalid_step"}

    stations = []

    def push(dist):
        delta_rad = dist / (2 * R)
        stations.append({
            "dist": dist,
            "deltaDeg": math.degrees(delta_rad),
            "chord": 2 * R * math.sin(delta_rad),
        })

    dist = 0.0
    while dist + step <= c["L"] + 1e-9:
        dist += step
        push(dist)
    if dist < c["L"] - 1e-9:
        push(c["L"])  # tramo fraccionario final
    return {"stations": stations, "L": c["L"]}


if __name__ == "__main__":
    # Δ=60°, R=100 m → T=57,74 · E=15,47 · L=104,72 · C=100,00 · M=13,40 · D=11,46
    c = curva_circular(60, 100)
    print("T=%.2f · E=%.2f · L=%.2f · C=%.2f · M=%.2f · D=%.2f°/20m" % (
        c["T"], c["E"], c["L"], c["C"], c["M"], c["degree"]))
    rep = replanteo(60, 100, 20)
    print("Replanteo (paso 20 m):")
    for i, s in enumerate(rep["stations"], 1):
        print("  est %d: arco=%6.2f m  deflexión=%7.3f°  cuerda=%6.2f m" % (
            i, s["dist"], s["deltaDeg"], s["chord"]))
