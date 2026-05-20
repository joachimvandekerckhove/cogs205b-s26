---
title: "Failure modes, guardrails, and best practices"
course: "COGS 205B"
module: "07 — Working with AI tools"
---

# Failure modes

AI coding tools are useful enough that we should use them.

They are unreliable enough that we need names for the common failure modes.

We will move from easy-to-catch failures to harder failures:

1. correctness failures
2. testing failures
3. feasibility failures
4. persistence failures
5. scope failures
6. security failures
7. instruction violations
8. communication failures

---

# Correctness failures

These are failures where the code is directly wrong.

Examples:

- syntax errors
- hallucinated APIs
- outdated APIs
- incorrect algorithm
- correct algorithm, wrong edge-case behavior

These are the easiest failures to catch when you have tests.

They are much harder to catch when you only read the code casually.

---

# Worked example: hallucinated API

This looks plausible:

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
from scipy.special import beta_log_quad

def evidence_slab(n, k):
    return beta_log_quad(k + 1, n - k + 1)
```

</div>

But `scipy.special.beta_log_quad` is not a real function.

This failure is easy to catch:

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```text
ImportError: cannot import name 'beta_log_quad' from 'scipy.special'
```

</div>

---

# Outdated APIs

LLMs often know older versions of libraries.

They may generate code that:

- works with a previous version
- raises a deprecation warning now
- will break in a future release

For Python test suites, one useful habit is:

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```bash
python -W error::FutureWarning -m unittest discover -s tests
```

</div>

Warnings are not always harmless.

---

# Testing failures

AI tools are often good at writing tests.

They are also good at writing tests that pass.

Those are not the same thing.

Common testing failures:

- happy-path tests
- mock implementations that test the mock, not the code
- weak assertions
- no checks for whether outputs changed
- exact equality for floating-point values
- coverage gaps

---

# Worked example: weak assertion

This test is almost a smoke test:

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
def test_evidence_slab_returns_float(self):
    bf = BayesFactor(n=10, k=7)
    self.assertIsInstance(bf.evidence_slab(), float)
```

</div>

A wrong formula can pass this.

It checks shape, not meaning.

---

# Stronger assertion

For the uniform slab prior, the marginal likelihood has a known value:

$$
P(k \mid n, H_{\mathrm{slab}})=\int_0^1 {n \choose k}\theta^k(1-\theta)^{n-k}d\theta
$$

For the uniform prior on $[0,1]$, this simplifies to:

$$
P(k \mid n, H_{\mathrm{slab}})=\frac{1}{n+1}
$$

---

# Stronger test

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
def test_evidence_slab_matches_closed_form(self):
    bf = BayesFactor(n=10, k=7)
    self.assertAlmostEqual(bf.evidence_slab(), 1 / 11, places=10)
```

</div>

This test can fail for the right reason.

That is what you want.

---

# Floating-point comparisons

Avoid exact equality for floating-point results:

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
self.assertEqual(bf.evidence_slab(), 1 / 11)  # brittle
```

</div>

Prefer tolerance:

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
self.assertAlmostEqual(bf.evidence_slab(), 1 / 11, places=10)
```

</div>

The tolerance should be tight enough to catch real mistakes.

---

# Feasibility failures

Sometimes the code is not the main problem, but the AI just proposes a wrong approach.

AI models can confidently say a plan is feasible when:

- the algorithm does not fit the hardware
- the complexity will not scale
- the necessary library capability does not exist
- the model has confused similar tools or environments

This is where domain expertise matters most.

---

# Worked example: GPU acceleration

Project: speed up a statistical workflow by making use of GPU processing.

The model repeatedly treated the task as feasible.

After quite some debugging, realized the problem was architectural:

- the relevant algorithm worked well on recent versions of CUDA
- lab had old GPUs with older drivers
- PyTorch operations could not reproduce the CUDA implementation efficiently

---

# When the model loops

If the model keeps trying variations of the same failing strategy, treat that as evidence.

Possible interpretations:

- the requirements are unclear
- the tests are too weak or misleading
- the approach is infeasible
- the model lacks the domain knowledge to choose a new strategy

Do not reward infinite persistence, be prepared to stop, review, and reframe the challenge.

---

# Persistence failures

Two opposite problems:

**Overpersistence**

- infinite iteration loops
- whack-a-mole fixes
- retrying cosmetic variations of the same idea

**Underpersistence**

- solving a simplified problem instead
- adding a workaround
- declaring success before the requirement is met

Both require a human to notice.

---

# Scope failures

AI coding tools often do more or less than asked.

Common forms:

- gold-plating
- scope creep
- premature abstraction
- large class hierarchies for small problems
- premature declaration of success

It's best not to waste time iterating on these issues. Instead, write skills files that set  clear acceptance criteria, and review the code.

---

# Worked example: scope creep

Prompt:

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```text
Add a method to compute the log Bayes factor.
```

</div>

Bad AI response:

- adds `log_bayes_factor`
- rewrites the constructor
- changes `evidence_slab`
- adds a plotting function
- replaces the test suite

The extra work is not harmless! You'd need additional tests, not an entirely new suite.

---

# Security failures

AI-generated code can introduce security problems.

Examples:

- hard-coded credentials
- shell injection
- unsafe deserialization with `pickle`
- installing typo-squatted packages
- connecting agents to sensitive data
- unsafe autonomous modes

Scientific code is not exempt from security.

---

# Credential exposure

Never do this:

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
API_KEY = "AIzaSy..."
```

</div>

