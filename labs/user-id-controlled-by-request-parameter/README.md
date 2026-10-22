# Lab: User ID Controlled by Request Parameter

**Platform:** PortSwigger Web Security Academy  
**Category:** Access Control  
**Difficulty:** Apprentice  
**Status:** Completed — Lab Solved  
**Tool:** Burp Suite Community Edition  
**Features Used:** Burp Browser, Proxy → HTTP history, Repeater

## 1. Objective

Obtain the API key belonging to the lab user `carlos` by identifying and exploiting a horizontal privilege escalation vulnerability on the account page.

The lab provided the following credentials for the account used during testing:

- **Username:** `wiener`
- **Password:** `peter`

The objective was to access Carlos's account information and submit his API key as the lab solution.

**Official lab:** <https://portswigger.net/web-security/access-control/lab-user-id-controlled-by-request-parameter>

## 2. Vulnerability Overview

This lab demonstrates **Insecure Direct Object Reference (IDOR)**, a common access-control vulnerability.

An application may use a user-controlled identifier to determine which account or resource to display. If the application does not properly verify whether the authenticated user is authorized to access the requested resource, changing that identifier may expose another user's information.

In this lab, the account page used an `id` query parameter to identify the account whose information was requested.

The vulnerable behavior allowed the logged-in user, `wiener`, to change the identifier to `carlos` and retrieve Carlos's API key.

## 3. Environment and Scope

- **Target:** The assigned PortSwigger Web Security Academy lab instance.
- **Testing scope:** The intentionally vulnerable lab application only.
- **Authentication:** Logged in as `wiener` using the credentials supplied by the lab.
- **Request examined:** Account-page request using the `id` query parameter.
- **Testing tool:** Burp Suite Community Edition.

All testing was performed within the authorized training environment.

## 4. Methodology

### Step 1: Open the lab and authenticate

Opened the assigned lab instance in Burp Suite's browser.

Navigated to the account page and logged in using the credentials provided by the lab:

```text
Username: wiener
Password: peter
```

After logging in, accessed my account page.

### Step 2: Inspect the HTTP request

Opened **Proxy → HTTP history** in Burp Suite and located the request associated with the account page.

The relevant request used the `id` query parameter to specify the account:

```http
GET /myaccount?id=wiener
```

This was the baseline request for my own account.

Sent the request to Burp Repeater to inspect and modify it.

### Step 3: Modify the account identifier

In Repeater, changed the `id` parameter from `wiener` to `carlos`, leaving the rest of the request unchanged.

The modified request was:

```http
GET /myaccount?id=carlos
```

Sent the request and inspected the response body.

### Step 4: Analyze the response

The response contained Carlos's API key, even though I was authenticated as `wiener`.

This demonstrated that the application allowed my authenticated session to retrieve information associated with another user's account without properly enforcing the required object-level authorization.

### Step 5: Confirm lab completion

Copied the API key obtained from the lab response and submitted it as the solution.

PortSwigger Web Security Academy confirmed that the lab was solved.

## 5. Findings

### Finding: Horizontal Privilege Escalation Through IDOR

**Vulnerability type:** Insecure Direct Object Reference (IDOR)

**Affected functionality:** Account page

**User-controlled parameter:** `id`

**Observed behavior:**

The application returned different account information based on the value of the `id` parameter. Changing the identifier from `wiener` to `carlos` exposed Carlos's API key to the authenticated `wiener` session.

**Expected behavior:**

The application should have verified that the authenticated user was authorized to access the requested account before returning its information.

**Actual behavior:**

The application accepted the modified account identifier and returned sensitive information belonging to another user.

**Evidence:**

1. The baseline request used `/myaccount?id=wiener`.
2. The modified request used `/myaccount?id=carlos`.
3. The modified response contained Carlos's API key.
4. Submitting the API key resulted in the lab being marked as solved.

## 6. Root Cause

The root cause was missing or ineffective **server-side object-level authorization**.

The application treated the account identifier supplied in the request as sufficient to select the account information to return, without correctly enforcing whether the authenticated user was permitted to access that account.

The vulnerability was not simply that the `id` parameter was visible or changeable. The actual security failure was that the application returned another user's sensitive information without the required authorization check.

## 7. Security Impact

In a real application, an equivalent vulnerability could allow a user to access another user's private information.

Depending on the exposed functionality, the impact could include:

- Unauthorized disclosure of personal or account information.
- Exposure of API keys or other sensitive account data.
- Potential misuse of exposed credentials or tokens, depending on their permissions and validity.
- Unauthorized modification of another user's data if similar authorization failures affect write operations.

The demonstrated impact in this lab was unauthorized access to Carlos's API key. Broader consequences would depend on the permissions associated with such a key and the affected application's design.

## 8. Recommended Remediation

### 8.1 Enforce server-side authorization

Before returning account information, the server must determine whether the authenticated user is permitted to access the requested account.

### 8.2 Derive identity from the authenticated session

For the user's own account page, the application should normally identify the account through the validated session rather than trusting a client-supplied identifier as proof of identity.

### 8.3 Check authorization for every object

Every account, invoice, document, or other protected object should have an appropriate access-control check. Authorization must be enforced consistently across read, update, and delete operations.

### 8.4 Do not rely on unpredictable identifiers

Replacing usernames or sequential IDs with random identifiers can make references harder to guess, but it does not replace authorization checks.

### 8.5 Add regression tests

Tests should verify that one authenticated user cannot retrieve or modify another user's protected resources without the required permission.

## 9. Key Lessons Learned

- A successfully authenticated user is not automatically authorized to access every account.
- Client-controlled parameters must not be treated as proof of permission.
- IDOR commonly leads to horizontal privilege escalation when a user accesses another user's resources.
- Object-level authorization must be enforced on the server.
- A response body may contain important evidence that is not apparent from inspecting the request alone.
- A successful lab completion confirms the behavior of the intentionally vulnerable training application, not the presence of the same vulnerability in an unrelated system.

## 10. Review Questions

1. What made the `id` parameter security-relevant in this lab?
2. Why was changing `id=wiener` to `id=carlos` successful?
3. What is the difference between IDOR and horizontal privilege escalation?
4. Which server-side authorization check should have been performed?
5. Why would changing account identifiers to unpredictable values not fully solve the problem?
6. What was the evidence that confirmed the lab had been solved?

## 11. Final Takeaway

**The key security failure was the absence of effective object-level authorization.**

The account page trusted a user-controlled account identifier without adequately verifying access permissions. By modifying the `id` parameter in Burp Repeater, I retrieved another user's API key and completed the lab.

The main defensive lesson is that the server must verify access permissions for every protected object. Knowing or supplying an object's identifier must never, by itself, grant access to that object.

---
