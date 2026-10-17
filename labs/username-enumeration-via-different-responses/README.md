# Username Enumeration via Different Responses

**Platform:** PortSwigger Web Security Academy  
**Difficulty:** Apprentice  
**Date performed:** 2026-10-16  
**Status:** Solved in the assigned lab instance  
**Tools:** Burp Suite Community Edition, Proxy, HTTP history, Intruder

## Overview

This lab demonstrates how differences in login error responses can reveal whether a username exists. After identifying a valid username, the lab's supplied candidate password list was used to identify the corresponding password and complete the login.

This was performed against the dedicated PortSwigger Web Security Academy lab instance only. The lab hostname is intentionally not recorded here because lab instances can be temporary and the hostname is not needed to explain the finding.

## Objective

1. Establish a baseline using an invalid username and password.
2. Compare login responses for candidate usernames.
3. Identify a response that differs from the invalid-username baseline.
4. Use the lab-provided candidate password list for the identified username.
5. Confirm successful authentication in the lab browser.
6. Document the observations without storing credentials or session secrets.

## Environment and scope

- **Target:** The assigned PortSwigger Web Security Academy lab instance.
- **Allowed scope:** The lab instance provided for this exercise.
- **Not in scope:** Other PortSwigger users, unrelated sites, or real accounts.
- **Request examined:** `POST /login`.
- **Evidence handling:** Do not commit passwords, session cookies, authorization tokens, or unredacted screenshots containing these values.

## Method

### 1. Establish the baseline

Opened the lab's login page in Burp's browser and submitted an invalid username and password. The corresponding `POST /login` request was located in **Proxy → HTTP history**.

### 2. Enumerate candidate usernames

Sent the login request to **Intruder** and used the candidate usernames supplied by the lab. The username was the only changing payload value; the password value was held constant.

### 3. Compare responses

Compared response status, length, and—most importantly—the response body. The key observation was a response containing **`Incorrect password`**, which differed from the **`Invalid username`** response observed for an invalid username.

This difference indicated that the application recognized the username but rejected the supplied password.

### 4. Test candidate passwords

Kept the identified username fixed and used the candidate passwords supplied by the lab as the changing payload. Inspected the response status and the corresponding response to distinguish a successful login from failed attempts.

### 5. Confirm the result

Observed an HTTP **`302`** response for the successful attempt and then logged in through the lab browser. The lab was successfully solved.

## Findings

### Finding: Username enumeration through different login responses

**Observed behavior:** The application returned different error messages for an invalid username and for a recognized username with an incorrect password.

**Evidence:** An Intruder result for a candidate username returned `Incorrect password` rather than the `Invalid username` message seen in the baseline. A subsequent password-candidate attempt returned HTTP `302`, and successful login was confirmed in the browser.

**Security impact:** An attacker may be able to distinguish valid usernames from invalid ones. That information can make subsequent targeted password attacks more efficient, especially if password controls and login-attempt defenses are weak.

**Suggested mitigations:**

- Use generic login errors that do not reveal whether the username or password was incorrect.
- Apply appropriate rate limiting or progressive delays to repeated authentication failures.
- Monitor and alert on unusual volumes of failed login attempts.
- Encourage strong, unique passwords and offer multifactor authentication where appropriate.
- Ensure authentication behavior is consistent enough that response bodies, status codes, and timing do not unnecessarily reveal account existence.

## Evidence and screenshots

Store screenshots in the repository's existing `labs/screenshots/` directory. Suggested filenames are listed below; treat them as naming recommendations, not proof that a file exists. Update the names to match the actual captures before committing.

| Evidence ID | Suggested filename | What it should show |
|---|---|---|
| E01 | `E01-login-baseline.png` | Baseline login request/response with the submitted values redacted. |
| E02 | `E02-username-enumeration.png` | Candidate username result and the different `Incorrect password` response. |
| E03 | `E03-password-result-302.png` | Successful result showing status `302`; redact credentials and sensitive headers. |
| E04 | `E04-lab-solved.png` | Lab completion or authenticated account page, with sensitive values hidden. |

If your screenshot filenames differ, update this table. Do not create placeholder screenshots or mark evidence captured until the actual image exists.

## Lessons learned

- Authentication responses can disclose whether an account exists.
- A response-length difference is a useful lead, but the response content and context should be inspected before drawing a conclusion.
- A `302` response alone is not universal proof of successful authentication; in this lab, it was corroborated by logging in and confirming the lab was solved.
- This exercise demonstrates an authentication weakness in the lab. It does **not** establish that an unrelated application is vulnerable.
- Preserve original evidence privately when useful, but commit only sanitized screenshots and notes.

## Reproduction notes

To repeat the exercise, start a fresh instance of the same PortSwigger lab and use its current instructions and supplied candidate lists. Lab instances and hostnames may change. Keep all requests within the assigned lab target.

## References

- [PortSwigger Web Security Academy — Authentication](https://portswigger.net/web-security/authentication)
- [Lab: Username enumeration via different responses](https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-different-responses)
- [Candidate usernames](https://portswigger.net/web-security/authentication/auth-lab-usernames)
- [Candidate passwords](https://portswigger.net/web-security/authentication/auth-lab-passwords)

---
