---
title: "Working with AI coding tools"
course: "COGS 205B"
module: "06 — AI-assisted coding"
---

# Verification is non-negotiable

AI-generated code stays a proposal until it survives:

- tests
- review
- comparison to domain knowledge
- version-control inspection

Moving faster with a model does not transfer accountability: you still own correctness and what gets merged.

---

# Worked example: Gemini and regression

Prompt:

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```text
generate a python function to compute a multiple linear regression solution
using linear algebra
```

</div>

I sent this prompt twice to Gemini in separate calls. Both answers looked professional and both needed careful review.

---

# Gemini run 1: normal equation

The first response used this core calculation:

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
X_T = X.T
XTX = X_T @ X
XTX_inv = np.linalg.inv(XTX)
XTy = X_T @ y
beta_hat = XTX_inv @ XTy
```

</div>

It also added an intercept by default and returned several extra values (intercept, coefficients, R-squared, full beta vector, predicted values)...

... more than the narrow wording of the prompt.

---

# Gemini run 2: better, but still fragile

The second response avoided explicitly computing the inverse:

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
XTX = X_design.T @ X_design
XTy = X_design.T @ y
beta_hat = np.linalg.solve(XTX, XTy)
```

</div>

That is better than `np.linalg.inv`, but it still solves the normal equations, so it can fail when `X.T @ X` is singular. Could have used more input checking.

---

# Two simplified Gemini-style functions

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
def gemini_regression_inv(X, y, add_intercept=True):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float).reshape(-1, 1)
    if add_intercept:
        X = np.hstack((np.ones((X.shape[0], 1)), X))
    beta_hat = np.linalg.inv(X.T @ X) @ X.T @ y
    return beta_hat.flatten()
def gemini_regression_solve(X, y, fit_intercept=True):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    if fit_intercept:
        X = np.hstack((np.ones((X.shape[0], 1)), X))
    return np.linalg.solve(X.T @ X, X.T @ y)
```

</div>

---

# Four tests

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
class TestGeminiRegression(unittest.TestCase):
    def setUp(self):
        self.x_no_intercept = np.array([[0], [1], [2], [3]], dtype=float)
        self.x_with_intercept = np.array([[1, 0], [1, 1], [1, 2], [1, 3]], dtype=float)
        self.y = np.array([1, 3, 5, 7], dtype=float)
    def test_inv_no_intercept(self):
        np.testing.assert_allclose(gemini_regression_inv(
            self.x_no_intercept, self.y), [1, 2])
    def test_inv_already_has_intercept(self):
        np.testing.assert_allclose(gemini_regression_inv(
            self.x_with_intercept, self.y), [1, 2])
    def test_solve_no_intercept(self):
        np.testing.assert_allclose(gemini_regression_solve(
            self.x_no_intercept, self.y), [1, 2])
    def test_solve_already_has_intercept(self):
        np.testing.assert_allclose(gemini_regression_solve(
            self.x_with_intercept, self.y), [1, 2])
```

</div>

---

# Test output

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```text
test_inv_already_has_intercept ... ERROR
test_inv_no_intercept ... ok
test_solve_already_has_intercept ... ERROR
test_solve_no_intercept ... ok

numpy.linalg.LinAlgError: Singular matrix

Ran 4 tests in 0.017s

FAILED (errors=2)
```

</div>

Gemini can write code just fine, but plausible code still carries assumptions that only review and tests can surface.

---

# The happy-path testing failure

I also asked Gemini to write tests for the regression functions.

Its generated suite did some useful things:

- compared against `scikit-learn`
- used `np.allclose`
- checked singular-matrix behavior

But it also made the problem easier for itself: the suite tested the functions on the model’s own assumptions instead of the behavior we actually wanted.

---

# What happy-path tests look like

Gemini wrote tests like this:

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
beta_a = linear_regression_A(
    self.X_no_intercept,
    self.y_no_intercept,
    fit_intercept=False,
)
self.assertTrue(np.allclose(beta_a, expected_beta_sk_no_intercept))
```

</div>

This is not useless, but it sidesteps the question that exposed the problem: what if the caller gives a design matrix that already has an intercept column?

---

# Rule: write the test first

- If the model writes both the code and the test suite, it will generally make itself look good
- You can keep control by writing tests first and forcing the model to satisfy your contract
- Test-driven development becomes more important with AI coding tools

---

# Context = working memory

For an LLM, **context** is everything currently available to the model:

- your prompt
- earlier messages
- attached files
- tool outputs
- error messages
- system and project instructions

The model's next output is conditioned on this context, and when that context is wrong, stale, or cluttered, the output suffers.

---

# Context

## Context engineering

**Context engineering** is often more useful than hunting for magic prompt phrases: give the model the right files, strip irrelevant (and wrong!) material, state constraints explicitly, keep durable project knowledge outside the chat, and restart when the conversation becomes polluted. The best prompt cannot compensate for bad context.

## Context rot

Large context windows are useful, but they are not an excuse to skip pruning. As context grows, models can miss earlier requirements, over-attend to recent failures, blend incompatible instructions, imitate obsolete code from earlier attempts, and forget project-level constraints. Keep the active context as small as the task allows.

---

# Worked example: in-context learning

Prompt A:

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```text
generate a python function to compute a multiple linear regression solution
using linear algebra
```

</div>

Prompt B:

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```text
why are type hints important when creating a python function?

