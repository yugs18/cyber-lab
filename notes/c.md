# C Notes

## Variables

- A variable is a named storage location in memory.
- Declaration example: `int score;`
- Initialization example: `int score = 10;`
- Variables have a type, a name, and a value.
- Scope controls where a name can be used.
  - local: inside a function/block
  - global: available across the file/program
- Storage duration/lifetime controls how long the object exists.
  - automatic variables die when the block ends
  - static/global variables live for the program lifetime
  - dynamically allocated memory must be freed manually

`static` can affect storage duration and linkage depending on where it is used, but for now the main distinction is scope vs. lifetime.

## Data types

C has several built-in categories:

- `char`: occupies exactly one byte in C and can represent a character or small integer value
- `int`: integer type, usually 4 bytes on modern systems
- `float`: single-precision floating point
- `double`: double-precision floating point
- `void`: no value / used for functions returning nothing or generic pointers

A C byte is not guaranteed to be 8 bits, although modern systems almost always use 8-bit bytes.

Type modifiers:

- `short` and `long` change size/range
- `signed` and `unsigned` change whether negatives are allowed
- `const` prevents accidental modification
- `volatile` tells the compiler the value can change outside normal code flow

Examples:

```c
int count = 42;
unsigned int total = 100;
float pi = 3.14f;
double precise = 3.1415926535;
const char *name = "Alice";
```

## Memory

Memory is where data is stored while a program runs.

Typical layout:

- code/text: program instructions
- static/global data: initialized and uninitialized global variables
- heap: dynamically allocated memory (`malloc`, `calloc`, `realloc`)
- stack: function call frames, local variables, return addresses

Important ideas:

- variables live in memory at some address
- stack memory is automatically managed for function-local data
- heap memory must be manually managed
- memory leaks happen when heap memory is never freed

## Addresses

Every variable has an address in memory.

- The address-of operator is `&`
- Example: `&score` gives the memory location of `score`
- Addresses are usually printed with `%p` in `printf`

Example:

```c
int score = 42;
printf("score = %d\n", score);
printf("address = %p\n", (void *)&score);
```

The value of a pointer is an address. A pointer tells you where something is stored.

## Pointers

A pointer is a variable that stores the address of another variable.

Syntax:

```c
int x = 10;
int *p = &x;
```

Meaning:

- `p` stores the address of `x`
- `*p` accesses the value stored at that address

Examples:

```c
int x = 10;
int *p = &x;

printf("x = %d\n", x);
printf("*p = %d\n", *p);
printf("p = %p\n", (void *)p);
```

Pointer rules:

- a pointer may be intentionally initialized to `NULL`
- never dereference an uninitialized or invalid pointer
- avoid dangling pointers after freed memory
- compare with `NULL` before dereferencing a pointer when appropriate
- pointer arithmetic works on the underlying type size

Example:

```c
int nums[3] = {10, 20, 30};
int *p = nums;

printf("%d\n", *(p + 1)); // 20
```

## Sizeof

`sizeof` is an operator that returns the size, in bytes, of a type or variable.

Examples:

```c
int a;
printf("%zu\n", sizeof(int));
printf("%zu\n", sizeof(a));
printf("%zu\n", sizeof(double));
```

Why it matters:

- helps with portability
- used for dynamic memory sizing
- important when working with arrays and structures
- avoids assuming a machine-specific integer size

Common use:

```c
int *arr = malloc(sizeof(int) * 10);
```

## Memory safety

Memory safety means using memory correctly so programs do not crash, corrupt data, or leak memory.

Common issues:

- out-of-bounds access on arrays
- dereferencing uninitialized pointers
- dereferencing `NULL` pointers
- use-after-free and dangling pointers
- memory leaks from `malloc` without `free`

Good practices:

- initialize variables before use
- check pointer results from allocation functions
- keep array bounds in mind
- free heap memory when finished
- use `const` when values should not change
- prefer clear ownership of allocated memory

Example:

```c
int *p = malloc(sizeof(int));
if (p == NULL) {
    return 1;
}

*p = 42;
free(p);
p = NULL;
```

Memory safety is one of the most important parts of writing correct C code.

## Memory Experiment

A simple C program can display both a variable's value and its memory address.

```c
int a = 10;

printf("a = %d\n", a);
printf("&a = %p\n", (void *)&a);
```

`a` refers to the value stored in the variable.

`&a` means "the address of `a`."

A pointer can store that address:

```c
int *p = &a;
```

Then:

- `p` → the address stored in the pointer
- `*p` → the value at that address
- `&p` → the address of the pointer itself

Conceptually:

```text
p
│
│ contains address
▼
┌──────┐
│  10  │
└──────┘
a
```

### Security connection

Programs store data and instructions in memory. Memory-related programming errors can cause unintended behavior, including corruption of program data or control flow.
