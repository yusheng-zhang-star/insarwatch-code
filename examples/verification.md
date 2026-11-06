# Hand-worked verification

Every module prints these numbers when executed directly. The intermediate
steps below are written out so a reviewer can reproduce them with a pocket
calculator — no library output is taken on trust.

## 1. `fases_suelo.py` — Mexico City clay, Gs = 2.70

Certificate data: gamma = 18 kN/m³, w = 15 %, gw = 9.81 kN/m³.

```
e      = 2.70 * 9.81 * 1.15 / 18 - 1                 = 0.6923
n      = 0.6923 / 1.6923                             = 0.4090
S      = 0.15 * 2.70 / 0.6923                        = 0.5850  (58.5 %)
gamma_d   = 18 / 1.15                                = 15.65 kN/m³
gamma_sat = (2.70 + 0.6923) * 9.81 / 1.6923          = 19.67 kN/m³
gamma'    = 19.67 - 9.81                             =  9.86 kN/m³
```

Inverse branch `from_ges(2.70, 0.70, 100)` gives gamma = 19.67 kN/m³,
w = 25.93 %, n = 0.412, gamma_d = 15.58, gamma_sat = 19.67,
gamma' = 9.86 kN/m³.

## 2. `shear_strength.py` — direct shear envelope

Points (sigma_n, tau) in kPa: (100, 55), (200, 90), (300, 130), (400, 175).
Centred least squares gives slope tan(phi) = 0.40 and intercept c = 15 kPa,
so phi = atan(0.40) = 21.8°. The function also returns R², per-point
residuals and 95 % limits from the t0.975 table (df = n - 2 = 2 → 4.303).

Triaxial companion set: (sigma3, sigma1) = (100, 300), (200, 500),
(300, 780), (400, 1080). Fitting in p–q space avoids treating sigma1 as a
shear stress. Specimens with sigma1 < sigma3 are rejected, not silently kept.

## 3. `atterberg.py` — synthetic flow curve

Construct w = -10·log10(N) + b with b = 40 + 10·log10(25), so LL = 40 % at
N = 25. Points at N = 10, 25, 50 lie exactly on the line, therefore R² = 1.0000.
With LP = 18 and w_n = 28:

```
LL = 40.0        IP = 40 - 18 = 22.0
IL = (28 - 18) / 22 = 0.455
A-line = 0.73 * (40 - 20) = 14.6  -> IP above the A-line
U-line = 0.9  * (40 - 8)  = 28.8  -> IP below the U-line
```

## 4. `slope_core.py` — homogeneous slope

`search(H=8, beta=25°, gamma=18, c=50, phi=35°, step=2, kh=0)` is a stable
configuration (FS > 1). The grid sweeps circle centres from cx = -0.5·L to
1.5·H and cy from 0.5·H to 2.5·H, with radii between 0.8·sqrt(cx²+cy²) and
sqrt((L-cx)²+(H-cy)²)+H. L = H/tan(beta) = 17.16 m. Slices = 24, u = 0.
Spencer is evaluated only on the 30 best Bishop circles and rejected when
FS_spencer > 1.3·FS_bishop for the same circle. The Python and JavaScript
implementations of this module are verified bit-identical.

## 5. `alerta_umbral.py` — classification checks

```
v =  5, a = None  -> green
v = 28, a = None  -> yellow
v = 80, a = None  -> red
v = 30, a = +10   -> red      (yellow + accelerating)
v =  8, a =  +3   -> yellow   (green at 0.7*10 = 7 mm/yr + accelerating)
```

Defaults yellow = 10, red = 50 mm/yr are literature screening values, not a
standard. Acceleration trend threshold is ±0.05 mm/yr².

## 6. `nivelacion.py` — closed level loop

Segments (dh in mm, d in m): (+1000, 200), (-600, 150), (-395, 250).

```
sum(dh)  = 1000 - 600 - 395 = 5 mm   -> fh = 5 - 0 = 5 mm
sum(d)   = 600 m = 0.6 km
E        = 20 * sqrt(0.6)            = 15.49 mm
1:T      = 5 / 600 = 1:120
passes   = |5| <= 15.49              -> True
v_1 = -5*200/600 = -1.67 mm
v_2 = -5*150/600 = -1.25 mm
v_3 = -5*250/600 = -2.08 mm   (sum = -5.00 mm)
```

## 7. `curva_circular.py` — delta = 60°, R = 100 m

```
T = 100*tan(30°)              = 57.74 m
E = 100*(1/cos(30°) - 1)      = 15.47 m
L = 100*pi/3                  = 104.72 m
C = 2*100*sin(30°)            = 100.00 m
M = 100*(1 - cos(30°))        = 13.40 m
degree = 1145.9156 / 100      = 11.46 deg per 20 m chord
```

Stakeout at 20 m steps: arc distances 20, 40, 60, 80, 100 m plus a final
fractional station at L = 104.72 m. Deflection delta = l/(2R) in radians,
chord = 2R·sin(delta). The final station is always emitted.

## Reproducing

```
for f in python/*.py; do python "$f"; done
```

Compare the printed values with the tables above, then with the corresponding
online calculator. If you change a formula, update both the Python and the
JavaScript implementation and this file together.
