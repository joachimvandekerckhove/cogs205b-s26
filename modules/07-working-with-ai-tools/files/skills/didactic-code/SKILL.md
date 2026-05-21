---
name: didactic-code
description: Enforce a readable, didactic coding style for non-expert programmers. Use when writing any code — scripts, functions, classes, or notebooks. Avoids overengineering, gold-plating, speculative generality, and macho coding. Keeps every line as simple as possible, uses human-readable bindings, and aligns code visually to aid comprehension.
disable-model-invocation: true
---

# Didactic Code Style

## Core principle

Code must always be written in a readable and accessible way. The goal of all code is to be didactic to non-expert programmers.

## Rules

**Simplicity above all**
- Keep every line of code and every script, function, and class as simple as possible to meet the requirements.
- Do not add complexity that isn't demanded by the current task.

**Avoid these failure modes**
- **Overengineering**: do not build abstractions or layers beyond what the task requires.
- **Gold-plating**: do not add features or polish that weren't asked for.
- **Speculative generality**: do not parameterize or generalize for hypothetical future needs.
- **Macho coding**: do not show off with terse, clever, or obscure constructs. Prefer obvious over impressive.

**Naming**
- Use human-readable bindings for everything: variables, functions, classes, arguments, loop counters.
- Names should read like plain English descriptions of what they hold or do.

**Visual formatting**
- Make use of whitespace to separate logical sections.
- Vertically align code at the assignment operator (`=`, `<-`, `=>`, `:`, etc.) so that semantically related lines visually chunk together.
- Vertically align consecutive numerical assignments at the decimal point (`.`) so that numbers are easy to compare.

## Alignment example

Prefer this:

```python
name        = "Alice"
age         = 30
occupation  = "researcher"
```

Over this:

```python
name = "Alice"
age = 30
occupation = "researcher"
```

Prefer this:

```python
age        =  30
height_cm  = 165
win_ratio  =   0.5
```

Over this:

```python
age        = 30
height_cm  = 165
win_ratio  = 0.5
```

## Quick checklist

Before finalizing any code, verify:

- [ ] A non-expert could read this without external explanation
- [ ] No class, function, or abstraction exists without a concrete, immediate need
- [ ] All names are self-documenting
- [ ] Related assignments are vertically aligned
- [ ] Whitespace separates distinct logical steps