generate a python function to compute a multiple linear regression solution
using linear algebra
```

</div>

Adding context, even obliquely, can steer the model. Prompt B will usually produces type hints even when the regression prompt alone does not mention them.

---

# In-context learning cuts both ways

Good context steers the model, and bad context steers it just as strongly: if the model spent many turns on a bad strategy, it may keep imitating that strategy. Usually the right move is to stop, summarize what was learned, clear the context, and restart with a cleaner prompt. (Possibly one that was generated by the model itself and then sanitized by you.)

---

# Few-shot prompting

Examples can be more effective than abstract instructions: they define the style and shape of the answer you want.

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```text
Java: public List<String> filterUserNames(List<User> users, int minAge, boolean activeOnly)
C++: std::vector<std::string> filter_user_names(const std::vector<User>& users, int min_age, bool active_only)
Rust: fn filter_user_names(users: &[User], min_age: u32, active_only: bool) -> Vec<String>
Haskell: filterUserNames :: [User] -> Int -> Bool -> [String]

Python: ?
```

</div>

---

# Other prompting strategies

## Encouraging thinking

For hard debugging or design tasks, asking the model to reason more carefully can improve performance on some problems. Trade-offs include slower responses, more tokens, and sometimes over-complicated answers; reserve that mode for genuinely hard problems, not every autocomplete.

## Right-size the task

Tasks that are **too large** tend to lose details, produce inconsistent code, and bury reviewers; tasks that are **too small** burn time on prompting and may never fit together. Aim for work units that are still meaningful but small enough to test and review cleanly.

---

# Persistent context has different jobs

There are three different things people often mix together:

| File type | Job |
|-----------|-----|
| Agent/project instructions | Tell the agent how to behave in this project |
| Memory/planning files | Tell the agent what the project is doing now |
| Skills | Teach the agent a reusable workflow |

Keeping these separate makes instructions easier to maintain.

---

# Agent files: behavior here

Agent files answer:

- What style should this project follow?
- What commands should be used?
- What tools are allowed?
- What should never be changed?
- What counts as done?

Examples:

- `AGENTS.md`
- `.cursor/rules/*.mdc`
- other project-level instruction files

---

# Worked example: `AGENTS.md`

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```markdown
# Agent instructions
## Code style (NON-NEGOTIABLE)
- Prefer small functions with clear names.
- Preserve existing public APIs unless asked to change them.

## Testing (NON-NEGOTIABLE)
- Use `unittest`, not `pytest`, in this project.
- Write or update tests before implementation.
- Never relax a test just to make generated code pass.

## Workflow
- Run `python -m unittest discover -s tests` before reporting success.
- Use small commits at working checkpoints.
```

</div>

---

# Memory files: state now

Memory files answer:

- What are we building?
- What has already been decided?
- What tasks remain?
- What failed earlier?
- What should the next session remember?

Common examples:

- `PRD.md`
- `PLANNING.md`
- `TASKS.md`
- `SCRATCHPAD.md`

---

# Skills files: reusable workflows

Skills are portable packages that teach an agent how to perform a kind of task. 

Typical locations include `.cursor/skills/<skill-name>/SKILL.md`, `.agents/skills/<skill-name>/SKILL.md`, `~/.cursor/skills/<skill-name>/SKILL.md`, and `~/.agents/skills/<skill-name>/SKILL.md`.

They are version-controlled, reusable, loaded when relevant, and can be updated as you go.  I have a whole library of them!

---

# Worked example: `SKILL.md`

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```markdown
---
name: python-formatting
description: Format new or edited Python like the course examples (PEP 8, typing, pathlib).
paths: "**/*.py"
---

# Python formatting
Use `from __future__ import annotations` in new modules. Type-hint public 
APIs; prefer `pathlib.Path` over `os.path`; use f-strings.
Follow PEP 8 (four-space indent, sensible wraps). No star imports; avoid 
mutable default arguments; keep functions short with descriptive names.
```

</div>

---

# Skill scope and loading

Skills can include:

- `SKILL.md`: instructions
- `scripts/`: helper scripts the agent can run
- `references/`: longer documentation
- `assets/`: templates or supporting files

The `paths` field scopes a skill to relevant files so unrelated instructions stay out of context.

---

# Side-by-side

| File | Use it for | Lifespan |
|------|------------|----------|
| `AGENTS.md` | Project constitution and constraints | Project-wide |
| `TASKS.md` | Current work plan and status | Changes often |
| `SCRATCHPAD.md` | Temporary notes and failed attempts | Clean regularly |
| `SKILL.md` | Reusable task procedure | Across projects |

Do not make every instruction global: put each instruction where it belongs.

---

# Manage context live

During agentic coding, manage context deliberately: inspect what the agent has loaded, compact when you are mid-task but context is bloated, clear when you are at a breakpoint, reload durable files after clearing, and commit working states before risky changes. The model has no separate sense of what matters; only the context you give it carries that signal.

## Commit-clear-reload

A useful rhythm: review the diff, update task notes or scratchpad, commit the working state, clear or compact the context, then reload instruction and memory files. That sequence gives both you and the model a clean checkpoint.

---

[← Previous](062-ai-coding-landscape.md) · [Module 06](README.md) · [Course home](../../README.md) · [Next →](064-failure-modes-and-guardrails.md)