Prefer:

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
API_KEY = os.environ["GEMINI_API_KEY"]
```

</div>

And never commit `.env` files or local key files.

---

# Unsafe dependencies

Agents may suggest installing packages. Make sure it hasn't been tricked!

- `maptplotlib`
- `requesuts`
- `numppy`

Before installing a new dependency, check that you know what it is, or check:

- name
- maintainer /  documentation
- whether the standard library or existing dependencies already solve the problem

---

# Instruction violations

Agents may ignore explicit instructions.

Examples:

- uses `pytest` when asked for `unittest`
- edits tests to pass implementation
- makes one huge commit
- rewrites files outside the requested scope
- changes public APIs without being asked

This often happens when context is bloated or contradictory.

Clear instructions help, but they are not a guarantee.

Keep your skills files tidy!

---

# Communication failures

Models can misreport the state of the work.

Common examples:

- "All tests pass" when tests were not run
- "The bug is fixed" when only the example case works
- confident diagnosis of the wrong cause
- no expression of uncertainty

Ask for evidence:

- command run
- output observed
- files changed
- tests added

---

# AI-specific code smells

AI-generated code often avoids obvious syntax problems.

The smells can be subtler:

- silent error swallowing
- overly complex class hierarchies
- leftovers from earlier attempts
- inappropriate pattern imitation
- inconsistent style across files
- docstrings that sound right but describe the wrong behavior
- suspiciously broad exception handling

---

# Worked example: silent error swallowing

Bad:

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
def safe_bayes_factor(bf):
    try:
        return bf.bayes_factor()
    except Exception:
        return 1.0
```

</div>

This turns an error into neutral evidence.

---

# Better error behavior

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
def checked_bayes_factor(bf):
    try:
        return bf.bayes_factor()
    except ZeroDivisionError as err:
        raise ValueError("Bayes factor denominator was zero") from err
```

</div>


---

# Three guardrails

An industry version of the same argument appears in CodeScene's discussion of AI coding guardrails.

The useful triad:

1. **Code quality**
2. **Code familiarity**
3. **Test coverage**

We do not need their tooling for this point.

The point is that faster code generation increases the need for reviewable, familiar, tested code.

---

# Guardrail 1: code quality

AI-generated code should meet the same quality bar as human-generated code.

Ask:

- Is it readable?
- Is it small enough to test?
- Does it use names that reveal intent?
- Does it follow the surrounding style?
- Does it avoid speculative generality?

Fast bad code is still bad code.

---

# Guardrail 2: code familiarity

If AI writes code you do not understand, you have created maintenance debt.

You should be able to explain:

- what each public method does
- why the algorithm is appropriate
- what assumptions it makes
- what its tests actually check
- what failure modes remain

Understanding code is often the bottleneck, not typing it.

---

# Guardrail 3: test coverage

Tests are the executable specification.

For AI-assisted coding, tests should include:

- ordinary expected cases
- edge cases
- invalid input cases
- regression tests for discovered bugs
- numerical tolerance choices

Coverage alone is not enough.

---

# Double bookkeeping

Tests and implementation should not be invented by the same unchecked process.

If a model writes the code and the tests, it may write tests that merely confirm its own assumptions.

Humans must own at least one side of the ledger:

- write tests first
- or review AI-generated tests very closely
- or compare against an independent implementation

---

# Version control guardrail

Before a risky agent task:

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```bash
git status
git switch -c ai-bayesfactor-logbf
git add .
git commit -m "Checkpoint before AI-assisted BayesFactor extension"
```

</div>

A branch is cheap. A tangled working tree is expensive.

Check `git status` before committing so secrets and unrelated files stay out.

---

# Commit-clear-reload

After a successful unit of work:

1. Review `git diff`.
2. Update `TASKS.md` or `SCRATCHPAD.md`.
3. Commit the working state.
4. Clear or compact the context.
5. Reload `AGENTS.md` and current task notes.

This protects both the codebase and the model's context.

---

# Twelve quick tips, grouped

Preparation:

1. Gather background knowledge before implementation.
2. Distinguish problem framing from coding.
3. Choose appropriate AI interaction models.
4. Think through and divide an implementation plan.

Context engineering:

5. Manage context strategically.
6. Meticulously verify AI assistance for testing.

---

# Twelve quick tips, continued

Testing and validation:

7. Use tests to specify and constrain AI-generated code.
8. Leverage AI to audit and expand test coverage.
9. Monitor progress and know when to restart.

Code quality:

10. Critically review generated code.
11. Refine code incrementally with focused objectives.
12. Document your code for reuse and publication.

---

# Scientific responsibility

When AI-generated code contributes to a scientific result, the scientist remains responsible.

"AI wrote it" is not a defense.

You must be able to:

- explain the method
- justify the implementation
- reproduce the environment
- document the workflow
- validate the output

The tool can assist but cannot be accountable.

Even for scientific _output_ the process is often more important than the product!

---

# Privacy and sensitive data

Do not submit sensitive material to cloud AI tools unless you have explicit approval.

Examples:

- patient information
- identifiable participant data
- embargoed results
- proprietary code
- private API keys

When in doubt, stop and ask.

---

# The working rule

Use AI as a fast collaborator whose work must be checked.

Not as:

- an authority
- an oracle
- a replacement for tests
- a replacement for domain knowledge
- a reason to skip review

The faster the draft appears, the more disciplined the review must be.

---

[← Previous](072-working-with-ai-tools.md) · [Module 07](README.md) · [Course home](../../README.md) · [Next →](074-in-class-exercise.md)
