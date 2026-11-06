---
name: Report a numerical discrepancy
about: Python output disagrees with a hand calculation, a standard or the online tool
title: "[discrepancy] "
labels: bug
assignees: ''
---

**Module / file**
e.g. `python/slope_core.py`, or the online page URL.

**Exact inputs**
Include units and all optional arguments (kh, yellow/red, k, mode, step...).

| | Value |
|---|---|
| Expected | |
| Actual | |
| Online calculator | |
| Python version | |

**Where the expected value comes from**
Hand calculation, textbook, standard, another program, or a laboratory report.
If it is a hand calculation, please show the intermediate steps.

**Before submitting**
- [ ] Units checked (percent vs ratio, degrees vs radians, kN/m³ vs kg/m³)
- [ ] Ran `python python/<file>.py` and compared with `examples/verification.md`
- [ ] Checked the documented boundaries in `docs/` — the module may not model
      pore pressure, layers, pore-water pressure, transition curves, etc.

A discrepancy caused by a documented limitation is still worth reporting: it
usually means the docs need to be clearer.
