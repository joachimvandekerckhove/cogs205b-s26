---
title: "Code smells and best practices for clean code"
course: "COGS 205B"
module: "05 — Code smells and refactoring"
---

# Introduction

Good coding practice is writing code that is not only effective, but also easy to read, adjust, and maintain.

It is more like *writing* than it is like problem-solving:

- requires psychological insight
- theory of mind
- thinking about the competence and working memory capacity of the reader

More often than not, good coding practice is what *not* to do.

With experience, you gain instincts that tell you when a piece of code is poorly written, hard to understand, or prone to generate bugs or runtime errors.

And then other people's code can start to *smell bad*.

---

# Code smells

## Definition

Code smells are *subjective indicators of potential problems in code* that can impact the *quality* and *maintainability* of software.

- Whether something is a code smell is an *informal judgment* about the quality of code, identifying issues such as code duplication, long method lengths, complexity, and lack of encapsulation.
- Code smells are not bugs or errors, but they make code more difficult to understand, maintain, and extend, and error-prone.
- Smelly code is not broken -- it works, but...
- Code smells can lead to bugs, make code more difficult to maintain, and increase the effort required to fix problems.

*Code smells are heuristics that indicate when to refactor.*

---

# Generic code smells

There are many code smells that are so common they've been given names.

The general idea is that a feeling of darkness and despair comes over you when you see some code and imagine having to do maintenance on it in the future:

- This is hard to read.
- This is hard to test.
- If I change this, things elsewhere break.
- I find myself changing this back and forth.

---

# 🏷️ Mysterious name

- Functions, modules, variables or classes that are named in a way that does not communicate what they do or how to use them.

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
doTheThing(a,aa,flag)
```

</div>

- Use meaningful and descriptive names.

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
marginalLikelihood(binomialData, prior, useCache)
```

</div>

- Use naming conventions and abbreviations that are widely recognized and understood.

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
margLik(binomData, prior, useCache)
```

</div>

---

# 📋 Duplicated code

- Identical or very similar code exists in more than one location.

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
np.mean(samples[0]['alpha'].flatten())
np.mean(samples[0]['gamma'].flatten())
np.mean(samples[0]['delta'].flatten())
```

</div>

- Extract duplicated code into a reusable function or class.

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
def chainMean(samples, parameter):
    chain = samples[0][parameter].flatten()
    return numpy.mean(chain)
```

</div>

---

# 📋 Duplicated code — calls and tests

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
chainMean(samples, 'alpha')
chainMean(samples, 'gamma')
chainMean(samples, 'delta')
```

</div>

- Now you can ensure that the extracted code is tested, so that it can be easily checked, maintained, and updated.

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
def testChainMean(unittest.TestCase):
    ...
```

</div>

---

# 🧩 Shotgun surgery

- Single changes often need to be applied to multiple classes or methods at the same time.

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
def integrand1(self, p):
    return self.pdf(p, self.n, self.k) * self.prior1(p)
def integrand2(self, p):
    return self.pdf(p, self.n, self.k) * self.prior2(p)
```

</div>

---

# 🧩 Shotgun surgery — consolidate

- Identify the commonality between the classes that need to be modified and extract it into a common class or function.

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
def integrand(self, prior, p):
    return self.pdf(p, self.n, self.k) * prior(p)
```

</div>

- Manage responsibilities
  - A class or method should generally have _one_ responsibility.
  - Don't split a single responsibility among classes or methods.

---

# 🔁 Variable mutations — avoid rebinding

- Frequently changing what a particular identifier refers to.

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
from math import comb

def binomial_pdf(obj, p):
    p = comb(obj.n, obj.k) * (p**obj.k) * ((1 - p)**(obj.n - obj.k))
    return p
```

</div>

---

# 🔁 Variable mutations — clearer names

- Avoid changing the reference of a variable, prefer creating new variables.
- Consider using constants or read-only variables where appropriate to reduce the likelihood of unexpected mutations.

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
from math import comb

