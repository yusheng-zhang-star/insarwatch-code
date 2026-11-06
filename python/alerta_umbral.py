# -*- coding: utf-8 -*-
"""
alerta_umbral.py — Clasificación de alerta InSAR por umbrales
==============================================================

Clasifica la velocidad de deformación (mm/año) y su aceleración opcional
(mm/año²) en tres niveles: verde / amarillo / rojo.

Versión Python del módulo JavaScript que ejecuta el calculador en:
    https://insarwatch.com/es/insar/alerta-umbral

Umbrales por defecto (10 / 50 mm/año), tomados de la literatura de monitoreo
de laderas con InSAR:
    · ±10 mm/año  — frontera estable/inestable (Wasowski & Bovenga 2014,
      y varios estudios SBAS-InSAR de Lanzhou, Bailong, Longhua).
    · >50 mm/año  — grietas de pie y daños en vías (validación de campo).
Los umbrales reales deben fijarse con la norma o el plan de monitoreo del
proyecto; este módulo es una clasificación de cribado, no un sistema de alerta.

Licencia: MIT. Solo biblioteca estándar.
"""

DEFAULT_YELLOW = 10
DEFAULT_RED = 50


def classify(velocity, acceleration=None, yellow=DEFAULT_YELLOW, red=DEFAULT_RED):
    """Devuelve {"level", "velocity", "accelTrend", "hasAccel"} o {"error"}.

    velocity: mm/año (con signo o en valor absoluto).
    acceleration: mm/año² (None = desconocida).
    """
    try:
        v = abs(float(velocity))
    except (TypeError, ValueError):
        return {"error": "invalid_velocity"}
    y = float(yellow)
    r = float(red)
    if not (y > 0 and r > y):
        return {"error": "invalid_thresholds"}

    level = "red" if v >= r else ("yellow" if v >= y else "green")

    has_accel = acceleration is not None and acceleration != ""
    accel_trend = None
    if has_accel:
        try:
            a = float(acceleration)
        except (TypeError, ValueError):
            a = 0.0
            has_accel = False
        accel_trend = "accelerating" if a > 0.05 else ("decelerating" if a < -0.05 else "steady")

    # La aceleración es el precursor típico: amarillo + aceleración → rojo;
    # verde cerca del umbral + aceleración → amarillo.
    if accel_trend == "accelerating":
        if level == "yellow":
            level = "red"
        elif level == "green" and v >= y * 0.7:
            level = "yellow"

    return {"level": level, "velocity": v, "accelTrend": accel_trend, "hasAccel": has_accel}


if __name__ == "__main__":
    # Verificación: v=28 → amarillo; v=80 → rojo; v=30 con a=10 → rojo (acelera)
    for v, a in [(5, None), (28, None), (80, None), (30, 10), (8, 3)]:
        r = classify(v, a)
        print("v=%s a=%s -> %s" % (v, a, r["level"]))
