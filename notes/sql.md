# SQL Fundamentals — Cybersecurity Notes

## 1. What Is SQL?

**SQL (Structured Query Language)** is a language used to interact with relational databases.

Applications use SQL to retrieve, insert, update, and delete information stored in a database.

Examples of application data include:

- User accounts and profiles
- Products and prices
- Orders and invoices
- Authentication-related records
- Application settings

SQL is important in cybersecurity because web applications often process user input and use it when interacting with a database. Understanding how queries work helps explain SQL injection and insecure data access.

---

## 2. Understanding Relational Databases

A relational database organizes related information into tables.

Consider a table named `products`.

| id | name | category | price |
|---:|---|---|---:|
| 1 | Keyboard | electronics | 1500 |
| 2 | Mouse | electronics | 600 |
| 3 | Notebook | stationery | 100 |
| 4 | SQL Basics | books | 450 |

### Table

A **table** is a collection of related records.

In this example, `products` stores information about products.

### Row

A **row** represents one record in a table.

For example:

```text
2 | Mouse | electronics | 600
```

This row represents one product.

### Column

A **column** represents an attribute of the records.

The `products` table has these columns:

- `id`
- `name`
- `category`
- `price`

Each column has a defined data type, such as integer, text, or numeric data.

### Primary key

A **primary key** uniquely identifies each row in a table.

For example, `id` can serve as the primary key in the `products` table.

An identifier helps locate a record, but knowing an identifier does not automatically grant permission to access that record.

---

## 3. A Second Example: The Users Table

Consider a fictional table named `users`.

| id | username | role | active |
|---:|---|---|---|
| 1 | alice | user | TRUE |
| 2 | bob | user | TRUE |
| 3 | charlie | admin | TRUE |
| 4 | diana | user | FALSE |

Here:

- `id` identifies a user.
- `username` stores a username.
- `role` represents the user's role.
- `active` indicates whether the fictional account is active.

These values are examples for learning SQL, not real credentials or accounts.

---

## 4. The SELECT Statement

`SELECT` specifies which columns should appear in the query result.

### Example

```sql
SELECT name, price
FROM products;
```

This query requests the product names and prices.

Result:

| name | price |
|---|---:|
| Keyboard | 1500 |
| Mouse | 600 |
| Notebook | 100 |
| SQL Basics | 450 |

The database returns the selected columns for matching rows.

### Selecting every column

```sql
SELECT *
FROM products;
```

The `*` requests all columns from the specified table.

Although useful for learning, selecting only the necessary columns is often clearer in application code.

---

## 5. The FROM Clause

`FROM` specifies the table from which records are retrieved.

Example:

```sql
SELECT username
FROM users;
```

Read this as:

> Retrieve the username column from the users table.

A basic SQL query can therefore be understood as:

```text
SELECT → Which columns?
FROM   → Which table?
```

---

## 6. The WHERE Clause

`WHERE` filters rows according to a condition.

Example:

```sql
SELECT name, price
FROM products
WHERE category = 'books';
```

Result:

| name | price |
|---|---:|
| SQL Basics | 450 |

Only the row whose category matches `books` is returned.

### Filtering by username

```sql
SELECT username, role
FROM users
WHERE username = 'alice';
```

This retrieves the matching user's username and role.

### Filtering by a number

```sql
SELECT name, price
FROM products
WHERE price < 1000;
```

This retrieves products costing less than 1000.

### Important distinction

- `SELECT` determines which columns appear.
- `FROM` identifies the source table.
- `WHERE` determines which rows satisfy the condition.

---

## 7. String Literals and Data Types

A **string literal** is a text value written directly into a SQL statement.

For example:

```sql
WHERE username = 'alice'
```

Here, `'alice'` is a string literal.

A numeric comparison looks different:

```sql
WHERE price = 450
```

Here, `450` is a numeric literal.

Common comparison operators include:

| Operator | Meaning |
|---|---|
| `=` | Equal to |
| `<>` | Not equal to |
| `>` | Greater than |
| `<` | Less than |
| `>=` | Greater than or equal to |
| `<=` | Less than or equal to |

Example:

```sql
SELECT username
FROM users
WHERE role <> 'admin';
```

This retrieves users whose role is not equal to `admin`.

String comparison behavior, including case sensitivity, can vary by database and collation.

---

## 8. Boolean Conditions

A Boolean condition evaluates to true or false. SQL uses conditions to determine which rows satisfy a `WHERE` clause.

Three important logical operators are `AND`, `OR`, and `NOT`.

### AND

`AND` requires both conditions to be true.

```sql
SELECT name, price
FROM products
WHERE category = 'electronics'
  AND price < 1000;
```

Result:

| name | price |
|---|---:|
| Mouse | 600 |

The product must belong to the electronics category and cost less than 1000.

### OR

`OR` requires at least one condition to be true.

```sql
SELECT username, role
FROM users
WHERE role = 'admin'
   OR username = 'alice';
```

This returns Charlie, because his role is `admin`, and Alice, because her username matches.

### NOT

`NOT` negates a condition.

```sql
SELECT username
FROM users
WHERE NOT active;
```

