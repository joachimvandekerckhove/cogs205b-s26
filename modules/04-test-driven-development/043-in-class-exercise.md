---
title: "In-class exercise: advanced SDT test suite"
course: "COGS 205B"
module: "04 — Test-driven development"
---

# In-class exercise: advanced SDT test suite

- Goal: practice TDD workflow on an advanced `SignalDetection` object.
- Focus on writing tests that are correct, clear, and runnable.
- Use this session to draft a strong baseline for homework.

---

# Setup

- Use Python and `unittest`.
- Put tests in:
  - `tests/test_signal_detection.py`
- Run tests with:

```bash
python -m unittest tests/test_signal_detection.py
```

---

# Exercise scope

You are writing tests for an advanced `SignalDetection` object with:

- rates (`hit_rate`, `false_alarm_rate`)
- SDT metrics (`d_prime`, `criterion`)
- operators (`__add__`, `__sub__`, `__mul__`)
- plotting methods (`plot_sdt`, `plot_roc`)

---

# Part 1: core SDT math tests

Create tests for:

- `hit_rate()` in normal cases
- `false_alarm_rate()` in normal cases
- `d_prime()` against known values
- `criterion()` against known values

Use explicit expected values and tolerances where needed.

---

# Part 2: input validation and object safety

Create tests for:

- invalid constructor values (e.g., negative counts, wrong types)
- invalid operator arguments
- internal consistency after operations

Your tests should verify that failure modes are clean and informative.

---

# Part 3: operator behavior

Create tests for:

- `__add__` elementwise count combination
- `__sub__` elementwise subtraction
- `__mul__` scalar scaling
- non-mutation of original objects when new objects are returned

---

# Part 4: plotting behavior

Create tests for:

- `plot_sdt()` returns matplotlib objects and labels key elements
- `plot_roc(sdt_list)` handles a sequence of objects
- `plot_roc` includes `(0,0)` and `(1,1)`
- plotting can be tested without interactive display

---

# Quality checklist

- Use descriptive test names.
- Keep one behavior per test.
- Use direct, readable assertions.
- Include at least one edge case per feature group.

---

# Deliverable for class

Before the end of class, submit a draft test suite that includes:

- a runnable `tests/test_signal_detection.py`
- at least one passing test in each of the four parts
- at least one deliberate failure you fixed during class

---

# Debrief prompt

- Which tests gave you the highest confidence?
- Which behavior was hardest to test and why?
- What assumption about the SDT object did your tests expose?

---

[← Previous](042-unittest.md) · [Module 04](README.md) · [Course home](../../README.md)
