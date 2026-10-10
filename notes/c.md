# C Notes

A practical reference for the C concepts covered so far: basic syntax, control flow, functions, arrays and strings, memory, pointers, dynamic allocation, structures, input/output, the preprocessor, Linux processes, `fork()`, `waitpid()`, file descriptors, `/proc`, and compilation.

---

## 1. A basic C program

```c
#include <stdio.h>

int main(void)
{
    printf("Hello, world!\n");
    return 0;
}
```

- `#include <stdio.h>` makes declarations for standard input/output functions such as `printf()` available.
- `int main(void)` defines the program's entry point. `void` means `main` takes no arguments in this declaration.
- `{ ... }` encloses a block.
- `printf()` writes formatted text to standard output.
- `\n` is a newline character.
- `return 0;` reports successful program termination to the environment.

### Compile and run

```bash
gcc -Wall -Wextra -Wpedantic hello.c -o hello
./hello
```

`gcc` invokes the compiler driver; `hello.c` is the source file; `-o hello` names the output executable. The warning flags ask GCC to report many common issues. They do not enable every possible warning, but they are a useful baseline.

Compilation creates or updates the executable; `./hello` runs it.

---

## 2. Variables, declarations, and initialization

A variable is a named object that stores a value of a particular type.

```c
int score;       // declaration; the value is not initialized here
int age = 20;    // declaration and initialization
char grade = 'A';
float temperature = 21.5f;
```

Do not declare the same variable twice in the same scope like this:

```c
int score;
int score = 10;  // invalid redeclaration in the same scope
```

Instead, either initialize it in the declaration or assign a value later:

```c
int score;
score = 10;
```

A local automatic variable that is not initialized has an indeterminate value. Do not read that value before assigning a valid one.

### Scope

Scope describes where a name can be used in source code.

```c
int global_value = 5;   // file scope

int main(void)
{
    int local_value = 10; // block scope
    printf("%d\n", local_value);
    return 0;
}
```

- `global_value` has file scope because it is declared outside a function.
- `local_value` has block scope because it is declared inside `main`'s block.

### Storage duration

Storage duration describes how long an object exists.

- **Automatic:** commonly used for local variables; the object's lifetime is tied to execution of its block.
- **Static:** the object exists for the entire execution of the program.
- **Allocated:** dynamically allocated storage exists until it is released, for example with `free()`.

```c
int global_count = 0; // static storage duration

int main(void)
{
    int x = 3;          // automatic storage duration
    static int y = 7;   // static storage duration
    (void)x;
    (void)y;
    return 0;
}
```

### Scope, storage duration, and linkage are different

- **Scope:** where an identifier can be used in the source code.
- **Storage duration:** how long an object exists.
- **Linkage:** whether declarations in different scopes or translation units refer to the same entity.

`static` has different effects depending on where it is used. At file scope, it can give an identifier internal linkage; for a local variable, it gives the object static storage duration.

---

## 3. Data types

Common built-in types:

```c
char letter = 'A';
int count = 42;
float ratio = 3.14f;
double precise = 3.1415926535;
```

- `char`: occupies exactly one C byte. It can represent a character or a small integer.
- `int`: integer type.
- `float`: floating-point type.
- `double`: floating-point type with at least the precision of `float`.
- `void`: represents no value, such as the return type of a function that returns nothing.

The sizes and ranges of types such as `int`, `long`, `float`, and `double` depend on the implementation. A C byte is the size of a `char`; it is commonly 8 bits on modern systems, but the C language does not require that everywhere.

### Type modifiers and qualifiers

```c
short int small = 12;
long int large = 123456789L;
unsigned int total = 100;
const int limit = 10;
volatile int hardware_value = 0;
```

- `short` and `long` select integer types with implementation-defined size/range relationships.
- `signed` and `unsigned` affect the values an integer type can represent.
- `const` means an object cannot be modified through an access path that treats it as `const`. It does not mean every object originally assigned to a `const` pointer is globally immutable.
- `volatile` tells the compiler that accesses to the object are significant and its value may change in ways not visible in ordinary program flow. It is **not** a general thread-synchronization mechanism.

