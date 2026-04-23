---
title: "Organizing Python files for unittest"
course: "COGS 205B"
module: "04 — Test-driven development"
---

# Organizing files for `unittest`

- `unittest` collects tests from `./tests/`.
- Each test file is a normal module: names resolve only via **`sys.path`**.
- **`ModuleNotFoundError`** → fix **layout** + **where you run** `unittest`.

---

# Flat layout

**Goal:** `tests/` imports a module sitting next to it at the **repo root**.

```text
myproject/
  counter.py          # implementation
  tests/
    test_counter.py   # tests
```

---

# Example test

`counter.py` defines `increment`. In `tests/test_counter.py`:

```python
import unittest
import counter

class TestCounter(unittest.TestCase):
    def test_increment(self):
        self.assertEqual(counter.increment(0), 1)
```

---

# `import counter`

- Run **`unittest` from `myproject/`** (the folder that contains **both** `counter.py` and `tests/`).
- With **`python -m unittest`**, the **current working directory** is on `sys.path`, so `counter` maps to `./counter.py`.

## Discover all tests

From `myproject/`:

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

## Single file:

```bash
python -m unittest tests.test_counter
```

---

[← Previous](043-in-class-exercise.md) · [Module 04](README.md) · [Course home](../../README.md)
