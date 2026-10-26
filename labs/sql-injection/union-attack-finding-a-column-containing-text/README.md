# Lab Report: SQL Injection UNION Attack — Finding a Column Containing Text

**Platform:** PortSwigger Web Security Academy  
**Difficulty:** Practitioner  
**Topic:** SQL Injection — UNION Attacks  
**Status:** ✅ Solved

## 1. Objective

Identify which column in the original SQL query is compatible with string data by performing a UNION-based SQL injection attack.

The lab provided a random value that had to appear in the application's query results to demonstrate that a compatible column had been identified.

## 2. Lab Description

The application contains a SQL injection vulnerability in its product category filter. The results of the underlying SQL query are reflected in the application's response.

Before identifying a text-compatible column, the number of columns returned by the original query must be established.

In the previous lab, I determined that the original query returns **three columns**. This lab builds on that result.

## 3. Methodology

### Step 1: Intercept the category request

I used Burp Suite to inspect the HTTP request generated when selecting a product category.

I located the category parameter and sent the request to Burp Repeater, allowing me to modify the parameter and observe the application's responses.

### Step 2: Confirm the column count

I verified the three-column structure using the following payload in the category parameter:

```sql
'+UNION+SELECT+NULL,NULL,NULL--
```

The three `NULL` expressions matched the number of columns returned by the original query.

### Step 3: Identify a text-compatible column

The lab required a randomly provided value to appear in the query results.

I tested the columns individually by replacing one `NULL` value with the provided string while leaving the other two values as `NULL`.

The successful payload was:

```sql
'+UNION+SELECT+NULL,'Hhvv8R',NULL--
```

**Observation:** The injected query succeeded, and the required value appeared in the application's response. The lab was solved.

## 4. Technical Explanation

The SQL `UNION` operator combines the results of two `SELECT` statements.

For a UNION operation to succeed:

- Both queries must return the same number of columns.
- Corresponding columns must have compatible data types.

The original query returned three columns, so the injected query also needed three expressions.

Initially, all three expressions were `NULL`. I then replaced each `NULL` individually with the lab's random string to determine which position could accept text.

The successful payload placed `'Hhvv8R'` in the **second column**:

| Column | Injected value | Purpose |
|---|---|---|
| 1 | `NULL` | Placeholder |
| 2 | `'Hhvv8R'` | Test string value |
| 3 | `NULL` | Placeholder |

Because the supplied string was accepted in the second position and appeared in the response, this established that the second result column was compatible with the text value in this context.

## 5. Result

**Confirmed findings:**

- The original query returns three columns.
- The UNION query succeeds with three corresponding expressions.
- The second column accepts the supplied string.
- The lab-provided value `Hhvv8R` appeared in the application's response.
- The lab was successfully solved.

## 6. Key Takeaways

1. Determine the original query's column count before attempting a UNION attack.
2. A successful UNION requires matching column counts and compatible corresponding data types.
3. Replacing one `NULL` value at a time helps isolate which column can accept a text value.
4. A string appearing in the response provides evidence that the corresponding result column is compatible with text and is reflected by the application.
5. The ability to accept text and the ability to display it in the HTTP response are related but distinct properties.

## 7. Personal Learning Note

In this lab, I built on my previous column-count discovery and tested the compatibility of individual columns.

My successful payload was:

```sql
'+UNION+SELECT+NULL,'Hhvv8R',NULL--
```

The key result was that **column 2 was compatible with the supplied string and its value appeared in the application's response**.

This technique is useful for understanding which columns can display text in a UNION-based SQL injection scenario.

**Next learning objective:** Learn how UNION attacks can retrieve additional information from other tables in an authorized lab environment.

---