Example of a pointer to constant characters:

```c
const char *name = "Alice";
printf("%s\n", name);
```

Do not attempt to modify the characters through `name`.

---

## 4. Operators and control flow

### Arithmetic operators

```c
int a = 10;
int b = 3;

printf("sum = %d\n", a + b);       // 13
printf("difference = %d\n", a - b); // 7
printf("product = %d\n", a * b);    // 30
printf("quotient = %d\n", a / b);   // 3: integer division
printf("remainder = %d\n", a % b);  // 1
```

When both operands of `/` are integers, the fractional part is discarded. For example, `10 / 3` evaluates to `3`.

### Comparisons and branching

```c
if (a > b) {
    puts("a is greater");
} else if (a == b) {
    puts("they are equal");
} else {
    puts("a is smaller");
}
```

Common comparison operators are `==`, `!=`, `<`, `<=`, `>`, and `>=`. Remember that `=` assigns a value, while `==` compares values.

### `for` loop

```c
for (int i = 0; i < 5; i++) {
    printf("%d\n", i);
}
```

This prints `0` through `4`.

### `while` loop

```c
int count = 0;
while (count < 3) {
    printf("%d\n", count);
    count++;
}
```

The loop continues while its condition is true.

### `switch`

```c
int choice = 2;

switch (choice) {
    case 1:
        puts("one");
        break;
    case 2:
        puts("two");
        break;
    default:
        puts("something else");
        break;
}
```

`break` exits the `switch`. Without a `break`, execution can fall through into the next case.

---

## 5. Functions

A function packages reusable logic.

```c
int add(int a, int b)
{
    return a + b;
}

int main(void)
{
    int result = add(2, 3);
    printf("%d\n", result); // 5
    return 0;
}
```

- `int` before `add` is its return type.
- `a` and `b` are parameters.
- `return` sends a result back to the caller.

### Function prototypes

A prototype declares a function's interface before its definition is encountered.

```c
int add(int a, int b);

int main(void)
{
    printf("%d\n", add(2, 3));
    return 0;
}

int add(int a, int b)
{
    return a + b;
}
```

### `void` functions and parameters

```c
void greet(void)
{
    puts("Hello");
}
```

- `void` as the return type means the function returns no value.
- `void` inside the parameter list means the function takes no arguments in traditional C declarations.

---

## 6. Arrays

An array stores a fixed number of elements of the same type in contiguous memory.

```c
int nums[5] = {10, 20, 30, 40, 50};

printf("%d\n", nums[0]); // 10
printf("%d\n", nums[2]); // 30
```

Array indexes start at `0`. For a five-element array, the valid indexes are `0` through `4`.

C does not automatically check array bounds. Reading or writing out of bounds causes undefined behavior.

### Arrays and pointers

In many expressions, an array name is converted to a pointer to its first element.

```c
int nums[3] = {10, 20, 30};
int *p = nums;       // equivalent here to: int *p = &nums[0];

printf("%d\n", nums[1]);   // 20
printf("%d\n", *(p + 1));  // 20
```

Pointer arithmetic advances by elements of the pointed-to type. If `p` is an `int *`, `p + 1` points to the next `int`, not necessarily the next byte.

Array elements themselves are contiguous. Structures may contain padding between members to satisfy alignment requirements.

---

## 7. C strings

C does not have a dedicated built-in string object type. A C string is a sequence of `char` elements terminated by the null character `\0`.

```c
char name[] = "Alice";
printf("%s\n", name);
```

The array contains six characters/bytes on typical systems: `A`, `l`, `i`, `c`, `e`, and the terminating `\0`. More generally, the array has `sizeof("Alice")` bytes, including the terminator.

### Common string functions

Include:

```c
#include <string.h>
```

Example:

```c
char text[] = "hello";
printf("length = %zu\n", strlen(text)); // 5; excludes '\0'
```

