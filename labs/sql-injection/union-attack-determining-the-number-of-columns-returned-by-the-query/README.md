# Lab Report: SQL Injection UNION Attack — Determining the Number of Columns

**Platform:** PortSwigger Web Security Academy  
**Lab difficulty:** Practitioner  
**Topic:** SQL Injection — UNION Attacks  
**Status:** ✅ Solved  
**Result:** The original query returns **3 columns**.

## 1. Objective

Determine the number of columns returned by the application's product category query by performing a SQL injection UNION attack that returns an additional row containing `NULL` values.

## 2. Lab Description

The application contains a SQL injection vulnerability in its product category filter. The results of the underlying query are reflected in the application's response, making it possible to investigate the query structure through controlled changes to the category parameter.

The task was to identify the number of columns returned by the original query.

## 3. Methodology

### Step 1: Intercept the category request

I used Burp Suite to inspect the HTTP request generated when selecting a product category.

I located the category parameter and sent the request to Burp Repeater so that I could modify the parameter and compare responses.

### Step 2: Test a UNION query with one NULL

I first changed the category parameter to:

```sql
'+UNION+SELECT+NULL--
```

**Observation:** The application returned an error.

This suggested that the injected `SELECT` statement did not satisfy the requirements for combining its results with the original query. A mismatch in the number of columns was a likely explanation.

### Step 3: Increase the number of NULL values

I then tested the query with additional `NULL` expressions, increasing the number of columns in the injected `SELECT` statement.

The key requirement was that the original query and the injected query must return the same number of columns.

### Step 4: Confirm the column count

The lab was solved when I supplied **three `NULL` values**:

```sql
'+UNION+SELECT+NULL,NULL,NULL--
```

**Observation:** The error disappeared, and the application's response included additional content containing the `NULL` values.

This provided evidence that the injected query had the required number of columns.

## 4. Technical Explanation

The SQL `UNION` operator combines the result sets of two `SELECT` statements.

For the operation to succeed:

- Both queries must return the same number of columns.
- Corresponding columns must have compatible data types.

The original query returned three columns, so the injected `SELECT` needed three expressions as well.

`NULL` was useful because it is compatible with many common SQL data types, reducing the likelihood of a data-type mismatch during this initial test.

The observed success with three `NULL` values established the required column count for the lab.

## 5. Result

| Test | Number of injected columns | Observation |
|---|---:|---|
| Initial test | 1 (`NULL`) | Error returned |
| Final successful test | 3 (`NULL, NULL, NULL`) | Error disappeared; additional content appeared |

**Conclusion:** The original product category query returns **three columns**.

## 6. Key Takeaways

1. A UNION attack requires both `SELECT` statements to return the same number of columns.
2. Testing different numbers of `NULL` expressions is a method for determining the required column count.
3. Errors and changes in the application response provide useful clues, but should be interpreted in the context of the test.
4. `NULL` values help reduce data-type compatibility issues during column-count discovery.
5. Once the column count is established, it becomes possible to investigate the compatibility of individual columns in subsequent authorized UNION attack labs.

## 7. Personal Learning Note

I learned how to use Burp Repeater to investigate the structure of a query by modifying a product category parameter and comparing the application's responses.

The main insight was that the number of expressions in the injected `SELECT` statement must match the number of columns returned by the original query. In this lab, **three `NULL` values produced the successful response**.

---