def binomial_pdf(obj, p):
    n_win, n_lose = obj.get_k(), obj.get_n() - obj.get_k()
    p_win, p_lose = p, 1 - p
    out = comb(n_win + n_lose, n_win) * (p_win**n_win) * (p_lose**n_lose)
    return out
```

</div>


---

# ⚡ Uncontrolled side effects

- Methods modify variables beyond scope (like globals or complex variables passed by reference).
- Refactor the code to avoid modifying variables outside of the method scope.
- Always use functional programming techniques, such as passing data through function arguments and return values, to reduce the likelihood of uncontrolled side effects.

*Respect scope.*

---

# 🔗 Uncontrolled side effects | Python passes objects by reference

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
class myClass:
    def __init__(self, X):
        self.X = X

def getX(obj):
    X = obj.X
    obj.X = None
    return X

n = myClass(5)

(n.X, getX(n), n.X)
```

</div>

---
# 🔗 Uncontrolled side effects | Python passes objects by reference

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
class myClass:
    def __init__(self, X):
        self.X = X

def getX(obj):
    X = obj.X
    obj.X = None
    return X

n = myClass(5)

(n.X, getX(n), n.X)  # --> (5, 5, None)
```

</div>

---

# 🛡️ Uncontrolled side effects | Prefer predictable reads

APIs should **read** state without surprising the caller by clearing fields as a side effect. Compare:

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
class Wallet:
    def __init__(self, balance):
        self.balance = balance

def peek_balance(wallet: Wallet) -> int:
    return wallet.balance

w = Wallet(5)
(w.balance, peek_balance(w), w.balance)  # --> (5, 5, 5)
```

</div>

---

# 📦 Data clumps

- Multiple related variables that are often passed together, indicating a need for a class.
- Refactor the code to extract the related variables into a class.
- Easier to understand and maintain.

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
def show_fixation(width_px, height_px, distance_cm, gamma, bg_color):
    ...


def run_trial(subject_id, width_px, height_px, distance_cm, gamma, bg_color):
    show_fixation(width_px, height_px, distance_cm, gamma, bg_color)
    # Same display settings travel together on every call: a clump.
```

</div>

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
from dataclasses import dataclass


@dataclass
class DisplaySettings:
    width_px: int
    height_px: int
    distance_cm: float
    gamma: float
    bg_color: str


def show_fixation(settings: DisplaySettings) -> None:
    ...


def run_trial(subject_id: str, settings: DisplaySettings) -> None:
    show_fixation(settings)
```

</div>

---

# 🔮 Speculative generality | You Aren't Gonna Need It

- Writing code for functionality that may not be needed in the future adds unnecessary complexity and makes the code difficult to maintain.

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
def mean(xs, weights=None, ignore_nans=False, trim_fraction=0.0):
    return sum(xs) / len(xs)
```

</div>

---

# 🌀 High cyclomatic complexity

- Every possible path through a function adds complexity.
- Many independent branches means many paths to read, test, and change safely.
- It may be possible to simplify the logic, or this needs to be multiple functions.

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
def label_trial(rt_ms, correct, practice):
    if practice:
        if rt_ms < 150:
            if not correct:
                return "practice_fast_error"
            return "practice_fast_correct"
        if rt_ms > 3000:
            if not correct:
                return "practice_slow_error"
            return "practice_slow_correct"
        return "practice_ok"
    if rt_ms < 150:
        if not correct:
            ...
```

</div>

---

# 🎛️ Too many parameters — crowded signature

- Makes calling and testing a function complicated

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
def plot_experiment(
    iv_data,
    iv_names,
    dv_data,
    dv_names,
    covariates,
    covariate_names,
    experiment_name,
    aesthetic,
):
    ...  # do stuff ...
```

</div>

---

# 🎛️ Too many parameters — reshape responsibility

- May indicate that the purpose of the function is ill-conceived
- Refactor so responsibility is assigned in a more clean-cut way

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
class Experiment:
    ...  # Class to contain experiment data ...
```

</div>

---

# 📏 Long method

