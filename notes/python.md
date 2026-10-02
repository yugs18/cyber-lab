# Python Notes

## Variables

A variable is a name bound to a Python object.

Python is dynamically typed, so you do not need to declare a variable's type explicitly.

Example:

```python
name = "Alice"
count = 10
is_ready = True
```

Important ideas:

* variables refer to objects
* assigning a variable binds it to an object
* reassigning a variable changes what object the name refers to
* objects have types; variables themselves do not have a fixed type
* Python manages memory automatically for many common objects

Example:

```python
x = 10
x = "hello"
```

`x` first refers to an integer object and later refers to a string object.

---

## Data Types

Python has several built-in types.

### Numeric types

```python
x = 10
y = 3.14
```

* `int`: whole numbers
* `float`: floating-point numbers

### Boolean

```python
is_ready = True
```

* `bool`: `True` or `False`

### String

```python
name = "Alice"
```

* `str`: text

### Collection types

* `list`: ordered, mutable sequence
* `tuple`: ordered, immutable sequence
* `dict`: key-value mapping
* `set`: collection of unique values

### `None`

```python
result = None
```

`None` represents the absence of a value.

---

## Type Conversion

Python provides functions for converting between compatible types.

```python
x = int("10")
y = float("3.5")
z = str(42)
flag = bool(1)
```

Examples:

```python
int("25")
float("3.14")
str(100)
```

Invalid conversions can raise exceptions.

```python
try:
    value = int("hello")
except ValueError:
    print("Invalid integer")
```

---

## Mutable and Immutable Objects

Some Python objects can be changed after creation.

### Mutable

Examples:

```text
list
dict
set
```

Example:

```python
numbers = [1, 2, 3]
numbers.append(4)
```

### Immutable

Examples:

```text
int
float
str
tuple
bool
```

Example:

```python
name = "Alice"
```

Operations that appear to modify an immutable object actually create or reference another object.

Understanding mutability becomes important when reasoning about functions, references, and program state.

---

## Strings

A string is a sequence of characters.

Example:

```python
text = "Hello World"
```

### Indexing

```python
print(text[0])
print(text[-1])
```

### Slicing

```python
print(text[0:5])
print(text[6:])
```

### Concatenation

```python
first = "Hello"
second = "World"

print(first + " " + second)
```

### Common methods

```python
text.lower()
text.upper()
text.strip()
text.split()
text.replace("World", "Python")
```

Example:

```python
name = " Alice "

print(name.strip())
print(name.lower())
```

### Splitting

```python
data = "192.168.1.10/24"

address = data.split("/")[0]

print(address)
```

This is useful when parsing command output and network information.

---

## Lists

Lists are ordered and mutable collections.

```python
numbers = [10, 20, 30]
```

Access elements:

```python
print(numbers[0])
print(numbers[-1])
```

Modify:

```python
numbers.append(40)
numbers.remove(20)
```

Useful operations:

```python
len(numbers)
numbers.sort()
numbers.reverse()
```

Lists are commonly used for storing collections of values and command-line arguments.

---

## Dictionaries

Dictionaries store key-value pairs.

```python
student = {
    "name": "Alice",
    "age": 20
}
```

Access:

```python
print(student["name"])
```

Safer lookup:

```python
print(student.get("age"))
```

Useful methods:

```python
student.keys()
student.values()
student.items()
```

Dictionaries are especially useful when data has named fields.

---

## Tuples

Tuples are ordered and immutable.

```python
coordinates = (10, 20)
```

Access:

```python
print(coordinates[0])
```

Tuples are useful when a fixed collection of values should not be modified.

A common networking example is the address passed to a socket:

```python
(target, port)
```

For example:

```python
sock.connect(("127.0.0.1", 8000))
```

---

## Sets

Sets contain unique values.

```python
values = {1, 2, 3, 3}

print(values)
```

The duplicate `3` is stored only once.

A set does not provide a guaranteed ordering that programs should depend on.

Useful operations include:

```python
values.add(4)
values.remove(2)
```

