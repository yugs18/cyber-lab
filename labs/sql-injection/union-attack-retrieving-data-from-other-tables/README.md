# Lab Report: SQL Injection UNION Attack — Retrieving Data from Other Tables

**Platform:** PortSwigger Web Security Academy  
**Difficulty:** Practitioner  
**Topic:** SQL Injection — UNION Attacks  
**Status:** ✅ Solved

## 1. Objective

Use a UNION-based SQL injection vulnerability in the product category filter to retrieve usernames and passwords from another database table, then use the administrator credentials to log in.

## 2. Lab Description

The application contains a SQL injection vulnerability in its product category filter. The results of the underlying SQL query are reflected in the application's response.

The database contains a separate table named `users`, with two columns:

- `username`
- `password`

To complete the lab, I needed to establish the structure of the original query, identify columns compatible with text, retrieve the contents of the `users` table, and log in as the administrator.

## 3. Methodology

### Step 1: Intercept the category request

I used Burp Suite to inspect the HTTP request generated when selecting a product category.

I located the category parameter and sent the request to Burp Repeater so I could modify the input and compare the application's responses.

### Step 2: Determine the query structure

The first step was to identify the number of columns returned by the original query and determine which columns could accept text.

I used the following payload in the category parameter:

```sql
'+UNION+SELECT+'abc','def'--
```

**Observation:** The UNION query was accepted with two text values, confirming that the original query returned two columns and that both result positions were compatible with text.

### Step 3: Retrieve data from the users table

With the column count and text compatibility established, I used the following payload:

```sql
'+UNION+SELECT+username,+password+FROM+users--
```

This query selected the `username` and `password` columns from the separate `users` table.

**Observation:** The application's response contained usernames and passwords from the table.

This demonstrated that the vulnerable query could be manipulated to include data from a different table in its results.

### Step 4: Log in as administrator

After retrieving the credentials, I navigated to the account page and logged in as the administrator.

**Result:** The administrator login succeeded, and the lab was marked as solved.

## 4. Technical Explanation

The SQL `UNION` operator combines the results of multiple `SELECT` statements into one result set.

For a UNION operation to work:

- Both queries must return the same number of columns.
- Corresponding columns must have compatible data types.

The original query returned two columns, and both could accept text. This made it possible to use the two columns to return the `username` and `password` values from the `users` table.

The vulnerability arose because user-controlled input could alter the SQL query's structure. Instead of restricting the results to the intended product category, the manipulated query could return information from another table.

## 5. Results

| Stage | Finding |
|---|---|
| Query structure | Two columns |
| Text compatibility | Both columns accepted text |
| Data retrieval | Usernames and passwords from `users` appeared in the response |
| Authentication | Successfully logged in as administrator |
| Final status | Lab solved |

## 6. Key Takeaways

1. Determining the original query's column count is an important first step in a UNION attack.
2. Testing with text values helps identify which result columns can accept strings.
3. UNION-based SQL injection can expose data from other tables when the query is vulnerable and its results are reflected in the response.
4. Database query manipulation can compromise confidentiality and, when retrieved credentials are accepted by the application, account security as well.
5. SQL injection can be prevented by using parameterized queries that keep user-supplied values separate from SQL instructions.

## 7. Remediation

The primary remediation is to replace unsafe query construction with parameterized queries.

Additional defensive measures include:

- Avoid concatenating untrusted input directly into SQL statements.
- Restrict database accounts to the minimum permissions required.
- Never store user passwords in plaintext; use a suitable password-hashing algorithm.
- Avoid exposing sensitive database results in application responses.
- Test database access paths for SQL injection vulnerabilities.

## 8. Personal Learning Note

This lab combined the techniques from my previous UNION attack exercises.

I first established that the query returned two columns, confirmed that both columns accepted text, retrieved data from the `users` table, and then used the administrator credentials to access the account page.

**The main lesson:** A SQL injection vulnerability can extend beyond manipulating product filters. If the database query is constructed unsafely, it may expose information from other tables and lead to account compromise.

**Next learning objective:** Learn how UNION attacks can retrieve specific types of information and understand how database-specific behavior affects these techniques.

---