- A method that has grown too large
- Difficult to understand and maintain
- Refactor into smaller, more focused methods that each perform a single, specific task

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
run_simulation_study(n_repetitions):
    parameters           = sample_parameters(n_repetitions)
    simulated_data       = simulate_data(parameters)
    estimated_parameters = estimate_parameters(simulated_data)
    return compare_parameters(
        true_parameters      = parameters, 
        estimated_parameters = estimated_parameters
    )
```

---

# 📐 Excessively long or short identifiers

- Naming conventions used to provide disambiguation that should be implicit in the software architecture
- Can make code harder to read and understand

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
compute_marginal_likelihood_from_binomial_data_and_priors(
    binomialData, prior, useCache
)
```

</div>

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
ml(d1, pr, uc)
```

</div>

---

# 📐 Excessively long or short identifiers

- Use concise but descriptive names

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
marginalLikelihood(binomialData, prior, useCache)
```

</div>


---

# 📜 Excessively long line of code — dense expression

- Makes code difficult to read, understand, debug, refactor, or identify possibilities for software reuse

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
subtab = data.loc[subset].groupby(
    factors
    )[value].agg(
        [numpy.mean, numpy.std, len]
    )
```

</div>

---

# 📜 Excessively long line of code — stepped layout

- Break up long lines into smaller, more manageable chunks

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
statistics_list  = [numpy.mean, numpy.std, len]
subset           = data.loc[subset]
grouped_subset   = subset.groupby(factors)
grouped_value    = grouped_subset[value]
aggregated_value = grouped_value.agg(statistics_list)
```

</div>

---

# 💬 Code deodorant

- Excessive comments betray you have something to apologize for
- A comment on an attribute setter/getter is a good example
- Can make code harder to read and maintain because a change in code leads to a change in comment
- Write short methods with descriptive titles so they don't need much explanation
- Practice *contractual programming*: document the *interface* carefully

---

# 🏛️ Class-level smells

- **📚 Large class**: a class that contains many unrelated methods.
- **😴 Lazy class**: a class that does too little.
- **🎯 Feature envy**: a class that uses methods of another class excessively.
- **🔢 Excessive use of literals**: these should be coded as named constants, to improve readability and to avoid programming errors.

---

# Naming

- Use clear and descriptive names for variables, functions, classes, and other identifiers.
- The names should clearly indicate the purpose and behavior of the code.
- Example:
  - Instead of using a variable name like `x`, use `customerName`
  - Instead of using a function name like `process`, use `calculateDiscount`

---

# ✏️ Naming conventions — bad practice

- Bad naming practices can make code difficult to read and understand

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
# Bad naming practice
lst = [1, 2, 3]
dct = {"a": 1, "b": 2}
def fnc(a, b):
    return a + b

class Cls:
    def __init__(self):
        self.x = None
        self.y = None
    def mtd(self):
        pass
```

</div>

---

# ✏️ Naming conventions — good practice

- Good naming practices make code more self-documenting and easier to maintain

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
# Good naming practice
numbers_list = [1, 2, 3]
data_dict = {"height": 1, "weight": 2}
def addNumbers(firstNumber, secondNumber):
    return firstNumber + secondNumber

class DataProcessor:
    def __init__(self):
        self.current_data = None
        self.previous_data = None
    def process_data(self):
        pass
```

</div>

---

# 📌 Functions

- Keep functions small and focused.
- A function should do one thing and do it well.
- Avoid long functions with multiple responsibilities.
- Example:
  - Instead of having a long function that retrieves data from a database, processes it, and sends an email all in one, have three separate functions: one for retrieving data, one for processing data, and one for sending emails.

---

# 📌 Refactor functions — before

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
def calculate_and_save_results(numbers):
    result = 0
    for number in numbers:
        result += number
    with open("result.txt", "w") as f:
        f.write(str(result))
    return result
```

</div>

---

# 📌 Refactor functions — after

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
def calculate_sum(numbers):
    result = 0
    for number in numbers:
        result += number
    return result

def save_to_file(result, file_path):
    with open(file_path, "w") as f:
        f.write(str(result))

numbers = [1, 2, 3, 4]
result = calculate_sum(numbers)
save_to_file(result, "result.txt")
```

</div>

---

# 💭 Comments