Sets are useful when uniqueness and membership testing matter.

---

## Conditionals

Python uses indentation to define blocks.

```python
age = 18

if age >= 18:
    print("adult")
else:
    print("minor")
```

Multiple conditions:

```python
if age >= 18:
    print("adult")
elif age >= 13:
    print("teenager")
else:
    print("child")
```

---

## Loops

### `for`

Used to iterate over a sequence or iterable.

```python
for i in range(3):
    print(i)
```

Output:

```text
0
1
2
```

Example:

```python
ports = [22, 80, 443]

for port in ports:
    print(port)
```

### `while`

Runs while a condition remains true.

```python
count = 0

while count < 3:
    print(count)
    count += 1
```

### `break`

Stops a loop:

```python
for i in range(10):
    if i == 5:
        break
```

### `continue`

Skips the current iteration:

```python
for i in range(5):
    if i == 2:
        continue

    print(i)
```

---

## Functions

A function is a reusable block of code.

```python
def add(a, b):
    return a + b

result = add(3, 4)
print(result)
```

Functions can:

* accept arguments
* return values
* reduce repetition
* separate logic into manageable components

Example:

```python
def is_valid_port(port):
    return 1 <= port <= 65535
```

Then:

```python
if is_valid_port(8000):
    print("Valid port")
```

---

## Input and Output

`print()` displays output.

```python
print("Hello, world!")
```

`input()` reads text from the user.

```python
name = input("Enter your name: ")
print("Hello", name)
```

`input()` always returns a string.

If a numeric value is required:

```python
age = int(input("Enter your age: "))
```

Invalid input may raise `ValueError`.

---

## f-Strings

F-strings provide convenient string formatting.

```python
user = "Alex"
age = 21

print(f"Hello {user}, you are {age} years old.")
```

They are especially useful for status messages:

```python
print(f"[+] {host}:{port} is OPEN")
```

---

# Modules and Imports

Python code can import built-in modules or installed packages.

Examples:

```python
import sys
import socket
import errno
import subprocess
import getpass
```

An import gives a program access to functions, classes, constants, and other objects provided by the module.

---

# `sys`

The `sys` module provides access to Python interpreter and command-line information.

```python
import sys
```

Useful examples:

```python
sys.argv
sys.exit()
```

---

## Command-Line Arguments

Command-line arguments are available through:

```python
sys.argv
```

Example:

```bash
python3 portpeek.py localhost 22 80 443
```

Conceptually:

```text
sys.argv[0] -> portpeek.py
sys.argv[1] -> localhost
sys.argv[2] -> 22
sys.argv[3] -> 80
sys.argv[4] -> 443
```

All command-line arguments are strings.

Therefore:

```python
port = int(sys.argv[2])
```

converts a string such as `"8000"` into the integer `8000`.

---

## Validating Command-Line Arguments

A program should validate its arguments before using them.

Example:

```python
if len(sys.argv) < 3:
    print(f"Usage: python3 {sys.argv[0]} <host> <port1> <port2> ...")
    sys.exit(1)
```

This ensures that the user supplied:

```text
script name
target host
at least one port
```

---

# `sys.exit()`

`sys.exit()` terminates the program.

Example:

```python
sys.exit(1)
```

A return code of `0` commonly indicates success.

Non-zero values commonly indicate an error or abnormal termination.

---

# Error Handling

Programs should handle expected failures instead of crashing unexpectedly.

The main tools are:

```text
try
except
else
finally
```

### `try` and `except`

```python
try:
    value = int("hello")
except ValueError:
    print("That is not a valid integer.")
```

### `finally`

`finally` runs regardless of whether an exception occurred.

```python
try:
    file = open("missing.txt", "r")
except FileNotFoundError:
    print("The file does not exist.")
finally:
    print("Cleanup or final steps")
```

### `else`

`else` runs when the `try` block completes without an exception.

```python
try:
    value = int("10")
except ValueError:
    print("Invalid value")
else:
    print("Conversion succeeded")
```

### Good practice

