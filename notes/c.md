# C Notes

## Variables

A variable is a named object used to store a value.

Example:

```c
int score;
int age = 20;
```

A variable has:

* a type
* a name
* a value
* storage in memory

A declaration tells the compiler about an identifier and its type.

An initialization gives an object its initial value.

Example:

```c
int score = 10;
```

Here:

```text
score → variable name
int   → type
10    → initial value
```

### Scope

Scope determines where an identifier can be used in source code.

Common scopes include:

* block scope: inside a block such as `{ ... }`
* function parameter scope
* file scope: declarations outside functions

Example:

```c
int global_value = 5;

int main(void)
{
    int local_value = 10;

    return 0;
}
```

`global_value` has file scope.

`local_value` has block scope.

### Storage duration / lifetime

Storage duration describes how long an object exists.

Common categories include:

* automatic: normally created when execution enters the block and ceases to exist when execution leaves it
* static: exists for the entire execution of the program
* allocated: dynamically created with functions such as `malloc()` and remains allocated until released

Important distinction:

```text
Scope
→ where an identifier can be used

Storage duration
→ how long the object exists

Linkage
→ whether declarations in different scopes or translation units
  refer to the same entity
```

`static` can affect storage duration and/or linkage depending on where it is used.

---

# Data Types

C provides several fundamental data types.

* `char`: exactly one byte; can represent a character or small integer value
* `int`: integer type
* `float`: single-precision floating-point type
* `double`: double-precision floating-point type
* `void`: represents the absence of a value

Example:

```c
int count = 42;
char letter = 'A';
float pi = 3.14f;
double precise = 3.1415926535;
```

The exact size and range of types such as `int`, `float`, and `double` are implementation-dependent.

---

## `char`

A `char` occupies exactly one byte in C.

A C byte is defined in terms of `char`; it is not required by the language to be exactly 8 bits.

Most modern systems use:

```text
1 byte = 8 bits
```

A `char` can be used as a character:

```c
char letter = 'A';
```

or as a small integer:

```c
char value = 65;
```

---

## Type Modifiers

Common modifiers include:

* `short`
* `long`
* `signed`
* `unsigned`
* `const`
* `volatile`

### `signed` and `unsigned`

```c
unsigned int count = 100;
```

An unsigned integer cannot represent negative values and can represent a larger positive range than the corresponding signed type of the same width.

### `short` and `long`

These modify integer types.

Examples:

```c
short int small;
long int large;
```

### `const`

`const` prevents modification through the associated object or access path.

Example:

```c
const int value = 10;
```

The program should not attempt to modify `value`.

With:

```c
const char *name = "Alice";
```

the characters pointed to by `name` should not be modified through that pointer.

### `volatile`

`volatile` tells the compiler that the value of an object may change in ways not represented by the normal flow of the program.

It is useful in certain low-level situations, such as memory-mapped hardware or externally modified objects.

`volatile` is **not** a general thread-synchronization mechanism.

---

# Memory

Memory is where program data and execution-related information are stored while a program runs.

A common conceptual process layout is:

```text
High addresses
┌─────────────────────┐
│       Stack         │
├─────────────────────┤
│         ↓           │
│                     │
│         ↑           │
├─────────────────────┤
│        Heap         │
├─────────────────────┤
│ Static / global data│
├─────────────────────┤
│    Code / text      │
└─────────────────────┘
Low addresses
```

The exact layout varies by operating system, architecture, executable format, compiler, runtime, and security features.

Common conceptual regions:

* code/text: program instructions
* static/global data: objects with static storage duration
* heap: dynamically allocated memory
* stack: function call frames and commonly automatic local variables

### Important ideas

* program objects occupy storage
* objects can have addresses
* automatic storage is managed by the language/runtime rules
* dynamically allocated memory must be explicitly released
* memory leaks happen when allocated memory is no longer needed but is never released

Do not assume that the conceptual layout above is a strict universal physical arrangement.

---

# Addresses

An address identifies the location of an object in the program's address space.

The address-of operator is:

```c
&
```

Example:

```c
int score = 42;

printf("score = %d\n", score);
printf("address = %p\n", (void *)&score);
```

`score` accesses the value.

`&score` produces the address of `score`.

`%p` is used to print a pointer value.

Casting to `(void *)` is the conventional form used with `%p`.

---

# Pointers

A pointer is an object that stores a pointer value, typically the address of another object or function.

Example:

```c
int x = 10;
int *p = &x;
```

Interpretation:

```text
x
┌─────────┐
│   10    │
└─────────┘
    ↑
    │
    p
```

`p` stores the address of `x`.

