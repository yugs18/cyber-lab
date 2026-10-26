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

### Completed

- [x] **Retrieving hidden data — Apprentice lab solved.** Separate lab report maintained.
- [x] **Subverting application logic — Apprentice lab solved on October 25, 2026.** Separate login-bypass lab report maintained.
- [x] **UNION attack: determining the number of columns — Practitioner lab solved on October 26, 2026.** Three columns were required in that lab's query.
- [x] **UNION attack: finding a column containing text — Practitioner lab solved on October 26, 2026.** The second column accepted and reflected the lab-provided string in that lab.
- [x] **UNION attack: retrieving data from other tables — Practitioner lab solved on October 26, 2026.** Retrieved values from the `users` table and successfully logged in as the administrator in the lab.
- [x] **UNION attack: retrieving multiple values in a single column — Practitioner lab solved on October 26, 2026.** Combined the username and password into one text expression and successfully logged in as the administrator in the lab.

### Next

- [ ] **Examining the database.** Learn how database type/version information and database structure can be investigated in authorized labs.

**Important:** Each PortSwigger lab has its own target application and query. Column counts and text-compatible column positions found in one lab do not automatically apply to another lab. Individual lab steps, payloads, request/response evidence, and credentials remain in separate lab reports; this file records theory and progress only.

This checklist records the progress reported in these notes. It does not claim to reflect the account-specific completion status displayed by PortSwigger.

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
9. Why must the original and injected SELECT statements return the same number of columns in a UNION operation?
10. What is the difference between a text-compatible column and a value visibly reflected by the application?
11. How can a UNION vulnerability expose rows from another table?
12. How can concatenation return multiple field values through a single result column?
13. Why should you re-determine column count and type compatibility for each separate lab or target query?

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

# SQL Injection — Detection Methodology

## 1. Overview

SQL injection detection is the process of identifying whether user-controlled input can influence the structure or behavior of an SQL query.

A tester modifies an input in a controlled way and observes how the application responds. The objective is to determine whether the observed behavior is consistent with SQL injection.

**Core methodology:**

`Baseline → Controlled Change → Compare → Repeat → Corroborate`

The goal is not to memorize payloads. It is to understand why application behavior changes and whether the evidence supports a vulnerability finding.

Testing must be limited to systems you own or are explicitly authorized to assess.

---

## 2. Syntax Errors and Error Messages

### 2.1 How syntax errors occur

An application may construct a query using user-supplied input. If that input changes the query's syntax unexpectedly, the database may reject the resulting query.

Example query:

```sql
SELECT username
FROM users
WHERE username = 'alice';
```

If the generated SQL becomes syntactically invalid, the database may produce an error.

### 2.2 What a tester may observe

- An error message referring to SQL syntax.
- A database-specific exception.
- An HTTP 500 Internal Server Error.
- A generic application error page.
- No visible error, even when query execution fails.

### 2.3 Why errors are useful

Error messages can reveal that input has reached a database-related processing path. Detailed errors may also expose information about the database engine or query structure.

However, an error alone does not prove SQL injection. It could originate from application validation, another component, or an unrelated failure.

**Key principle:** A syntax error is a clue that requires further investigation, not proof by itself.

---

## 3. Logically True and False Conditions

SQL supports Boolean expressions that evaluate to either true or false.

Examples:

```sql
1 = 1
```

This expression evaluates to true.

```sql
1 = 2
```

This expression evaluates to false.

### 3.1 Why Boolean conditions matter

Consider a query that retrieves users matching a specified username:

```sql
SELECT username
FROM users
WHERE username = 'alice';
```

If user-controlled input can alter the query's condition, the query may return unexpected results.

A condition that evaluates to true may allow additional records to match. A condition that evaluates to false may prevent records from matching.

This behavior can provide evidence that the input is affecting SQL logic.

### 3.2 The comparison methodology

In an authorized testing environment:

1. Record the normal response for a baseline input.
2. Compare behavior when the relevant condition evaluates to true.
3. Compare behavior when that condition evaluates to false.
4. Keep other request details unchanged.
5. Repeat the comparison to determine whether the difference is consistent.