* catch specific exceptions
* avoid broad `except Exception` unless there is a reason
* validate input before performing operations
* produce clear error messages
* clean up resources

---

# `errno`

The `errno` module provides symbolic names for operating-system error codes.

```python
import errno
```

Example:

```python
error_name = errno.errorcode.get(result, "UNKNOWN")
```

For socket operations, an error code may correspond to a name such as:

```text
ECONNREFUSED
ETIMEDOUT
```

Error interpretation must be done carefully.

For example:

```text
ECONNREFUSED
```

commonly indicates that a TCP connection was refused, often because no service is listening on the destination port.

A timeout does not automatically prove that a port is closed. A firewall or network condition may simply prevent the response from reaching the client.

---

# Subprocess

The `subprocess` module allows Python to execute external programs.

```python
import subprocess
```

Example:

```python
result = subprocess.run(
    ["ip", "-br", "addr"],
    capture_output=True,
    text=True,
)
```

Useful attributes include:

```python
result.stdout
result.stderr
result.returncode
```

### `capture_output=True`

Captures the command's standard output and standard error.

### `text=True`

Returns the captured output as normal Python strings rather than bytes.

### `returncode`

A successful command usually returns:

```text
0
```

A non-zero value generally indicates an error.

Example:

```python
if result.returncode != 0:
    print("Command failed")
```

Passing command arguments as a list is generally preferable to constructing a shell command string when shell features are not required.

---

# Parsing Command Output

Captured command output can be processed as normal text.

Example:

```python
output = """2: ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500
    inet 192.168.136.128/24 brd 192.168.136.255 scope global ens33
"""

fields = output.split()

print(fields)
```

Common parsing techniques:

```python
output.split()
```

separates whitespace-delimited fields.

```python
value.split("/")
```

can separate a value such as:

```text
192.168.136.128/24
```

into:

```text
192.168.136.128
24
```

A parser should avoid unnecessary assumptions about fixed field positions.

For example, searching for an identifier such as:

```python
fields.index("ens33")
```

can be preferable to assuming a value is always at a specific numeric index.

However, hardcoding an interface name such as `ens33` still makes the program machine-specific.

---

# Socket Programming

Python provides the `socket` module for network communication.

```python
import socket
```

A socket is an operating-system abstraction that a program uses to communicate through a network protocol.

Conceptually:

```text
Python program
      ↓
Python socket API
      ↓
Operating system
      ↓
TCP / UDP
      ↓
Network
```

---

# Creating a TCP Socket

```python
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

### `AF_INET`

Specifies the IPv4 address family.

```text
AF_INET  -> IPv4
AF_INET6 -> IPv6
```

### `SOCK_STREAM`

Specifies a stream socket.

For IPv4 networking, this normally means TCP.

Therefore:

```python
socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

means:

> Create an IPv4 TCP socket.

---

# Socket Address

A typical TCP destination consists of:

```text
IP address + port
```

Example:

```python
target = "127.0.0.1"
port = 8000
```

The pair can be passed to a socket as:

```python
(target, port)
```

Example:

```python
sock.connect((target, port))
```

---

# Connecting

A TCP client can attempt to establish a connection using:

```python
sock.connect((target, port))
```

The operating system handles the underlying TCP connection process.

The application does not manually construct the TCP three-way handshake.

Conceptually:

```text
Python
   ↓
socket()
   ↓
connect()
   ↓
Operating System
   ↓
TCP
   ↓
Target IP + Port
```

---

# `connect_ex()`

`connect_ex()` is useful when a program wants a numeric result from the connection attempt.

Example:

```python
result = sock.connect_ex((target, port))
```

A result of:

```python
result == 0
```

means the TCP connection was successfully established.

A non-zero result indicates that the connection attempt did not succeed normally.

The exact error should be interpreted using the returned error code.

---

# Socket Timeouts

Network operations can block while waiting for a response.

A timeout limits how long a socket operation waits.

```python
sock.settimeout(1)
```

This sets a timeout of approximately one second.

