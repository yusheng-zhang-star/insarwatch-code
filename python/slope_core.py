# -*- coding: utf-8 -*-
"""
slope_core.py — Búsqueda del círculo crítico de un talud homogéneo
===================================================================

Tres métodos sobre la misma discretización geométrica (rebanadas verticales,
sin presión de poro u = 0): Fellenius, Bishop simplificado y Spencer (1967),
con búsqueda del círculo crítico por malla de centros y radios.

Versión Python del módulo JavaScript que ejecuta el calculador en:
    https://insarwatch.com/es/taludes/slip-surface

Coeficiente sísmico pseudoestático kh opcional (por defecto 0 = estático):
    Fellenius:  fuerza resistente (W·cosα − kh·W·sinα)·tanφ′
                fuerza motora  W·sinα + kh·W·cosα
    Bishop:     kh solo se suma a la fuerza motora (mα y N′ no cambian)
    Spencer:    kh·W entra al equilibrio horizontal; su momento se suma.

Licencia: MIT. Solo biblioteca estándar.
"""

import math

EPS = 1e-9
N_SLICES = 24


def build_slices(H, beta, gamma, cx, cy, R, n=N_SLICES):
    """Discretiza el talud en rebanadas verticales. Devuelve dict."""
    b_r = math.radians(beta)
    L = H / math.tan(b_r)
    slices = []
    overflow = False
    for i in range(n):
        x1 = (i / n) * L
        x2 = ((i + 1) / n) * L
        xm = (x1 + x2) / 2
        y_ground = H - (H / L) * xm
        dy = math.sqrt(max(0.0, R * R - (xm - cx) * (xm - cx)))
        y_circle = cy - dy
        if y_circle > y_ground:
            continue  # círculo sobre la superficie: rebanada fuera
        thick = y_ground - y_circle
        if thick <= 0:
            continue
        if x2 - cx > R or x1 - cx < -R:
            overflow = True
            break  # el arco corta por el lateral: círculo inválido
        alpha = math.asin((xm - cx) / R)
        if not math.isfinite(alpha):
            alpha = 0.0
        dl = abs(R * (math.asin((x2 - cx) / R) - math.asin((x1 - cx) / R)))
        slices.append({
            "x1": x1, "x2": x2, "xm": xm, "b": x2 - x1,
            "yC": y_circle, "thick": thick,
            "W": gamma * thick * (x2 - x1),
            "alpha": alpha, "dl": dl,
        })
    return {"slices": slices, "L": L, "H": H, "cx": cx, "cy": cy, "R": R, "overflow": overflow}


def fellenius_fs(slices, c, phi_r, kh=0):
    """Fellenius (ordinario) con α con signo, sin truncamiento."""
    res = sol = 0.0
    if not kh:
        for s in slices:
            res += c * s["dl"] + s["W"] * math.cos(s["alpha"]) * math.tan(phi_r)
            sol += s["W"] * math.sin(s["alpha"])
    else:
        tan_p = math.tan(phi_r)
        for s in slices:
            ca = math.cos(s["alpha"])
            sa = math.sin(s["alpha"])
            res += c * s["dl"] + (s["W"] * ca - kh * s["W"] * sa) * tan_p
            sol += s["W"] * sa + kh * s["W"] * ca
    return res / sol if sol > EPS else None


def bishop_fs(slices, c, phi_r, kh=0):
    """Bishop simplificado por iteración de punto fijo."""
    tan_p = math.tan(phi_r)
    sol = 0.0
    for s in slices:
        sol += s["W"] * math.sin(s["alpha"])
        if kh:
            sol += kh * s["W"] * math.cos(s["alpha"])
    if sol <= EPS:
        return None
    fs = fellenius_fs(slices, c, phi_r, kh)
    if fs is None:
        fs = 1.0
    for _ in range(200):
        total = 0.0
        for s in slices:
            m_a = math.cos(s["alpha"]) + tan_p * math.sin(s["alpha"]) / fs
            if m_a <= EPS:
                return None  # mα ≤ 0: círculo inválido en Bishop
            total += (c * s["b"] + s["W"] * tan_p) / m_a
        nxt = total / sol
        if not math.isfinite(nxt) or nxt <= 0:
            return None
        if abs(nxt - fs) < 1e-8:
            return nxt
        fs = nxt
    return None


def spencer_residuals(slices, c, phi_r, fs, theta, kh=0):
    """Residuos de Spencer: E_end (fuerza horizontal) y M (momento)."""
    tan_p = math.tan(phi_r)
    tan_t = math.tan(theta)
    E = M = neg_n = 0.0
    for s in slices:
        m_al = math.cos(s["alpha"]) + tan_p * math.sin(s["alpha"]) / fs
        if not m_al > EPS:
            return None
        A = (tan_p * math.cos(s["alpha"]) / fs - math.sin(s["alpha"])) / m_al
        denom = 1 + tan_t * A
        if abs(denom) < 1e-10:
            return None
        rhs = c * s["dl"] * math.cos(s["alpha"]) / fs \
            + (s["W"] - c * s["dl"] * math.sin(s["alpha"]) / fs) * A
        if kh:
            rhs -= kh * s["W"]
        d = rhs / denom
        n_p = (s["W"] - d * tan_t - c * s["dl"] * math.sin(s["alpha"]) / fs) / m_al
        if not (math.isfinite(n_p) and math.isfinite(d)):
            return None
        if n_p < 0:
            neg_n += 1
        T = (c * s["dl"] + n_p * tan_p) / fs
        E += d
        M += (-s["W"] * s["xm"]
              + n_p * (s["xm"] * math.cos(s["alpha"]) + s["yC"] * math.sin(s["alpha"]))
              + T * (s["xm"] * math.sin(s["alpha"]) - s["yC"] * math.cos(s["alpha"])))
        if kh:
            M += (s["yC"] + s["thick"] / 2) * kh * s["W"]
    return {"Eend": E, "M": M, "negN": neg_n}