### 3.3 What to compare

- HTTP status code.
- Response body and page content.
- Number of returned records.
- Response length.
- Redirect destination.
- Response time, when relevant.

**Key principle:** Change one variable at a time so that the cause of a behavioral difference is easier to identify.

---

## 4. Response Differences: Clues, Not Proof

A difference between two responses does not automatically establish SQL injection.

For example, a normal request might return HTTP 200, while a modified request returns HTTP 500. This could indicate a query-processing problem, but other explanations are possible.

### 4.1 Alternative explanations

- Application input validation.
- Authentication or session-state differences.
- Caching.
- Rate limiting.
- Network instability.
- An unrelated application error.
- Dynamic content that changes between requests.

### 4.2 How to evaluate evidence

**Step 1 — Establish a baseline**

Record how the application responds to ordinary input.

**Step 2 — Make a controlled change**

Modify only the input relevant to the hypothesis.

**Step 3 — Compare the responses**

Inspect status codes, response bodies, lengths, redirects, and timing.

**Step 4 — Repeat the observation**

Check whether the same behavior occurs consistently.

**Step 5 — Seek corroborating evidence**

Use additional authorized testing or application-side logs when available.

A repeatable difference that closely follows a controlled input change is stronger evidence than a single unexpected response.

**Key principle:** Form a hypothesis, test it, and investigate alternative explanations before reaching a conclusion.

---

## 5. UNION-Based SQL Injection

### 5.1 What does UNION do?

`UNION` combines the result sets of two or more `SELECT` statements into a single result set.

Example using fictional data:

```sql
SELECT username FROM users
UNION
SELECT category FROM products;
```

Both queries return one column. Their results can therefore be combined, assuming the corresponding result types are compatible.

By default, `UNION` removes duplicate rows.

`UNION ALL` retains duplicates.

### 5.2 Why column counts must match

Consider the following query:

```sql
SELECT username, display_name
FROM users;
```

It returns two columns.

A `SELECT` statement combined with this query through `UNION` must also return two columns. A query returning only one column is structurally incompatible.

### 5.3 Why data types matter

Corresponding columns must have compatible data types for the database to combine their results meaningfully.

For example:

| First result column | Corresponding second column | Concept |
|---|---|---|
| Text | Text | Generally compatible |
| Two-column result | One-column result | Incompatible column counts |
| Incompatible values | Database-dependent | May fail or require conversion |

Exact compatibility and conversion behavior depend on the database engine.

### 5.4 Why UNION matters in SQL injection testing

If a vulnerable query's results are displayed by an application, a UNION-based vulnerability may allow additional query results to become part of the displayed output.

The tester investigates the structure of the original query and whether compatible results can be combined with it.

For this stage of learning, remember these two requirements:

- The combined `SELECT` statements must return the same number of columns.
- Corresponding columns must have compatible data types.

Do not try to memorize every database-specific syntax variation yet.

---

## 6. Blind SQL Injection

### 6.1 Definition

Blind SQL injection occurs when an application is vulnerable to SQL injection, but it does not directly reveal useful query results or database error details.

Instead, the tester infers query behavior from indirect signals.

### 6.2 Boolean-based blind SQL injection

The application's behavior changes depending on whether a condition evaluates to true or false.

Possible signals include:

- Different page content.
- A record appearing or disappearing.
- Different application messages.
- A repeatable difference in response behavior.

The tester uses these differences to infer how the database evaluates a condition.

### 6.3 Time-based blind SQL injection

In some cases, a condition can influence how long the database takes to respond.

The tester may observe a repeatable timing difference and use it as an indirect signal.

Timing evidence requires caution because network latency, server load, and other processing delays can produce similar effects.

### 6.4 Important distinction

| Technique | Main observable signal |
|---|---|
| Error-based detection | Database or application errors |
| Boolean-based detection | Different behavior for true and false conditions |
| UNION-based detection | Additional query results appearing in application output |
| Time-based blind detection | Condition-dependent response timing |