A useful beginner mental model:

> The value of a pointer is an address.

---

## Dereferencing

The unary `*` operator can be used to dereference a pointer.

Example:

```c
int x = 10;
int *p = &x;

printf("%d\n", *p);
```

`*p` means:

> Access the object located at the address stored in `p`.

Changing `*p` changes the pointed-to object:

```c
*p = 20;
```

Now:

```c
printf("%d\n", x);
```

prints:

```text
20
```

Conceptually:

```text
p
│
│ contains address
▼
┌─────────┐
│   20    │
└─────────┘
x
```

---

## Pointer Rules

Important pointer rules:

* a pointer may intentionally contain `NULL`
* never dereference an uninitialized pointer
* never dereference an invalid pointer
* never dereference a dangling pointer
* check for `NULL` when a pointer may legitimately be null
* understand the lifetime of the object being pointed to
* pointer arithmetic depends on the pointed-to type

Example:

```c
int nums[3] = {10, 20, 30};
int *p = nums;

printf("%d\n", *(p + 1));
```

Output:

```text
20
```

`p + 1` points to the next `int`, not merely the next byte.

---

# `NULL` Pointers

A pointer can intentionally contain no valid object address:

```c
int *p = NULL;
```

Testing:

```c
if (p != NULL)
{
    printf("%d\n", *p);
}
```

Dereferencing `NULL` is invalid.

```c
int *p = NULL;
printf("%d\n", *p);   // invalid
```

---

# Arrays

An array stores multiple elements of the same type in contiguous memory.

Example:

```c
int nums[3] = {10, 20, 30};
```

Conceptually:

```text
nums[0]   nums[1]   nums[2]
  10        20        30
```

The elements are stored contiguously.

Important:

* arrays have a fixed size when declared this way
* C does not automatically perform bounds checking
* reading or writing outside the valid range is undefined behavior

Example of valid access:

```c
printf("%d\n", nums[1]);
```

Invalid:

```c
printf("%d\n", nums[3]);
```

For a three-element array, valid indexes are:

```text
0
1
2
```

---

# Arrays and Pointers

In many expressions, an array name is converted to a pointer to its first element.

Example:

```c
int nums[3] = {10, 20, 30};

int *p = nums;
```

This is conceptually similar to:

```c
int *p = &nums[0];
```

Therefore:

```c
*(p + 1)
```

accesses the second element.

Array notation and pointer notation are closely related:

```c
nums[1]
```

and:

```c
*(nums + 1)
```

refer to the same element.

---

# `sizeof`

`sizeof` is an operator that returns the size, in bytes, of a type or object.

Example:

```c
int a = 10;

printf("%zu\n", sizeof(int));
printf("%zu\n", sizeof(a));
printf("%zu\n", sizeof(double));
```

Important properties:

* it helps avoid hard-coding platform-specific sizes
* it is useful for dynamic allocation
* it is useful with arrays and structures
* it helps write more portable code

Example:

```c
int *arr = malloc(sizeof(int) * 10);
```

This requests enough storage for ten `int` objects, assuming the allocation succeeds.

A more common pattern is:

```c
int *arr = malloc(sizeof *arr * 10);
```

because it avoids repeating the type.

---

# Dynamic Memory

Dynamic memory is obtained at runtime.

The standard allocation functions are provided by:

```c
#include <stdlib.h>
```

Common functions:

```text
malloc()
calloc()
realloc()
free()
```

Example:

```c
int *p = malloc(sizeof *p);

if (p == NULL)
{
    return 1;
}

*p = 42;

free(p);
p = NULL;
```

Conceptual lifecycle:

```text
allocate
   ↓
initialize
   ↓
use
   ↓
free
```

---

# Memory Safety

Memory safety means using memory within its valid lifetime and bounds.

Common memory bugs include:

* out-of-bounds access
* uninitialized pointer dereference
* `NULL` pointer dereference
* use-after-free
* dangling pointers
* double free
* memory leaks
* invalid pointer arithmetic

Good practices:

* initialize variables appropriately
* validate allocation results
* respect array bounds
* understand object lifetimes
* free allocated memory when finished
* avoid using pointers after the objects they refer to cease to exist
* use `const` when data should not be modified

Example:

```c
int *p = malloc(sizeof *p);

if (p == NULL)
{
    return 1;
}

*p = 42;

free(p);
p = NULL;
```

Setting the pointer to `NULL` after `free()` does not restore the freed memory; it simply prevents that pointer variable from continuing to hold the old address.

---

# Scope, Lifetime, and Linkage

These concepts are related but distinct.

## Scope

Determines where an identifier can be referenced in source code.