def bisect_in_band(f, lo, hi, scan_n):
    """Busca f(x)=0 escaneando primero un cambio de signo y luego bisección."""
    prev_x = prev_v = None
    bracket = None
    for k in range(scan_n + 1):
        x = lo + (hi - lo) * k / scan_n
        v = f(x)
        if v is None:
            continue
        if prev_v is not None and (prev_v <= 0) != (v <= 0):
            bracket = (prev_x, x)
            break
        prev_x, prev_v = x, v
    if bracket is None:
        return None
    a, b = bracket
    for _ in range(50):
        mid = (a + b) / 2
        vm = f(mid)
        if vm is None:
            return None
        if (vm <= 0) != (prev_v <= 0):
            b = mid
        else:
            a = mid
            prev_v = vm
        if b - a < 1e-11:
            break
    return (a + b) / 2


def spencer(geom, c, phi_r, kh=0):
    """Spencer (1967): doble equilibrio fuerza/momento, θ anidado."""
    slices = geom["slices"]
    if not slices:
        return None
    fs0 = fellenius_fs(slices, c, phi_r, kh)
    if fs0 is None:
        fs0 = bishop_fs(slices, c, phi_r, kh)
    if fs0 is None:
        fs0 = 1.0
    lo = max(0.02, fs0 / 4)
    hi = min(50.0, fs0 * 4)

    def g_of(theta):
        def eend(x):
            r = spencer_residuals(slices, c, phi_r, x, theta, kh)
            return None if r is None else r["Eend"]
        fs_star = bisect_in_band(eend, lo, hi, 40)
        if fs_star is None:
            return None
        r = spencer_residuals(slices, c, phi_r, fs_star, theta, kh)
        return None if r is None else {"fs": fs_star, "M": r["M"], "negN": r["negN"]}

    theta = bisect_in_band(lambda t: (lambda v: None if v is None else v["M"])(g_of(t)),
                           -60 * math.pi / 180, 60 * math.pi / 180, 40)
    if theta is None:
        return None
    fin = g_of(theta)
    if fin is None or not math.isfinite(fin["fs"]) or fin["fs"] <= 0:
        return None
    return {"fs": fin["fs"], "theta": theta, "negN": fin["negN"]}


def search(H, beta, gamma, c, phi_deg, step, kh=0):
    """Malla completa: Fellenius y Bishop por mínimo; Spencer sobre top-30 Bishop."""
    kh = kh or 0
    b_r = math.radians(beta)
    phi_r = math.radians(phi_deg)
    L = H / math.tan(b_r)
    tried = 0
    best_f = best_b = None
    cands = []
    cx = -0.5 * L
    while cx <= 1.5 * H:
        cy = 0.5 * H
        while cy <= 2.5 * H:
            r_min = math.sqrt(cx * cx + cy * cy) * 0.8
            r_max = math.sqrt((L - cx) ** 2 + (H - cy) ** 2) + H
            R = r_min
            while R <= r_max:
                tried += 1
                g = build_slices(H, beta, gamma, cx, cy, R)
                if g["overflow"] or not g["slices"]:
                    R += step
                    continue
                f_f = fellenius_fs(g["slices"], c, phi_r, kh)
                f_b = bishop_fs(g["slices"], c, phi_r, kh)
                if f_f is not None and math.isfinite(f_f) and (best_f is None or f_f < best_f["fs"]):
                    best_f = {"fs": f_f, "cx": cx, "cy": cy, "R": R}
                if f_b is not None:
                    if best_b is None or f_b < best_b["fs"]:
                        best_b = {"fs": f_b, "cx": cx, "cy": cy, "R": R}
                    cands.append({"fsB": f_b, "cx": cx, "cy": cy, "R": R})
                R += step
            cy += step
        cx += step
    cands.sort(key=lambda x: x["fsB"])
    best_s = None
    for cd in cands[:30]:
        g2 = build_slices(H, beta, gamma, cd["cx"], cd["cy"], cd["R"])
        r = spencer(g2, c, phi_r, kh)
        # Puerta física: Spencer no debe superar 1.3× el Bishop del mismo círculo.
        if r is not None and r["fs"] <= 1.3 * cd["fsB"] and (best_s is None or r["fs"] < best_s["fs"]):
            best_s = {"fs": r["fs"], "cx": cd["cx"], "cy": cd["cy"], "R": cd["R"],
                      "theta": r["theta"], "negN": r["negN"]}
    if best_s is not None and best_b is not None and best_s["fs"] > 1.3 * best_b["fs"]:
        best_s = None
    return {"tried": tried, "L": L, "kh": kh, "fellenius": best_f,
            "bishop": best_b, "spencer": best_s}


if __name__ == "__main__":
    # Talud homogéneo: H=8, β=25°, γ=18, c=50, φ=35° (estable, FS > 1)
    r = search(8, 25, 18, 50, 35, 2, 0)
    print("tried=%d · L=%.2f" % (r["tried"], r["L"]))
    for m in ("fellenius", "bishop", "spencer"):
        v = r[m]
        print("  %-9s FS=%s" % (m, ("%.3f" % v["fs"]) if v else "—"))
