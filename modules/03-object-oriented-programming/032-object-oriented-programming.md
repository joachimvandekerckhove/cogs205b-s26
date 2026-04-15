---
title: "Object-oriented programming"
course: "COGS 205B"
module: "03 — Object-oriented programming"
---

# Object-oriented programming

Object-oriented programming involves thinking of problems as interactions between entities.

A *class* is a set of *objects* (or _instances_) with similar features. A typical kind of class is a `User` or a `Product`, and objects might be `Ashley` or `BananaBunch`. Objects have _properties_ (variables that belong to it) and _methods_ (functions that belong to it), like `firstName`, `lastName`, or `numberOfBananas`.

Classes can exist in a hierarchy, where they inherit properties or methods from superclasses.

You can think of a class as your own custom type of variable, with data fields (properties) and dedicated functions (methods).

---

# Methods

| | Python |
|---|---|
| Constructors | `def __init__(self, input):` |
| Display | `def __repr__(self):` |
| Getters | `@property` / `def myProperty(self):` |
| Setters | `@myProperty.setter` / `def myProperty(self, value):` |
| Ordinary methods | `def someMethod(self, input):` |
| Static methods | `@staticmethod` / `def someMethod(input):` |

---

# Methods

| | Python |
|---|---|
| Public attributes | `self.myProperty` |
| Private properties | `self.__myPrivateProperty` |
| Constants | Class attribute |

---

# Class files and modules

Class methods and properties are _scoped to the class_; they can be _public_ (visible externally), _private_ (meant only for other methods in the class), or _protected_ (also meant for child class methods). They can be given a number of attributes.

---

# A Python class

```python
class LabResult:
    def __init__(self, cv):
        self.current_value = cv
        self.assign_status()
    def assign_status(self):
        if self.current_value < 10:
            self.status = "Too low"
        else:
            self.status = "Too high"
    @staticmethod
    def load_object(s):
        return LabResult(s)
```

---

# Package folders and modules

Python is very widely used and many people contribute code to it. Function name clashes are somewhat inevitable. This is where modules come in handy.

A module is just a folder.

You can import modules the regular way. In general, do not `from myModule import ...`; import the whole module and use `myModule.myFunction()`. That is less prone to errors.

---

# Use cases

**Classes** are most useful when you have multiple functions that operate on a similar kind of data or type of variable.

**Modules** are most useful when you have many functions that functionally belong together but are not necessarily associated with a particular kind of input.

---

# Input Validation

