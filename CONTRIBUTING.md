# Contributing — the verification protocol

The README explains *what* to contribute. This file explains *how a change is
accepted*, because the value of this repository is that every number can be
audited. A pull request that changes a formula without updating its evidence
will be asked to reconcile it first.

## Non-negotiable constraints

1. **Standard library only.** `import math` and nothing else. No numpy, no
   pandas, no packaging metadata. The file must run on a bare Python 3.8+.
2. **Pure calculation.** Functions take numbers or plain lists/dicts and return
   a dict. No `print()` in library code, no file I/O, no clock, no randomness.
3. **Language-neutral errors.** Invalid input returns `{"error": "code"}` or
   `None`. Never embed Spanish, English or any UI sentence in the module — the
   website layer owns the wording.
4. **Fixed units.** kN/m³, kPa, %, mm, m, degrees, gw = 9.81. Document any
   exception in the module docstring and in `docs/`.
5. **Honest boundaries.** If a value is a screening threshold from the
   literature rather than a standard, say so in the code comments, in the
   online tool page and in the technical reference. If the model ignores pore
   pressure, layers or a correction, list it explicitly.

## Dual-implementation agreement

The online calculators are JavaScript; this repository is Python. They are
written independently on purpose, then compared:

- agreement target better than **0.1 %** for every module;
- `slope_core.py` must stay **bit-identical** to the site's JS core — same
  circle grid bounds, same 24 slices, same Fellenius / Bishop / Spencer
  equations and the same 1.3× Bishop physical gate;
- any change to a formula must be applied to both sides in the same release.

To verify locally, run each module directly and compare with
`examples/verification.md`. The site's JS cores ship `test-*.js` Node assert
suites; run those too when you touch the shared algorithm.

## Adding a module

- Put the hand-worked example in the `if __name__ == "__main__"` block with
  intermediate values written in comments.
- Add the derivation to `examples/verification.md`.
- Add a row to the calculator table in `README.md` linking the matching online
  tool.
- Add a section to `docs/index.html`: inputs, equations, worked example and a
  **Boundaries** paragraph. If you add FAQ entries, keep the visible `<dt>`/`<dd>`
  text and the FAQPage JSON-LD in sync — the schema is generated from the
  visible FAQ, not written by hand.

## Content languages

The online tools are in Spanish and the technical reference is in English.
These are two independently written documents for two different audiences, not
translations of each other. Do not translate a Spanish page into English line
by line, or vice versa. Use the scenarios, terminology and question order that
real users of that language actually search for, and keep the equations and the
documented limitations identical on both sides.

## Pull request checklist

- [ ] `python python/<file>.py` prints the documented worked example
- [ ] `examples/verification.md` updated
- [ ] JS counterpart reconciled (or the PR states why not applicable)
- [ ] `docs/index.html` updated, boundaries included
- [ ] Error codes are language-neutral
- [ ] No credentials, tokens or absolute local paths anywhere in the diff
