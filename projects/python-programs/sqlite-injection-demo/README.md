# SQLite SQL Injection Demo

A small, local-only Python project demonstrating the difference between unsafe SQL string concatenation and parameterized queries.

## Scope

The project uses an in-memory SQLite database populated only with fictional user records. It is a focused teaching lab for understanding query construction and regression testing, **not a general-purpose SQL injection scanner**. The unsafe function is intentionally vulnerable and must never be used in production.

## Project structure

```text
sqlite-injection-demo/
├── sqlite_injection_demo.py
├── test_sqlite_injection_demo.py
└── README.md
```

- `sqlite_injection_demo.py` creates the database and defines `unsafe_lookup()` and `safe_lookup()`.
- `test_sqlite_injection_demo.py` verifies expected returned records for ordinary values, unknown and empty input, an apostrophe in a valid username, and an injection-like string.

## Requirements

- Python 3.9 or newer (uses built-in `sqlite3` and `unittest` modules)
- No third-party packages

## Run the demo

```bash
python3 sqlite_injection_demo.py
```

The same injection-like input is sent to both implementations. The unsafe query returns all fictional users because the input changes query logic; the parameterized query treats the complete input as a username and returns no records.

## Run the regression tests

From this directory:

```bash
python3 -m unittest -v
```

The tests assert specific expected records, rather than merely checking that functions do not crash. They cover:

1. Normal searches for `alice`, `bob`, and `charlie`.
2. An unknown username.
3. Empty input.
4. A valid username containing an apostrophe (`o'brien`).
5. Injection-like input treated as data by the parameterized query.
6. The same input changing the unsafe query's results.

## Security lesson

Use parameterized queries for user-supplied values:

```python
query = "SELECT username, display_name FROM users WHERE username = ?"
rows = conn.execute(query, (username,)).fetchall()
```

Parameterization separates query structure from data values. It is the primary defense demonstrated by this project; input validation and generic error messages are not substitutes for it.