Important functions include:

- `strlen(s)`: counts characters before the terminating `\0`.
- `strcpy(dest, src)`: copies a string including its terminator; `dest` must have enough space.
- `strcmp(a, b)`: compares two strings lexicographically.

Example of copying into a sufficiently large destination:

```c
char source[] = "world";
char destination[16];

strcpy(destination, source);
printf("%s\n", destination);
```

`strcpy()` does not know the destination capacity. If the destination is too small, the copy can write out of bounds. Always reason about the destination size.

---

## 8. Memory and addresses

A running process uses memory for code and data. A common conceptual diagram is:

```text
Higher addresses
┌─────────────────────┐
│ Stack (often)       │
├─────────────────────┤
│                     │
│ Address-space area  │
│                     │
├─────────────────────┤
│ Heap (often)        │
├─────────────────────┤
│ Static/global data  │
├─────────────────────┤
│ Code/text (often)   │
└─────────────────────┘
Lower addresses
```

This is only a teaching model. The actual layout depends on the operating system, architecture, executable format, compiler, runtime, and security features.

- **Code/text:** machine instructions for the program.
- **Static/global data:** objects with static storage duration.
- **Heap:** commonly used for dynamically allocated storage.
- **Stack:** commonly used for function-call information and many local variables.

The C language does not require every local variable to be physically placed on a stack; compilers can optimize how objects are represented.

### Address-of operator: `&`

```c
int score = 42;

printf("score = %d\n", score);
printf("address = %p\n", (void *)&score);
```

- `score` means the value stored in the object.
- `&score` obtains the address of the object.
- `%p` is the `printf` conversion specifier for a pointer; passing `(void *)&score` is the conventional portable form.

Addresses can differ between runs. Do not assume variables declared next to each other in source code will have adjacent addresses or appear in source order in memory.

---

## 9. Pointers

A pointer is an object that stores a pointer value, commonly the address of another object.

```c
int x = 10;
int *p = &x;

printf("x = %d\n", x);        // value of x
printf("&x = %p\n", (void *)&x); // address of x
printf("p = %p\n", (void *)p);   // address stored in p
printf("*p = %d\n", *p);      // value of the pointed-to object
```

Remember:

```text
x   → value of x
&x  → address of x
p   → pointer value (the address stored in p)
*p  → value of the object p points to
&p  → address of the pointer variable itself
```

### Dereferencing and modifying an object

```c
int x = 10;
int *p = &x;

*p = 25;
printf("%d\n", x); // 25
```

`*p = 25` writes through the pointer and changes `x`.

### Null pointers

A pointer can intentionally be initialized to `NULL`:

```c
int *p = NULL;

if (p != NULL) {
    printf("%d\n", *p);
}
```

Do not dereference a null pointer.

### Pointer safety rules

- Do not dereference an uninitialized pointer.
- Do not dereference a null, invalid, or dangling pointer.
- Do not access an object after its lifetime has ended.
- Do not perform pointer arithmetic outside the permitted bounds of an array object (apart from forming a one-past-the-end pointer, which must not be dereferenced).
- Check whether allocation functions returned `NULL` before using the result.

---

## 10. `sizeof`

`sizeof` gives the size of a type or object in bytes.

```c
int a = 10;

printf("sizeof(int) = %zu\n", sizeof(int));
printf("sizeof(a) = %zu\n", sizeof(a));
printf("sizeof(double) = %zu\n", sizeof(double));
```

Use `%zu` to print a `size_t`, the type returned by `sizeof`.

The sizes of types such as `int` can vary between platforms, so avoid assuming a size unless your program targets a specific platform.

For memory allocation, this pattern ties the allocation size to the pointed-to type:

```c
int *values = malloc(10 * sizeof *values);
```

This requests enough space for ten `int` objects, assuming allocation succeeds.

---

## 11. Dynamic memory

Dynamic allocation requests storage while the program is running. The standard allocation functions are declared in `<stdlib.h>`.