## Storage duration

Determines how long an object exists.

## Linkage

Determines whether identifiers in different declarations refer to the same entity.

For example:

```c
int global_count = 0;

int main(void)
{
    int local_count = 1;

    return 0;
}
```

`global_count` has file scope and static storage duration.

`local_count` has block scope and automatic storage duration.

---

# Functions

Functions provide reusable units of execution.

Example:

```c
int add(int a, int b)
{
    return a + b;
}
```

Calling:

```c
int result = add(2, 3);
```

Functions have:

* return type
* name
* parameters
* body

Example:

```c
int multiply(int a, int b)
{
    return a * b;
}
```

A function returning no value can use:

```c
void
```

Example:

```c
void greet(void)
{
    printf("Hello\n");
}
```

---

# Processes

A process is a running instance of a program.

A Linux process has information such as:

* PID
* PPID
* memory mappings
* file descriptors
* environment
* execution state
* user and group identity

A useful model:

```text
Program
   ↓
execution
   ↓
Process
   ↓
PID
```

---

# `fork()`

`fork()` is a POSIX function used on Unix-like systems to create a new process.

Include:

```c
#include <unistd.h>
```

Example:

```c
pid_t pid = fork();
```

After a successful `fork()`, there are two processes:

```text
             Parent
             PID 1000
                |
              fork()
             /      \
            /        \
     Parent 1000    Child 1001
```

The child is created from the calling process.

---

# `fork()` Return Value

`fork()` returns different values in the parent and child.

### In the child

```c
pid == 0
```

### In the parent

```c
pid > 0
```

The value returned to the parent is the child's PID.

### On failure

```c
pid < 0
```

Example:

```c
pid_t pid = fork();

if (pid < 0)
{
    perror("fork");
    return 1;
}
```

Then:

```c
if (pid == 0)
{
    // child
}
else
{
    // parent
}
```

The same source code therefore executes in two separate processes, but each process receives a different return value from `fork()`.

---

# `getpid()`

```c
getpid()
```

returns the process ID of the calling process.

Example:

```c
printf("PID = %d\n", getpid());
```

---

# `getppid()`

```c
getppid()
```

returns the process ID of the current process's parent.

Example:

```c
printf("PPID = %d\n", getppid());
```

Conceptually:

```text
PID
→ identity of the current process

PPID
→ identity of its parent process
```

---

# Parent and Child Execution Order

`fork()` does not guarantee which process executes first after the fork.

For example, this is possible:

```text
Parent
Child
```

But this is also possible:

```text
Child
Parent
```

After `fork()` both processes may be runnable, and the operating-system scheduler determines when each gets CPU time.

Therefore:

> The order in which parent and child print output is not guaranteed.

Example:

```c
if (pid == 0)
{
    printf("Child\n");
}
else
{
    printf("Parent\n");
}
```

Seeing:

```text
Parent
Child
```

does **not** mean the parent always runs first.

It only describes that particular execution.

---

# Process Observation with `/proc`

On Linux, process information can be inspected through:

```text
/proc/<PID>/
```

Examples:

```bash
ls -l /proc/<PID>
```

Useful entries include:

```text
/proc/<PID>/status
/proc/<PID>/fd/
/proc/<PID>/maps
/proc/<PID>/cmdline
```

This connects C process creation with Linux process inspection:

```text
C program
   ↓
fork()
   ↓
parent + child
   ↓
different PIDs
   ↓
/proc/<PID>
```

---

# File Descriptors

A file descriptor (FD) is a small integer used by a process to refer to an open operating-system resource.

The standard file descriptors are:

```text
0 → stdin
1 → stdout
2 → stderr
```

Example:

```text
0 → terminal input
1 → terminal output
2 → terminal error output
```

A process may have additional descriptors referring to:

* files
* pipes
* sockets
* devices
* other kernel-managed resources

For example:

```text
FD 3 → socket
```

On Linux, these can be inspected through:

```bash
ls -l /proc/<PID>/fd
```

Example:

```text
3 -> socket:[66597]
```

This gives an important systems-level model:

```text
Process
   ↓
File Descriptor
   ↓
Kernel Resource
```

For networking:

```text
Process
   ↓
FD
   ↓
Socket
   ↓
TCP / UDP
```

---

# C and the Operating System

C is particularly useful for systems programming because it provides relatively direct access to:

* memory
* pointers
* arrays
* processes
* file descriptors
* system calls
* binary data

This makes C valuable for understanding:

```text
Operating systems
Networking
Reverse engineering
Binary analysis
Systems security
Memory vulnerabilities
```

---

# Security Connection

C gives programmers significant control and responsibility.