In a database that supports the Boolean column shown in the example, this returns users whose `active` value is false.

### Combining conditions

```sql
SELECT name, price
FROM products
WHERE category = 'electronics'
   OR (category = 'books' AND price < 500);
```

This selects electronics products, plus books costing less than 500.

Parentheses make the intended grouping explicit.

### Key distinction

```text
AND → Both conditions must be true.
OR  → At least one condition must be true.
NOT → Negates a condition.
```

SQL also has three-valued logic involving `NULL`, so not every condition evaluates simply to true or false. That is a topic to study later.

---

## 9. How an Application Uses SQL

Consider a fictional application that displays a user's profile.

The application might execute a query conceptually equivalent to:

```sql
SELECT id, username, role
FROM users
WHERE username = 'alice';
```

The query retrieves the matching record, and the application uses the result to construct an HTTP response.

A simplified flow is:

```text
User sends request
        |
        v
Application processes input
        |
        v
Application executes SQL query
        |
        v
Database evaluates conditions
        |
        v
Matching records are returned
        |
        v
Application processes results
        |
        v
HTTP response is generated
```

The application determines how input is handled and how returned records are used.

This is important because a security problem can arise either from constructing an unsafe query or from failing to enforce the correct access permissions.

---

## 10. SQL Injection: The Connection to Cybersecurity

**SQL injection (SQLi)** occurs when untrusted input is interpreted as part of SQL syntax instead of being handled strictly as data.

For example, an application might construct a query by concatenating a username into a string:

```python
query = (
    "SELECT id, username FROM users "
    "WHERE username = '" + username + "'"
)
```

This is unsafe because the application mixes SQL instructions with user-controlled input.

The fundamental problem is not merely that a user supplied unusual text. It is that the program constructed a database query in a way that may allow the input to change the query's meaning.

### Use parameterized queries

A safer approach is to separate the SQL statement from its values.

For example, Python's `sqlite3` module supports parameterized queries:

```python
cursor.execute(
    "SELECT id, username, role FROM users WHERE username = ?",
    (username,),
)
```

The `?` is SQLite's parameter placeholder. The username is passed separately as data rather than concatenated into the SQL statement.

Placeholder syntax varies between database drivers, but the principle remains the same: **use parameterized queries rather than inserting untrusted values into SQL text.**

---

## 11. SQL Injection Prevention vs. Authorization

These are separate security concerns.

### Query safety

Parameterized queries help ensure that user input is treated as a value rather than executable SQL syntax.

### Access control

Authorization determines whether the current user is allowed to access a particular resource or perform a particular action.

Even a safely parameterized query can retrieve another user's data if the application uses the wrong identity or fails to check permissions.

For example, an application should not assume that a user may access a private account merely because the request contains that account's identifier.

Remember:

```text
Parameterized query
        |
        v
Helps prevent SQL injection

Authorization check
        |
        v
Helps prevent unauthorized access
```

Secure applications need both.

---

## 12. Practical Query Reference

| Goal | SQL example |
|---|---|
| Retrieve all products | `SELECT * FROM products;` |
| Retrieve product names | `SELECT name FROM products;` |
| Retrieve names and prices | `SELECT name, price FROM products;` |
| Find books | `SELECT * FROM products WHERE category = 'books';` |
| Find inexpensive products | `SELECT * FROM products WHERE price < 500;` |
| Find active ordinary users | `SELECT username FROM users WHERE role = 'user' AND active = TRUE;` |
| Find administrators or Alice | `SELECT username FROM users WHERE role = 'admin' OR username = 'alice';` |
| Exclude administrators | `SELECT username FROM users WHERE role <> 'admin';` |

These examples use the fictional tables defined in this document. Exact syntax and supported types can differ between database systems.

---

## 13. Key Takeaways

1. A table stores related records, a row represents one record, and a column represents an attribute.
2. `SELECT` specifies the columns requested.
3. `FROM` specifies the table being queried.
4. `WHERE` filters rows using conditions.
5. String literals represent text values, commonly enclosed in single quotes.
6. `AND`, `OR`, and `NOT` combine or negate logical conditions.
7. SQL injection can occur when untrusted input is incorporated into SQL syntax unsafely.
8. Parameterized queries help keep input separate from SQL instructions.
9. Safe query construction does not replace authorization.
10. A record's identifier does not itself grant permission to access that record.

## 14. Review Questions

Answer these without looking at the notes:

1. What is the difference between a table, a row, and a column?
2. What does `SELECT name FROM products` retrieve?
3. What is the purpose of `WHERE`?
4. What is the difference between `AND` and `OR`?
5. What is a string literal?
6. Why can concatenating untrusted input into an SQL statement be unsafe?
7. How does a parameterized query help prevent SQL injection?
8. Why can a parameterized query still expose another user's data if authorization is missing?

**Final mental model:**

```text
Application input
       |
       v
Safe query construction
       |
       v
Database evaluates SQL
       |
       v
Records are returned
       |
       v
Application enforces access rules
       |
       v
Appropriate response
```

Understanding this flow will prepare you for later work on SQL injection, authentication, access control, and secure backend development.

---
