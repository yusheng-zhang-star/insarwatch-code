---
name: Propose a new calculator
about: Suggest a calculation a field engineer currently does in a spreadsheet
title: "[calculator] "
labels: enhancement
assignees: ''
---

**What calculation does a field engineer repeat by hand?**
Describe the real task, not the formula. For example: "distributing a level-loop
misclosure across legs of different length", not "implement least squares".

**Inputs and outputs**
- Inputs (with units):
- Outputs (with units):
- Typical range of values:

**Source of the formula**
Give a textbook, standard, paper or a worked example we can verify against.
If the value depends on a local standard, say which one and which parameter
must stay configurable.

**A worked example with numbers**
Paste at least one hand-checkable case, including intermediate values.

**Existing material**
- [ ] I checked that this calculation is not already in `python/` or on insarwatch.com
- [ ] There is a matching online tool page (or one is planned)
- [ ] I can write the stdlib-only Python version
- [ ] I can help reconcile it with the JavaScript version on the site

**Scope check**
The module must stay a pure calculation: dict in, dict out, language-neutral
error codes, no UI text, no third-party dependencies. Screening values that are
not norms must be labelled as such in the docs.