- Input validation is the process of checking if input data is valid before using it.
- It helps ensure that your program runs correctly and securely.
- Important if you end up with a large code base and no longer expect the user (that's you) to be looking at every part of the code every time they use it.
- Common types of input validation include range checking, type checking, format checking, and existence checking.

---

# Benefits of Input Validation

- Helps prevent unexpected behavior.
- Improves code readability and maintainability.
- Reduces security risks.
- Provides better user experience by giving informative error messages.

---

# Common Types of Input Validation

- Range checking: Ensures input falls within acceptable range of values.
- Type checking: Ensures input is of the expected type.
- Format checking: Ensures input conforms to a specific format (e.g., phone numbers or email addresses).
- Existence checking: Ensures input is not empty or null.

---

# Basic Input Validation Example

```python
class BankAccount:
    def __init__(self, owner, balance):
        if balance < 0:
            raise ValueError("Balance cannot be negative.")
        self.owner = owner
        self.balance = balance
    # ...
```

---

# Handling Invalid Inputs Gracefully

- Provide informative error messages to the user.
- Log error messages for developers to review.
- Raise exceptions with descriptive error messages.
- Ensure that the program does not continue with invalid input.

---

# Input Validation in the Context of OOP

- Input validation can be incorporated into methods and class constructors.
- It's a good practice to perform input validation as close to the source of input as possible.
- Encapsulation allows you to define rules for valid state and prevent invalid input from corrupting the state of the object.

---

# Corrupted State

A corrupted state is a situation where an object's data is in an inconsistent or invalid state, often caused by an error in the program or a violation of the object's invariants.

- An object is in a corrupted state when its internal data is inconsistent with the object's intended behavior
- A corrupted state can lead to bugs and errors in the program
- Preventing corrupted states is an important part of writing correct, reliable code

---

# Example: Workflow that leads to a Corrupted State

Consider this object, with a balance attribute and a deposit and withdraw method.

```python
class BankAccount:
    def __init__(self, balance):
        if balance < 0:
            raise ValueError("Balance must be positive.")
        self.balance = balance
    def deposit(self, amount):
        self.balance += amount
    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Overdrawing not allowed!")
        self.balance -= amount
```

---

# Example: Workflow that leads to a Corrupted State

Suppose we have the following workflow:

1. Create a new bank account with initial balance of 100 dollars
2. Make a deposit of -50 dollars
3. That's arguably not a deposit
4. This workflow violates the invariants of the bank account object and results in a corrupted state, where the balance is negative.

---

# Example: External Function Bypassing Logger Method

```python
class BankAccount:
    def __init__(self, balance):
        self.balance = balance
        self.history = []
    def deposit(self, amount):
        self.balance += amount
        self.history.append(('deposit', amount))
    def withdraw(self, amount):
        self.balance -= amount
        self.history.append(('withdraw', amount))
    def logger(self):
        for transaction in self.history:
            print(transaction)
```

---

# Example: External Function Bypassing Logger Method

Now suppose an _external_ function edits the balance attribute of the BankAccount object directly, bypassing the deposit and withdraw methods and the logger method:

```python
def yoink(account):
    account.balance -= 100
```

This bypasses the logger method and leads to a corrupted state where the transaction history no longer reflects the actual transactions made on the account.

---

# Private vs Public in OOP

Public methods and attributes are accessible from outside the class.

Private methods and attributes are only accessible within the class.

```python
class MyClass:
    def __init__(self):
        self.public_attr = 0
        self.__private_attr = 1
    def public_method(self):
        print("This is a public method")
        self.__private_method()
    def __private_method(self):
        print("This is a private method")
```

---

# Private vs Public Methods and Attributes

- By convention, two leading underscores indicate a "private" method or attribute
- Private methods and attributes are intended for internal use only, and should not be accessed from outside the class
- Public methods and attributes can be freely accessed from outside the class
- In Python, there are no _truly_ private methods or attributes

---

# Private Attributes in the BankAccount Class

```python
class BankAccount:
    def __init__(self, initial_balance):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be <0")
        self.__balance = initial_balance

    def get_balance(self):
        return self.__balance
```

---

# Private Attributes in the BankAccount Class

- The `__balance` attribute in `BankAccount` is now private
- It is accessed using the `get_balance()` method, which is public
- External code shouldn't modify the `__balance` attribute directly
- This ensures that the balance is always valid and prevents external code from corrupting the object's state

---

# Public Methods in the BankAccount Class

```python
class BankAccount:
    def __init__(self, initial_balance):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be <0")
        self.__balance = initial_balance

    def get_balance(self):
        return self.__balance
```

---

# Public Methods in the BankAccount Class

```python
class BankAccount:
    def deposit(self, amount):
        if amount < 0:
            raise ValueError("Deposit amount cannot be <0")
        self.__balance += amount

    def withdraw(self, amount):
        if amount < 0:
            raise ValueError("Withdrawal amount cannot be <0")
        if self.__balance < amount:
            raise ValueError("Insufficient funds")
        self.__balance -= amount
```

---

# Public Methods in the BankAccount Class

- The `deposit()` and `withdraw()` methods in `BankAccount` are public
- They allow external code to modify the object's state in a controlled manner
- They perform validation to ensure that the object remains in a valid state
- External code cannot access the `balance` attribute directly, so it cannot corrupt the object's state

---

# Operator Overloading in Object-Oriented Programming

Operator overloading is a technique in object-oriented programming that allows us to define the behavior of operators (+, -, *, /, etc.) for user-defined objects.

In Python, operator overloading is achieved by defining special methods (with double underscores) in a class that correspond to the operator being used.

For example, the addition operator (+) can be overloaded by defining the `__add__` method in a class.

---

# Operator Overloading in Object-Oriented Programming

Suppose we have a class called `Vector` that represents a mathematical vector in 2D space. We can overload the addition operator (+) to allow adding two vectors together.

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
```

---

# Using Overloaded Operators

Let's create two `Vector` objects and add them together using the overloaded addition operator (+):

```python
v1 = Vector(1, 2)
v2 = Vector(3, 4)
v3 = v1 + v2
print(v3.x, v3.y)
```

Output: `4 6`

Here, we create two `Vector` objects, `v1` and `v2`, and add them together using the overloaded addition operator `+`. The resulting `Vector` object, `v3`, has components `(4, 6)`.

---

# Operator Overloading in Object-Oriented Programming

We can also overload other operators, such as the multiplication operator (*), to perform scalar multiplication of a vector.

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
```

By overloading operators, we can make our code more intuitive and expressive, and allow our user-defined objects to behave more like built-in types.

---

# List of Overloaded Operators in Python

| Operator | Method Name | Description |
|---|---|---|
| `+` | `__add__` | Addition |
| `-` | `__sub__` | Subtraction |
| `*` | `__mul__` | Multiplication |
| `/` | `__truediv__` | Division |
| `//` | `__floordiv__` | Floor Division |
| `%` | `__mod__` | Modulo |

---

# List of Overloaded Operators in Python

| Operator | Method Name | Description |
|---|---|---|
| `**` | `__pow__` | Exponentiation |
| `<` | `__lt__` | Less Than |
| `<=` | `__le__` | Less Than or Equal To |
| `==` | `__eq__` | Equal To |
| `!=` | `__ne__` | Not Equal To |
| `>` | `__gt__` | Greater Than |
| `>=` | `__ge__` | Greater Than or Equal To |

---

# Example object for normal distribution functions

```python
import math

class NormalDistribution:
    def __init__(self, mu=0.0, sigma=1.0):
        if sigma <= 0:
            raise ValueError("sigma must be positive")
        self.mu = float(mu)
        self.sigma = float(sigma)

    def z(self, x):
        return (x - self.mu) / self.sigma
```

---

# A worked object for normal distribution functions

```python
    ...
    def pdf(self, x):
        z = self.z(x)
        return (
            math.exp(-0.5 * z * z)
            / (self.sigma * math.sqrt(2.0 * math.pi))
        )
  
    def cdf(self, x):
        z = self.z(x)
        return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))
```

---

# A worked object for normal distribution functions

```python
nd = NormalDistribution(mu=0.0, sigma=1.0)

print(nd.pdf(0.0))   # 0.3989422804014327
print(nd.cdf(0.0))   # 0.5
print(nd.cdf(1.96))  # about 0.975
```

This object keeps parameters and distribution functions together in one reusable interface.

---

[← Previous](031-code-organization.md) · [Module 03](README.md) · [Course home](../../README.md) · [Next →](../04-test-driven-development/README.md)