- Use comments only when they provide additional information that is not already clear from the code.
- Avoid writing comments that simply repeat the code.
- Example:
  - Instead of writing a comment like "increment the value of x" before "x += 1"... don't write that
- If you find you need to explain your code a lot, you might want to simplify the code rather than apologizing for it

---

# 💭 Bad commenting practice

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
def calculate_sum(numbers):
    # Calculating the sum of numbers
    result = 0
    for number in numbers:
        result += number
    # Return result
    return result
```

</div>

---

# 💭 Best commenting practice

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
def calculate_sum(numbers):
    """
    Calculate the sum of a list of numbers.

    Arguments:
    numbers -- list of numbers to be summed

    Returns:
    result -- the sum of the numbers
    """
    result = 0
    for number in numbers:
        result += number
    return result
```

</div>

---

# 🧾 Formatting

- Use consistent formatting throughout the codebase.
- This makes the code easier to read and understand.
- Example:
  - Use a consistent indentation level throughout the code.
  - Use consistent capitalization for variables and functions.
  - Use consistent spacing and alignment.

---

# 🧾 Bad formatting practice — cramped layout

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
def calculate_sum(numbers):
    output_arg=0
    for i in range(len(numbers)): output_arg=output_arg+numbers[i]
    return output_arg
```

</div>

---

# 🧾 Bad formatting practice — consistent layout

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
def calculate_sum(numbers):
    output_arg = 0
    for i in range(len(numbers)):
        output_arg = output_arg + numbers[i]
    return output_arg
```

</div>

---

# 🚨 Error handling

- Handle errors/exceptions in a consistent and predictable way.
- Use exceptions to indicate *what* has gone wrong.
- In general, do not try to fix a user's input error.  Wrong input should give an informative error message to set the user straight.  *Code should never quietly give a result that might not be what the user wanted.*

---

# ✅ Error handling — good practice

Good Error Handling Practice

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
def centered_normpdf(x, sigma):
    if sigma == 0:
        raise ValueError("The standard deviation" +
            " must be non-zero.")
    return (1 / (math.sqrt(2 * math.pi) * sigma)) * \
        math.exp(-0.5 * (x / sigma) ** 2)

print(centered_normpdf(0, 0))
# ValueError: The standard deviation must be non-zero.
```

</div>

---

# ⚠️ Error handling — inferior practice

Inferior Error Handling Practice

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
def centered_normpdf(x, s):
    return (1 / (math.sqrt(2 * math.pi) * s)) * \
        math.exp(-0.5 * (x / s) ** 2)

print(centered_normpdf(0, 0))
# ZeroDivisionError: float division by zero
```

</div>


---

# ⚠️ Error handling — straight to jail

Overly Defensive Error Handling Practice

<div style="background-color:#f6f8fa;border-radius:8px;padding:12px;margin:12px 0">

```python
def centered_normpdf(x, s):
    s = max(0.0001, s)
    return (1 / (math.sqrt(2 * math.pi) * s)) * \
        math.exp(-0.5 * (x / s) ** 2)

print(centered_normpdf(0, 0))
# 3989.4228040143275
```

</div>

---

# 🔧 Refactoring

- Regularly review and refactor the code to improve its design and maintainability.
- Make small, incremental changes to the code rather than large, sweeping changes.
- Example:
  - Instead of rewriting an entire module, extract the reusable parts into a separate function or class.
  - Instead of adding new features to a class with many responsibilities, extract the new feature into a separate class.
- Constant unit testing
  - Write unit tests to ensure that the code behaves as expected and to catch regressions.
  - A good test suite gives you confidence to make changes to the code without fear of breaking existing functionality.

---

# 📖 Final good practices — continual learning

- Continual learning
  - Stay up-to-date with new technologies and industry best practices.
  - Continuously improve your skills and knowledge.
  - Example:
    - Read books and articles on software development.
    - Attend conferences, meetups, and other events.
    - Experiment with new technologies and programming languages.

---

[← Module 05](README.md) · [Course home](../../README.md) · [Next →](052-advanced-smells-and-refactorings.md)