These are different detection approaches, not mutually exclusive categories. One application may expose more than one kind of signal.

**Key principle:** An application does not need to display SQL errors for SQL injection to exist.

---

## 7. A Systematic Detection Workflow

Use this workflow when investigating a suspected SQL injection vulnerability in an authorized lab.

1. **Understand the input.** Identify which request parameter or field may influence a database query.
2. **Establish normal behavior.** Record a baseline request and response.
3. **Form a hypothesis.** Decide what behavior would be expected if the input affected SQL syntax or logic.
4. **Change one variable.** Keep the rest of the request consistent.
5. **Observe the response.** Check content, status, response length, redirects, and timing.
6. **Repeat and compare.** Confirm that the observed difference is reproducible.
7. **Evaluate alternative explanations.** Consider validation, sessions, caching, infrastructure, and application logic.
8. **Document the evidence.** Record the request, observation, conclusion, and remaining uncertainty.
9. **Recommend remediation.** Prefer parameterized queries and review other unsafe query-construction paths.

---

## 8. Common Mistakes

### Mistake 1: Treating every server error as SQL injection

An HTTP 500 response has several possible causes. Investigate rather than assuming.

### Mistake 2: Changing multiple inputs simultaneously

When several variables change, it becomes difficult to determine which one caused the response difference.

### Mistake 3: Relying on a single observation

Repeat the test and consider ordinary sources of variation.

### Mistake 4: Assuming no error means no vulnerability

Blind SQL injection can be detectable through indirect behavior.

### Mistake 5: Memorizing syntax without understanding query structure

Database syntax varies. Understanding Boolean logic, result sets, column counts, and data types transfers across systems more effectively than memorizing isolated payloads.

---

## 9. Remediation

The primary defense against SQL injection is to separate SQL instructions from user-supplied data.

Use parameterized queries rather than concatenating untrusted values into SQL strings.

For example, with Python's SQLite interface:

```python
query = "SELECT username FROM users WHERE username = ?"
rows = connection.execute(query, (username,)).fetchall()
```

The placeholder keeps the query structure separate from the supplied value.

Additional practices include:

- Avoid exposing detailed database errors to users.
- Apply appropriate database privileges.
- Validate input according to the application's requirements.
- Review query-building code for unsafe concatenation.
- Use logging and testing to investigate failures without leaking sensitive information.

Input validation and generic error messages are useful supporting controls, but they do not replace parameterized queries.

---

## 10. Key Takeaways

- Syntax errors can be useful clues, but they do not prove SQL injection on their own.
- Comparing logically true and false conditions can reveal whether input influences query behavior.
- Response differences should be reproduced and evaluated against alternative explanations.
- `UNION` combines query results; column counts must match and corresponding data types must be compatible.
- Blind SQL injection relies on indirect signals rather than directly visible database output.
- Controlled, repeatable testing is more reliable than guessing based on one response.
- Parameterized queries are the primary defense against SQL injection through user-supplied values.

### Mental Model

**Baseline → Controlled Change → Compare → Repeat → Corroborate → Document**

The most important skill is not knowing the largest number of payloads. It is being able to explain why an observation supports—or fails to support—a security hypothesis.

---

## UNION Attacks — Determining the Number of Columns

### 1. Overview

In a SQL injection UNION attack, the injected query must return the same number of columns as the original query. Corresponding columns must also have compatible data types.

There are two common methods for determining the number of columns returned by the original query:

1. Using `ORDER BY` and incrementing the column index.
2. Using `UNION SELECT` with different numbers of `NULL` values.

The objective is to observe how the application's response changes as the number of columns is varied.

---

### 2. Method One — Using ORDER BY

#### 2.1 Concept

The `ORDER BY` clause sorts query results according to a specified column. A column can be referenced by its position in the result set, so the column's name does not need to be known.

For example:

```sql
ORDER BY 1
ORDER BY 2
ORDER BY 3
```

Each statement attempts to order the results using the corresponding column position.

#### 2.2 How it works

