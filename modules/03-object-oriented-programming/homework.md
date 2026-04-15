# Homework — Signal detection (`SignalDetection` class)

## Purpose

Implement a **signal detection theory (SDT)** class in Python, then extend it with operator overloading and plotting.

## Background (formulas)

Use **hits**, **misses**, **false alarms**, and **correct rejections** as counts from a yes/no detection experiment.

- **Hit rate** \(H = \frac{\text{hits}}{\text{hits} + \text{misses}}\) (avoid dividing by zero if both are zero; same for FA rate below.)
- **False alarm rate** \(FA = \frac{\text{false alarms}}{\text{false alarms} + \text{correct rejections}}\)
- Let \(Z\) be the **standard normal quantile** (inverse CDF), `scipy.stats.norm.ppf` in Python.
- **Sensitivity:** \(d' = Z(H) - Z(FA)\)
- **Criterion (C):** \(C = -\tfrac{1}{2}\bigl(Z(H) + Z(FA)\bigr)\)

Short SDT background if you need it: [sdt-advanced.pdf](https://www.cns.nyu.edu/~david/handouts/sdt-advanced.pdf).

## Requirements

### Core class

- [ ] Constructor `SignalDetection(hits, misses, false_alarms, correct_rejections)` storing the four counts.
- [ ] `hit_rate()` and `false_alarm_rate()` returning floats in \([0,1]\) when defined; document or handle edge cases where denominators are zero (tests use only well-behaved counts).
- [ ] `d_prime()` and `criterion()` matching the formulas above using `scipy.stats.norm.ppf`.

### Operators (instance methods)

- [ ] `__add__(self, other)` — new `SignalDetection` whose four counts are **elementwise sums** of two instances.
- [ ] `__sub__(self, other)` — new `SignalDetection` whose four counts are **elementwise differences** of two instances.
- [ ] `__mul__(self, factor)` — new `SignalDetection` whose four counts are **multiplied by a scalar** `factor`.

### Plotting

Use **matplotlib**.

- [ ] `plot_sdt(self)` — **SDT plot**: overlapping **signal** and **noise** normal distributions (same variance, sensible x-range), a vertical line for the **criterion**, and a visual indication of **\(d'\)** (e.g. horizontal arrow or segment between distribution means). Label axes and include a title or legend so the figure is interpretable.
- [ ] `plot_roc(sdt_list)` — **static** method taking a **sequence** of `SignalDetection` instances. Plot an **ROC-style** curve: **hit rate** on the **horizontal** axis, **false alarm rate** on the **vertical** axis, one point per object; include **(0,0)** and **(1,1)** on the curve by definition. Label axes.

## Reading

Course module: [Object-oriented programming](../repo/modules/03-object-oriented-programming/032-object-oriented-programming.md) · Poldrack — Software engineering (objects, APIs).

