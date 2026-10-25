# SQLite SQL Injection Demo

A small, local-only Python project demonstrating SQL injection by comparing unsafe SQL query concatenation with parameterized queries using SQLite.

## Overview

This project uses an in-memory SQLite database populated with fictional user records to demonstrate how SQL injection can alter a query's intended behavior and how parameterized queries prevent user input from being interpreted as SQL syntax.

The project is designed for cybersecurity learning and experimentation. It does not connect to an external database or use real user data.

## Project Structure

```text
sqlite-injection-demo/
├── sqlite_injection_demo.py
├── test_sqlite_injection_demo.py
└── README.md
```

- **`sqlite_injection_demo.py`** — Creates the database and implements the unsafe and parameterized lookup functions, along with a demonstration runner.
- **`test_sqlite_injection_demo.py`** — Contains automated tests for normal input, SQL injection behavior, parameterized queries, and apostrophe handling.
- **`README.md`** — Documents the project and how to use it.

## Requirements

- Python 3
- SQLite support through Python's built-in `sqlite3` module
- Python's built-in `unittest` module

No third-party packages are required.

## How It Works

### 1. In-memory database

The application creates a temporary SQLite database using:

```python
sqlite3.connect(":memory:")
```

It creates a `users` table containing three fictional users:

| Username | Display name |
|---|---|
| `alice` | Alice Wonderland |
| `bob` | Bob Builder |
| `charlie` | Charlie Brown |

The database exists in memory for the lifetime of the connection.

### 2. Unsafe query concatenation

The `unsafe_lookup()` function inserts the supplied username directly into an SQL query string.

This allows specially crafted input to change the meaning of the query instead of being treated solely as a username.

**This function is intentionally vulnerable and must not be used in production applications.**

### 3. Parameterized query

The `safe_lookup()` function uses a parameter placeholder:

```python
query = "SELECT username, display_name FROM users WHERE username = ?"
```

It passes the username separately:

```python
conn.execute(query, (username,))
```

SQLite treats the supplied username as a data value rather than SQL instructions. This prevents the input from changing the query's structure.

## Running the Demonstration

From the project directory, execute:

```bash
python3 sqlite_injection_demo.py
```

The demonstration prints the fictional database records and compares the results from the unsafe and parameterized functions using the same input.

## Running the Tests

Execute the automated tests with:

```bash
python3 -m unittest -v
```

The test suite covers:

1. Normal username lookups in both implementations.
2. Input that changes the meaning of the unsafe query.
3. The same input being treated as data by the parameterized query.
4. Apostrophe handling in both implementations.

All tests should pass when the implementation and test setup are correct.

## Key Security Concepts

- **SQL injection:** Occurs when untrusted input changes the intended structure or meaning of an SQL query.
- **Query concatenation:** Combining user input directly with SQL text can introduce vulnerabilities.
- **Parameterized queries:** Separate query structure from input values.
- **Input as data:** Characters such as apostrophes and SQL keywords should not become executable SQL syntax merely because they appear in user input.
- **Automated testing:** Tests can demonstrate vulnerable behavior and verify that a safer implementation handles the same input correctly.

## Security Recommendation

Use parameterized queries for database operations involving user-supplied values. Avoid constructing SQL statements by directly concatenating untrusted input.

The unsafe implementation in this repository is provided strictly for educational comparison. Keep experiments isolated and use fictional data only.

## Learning Objective

The goal of this project is to understand the mechanism behind SQL injection, observe the difference between unsafe and parameterized SQL queries, and practice verifying security behavior with automated Python tests.

**Environment:** Python 3 · SQLite · `unittest`  
**Project type:** Local cybersecurity learning lab  
**Data:** Fictional records only

---