- Start with a low column index.
- Increment the index in subsequent tests.
- Observe the application's response.
- When the specified position exceeds the number of columns in the result set, the database may return an error.

Example error:

```text
The ORDER BY position number 3 is out of range
of the number of items in the select list.
```

If position 2 is valid and position 3 produces a column-position error, this suggests that the result set has two columns.

#### 2.3 Interpreting the response

The application may:

- Display the database error.
- Return a generic error page.
- Return an empty result.
- Produce another observable response difference.

A response difference can help infer the column count, but the tester must consider other possible causes of the behavior.

**Key point:** An invalid column position can reveal the upper limit of the result set's column indexes.

---

### 3. Method Two — Using UNION SELECT with NULL

#### 3.1 Concept

The `UNION` operator combines the results of multiple `SELECT` statements.

For a UNION operation to work, both queries must return the same number of columns, and their corresponding column types must be compatible.

The tester can compare query results while varying the number of expressions in the second `SELECT` statement.

Conceptual examples:

```sql
SELECT NULL
```

```sql
SELECT NULL, NULL
```

```sql
SELECT NULL, NULL, NULL
```

These statements return one, two, and three columns, respectively.

#### 3.2 Why NULL is used

`NULL` represents the absence of a value.

It is useful for column-count testing because it is compatible with many common SQL data types. This can reduce type-compatibility problems when the original column types are unknown.

However, exact behavior depends on the database engine and the context in which the values are used.

#### 3.3 Interpreting the response

When the number of expressions does not match the original query's column count, the database may reject the UNION operation.

Example error:

```text
All queries combined using a UNION, INTERSECT or EXCEPT
operator must have an equal number of expressions
in their target lists.
```

When the column counts match and the types are compatible, the query may succeed and produce an additional result row containing NULL values.

Depending on the application, the response may show:

- Additional content, such as another row in a table.
- A different application error caused by NULL values.
- A generic response that hides the difference.
- No obvious visible change.

If the response looks the same for successful and unsuccessful attempts, this method may not provide enough information to determine the column count.

**Key point:** A successful UNION requires matching column counts and compatible corresponding data types.

---

### 4. Comparing the Two Methods

| Feature | ORDER BY method | UNION SELECT NULL method |
|---|---|---|
| Main idea | Test column positions | Test numbers of returned expressions |
| What is varied? | Column index | Number of columns in the injected SELECT |
| Useful signal | An invalid column-position error | A UNION column-count error or a changed response |
| Requires column names? | No | No |
| Possible limitation | Errors may be hidden or ambiguous | Successful results may not be visible |
| Type compatibility | Not the main test objective | Must be considered for a successful UNION |

Both methods rely on observing response differences. Neither is guaranteed to work if the application hides errors or produces indistinguishable responses.

---

### 5. Limitations and Evidence

A tester should not assume that every error or response change identifies the exact number of columns.

Possible complications include:

- The application hides database errors.
- The application returns the same generic response for different database outcomes.
- NULL values cause application-level errors.
- Database engines differ in syntax and error messages.
- Other application behavior causes the observed response difference.

Use controlled comparisons and repeat observations where appropriate. Record what was observed and distinguish confirmed behavior from an inference.

---

### 6. Key Takeaways

- A UNION attack requires both SELECT statements to return the same number of columns.
- Corresponding columns must have compatible data types.
- `ORDER BY` column indexes can help infer the number of columns.
- `UNION SELECT` with different numbers of `NULL` expressions is another column-count technique.
- `NULL` is useful because it is compatible with many common data types, but compatibility is not universal in every context.
- Database errors, generic errors, additional rows, and response differences can all provide clues.
- If the application hides or normalizes the differences, the result may remain inconclusive.

### Mental Model

**Vary the column position or expression count → Observe the response → Compare outcomes → Evaluate the evidence.**

The goal is to understand the structure of the original query, not to memorize every database-specific syntax variation.

---

## 13. UNION Attacks — Finding a Text-Compatible Column

### 13.1 What does text-compatible mean?