Timeouts are important because an unresponsive network target should not cause a program to wait indefinitely.

---

# Closing Sockets

Sockets consume operating-system resources and should be closed when no longer needed.

```python
sock.close()
```

For multiple connection attempts, each connection should get its own socket.

Example:

```python
for port in ports:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)

    result = sock.connect_ex((target, port))

    sock.close()
```

A context manager is usually cleaner:

```python
for port in ports:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
```

The socket is automatically closed when the `with` block ends.

---

# Port Validation

TCP and UDP ports use a 16-bit port-number space.

The commonly usable port range for applications is:

```text
1–65535
```

A simple validation check:

```python
if not 1 <= port <= 65535:
    print(f"Port '{port}' is out of range")
```

Command-line input arrives as a string, so conversion should happen before numeric validation:

```python
try:
    port = int(port_arg)
except ValueError:
    print(f"Port '{port_arg}' is not a number")
    continue
```

---

# PortPeek

`PortPeek` is a small Python TCP connectivity-testing utility.

Its purpose is to determine whether a TCP connection can be successfully established to a specified host and port.

Example:

```bash
python3 portpeek.py 127.0.0.1 8000
```

It can also accept multiple ports:

```bash
python3 portpeek.py 127.0.0.1 22 80 443 8000
```

Basic flow:

```text
Command-line arguments
        ↓
Validate input
        ↓
Create TCP socket
        ↓
Set timeout
        ↓
connect_ex()
        ↓
Operating system
        ↓
TCP connection attempt
        ↓
Interpret result
        ↓
Close socket
```

---

## PortPeek Socket Model

For each tested port:

```text
PortPeek
   ↓
create socket
   ↓
file descriptor inside the process
   ↓
socket resource
   ↓
TCP connection attempt
   ↓
target IP + port
```

The Python program uses the socket API while the operating system handles the actual TCP/IP networking.

---

## PortPeek and TCP

For an open local TCP service:

```text
Client                         Server

127.0.0.1:ephemeral            127.0.0.1:8000

       SYN -------------------->
       <---------------- SYN-ACK
       ACK -------------------->
```

If the connection is successfully established:

```python
result == 0
```

and PortPeek reports:

```text
[+] 127.0.0.1:8000 is OPEN
```

An open result means:

> A TCP connection to that host and port was successfully established.

It does not by itself mean that the service is vulnerable.

---

# Connection Errors

A connection attempt can fail for different reasons.

Examples include:

```text
ECONNREFUSED
ETIMEDOUT
```

A refusal and a timeout should not automatically be interpreted as the same thing.

### Connection refused

A TCP connection was actively refused.

A common reason is that no service is listening on the target port.

### Timeout

The expected response was not received within the configured timeout.

Possible causes can include:

* firewall filtering
* packet loss
* routing problems
* unavailable host
* slow response

Therefore:

> Failed connection ≠ automatically "port is closed."

The result is evidence about the connection attempt and must be interpreted in context.

---

# PortPeek Limitations

The current implementation:

* tests TCP only
* uses IPv4 with `AF_INET`
* checks connectivity rather than identifying the application protocol
* uses a fixed timeout
* does not identify service versions
* does not implement UDP scanning
* does not perform sophisticated scan-state analysis

These limitations are intentional because the project is being used to understand the foundations of network programming.

---

# Resource Management

Programs use operating-system resources such as:

```text
files
sockets
pipes
processes
```

Resources should be released when they are no longer needed.

For sockets:

```python
sock.close()
```

A context manager can make cleanup automatic:

```python
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    ...
```

Security-relevant principle:

> Programs should not unnecessarily keep resources open.

Poor resource management can lead to resource exhaustion and difficult-to-debug behavior.

---

# `getpass`

The `getpass` module can retrieve the current user name.

```python
import getpass

user_name = getpass.getuser()
```

Example:

```python
print(f"User: {user_name}")
```

This was used in the `sysprobe` project.

---

# `socket.gethostname()`

The `socket` module can retrieve the current system's hostname:

```python
host_name = socket.gethostname()
```

