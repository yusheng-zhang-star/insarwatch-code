# -*- coding: utf-8 -*-
"""
fases_suelo.py — Relaciones volumétricas y gravimétricas del suelo
=================================================================

Convierte los tres valores que mide el laboratorio (gravedad específica Gs,
peso específico natural γ y humedad w) en todas las magnitudes que el
proyecto usa después: índice de vacíos e, porosidad n, saturación S y los
pesos específicos seco, saturado y sumergido.

Este archivo es la versión Python del módulo JavaScript que ejecuta el
calculador en línea en:
    https://insarwatch.com/es/foundations/fases-suelo

Las tres relaciones que gobiernan el suelo:

    1) γ  = Gs·γw·(1+w)/(1+e)        (relación de pesos)
    2) n  = e/(1+e)   ⇔  e = n/(1−n) (relación de volúmenes)
    3) S·e = w·Gs     ⇔  S = w·Gs/e  (relación de saturación)

Dados tres valores independientes se determinan los otros tres. Los dos
tríos más usados en la práctica son (Gs, γ, w) y (Gs, e, S).

Licencia: MIT. Úselo libremente; cite la fuente si lo publica.
Solo biblioteca estándar de Python — sin dependencias externas.
"""

GW = 9.81  # peso específico del agua, kN/m³


def from_gsw(Gs, gamma, w):
    """Dados Gs, peso específico natural γ (kN/m³) y humedad w (%).

    Devuelve un diccionario con e, n (tanto por uno), S (tanto por uno),
    gd, gsat y gprime (kN/m³). Devuelve None si los datos no son físicamente
    posibles (índice de vacíos no positivo).

    Ejemplo:
        >>> from_gsw(2.70, 18, 15)
        {'e': 0.692, 'n': 0.409, 'S': 0.585, 'gd': 15.65, 'gsat': 19.67, 'gprime': 9.86}
    """
    if not (Gs > 0 and gamma > 0 and w >= 0):
        return None
    wd = w / 100
    e = Gs * GW * (1 + wd) / gamma - 1
    if not (e > 0):
        return None  # índice de vacíos no positivo: datos inconsistentes
    n = e / (1 + e)
    S = wd * Gs / e          # permite S > 1 (sobresaturación, señal de error)
    gd = gamma / (1 + wd)
    gsat = (Gs + e) * GW / (1 + e)
    gprime = gsat - GW
    return {
        "e": e,
        "n": n,
        "S": S,
        "gd": gd,
        "gsat": gsat,
        "gprime": gprime,
    }


def from_ges(Gs, e, S):
    """Dados Gs, índice de vacíos e y saturación S (%).

    Devuelve γ (kN/m³), w (%), n (tanto por uno) y los pesos específicos
    seco, saturado y sumergido. Devuelve None si e ≤ 0 o S ≤ 0.

    Ejemplo:
        >>> from_ges(2.70, 0.70, 100)
        {'gamma': 19.67, 'w': 25.93, 'n': 0.412, 'gd': 15.58, 'gsat': 19.67, 'gprime': 9.86}
    """
    if not (Gs > 0 and e > 0 and S > 0):
        return None
    Sd = S / 100
    wd = Sd * e / Gs
    n = e / (1 + e)
    gamma = Gs * GW * (1 + wd) / (1 + e)
    gd = Gs * GW / (1 + e)
    gsat = (Gs + e) * GW / (1 + e)
    gprime = gsat - GW
    return {
        "gamma": gamma,
        "w": wd * 100,
        "n": n,
        "gd": gd,
        "gsat": gsat,
        "gprime": gprime,
    }


if __name__ == "__main__":
    # ── Verificación manual (arcilla de la CDMX, Gs=2.70) ──────────────
    # Datos del certificado: γ = 18 kN/m³, w = 15 %
    r = from_gsw(2.70, 18, 15)

    # e = 2.70 · 9.81 · 1.15 / 18 − 1 = 0.6923
    # n = 0.6923 / 1.6923 = 0.4090
    # S = 0.15 · 2.70 / 0.6923 = 0.5850  (58.5 %)
    # γd = 18 / 1.15 = 15.65 kN/m³
    # γsat = (2.70 + 0.6923) · 9.81 / 1.6923 = 19.67 kN/m³
    # γ′  = 19.67 − 9.81 = 9.86 kN/m³
    print("Triaxial (Gs, γ, w) = (2.70, 18, 15):")
    for k, v in r.items():
        print("  %-6s = %.3f" % (k, v))

    print()
    print("Saturado (Gs, e, S) = (2.70, 0.70, 100):")
    s = from_ges(2.70, 0.70, 100)
    for k, v in s.items():
        print("  %-6s = %.3f" % (k, v))
