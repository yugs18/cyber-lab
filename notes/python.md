# Python Notes

## Variables

- A variable is a name bound to a Python object.
- Python is dynamically typed, so you do not need to declare the type explicitly.
- Example:

```python
name = "Alice"
count = 10
is_ready = True
```

- Variables are references to Python objects.
- Reassigning a variable changes what it points to.

## Data types

Python has several common built-in types:

- `int`: whole numbers such as `5`, `-3`, `1000`
- `float`: decimal numbers such as `3.14`, `2.0`
- `str`: text such as `"hello"`
- `bool`: `True` or `False`
- `list`: ordered, changeable collection
- `tuple`: ordered, immutable collection
- `dict`: key-value pairs
- `set`: unordered unique values

Type conversion examples:

```python
x = int("10")
y = float("3.5")
z = str(42)
flag = bool(1)
```

## Strings

A string is a sequence of characters.

Common operations:

- indexing: `text[0]`
- slicing: `text[1:4]`
- concatenation: `"hi" + " there"`
- methods: `.lower()`, `.upper()`, `.strip()`, `.split()`

Example:

```python
name = "Alice"
print(name[0])
print(name[1:4])
print(name.lower())
print(name.split("l"))
```

## Lists and dictionaries

A list stores multiple values in order.

```python
numbers = [10, 20, 30]
print(numbers[0])
print(numbers[-1])

numbers.append(40)
print(numbers)
```

A dictionary stores values by key.

```python
student = {"name": "Alice", "age": 20}
print(student["name"])
print(student.get("age"))
```

Important ideas:

- lists are mutable
- tuples are immutable
- dictionaries map keys to values
- sets store unique items without order

## Conditionals and loops

Python uses indentation to define blocks.

```python
age = 18

if age >= 18:
    print("adult")
else:
    print("minor")
```

Loops:

```python
for i in range(3):
    print(i)

count = 0
while count < 3:
    print(count)
    count += 1
```

## Functions

A function is a reusable block of code.

```python
def add(a, b):
    return a + b

result = add(3, 4)
print(result)
```

Functions help organize code and reduce repetition.

## Input and output

`print()` displays output.

```python
print("Hello, world!")
```

`input()` reads text from the user.

```python
name = input("Enter your name: ")
print("Hello", name)
```

String formatting can be done with f-strings:

```python
user = "Alex"
print(f"Hello {user}!")
```

## Modules and imports

Python code can import built-in modules or external packages.

```python
import sys
import socket
import getpass
```

Imports give access to additional functions and classes.

## Running external commands

The `subprocess` module lets Python run system commands.

```python
import subprocess

result = subprocess.run(["ip", "-br", "addr"], capture_output=True, text=True)
print(result.returncode)
print(result.stdout)
```

Important points:

- `capture_output=True` stores output instead of printing it immediately
- `text=True` makes output a normal string
- `returncode` tells whether the command succeeded
- `stdout` and `stderr` hold output from the command

This is useful for automating system checks and reading information from tools already installed on the machine.

## Parsing command output

Once output is captured, it can be split and processed.

```python
output = "2: ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500\n"
fields = output.split()
print(fields)
```

Common techniques:

- `.split()` to separate whitespace
- indexing to select a value from a list
- `.split("/")[0]` to remove a network prefix like `/24`

## Security connection

Python is often used for automation, monitoring, and system investigation. These tasks can be useful, but they also raise security questions:

- avoid collecting or exposing sensitive data without permission
- check whether the script is running in an approved environment
- handle command failures safely
- never assume command output is always in the expected format

Good scripting habits include validating input, checking errors, and being careful about what information is revealed.

## Error handling

Programs should handle problems gracefully instead of crashing unexpectedly.

The `try` and `except` blocks are the main way to do this in Python.

```python
try:
    value = int("hello")
except ValueError:
    print("That is not a valid integer.")
```

Common ideas:

- `try` contains code that may fail
- `except` catches a specific error type
- `finally` contains code that normally runs whether an exception occurs or not
- broad exception handling should be avoided unless necessary

Example:

```python
try:
    file = open("missing.txt", "r")
except FileNotFoundError:
    print("The file does not exist.")
finally:
    print("This always runs.")
```

Why it matters:

- prevents crashes from bad input
- makes scripts more reliable
- helps debug problems more clearly

## Practical caution

Real-world scripts should be designed with proper permissions, edge-case handling, and awareness of the environment they run in.
