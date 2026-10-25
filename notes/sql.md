# SQL Fundamentals and SQL Injection

These notes cover the underlying concepts of SQL and SQL injection. **Individual PortSwigger lab reports are stored separately**; this file records theory, mental models, and learning-path progress rather than reproducing lab procedures.

## 1. What Is SQL?

SQL (Structured Query Language) is used to interact with relational databases. Applications commonly use SQL to retrieve, insert, update, and delete data.

Security relevance: applications frequently pass user-controlled values to database queries. If the application combines input with SQL incorrectly, that input may change the query's intended structure or logic.

Common SQL commands:

- `SELECT` — retrieve records.
- `FROM` — specify the table to query.
- `WHERE` — filter records.
- `INSERT` — add records.
- `UPDATE` — modify records.
- `DELETE` — remove records.

## 2. Tables, Rows, and Columns

Imagine a fictional `products` table:

| id | name | category | released |
|---:|---|---|---:|
| 1 | Mug | Gifts | 1 |
| 2 | Notebook | Gifts | 1 |
| 3 | Prototype | Gifts | 0 |
| 4 | Keyboard | Electronics | 1 |

In this example, `1` means released and `0` means unreleased.

- **Table:** a collection of related records.
- **Row:** one record, such as the Prototype product.
- **Column:** an attribute, such as `category`.
- **Query:** an instruction sent to the database.

A query such as:

```sql
SELECT * FROM products
WHERE category = 'Gifts'
AND released = 1;
```

retrieves products whose category is `Gifts` and whose `released` value is `1`.

The `AND` operator requires both conditions to be true.

## 3. Basic Filtering and Boolean Logic

### Comparison operators

Common comparison operators include:

| Operator | Meaning |
|---|---|
| `=` | equal to |
| `!=` or `<>` | not equal to |
| `>` | greater than |
| `<` | less than |
| `>=` | greater than or equal to |
| `<=` | less than or equal to |

### Boolean operators

- `AND` — the expression is true only when both conditions are true.
- `OR` — the expression is true when at least one condition is true.
- `NOT` — negates a condition.

For example, `1=1` is always true. Boolean expressions are important to SQL injection because changing an expression can broaden or otherwise alter which rows match a query.

Use parentheses when reasoning about complex Boolean expressions; they make grouping explicit. SQL's exact evaluation rules and dialect details can matter.

### Strings and numbers

Text values are commonly represented inside single quotes:

```sql
WHERE category = 'Gifts'
```

Numeric values are commonly written without quotes:

```sql
WHERE released = 1
```

The meaning of quote characters is important when examining how a query is constructed.

## 4. What Is SQL Injection?

**SQL injection (SQLi)** is a vulnerability in which untrusted input is handled in a way that lets it alter the structure or meaning of an SQL statement.

The key issue is not simply that input contains unusual characters. The issue is whether the application allows that input to be interpreted as part of the SQL program rather than as a data value.

A useful mental model is:

```text
User-controlled input
        ↓
Application builds a query
        ↓
Database parses the resulting SQL
        ↓
Query behaves differently than intended
```

## 5. Unsafe Concatenation vs. Parameterized Queries

### Unsafe: putting input directly into SQL

```python
category = request_parameter

query = (
    "SELECT * FROM products WHERE category = '" + category +
    "' AND released = 1"
)
```

The application joins SQL text and user-controlled input into one statement. If the input affects SQL syntax, it can change the query's logic.

### Safer: parameter binding

```python
category = request_parameter

query = "SELECT * FROM products WHERE category = ? AND released = 1"
cursor.execute(query, (category,))
```

Here, the SQL statement and the category value are supplied separately. The database driver binds the value as data instead of treating it as newly supplied SQL syntax. The `?` placeholder is used by SQLite; other database drivers may use different placeholder formats.

**Core principle:** use parameterized queries consistently. Do not rely on manually removing or escaping suspicious characters as the primary defense.

## 6. Why Quotes, Boolean Conditions, and Comments Matter

When input is concatenated into a quoted SQL expression, a quote may close the original string. The parser may then interpret subsequent input as SQL syntax.

A Boolean expression such as `OR 1=1` is significant because `1=1` is always true. Depending on how the query is built, adding such a condition may weaken the original filter.

