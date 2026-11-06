<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/Dependencies-none-brightgreen.svg" alt="No dependencies">
</p>

# insarwatch-code

Open-source Python calculators for **geotechnical engineering, surveying and InSAR
monitoring** — the same math that runs the free online calculators at
[insarwatch.com](https://insarwatch.com) (Spanish).

> **⭐ If this saves you an hour of spreadsheet work, give it a star** — it helps more
> engineers find it. *(¿Te sirve? Dale una estrella para que más ingenieros lo encuentren.)*

## Why this repo

Geotechnical work still runs on spreadsheets: one tab per soil layer, copy-pasted
Boussinesq equations, magic-number unit conversions, and `=IF()` ladders nobody can
read six months later. Reports are non-reproducible and every project re-derives the
same formulas from scratch.

This repo replaces that with **plain, dependency-free Python** you can copy into your
own scripts. Every function:

- is **stdlib-only** (no numpy/scipy — just `import math`),
- is **hand-verified** against worked examples, and
- matches the live online calculator **to the digit** (error < 0.1 %).

## Calculators

| Function | Python | Online calculator (ES) |
|---|---|---|
| Soil phase relations (γ, w, Gs, e, n, S) | [`python/fases_suelo.py`](python/fases_suelo.py) | [/es/foundations/fases-suelo](https://insarwatch.com/es/foundations/fases-suelo) |
| Shear strength c, φ from direct shear / triaxial | [`python/shear_strength.py`](python/shear_strength.py) | [/es/foundations/shear-strength](https://insarwatch.com/es/foundations/shear-strength) |
| Atterberg limits (LL, IP, IL from flow curve) | [`python/atterberg.py`](python/atterberg.py) | [/es/foundations/atterberg-limits](https://insarwatch.com/es/foundations/atterberg-limits) |
| Slope stability (Fellenius / Bishop / Spencer) | [`python/slope_core.py`](python/slope_core.py) | [/es/taludes/slip-surface](https://insarwatch.com/es/taludes/slip-surface) |
| InSAR velocity alert thresholds (green/yellow/red) | [`python/alerta_umbral.py`](python/alerta_umbral.py) | [/es/insar/alerta-umbral](https://insarwatch.com/es/insar/alerta-umbral) |
| Level-loop closure and adjustment | [`python/nivelacion.py`](python/nivelacion.py) | [/es/medicion/cierre-nivelacion](https://insarwatch.com/es/medicion/cierre-nivelacion) |
| Circular curve and stakeout by deflections | [`python/curva_circular.py`](python/curva_circular.py) | [/es/medicion/curva-circular](https://insarwatch.com/es/medicion/curva-circular) |

## Quick start

```bash
git clone https://github.com/yusheng-zhang-star/insarwatch-code.git
cd insarwatch-code
python python/fases_suelo.py
```

Each file prints a worked example; the numbers must match the online calculator to
< 0.1 %.

## Verification

There is no `numpy` black box here. Each module ships a hand-worked verification inside
its docstring (see `examples/`), so you can trace every number back to the formula. The
slope-stability core is verified **bit-identical** against the JavaScript that runs on
the live site — same circle search, same Fellenius / Bishop / Spencer factors.

## Contributing

Adding a calculator is a small, well-defined task:

1. Pick a calculation that a field engineer does by hand (spreadsheet) every week.
2. Write the math as pure-stdlib Python — functions in, dict out, Spanish docstrings.
3. Add a worked example with hand-verified numbers to `examples/`.
4. Link it to the matching online calculator in the table above.

Open an issue to discuss a new calculator before sending a PR. Spanish docstrings are
preferred (the target users are Latin American engineers), but English is welcome.

## License

[MIT](LICENSE) — use it freely; cite the source if you publish it.