A UNION query combines rows returned by two `SELECT` statements. The statements must return the same number of columns, and corresponding columns must have compatible data types.

In some applications, the original query returns multiple columns, but only some positions can accept a text value. A **text-compatible column** is a result position in which a string value can be returned without a data-type incompatibility in that query context.

### 13.2 General method

After determining the original query's column count:

1. Keep that column count fixed.
2. Use a recognizable test string in one result position.
3. Keep the other positions as `NULL` placeholders where appropriate.
4. Test one position at a time, observing the response.
5. Record which position accepts the string and whether the application actually displays it.

This process distinguishes two related but different facts:

- **Type compatibility:** the database can return the supplied text in that position.
- **Reflection:** the application includes that returned value in its response in a way the tester can observe.

A value may be compatible but not visibly displayed if the application hides, transforms, or fails to render the result. Therefore, lack of visible output alone does not always prove a type mismatch.

### 13.3 Key points

- Determine the column count before testing individual column types.
- Change one position at a time so the result is easier to interpret.
- The text-compatible position is specific to the query being tested.
- Errors and response changes are evidence to interpret, not conclusions on their own.

---

## 14. UNION Attacks — Retrieving Data from Other Tables

### 14.1 Concept

A UNION-based SQL injection may allow a vulnerable query to include rows from a different table in its result set. This can expose information that the original application feature was not intended to return.

Conceptually, `UNION` appends compatible rows to a result set; it does not join columns side by side. The injected `SELECT` must satisfy the original query's column-count and data-type requirements.

### 14.2 Requirements for useful results

- The injected and original `SELECT` statements return the same number of columns.
- Corresponding values have compatible data types.
- The database account has permission to read the target table.
- The application's response exposes the relevant result values.
- The table and column names used by the query are known or have been established in the authorized test.

Even when the database query succeeds, the application may not visibly display the additional rows. Response rendering and database query success are separate considerations.

### 14.3 Security impact

If a product-filter input can be manipulated to retrieve rows from a users table, the vulnerability can cross the intended data boundary and expose sensitive information. If exposed credentials are usable, the impact may extend to account compromise.

The impact depends on the vulnerable query, database permissions, the data stored, and how the application handles the results.

### 14.4 Defensive takeaway

Use parameterized queries to prevent user-controlled values from changing SQL structure. Also apply least-privilege database permissions and avoid returning sensitive records through unrelated application features. Parameterization and least privilege address different parts of the risk and should be used together.

---

## 15. UNION Attacks — Retrieving Multiple Values in a Single Column

### 15.1 Why combine values?

Sometimes only one column in the original result set is compatible with text, but the information of interest consists of multiple fields. SQL string concatenation can combine several values into one text expression, producing one output value per row.

For example, the expression below illustrates the concept with fictional fields:

```sql
username || '~' || password
```

Here, `||` concatenates strings in SQL dialects that support this operator. The `~` character is a delimiter that helps distinguish the two values in the combined output.

### 15.2 How to reason about the result

- `username` supplies the first value.
- The delimiter separates the values in the displayed string.
- `password` supplies the second value.
- The complete expression occupies one result column.

This can make multiple fields observable through one text-compatible output position, provided the expression is compatible with the database and the application reflects the resulting value.

### 15.3 Database and data caveats

- Concatenation syntax varies across database engines; `||`, `CONCAT()`, and other forms are not interchangeable in every dialect.
- NULL handling can affect the result. In some engines, concatenating a NULL value can make the whole expression NULL unless NULLs are handled explicitly.
- A delimiter should be chosen so it is unlikely to occur within the source values; otherwise, parsing the combined result may be ambiguous.
- Successful concatenation does not itself prove that the application will display the result.

### 15.4 Security lesson

When several sensitive fields can be combined into one reflected value, a limitation on the number of text-compatible result columns may not prevent data exposure. The underlying issue remains the ability to change SQL structure through untrusted input.

**Defensive takeaway:** Parameterized queries prevent injection through bound values. Least-privilege database access and careful control over which query results are returned further reduce the possible impact.

---