Incorrect memory handling can lead to:

* crashes
* memory corruption
* unintended data modification
* invalid control flow
* security vulnerabilities

Important vulnerability classes include:

```text
buffer overflow
out-of-bounds access
use-after-free
double free
heap corruption
invalid pointer dereference
```

Understanding C memory, pointers, processes, and file descriptors is therefore foundational for systems security.

The important progression is:

```text
Memory
   ↓
Pointers
   ↓
Memory safety
   ↓
Processes
   ↓
File descriptors
   ↓
System calls
   ↓
Operating-system behavior
   ↓
Security
```

---

# Practical Memory Experiment

Example:

```c
#include <stdio.h>

int main(void)
{
    int a = 10;
    char b = 'A';
    int c = 20;

    printf("a = %d\n", a);
    printf("b = %c\n", b);
    printf("c = %d\n", c);

    printf("&a = %p\n", (void *)&a);
    printf("&b = %p\n", (void *)&b);
    printf("&c = %p\n", (void *)&c);

    printf("sizeof(a) = %zu\n", sizeof(a));
    printf("sizeof(b) = %zu\n", sizeof(b));
    printf("sizeof(c) = %zu\n", sizeof(c));

    return 0;
}
```

This demonstrates:

```text
variable → value
&a       → address
sizeof   → object size
```

The addresses of variables declared next to each other in source code should not be assumed to be adjacent or in source order.

---

# Practical Pointer Experiment

```c
#include <stdio.h>

int main(void)
{
    int a = 10;
    int *p = &a;

    printf("a  = %d\n", a);
    printf("&a = %p\n", (void *)&a);

    printf("p  = %p\n", (void *)p);
    printf("*p = %d\n", *p);

    return 0;
}
```

Conceptually:

```text
a
│
│ contains 10
▼
memory location

p
│
│ contains address of a
▼
&a
```

Therefore:

```text
a   → value of a
&a  → address of a
p   → address stored in p
*p  → value at that address
&p  → address of p itself
```

---

# Practical `fork()` Experiment

```c
#include <stdio.h>
#include <unistd.h>

int main(void)
{
    pid_t pid = fork();

    if (pid < 0)
    {
        perror("fork");
        return 1;
    }

    if (pid == 0)
    {
        printf("Child process\n");
        printf("PID = %d\n", getpid());
        printf("PPID = %d\n", getppid());
    }
    else
    {
        printf("Parent process\n");
        printf("PID = %d\n", getpid());
        printf("Child PID = %d\n", pid);
    }

    return 0;
}
```

Possible output:

```text
Parent process
PID = 23836
Child PID = 23837
Child process
PID = 23837
PPID = 23836
```

This does not imply that the parent always executes first.

Another execution may produce the child output first.

---

# Compilation

A basic C program can be compiled with GCC:

```bash
gcc program.c -o program
```

Run it with:

```bash
./program
```

Useful warning flags:

```bash
gcc -Wall -Wextra -Wpedantic program.c -o program
```

Warnings are valuable because they can reveal possible bugs before runtime.

During security-oriented development, compiler warnings should generally be treated seriously rather than ignored.

---

# Quick Recap

### Variables

```text
name
type
value
storage
```

### Memory

```text
code
static/global data
heap
stack
```

### Pointers

```text
pointer → stores an address
*pointer → accesses pointed-to object
&object → obtains address
```

### Arrays

```text
same-type elements
stored contiguously
no automatic bounds checking
```

### Dynamic memory

```text
malloc
   ↓
use
   ↓
free
```

### Processes

```text
program
   ↓
process
   ↓
PID
```

### `fork()`

```text
one process
   ↓
fork()
   ↓
parent + child
```

### Process identity

```text
getpid()  → current PID
getppid() → parent PID
```

### File descriptors

```text
0 → stdin
1 → stdout
2 → stderr
3+ → additional resources
```

### Linux process inspection

```text
/proc/<PID>/
```

### Core systems model

```text
Program
   ↓
Process
   ↓
PID
   ↓
File Descriptors
   ↓
Kernel Resources
   ↓
Memory / Files / Sockets / Pipes
```

---

# Security Mindset

When dealing with low-level C and operating-system behavior, keep asking:

```text
What object am I accessing?
Where does it live?
How long does it exist?
Who owns it?
What happens if I access it incorrectly?
What does the operating system do underneath?
```

That mindset will become increasingly important when moving into:

```text
memory corruption
debugging
reverse engineering
binary exploitation
system calls
privilege boundaries
process internals
```

This foundation is what turns C from a syntax exercise into a tool for understanding how software actually works.