Example:

```python
print(host_name)
```

Hostname resolution should not automatically be assumed to produce the IP address of the active network interface.

For example, a hostname lookup may return a loopback address such as:

```text
127.0.1.1
```

even when a real network interface has an address such as:

```text
192.168.x.x
```

Therefore:

> Hostname resolution and active network-interface discovery are separate problems.

---

# System Information with Python

The `sysprobe` project used Python to collect system information.

A simplified flow:

```text
Python
   ↓
subprocess
   ↓
ip -br addr
   ↓
capture stdout
   ↓
parse output
   ↓
extract interface information
```

This demonstrates how Python can combine:

```text
system commands
+
text processing
+
error handling
+
program logic
```

to build useful utilities.

---

# Security-Relevant Python Concepts

Python is commonly useful for:

```text
automation
system analysis
networking
reconnaissance
log processing
data parsing
security tooling
```

Security-oriented scripts should pay particular attention to:

* input validation
* error handling
* timeouts
* resource cleanup
* command execution safety
* sensitive-data handling
* correct interpretation of results

A script should never assume that an observation proves more than it actually does.

For example:

```text
TCP connection refused
```

does not automatically prove:

```text
The machine is completely unreachable.
```

Likewise:

```text
TCP connection timed out
```

does not automatically prove:

```text
The port is closed.
```

---

# Safer External Command Execution

When using `subprocess`, passing arguments as a list is generally preferable when shell functionality is unnecessary.

Preferred:

```python
subprocess.run(
    ["ip", "-br", "addr"],
    capture_output=True,
    text=True,
)
```

Avoid unnecessarily constructing shell commands such as:

```python
subprocess.run(f"ip -br addr {user_input}", shell=True)
```

when a structured argument list can be used instead.

Untrusted input combined with shell execution can create command-injection risks.

---

# Python Networking Mental Model

A useful model to remember:

```text
Python program
      ↓
socket API
      ↓
process
      ↓
file descriptor
      ↓
socket
      ↓
TCP / UDP
      ↓
IP
      ↓
network interface
      ↓
network
```

The Python program interacts with the operating system through APIs.

The operating system provides the underlying networking mechanisms.

---

# Python and the Operating System

Python often sits at a higher abstraction level than C.

For example:

```text
Python
   ↓
socket.connect_ex()
   ↓
OS networking API
   ↓
kernel TCP/IP stack
```

The Python program does not need to manually implement TCP.

C can provide a lower-level view of many of these same operating-system concepts, which is one reason C is valuable for systems and security work.

---

# Quick Recap

* Python variables are names bound to objects
* Python is dynamically typed
* mutable and immutable objects behave differently
* lists, dictionaries, sets, and tuples are core data structures
* loops and conditionals use indentation
* functions organize reusable logic
* `sys.argv` provides command-line arguments
* `try` / `except` handles expected exceptions
* `subprocess` allows Python to execute external commands
* `stdout`, `stderr`, and `returncode` describe command execution results
* `socket` provides network communication
* `AF_INET` represents IPv4
* `SOCK_STREAM` normally represents TCP
* `connect_ex()` attempts a TCP connection and returns a status code
* `errno` can translate socket error codes into symbolic names
* timeouts prevent network operations from waiting indefinitely
* sockets should be closed after use
* context managers provide automatic resource cleanup
* `PortPeek` is a basic TCP connectivity-testing tool
* an open result means a TCP connection was successfully established
* a timeout does not automatically mean a port is closed
* hostname resolution is not the same as discovering the active network interface
* Python can combine OS commands, parsing, networking, and automation to build security tools

---

# Security Mindset

When writing security tooling, always ask:

```text
What exactly did my program observe?
What does that observation prove?
What does it NOT prove?
What could explain the result?
```

This prevents assumptions from turning into false conclusions.

A useful progression is:

```text
Observation
    ↓
Evidence
    ↓
Interpretation
    ↓
Hypothesis
    ↓
Further testing
```

This mindset is more important than any individual Python library or command.
