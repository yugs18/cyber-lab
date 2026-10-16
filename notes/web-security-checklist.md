# Web Security Testing Checklist

## 1. Scope and Setup

- [ ] Confirm the authorized target and testing scope.
- [ ] Identify the test accounts and their roles.
- [ ] Record the starting URL and application behavior.
- [ ] Use Burp Suite to capture relevant requests and responses.
- [ ] Avoid recording real passwords, session cookies, or tokens.

## 2. Authentication

- [ ] Identify login and logout endpoints.
- [ ] Observe successful and unsuccessful login responses.
- [ ] Check redirects and relevant response headers.
- [ ] Observe password recovery and account recovery behavior where available.
- [ ] Distinguish confirmed findings from hypotheses.

## 3. Session Management

- [ ] Observe `Set-Cookie` after login.
- [ ] Check whether authenticated requests send a `Cookie` header.
- [ ] Inspect cookie attributes such as `Secure`, `HttpOnly`, and `SameSite`.
- [ ] Observe cookie behavior during logout.
- [ ] Test a fresh request to a protected page after logout.
- [ ] Do not assume that clearing a browser cookie proves server-side invalidation.

## 4. Object-Level Authorization

- [ ] Identify resources belonging to different test users.
- [ ] Determine which user should be allowed to access each resource.
- [ ] Compare authorized and unauthorized access using permitted test accounts.
- [ ] Test user-controlled resource identifiers only within scope.
- [ ] Record whether the server denies unauthorized access.

## 5. Function-Level Authorization

- [ ] Identify privileged functions and administrative endpoints.
- [ ] Determine the expected role required for each function.
- [ ] Check whether the server enforces the role requirement.
- [ ] Test with a lower-privileged account where the lab or scope permits.
- [ ] Check whether the underlying action endpoint is protected, not merely the interface.

## 6. Evidence and Reporting

- [ ] Record the endpoint and HTTP method.
- [ ] Record the expected behavior.
- [ ] Record the observed behavior and status code.
- [ ] Document clear, repeatable reproduction steps.
- [ ] Save redacted request/response evidence when appropriate.
- [ ] Explain realistic impact without exaggeration.
- [ ] Recommend a server-side fix.
- [ ] Document limitations and untested assumptions.

## 7. Final Review

- [ ] Confirm that all testing stayed within the authorized scope.
- [ ] Remove cookies, tokens, credentials, and other sensitive values from evidence.
- [ ] Ensure each finding is supported by observations.
- [ ] Separate confirmed vulnerabilities from potential concerns.
- [ ] Verify the notes and evidence are saved in the intended repository.
