# Lab Report: SQL Injection UNION Attack — Retrieving Multiple Values in a Single Column

**Platform:** PortSwigger Web Security Academy  
**Difficulty:** Practitioner  
**Topic:** SQL Injection — UNION Attacks  
**Status:** ✅ Solved

## 1. Objective

Perform a UNION-based SQL injection attack to retrieve usernames and passwords from the `users` table, combine each username and password into a single result value, and use the retrieved administrator credentials to log in.

## 2. Lab Description

The application contains a SQL injection vulnerability in its product category filter. The results of the underlying SQL query are reflected in the application's response.

The database contains a separate table named `users`, with two columns:

- `username`
- `password`

Unlike the previous lab, only one of the original query's two columns was compatible with text. Therefore, retrieving the username and password as separate columns would not satisfy the query's column type requirements.

The objective was to combine both values into a single text expression.

## 3. Methodology

### Step 1: Intercept the category request

I used Burp Suite to inspect the HTTP request generated when selecting a product category.

I located the category parameter and sent the request to Burp Repeater so I could modify the input and observe the application's responses.

### Step 2: Confirm column count and text compatibility

I tested the following payload in the category parameter:

```sql
'+UNION+SELECT+NULL,'abc'--
```

**Observation:** The UNION query succeeded, confirming that the original query returned two columns and that the second column was compatible with a text value.

The first column was represented by `NULL`, while the second contained the test string `'abc'`.

### Step 3: Retrieve multiple values in one column

I then used the following successful payload:

```sql
'+UNION+SELECT+NULL,username+||+'~'+||password+FROM+users--
```

**Observation:** The application response contained usernames and passwords combined into single values, separated by the `~` character.

The `||` operator concatenates strings in the SQL syntax used by this lab.

### Step 4: Log in as administrator

After retrieving the credentials, I navigated to the account page and used the administrator's credentials to log in.

**Result:** The administrator login succeeded, and the lab was marked as solved.

## 4. Technical Explanation

### Why was concatenation necessary?

A UNION operation requires both queries to return the same number of columns, with compatible data types in corresponding positions.

In this lab:

- The original query returned two columns.
- Only the second column was compatible with text.
- The `username` and `password` values needed to be retrieved through that single text-compatible column.

Concatenation made it possible to combine two database values into one result.

### Understanding the expression

The core expression was:

```sql
username || '~' || password
```

It combines three components:

| Component | Purpose |
|---|---|
| `username` | Retrieves the username value |
| `~` | Separates the username and password |
| `password` | Retrieves the password value |

For example, fictional values could produce a combined result such as:

```text
alice~example-password
```

The separator makes it easier to distinguish the two values in the application's response.

The full query placed this concatenated expression in the second column and used `NULL` in the first.

## 5. Results

| Stage | Finding |
|---|---|
| Original query structure | Two columns |
| Text-compatible columns | Second column |
| Data retrieval | Usernames and passwords appeared in the response |
| Concatenation | Both values combined using `~` |
| Authentication | Successfully logged in as administrator |
| Final status | Lab solved |

## 6. Key Takeaways

1. A UNION attack requires matching column counts and compatible corresponding data types.
2. The original query's column positions may have different data type requirements.
3. When only one column accepts text, multiple values can sometimes be combined into one string expression.
4. The `||` operator performs string concatenation in the SQL syntax used by this lab; concatenation syntax varies across database engines.
5. A visible response containing combined database values can expose information from other tables.
6. SQL injection can lead to account compromise when exposed credentials are accepted by the application's authentication system.

## 7. Security Remediation

The primary defense is to use parameterized queries rather than constructing SQL statements by concatenating untrusted input.

Other important protections include:

- Apply least-privilege permissions to database accounts.
- Store passwords using an appropriate password-hashing algorithm rather than plaintext.
- Avoid exposing sensitive database results in application responses.
- Review query-building code for unsafe string concatenation.
- Test database access paths for SQL injection vulnerabilities.

## 8. Personal Learning Note

This lab built on my previous UNION attack exercises.

I confirmed that the original query returned two columns, identified the second as text-compatible, and used string concatenation to retrieve usernames and passwords through that single column.

My successful payload was:

```sql
'+UNION+SELECT+NULL,username+||+'~'+||password+FROM+users--
```

I then used the administrator's credentials to log in and solve the lab.

**Main lesson:** When the original query has only one text-compatible column, concatenation can combine multiple database values into a single result.

**Next learning objective:** Continue studying UNION-based SQL injection and how database-specific syntax affects query behavior.

---