- `malloc(size)`: allocates a block of the requested size; its contents are uninitialized.
- `calloc(count, size)`: allocates space for an array and initializes all bits to zero.
- `realloc(ptr, size)`: resizes a previously allocated block, potentially moving it.
- `free(ptr)`: releases a previously allocated block.

### Example with `malloc()`

```c
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int *value = malloc(sizeof *value);
    if (value == NULL) {
        perror("malloc");
        return EXIT_FAILURE;
    }

    *value = 42;
    printf("%d\n", *value);

    free(value);
    value = NULL;
    return EXIT_SUCCESS;
}
```

Conceptual lifecycle:

```text
allocate → check result → initialize/use → free
```

A **memory leak** happens when allocated memory is no longer needed but is not released. A **use-after-free** happens when code accesses memory after it has been freed. Setting a pointer to `NULL` after `free()` only changes that pointer variable; it does not restore the freed allocation or fix other pointers that may refer to it.

---

## 12. Structures and `typedef`

A `struct` groups related members into one object.

```c
#include <stdio.h>

struct Student {
    char name[20];
    int age;
};

int main(void)
{
    struct Student student = {"Alice", 20};
    printf("%s, %d\n", student.name, student.age);
    return 0;
}
```

Access members with the dot operator: `student.name`, `student.age`.

A structure can contain padding between members for alignment, so its total size may be larger than the sum of member sizes.

### `typedef`

`typedef` creates an alias for a type.

```c
typedef struct Student Student;

Student student = {"Bob", 22};
```

The alias avoids writing `struct Student` every time. The `typedef` does not create a new, distinct type by itself; it gives an existing type another name.

---

## 13. Input and output

Standard I/O functions are declared in `<stdio.h>`.

### Standard output

```c
printf("Hello, %s!\n", "world");
printf("Value: %d\n", 42);
puts("A line of text");
```

- `printf()` supports formatted output.
- `puts()` writes a string followed by a newline.

### Standard input with `scanf()`

```c
int age;

if (scanf("%d", &age) != 1) {
    fprintf(stderr, "Expected an integer.\n");
    return EXIT_FAILURE;
}
```

`scanf()` needs the address of `age` so it can store the value there. Always check its return value; it reports how many input items were successfully assigned.

### Standard file descriptors

On Unix-like systems, the conventional standard descriptors are:

```text
0 → stdin   (standard input)
1 → stdout  (standard output)
2 → stderr  (standard error)
```

### File I/O

```c
#include <stdio.h>

int main(void)
{
    FILE *fp = fopen("data.txt", "w");
    if (fp == NULL) {
        perror("fopen");
        return 1;
    }

    if (fprintf(fp, "hello\n") < 0) {
        perror("fprintf");
        fclose(fp);
        return 1;
    }

    if (fclose(fp) == EOF) {
        perror("fclose");
        return 1;
    }

    return 0;
}
```

- `fopen()` opens a file and returns a `FILE *` stream.
- `fprintf()` writes formatted output to the stream.
- `fclose()` closes the stream and may report a write/close error.

---

## 14. Preprocessor and headers

The preprocessor handles directives before the compiler compiles the C code.

```c
#include <stdio.h>
#include <stdlib.h>

#define MAX_ITEMS 100
```

- `#include` brings declarations from a header into the translation unit.
- `#define` defines a macro.

### Macro example

```c
#define SQUARE(x) ((x) * (x))

int result = SQUARE(4); // 16
```

Parentheses help preserve intended grouping, but macros can still be tricky: `SQUARE(i++)` evaluates its argument more than once and is unsafe. Prefer a function when appropriate.

---

## 15. Processes on Linux

A **program** is executable code; a **process** is an instance of a program being executed.

A process has operating-system-managed information such as:

- PID (process ID)
- PPID (parent process ID)
- virtual memory mappings
- file descriptors
- environment and execution state

Useful Linux commands:

```bash
ps -ef
ps aux
ps -p <PID> -o pid,ppid,stat,cmd
```

Replace `<PID>` with a real process ID.

### `getpid()` and `getppid()`

These POSIX functions are declared in `<unistd.h>`.

```c
printf("PID = %d\n", (int)getpid());
printf("PPID = %d\n", (int)getppid());
```

- `getpid()` returns the current process ID.
- `getppid()` returns the current parent process ID.

The cast makes the value match the `%d` format specifier for this Linux-oriented example.

---

## 16. `fork()`

`fork()` is a POSIX function available on Unix-like systems. It creates a child process based on the calling process.

```c
#include <sys/types.h>
#include <unistd.h>

pid_t pid = fork();
```

After a successful call, both parent and child continue from the statement after `fork()`, but the return value differs:

- **Child:** `fork()` returns `0`.
- **Parent:** `fork()` returns the child's PID (a positive value).
- **Failure:** `fork()` returns `-1` in the parent and no child is created.

```text
Before fork:
    Process A
        |
      fork()
      /    \
Parent    Child
```

The parent and child have separate process identities and separate virtual address spaces. The child initially inherits the parent's process state; operating systems commonly use copy-on-write to avoid eagerly copying every memory page.

### Small `fork()` example

```c
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

int main(void)
{
    pid_t pid = fork();

    if (pid < 0) {
        perror("fork");
        return EXIT_FAILURE;
    }

    if (pid == 0) {
        printf("Child: PID=%d, PPID=%d\n",
               (int)getpid(), (int)getppid());
    } else {
        printf("Parent: PID=%d, child PID=%d\n",
               (int)getpid(), (int)pid);
    }

    return EXIT_SUCCESS;
}
```

### Parent/child execution order

`fork()` does not guarantee which process runs first. Output may appear as parent then child, or child then parent. The scheduler determines when each runnable process gets CPU time. If one process must wait for another, use synchronization such as `waitpid()` rather than relying on `sleep()` or expected output order.

---

## 17. Waiting for a child with `waitpid()`

`waitpid()` lets a parent wait for a particular child to change state; with options `0`, it waits for that child to terminate. It also allows the parent to collect the child's termination status.

Include:

```c
#include <sys/types.h>
#include <sys/wait.h>
```

Example:

```c
int status;
pid_t result = waitpid(child_pid, &status, 0);

if (result == -1) {
    perror("waitpid");
    return EXIT_FAILURE;
}

if (WIFEXITED(status)) {
    printf("Child exit code: %d\n", WEXITSTATUS(status));
} else {
    puts("Child did not exit normally.");
}
```

- `child_pid`: the child to wait for.
- `&status`: address where the wait status is stored.
- `0`: no special options; wait for termination.
- `WIFEXITED(status)`: true if the child terminated normally via `exit()` or a return from `main()`.
- `WEXITSTATUS(status)`: extracts the exit code; use it only if `WIFEXITED(status)` is true.

### Complete `fork()` + `waitpid()` example

This matches the process experiment covered so far.

```c
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int main(void)
{
    pid_t pid = fork();

    if (pid < 0) {
        perror("fork");
        return EXIT_FAILURE;
    }

    if (pid == 0) {
        printf("Child process\n");
        printf("PID  = %d\n", (int)getpid());
        printf("PPID = %d\n", (int)getppid());
        sleep(2);  // gives time to observe the child while it exists
        return 7;  // child's exit code for this experiment
    }

    int status;
    pid_t terminated_pid = waitpid(pid, &status, 0);

    if (terminated_pid == -1) {
        perror("waitpid");
        return EXIT_FAILURE;
    }

    if (WIFEXITED(status)) {
        printf("Child %d exited with code %d\n",
               (int)terminated_pid, WEXITSTATUS(status));
    } else {
        printf("Child %d did not exit normally\n", (int)terminated_pid);
    }

    printf("Parent PID = %d\n", (int)getpid());
    printf("Child PID  = %d\n", (int)pid);

    return EXIT_SUCCESS;
}
```