Some SQL dialects use `--` to begin a line comment. A comment can cause the remainder of a query line to be ignored. Whether a comment works as expected depends on the database dialect and syntax context.

These are parts of the mechanism—not universal payloads. Understand the query context and why the logic changes instead of memorizing strings.

## 7. SQL Injection Can Subvert Application Logic

Applications use SQL to implement decisions, not only to retrieve lists of data. For example, a query may help the application decide whether a login attempt corresponds to a user record.

If user input can alter the query's intended logic, SQL injection may affect application behavior such as:

- **Filtering data:** records outside the intended filter may be returned.
- **Authentication:** a vulnerable login query may accept a request without correctly verifying the supplied credentials.
- **Other database operations:** impact depends on the vulnerable query, database permissions, and application design.

The important distinction is between the intended application rule and the query that is actually executed. If SQL input can modify the query, the database result may no longer represent the decision the developer intended.

### Two completed learning examples

The following are progress references only; their steps, payloads, request/response evidence, impact, and remediation are documented in separate lab reports.

1. **Retrieving hidden data:** a vulnerable product category filter allowed unreleased products to be displayed.
2. **Subverting application logic:** a vulnerable login function allowed authentication as the administrator without knowing the administrator's password.

These examples use the same fundamental weakness—user input changing SQL logic—but demonstrate different consequences. The first bypasses a data filter; the second subverts an authentication decision.

## 8. SQL Injection vs. Authorization

SQL injection and broken authorization are different vulnerability classes.

- **SQL injection:** input can alter the structure or meaning of an SQL query.
- **Broken authorization:** the application fails to enforce what the current user is allowed to access or do.

A parameterized query can prevent SQL injection in a query while the application still has an authorization flaw. For example, an application must separately check whether the logged-in user is allowed to view a particular private record.

Authentication asks, **“Who are you?”** Authorization asks, **“What are you allowed to access or do?”** Neither is replaced by parameterization.

## 9. Prevention and Defensive Practices

1. **Use parameterized queries / prepared statements.** Keep SQL structure separate from user-supplied values.
2. **Avoid dynamic SQL built from untrusted input.** If a query element cannot be represented by a bind parameter (such as a table or column name), use a strict allowlist of valid choices and construct the query safely.
3. **Use least-privilege database accounts.** Limit what the application's database account can read or change.
4. **Avoid disclosing unnecessary database errors.** Detailed errors can reveal implementation information.
5. **Enforce authorization separately.** A safely parameterized query does not automatically prove that a user is permitted to access a record.
6. **Test fixes.** Verify that intended results remain correct and that user input is still treated as data.

## 10. PortSwigger SQL Injection Learning-Path Progress

Learning path: [SQL injection](https://portswigger.net/web-security/learning-paths/sql-injection)

- [x] **Retrieving hidden data — lab solved.** Separate lab report maintained.
- [x] **Subverting application logic — completed on October 25, 2026.** Separate login-bypass lab report maintained.
- [ ] **Next suggested section: SQL injection UNION attacks.**

This checklist reflects the progress recorded in these notes; it is not a statement about the status displayed by PortSwigger's website.

## 11. Quick Reference

```sql
-- Retrieve every row
SELECT * FROM products;

-- Filter by category
SELECT * FROM products
WHERE category = 'Gifts';

-- Require both conditions
SELECT * FROM products
WHERE category = 'Gifts'
AND released = 1;
```

Parameterized SQLite example:

```python
cursor.execute(
    "SELECT * FROM products WHERE category = ? AND released = 1",
    (category,)
)
```

## 12. Review Questions

Try answering these without looking back:

1. What do `SELECT`, `FROM`, and `WHERE` do?
2. What is the difference between string data and SQL syntax?
3. Why is constructing SQL through string concatenation risky?
4. Why can a Boolean condition such as `1=1` alter a vulnerable filter?
5. How does parameter binding address the root cause of SQL injection?
6. How does bypassing a product filter differ from bypassing a login decision?
7. Why does using a parameterized query not eliminate the need for authorization checks?
8. Why should database permissions follow the principle of least privilege?

## Core Mental Model

```text
Input
  ↓
Application
  ↓
Query construction
  ↓
SQL parsing and execution
  ↓
Database result
  ↓
Application decision
```

Ask at each step: **Who controls this value? Is it data or executable structure? What decision depends on the result? What security control must still be enforced?**

---