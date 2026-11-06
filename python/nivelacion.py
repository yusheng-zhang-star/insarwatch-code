# -*- coding: utf-8 -*-
"""
nivelacion.py — Cierre y compensación de una nivelación geométrica
===================================================================

Dados los tramos (desnivel Δh en mm, distancia d en m) y el desnivel conocido,
calcula el error de cierre, la tolerancia E = k·√L, la compensación proporcional
por distancia y la precisión relativa 1:T.

Versión Python del módulo JavaScript que ejecuta el calculador en:
    https://insarwatch.com/es/medicion/cierre-nivelacion

    fh = ΣΔh − Δh_conocido        (cerrada: Δh_conocido = 0)
    E  = k·√L                     (L en km, k en mm/√km; 20 = ordinaria/4º orden)
    v_i = −fh·d_i/Σd              (reparto proporcional a la distancia)
    1:T = |fh| / Σd

Licencia: MIT. Solo biblioteca estándar.
"""

import math


def nivelacion(segments, h_known=0, k=20):
    """segments: lista de dicts {"dh": mm, "dist": m}. Devuelve dict o {"error"}."""
    if not segments:
        return {"error": "no_segments"}
    kk = float(k)
    if not kk > 0:
        return {"error": "invalid_k"}

    total_dh = 0.0
    total_dist = 0.0
    for s in segments:
        try:
            dh = float(s["dh"])
            d = float(s["dist"])
        except (KeyError, TypeError, ValueError):
            return {"error": "invalid_segment"}
        if not d >= 0:
            return {"error": "invalid_segment"}
        total_dh += dh
        total_dist += d
    if not total_dist > 0:
        return {"error": "zero_distance"}

    hk = float(h_known)
    fh = total_dh - hk                     # error de cierre, mm
    fh_allow = kk * math.sqrt(total_dist / 1000)  # tolerancia, mm
    precision = abs(fh) / total_dist       # precisión relativa (adimensional)

    corrected = []
    for s in segments:
        dh = float(s["dh"])
        d = float(s["dist"])
        v = -fh * d / total_dist           # reparto proporcional, signo contrario
        corrected.append({"dh": dh, "dist": d, "v": v, "dhCorr": dh + v})

    return {
        "fh": fh,
        "fhAllow": fh_allow,
        "totalDh": total_dh,
        "totalDist": total_dist,
        "precision": precision,
        "k": kk,
        "corrected": corrected,
        "passes": abs(fh) <= fh_allow,
    }


if __name__ == "__main__":
    # Nivelación cerrada: +1000, −600, −395 mm → fh = 5 mm, E = 20·√0,6 = 15,49 mm
    segs = [
        {"dh": 1000, "dist": 200},
        {"dh": -600, "dist": 150},
        {"dh": -395, "dist": 250},
    ]
    r = nivelacion(segs, 0, 20)
    print("fh = %.1f mm · E = %.2f mm · 1:%d · %s" % (
        r["fh"], r["fhAllow"], round(1 / r["precision"]) if r["precision"] else 0,
        "dentro de tolerancia" if r["passes"] else "fuera de tolerancia"))
    for i, c in enumerate(r["corrected"], 1):
        print("  tramo %d: Δh=%+.1f  v=%+.2f  Δh_corr=%+.2f" % (i, c["dh"], c["v"], c["dhCorr"]))