The parent waits while the child sleeps. Once the child exits, `waitpid()` returns and the parent can report the exit code (`7` in this example).

A `sleep()` call is useful for observation during this lab, but it is not a general synchronization mechanism. `waitpid()` is what guarantees the parent waits for the specified child to terminate.

---

## 18. File descriptors

A **file descriptor (FD)** is a small non-negative integer that a process uses to refer to an open resource managed by the operating system.

Conventional descriptors:

```text
0 → stdin
1 → stdout
2 → stderr
```

A process may have more descriptors for files, pipes, sockets, devices, and other resources.

For example, `printf()` writes to standard output, conventionally FD `1`.

A process's file descriptors are visible on Linux under:

```bash
ls -l /proc/<PID>/fd
```

Example output might contain:

```text
0 -> /dev/pts/1
1 -> /dev/pts/1
2 -> /dev/pts/1
3 -> socket:[66597]
```

Here FD `3` refers to a socket. The number is a descriptor in that process; `socket:[66597]` is Linux's representation of the underlying socket object.

Conceptual model:

```text
Process
   ↓
File descriptor
   ↓
Kernel-managed resource
```

---

## 19. Linux `/proc` process inspection

`/proc` is a Linux virtual filesystem exposing information about processes and kernel state. It is not an ordinary directory of static files.

For a process with PID `1234`, examples include:

```bash
ls /proc/1234
cat /proc/1234/status
ls -l /proc/1234/fd
cat /proc/1234/cmdline
cat /proc/1234/maps
```

Useful entries:

- `/proc/<PID>/status`: process state and identity information, including IDs and memory-related fields.
- `/proc/<PID>/fd/`: symbolic links representing the process's open file descriptors.
- `/proc/<PID>/cmdline`: command-line arguments used to start the process (represented with null separators).
- `/proc/<PID>/maps`: memory mappings for the process.

Access to some process information can be restricted by permissions or system settings.

This connects process creation in C to observation through Linux:

```text
C program
   ↓
fork()
   ↓
parent + child processes
   ↓
PIDs
   ↓
/proc/<PID>
```

---

## 20. Compilation with GCC

Basic compile-and-run workflow:

```bash
gcc program.c -o program
./program
```

Recommended warnings while learning:

```bash
gcc -Wall -Wextra -Wpedantic program.c -o program
```

Meaning:

- `gcc`: compiler driver.
- `-Wall`: enables many common warnings (not literally every warning).
- `-Wextra`: enables additional warnings.
- `-Wpedantic`: warns about certain non-standard extensions relative to the selected standard.
- `program.c`: input source file.
- `-o program`: names the output executable `program`.
- `./program`: runs the executable in the current directory.

Conceptually, building a program involves preprocessing, compiling, assembling, and linking. GCC coordinates these stages; some may be combined internally.

Warnings are worth understanding rather than automatically ignoring. They often help find mistakes before the program runs.

---

## 21. Quick reference

### Variables and memory

```text
object        → an instance of a type stored somewhere
&object       → address of an object
pointer        → stores a pointer value, commonly an address
*pointer       → accesses the pointed-to object
sizeof(object) → size in bytes
```

### Arrays and strings

```text
array[index]   → element at index (starts at 0)
C string       → char sequence ending with '\0'
strlen(s)      → string length excluding '\0'
```

### Dynamic memory

```text
malloc()  → allocate storage
calloc()  → allocate and zero-initialize bytes
realloc() → resize an allocation
free()    → release allocated storage
```

### Process functions

```text
fork()     → create a child process (POSIX)
getpid()   → current process ID
getppid()  → parent process ID
waitpid()  → wait for a child and collect its status
```

### File descriptors

```text
0 → stdin
1 → stdout
2 → stderr
3+ → other open resources (not guaranteed to start at 3 in every situation)
```

### Compile

```bash
gcc -Wall -Wextra -Wpedantic source.c -o program
./program
```
