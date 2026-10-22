# Web Security Notes: HTTP, Attack-Surface Mapping, and Burp Suite

These notes cover HTTP revision and the first steps in mapping a web application's attack surface. They are organized by topic, not by study day.

## 1. What is an attack surface?

An **attack surface** is the set of places through which an application can receive input, expose data, or perform actions.

Examples include:

- Pages and URLs
- HTTP endpoints
- Query parameters and request-body fields
- Request headers and cookies
- Login forms and authenticated features
- APIs
- File uploads and downloads
- Actions such as creating, changing, or deleting records

An attack surface is a map of things to understand and test. Its existence does **not** mean the application is vulnerable.

## 2. A simple web-application model

```text
Browser / client
       |
       | HTTP request
       v
Web server / reverse proxy
       |
       v
Application routing
       |
       v
Authentication -> Authorization
       |
       v
Business logic
       |
       +------> API / cache / database
       |
       v
HTTP response
       |
       v
Browser / client
```

This is a conceptual model. Not every application has every component, and the order may differ. A simple static-file server, like the local lab in this exercise, does **not** implement login, authorization, a database, or application business logic.

## 3. Important terms

### HTTP request

A client sends an HTTP request to ask for a resource or request an operation. A request can contain a method, target, headers, and sometimes a body.

```http
GET /products?id=12 HTTP/1.1
Host: example.test
User-Agent: CyberLab
```

### Method

The method indicates the kind of operation requested. Common methods include `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, and `OPTIONS`.

### Path

The path identifies the requested route or resource within the target host.

```text
/products
/products/12
/login
```

A path does not, by itself, prove that a corresponding resource exists.

### Query parameter

Query parameters appear after `?` in a URL. Multiple parameters are commonly separated by `&`.

```text
/products?id=12&sort=price
```

Here, `id=12` and `sort=price` are query parameters. A parameter only matters if the application actually reads or uses it.

### Headers

Headers carry request or response metadata, such as `Host`, `User-Agent`, `Accept`, `Content-Type`, `Authorization`, and `Cookie`.

A client can supply many request headers. A server should not treat client-supplied values as trustworthy proof of identity or permission.

### Request body

A request body can carry data submitted to the server, such as form fields or JSON. Not every request has a body.

Example JSON body:

```json
{"name": "Alice"}
```

### Endpoint

For mapping purposes, record an endpoint as the **HTTP method plus path**, and note its query parameters and body fields separately. For example, `GET /products` and `POST /products` may trigger different behavior.

### Authentication and authorization

- **Authentication:** establishes the identity associated with a request — “Who are you?”
- **Authorization:** determines what that identity is allowed to access or do — “What are you allowed to do?”

A user may be authenticated successfully and still not be authorized to perform a particular action.

## 4. HTTP status-code revision

| Status | General meaning | What to remember |
|---|---|---|
| `200` | OK | The request was handled successfully. |
| `201` | Created | A resource was created. |
| `301` | Moved Permanently | A redirect response. |
| `302` | Found | A redirect response. |
| `400` | Bad Request | The request was invalid or could not be processed as sent. |
| `401` | Unauthorized | Authentication credentials are missing or invalid, or authentication is required. |
| `403` | Forbidden | The server refuses the requested operation. |
| `404` | Not Found | The requested resource was not found. |
| `405` | Method Not Allowed | That method is not supported for the target resource. |
| `429` | Too Many Requests | The client has sent too many requests in a period. |
| `500` | Internal Server Error | A server-side failure occurred. |
| `502` | Bad Gateway | A gateway or proxy received an invalid upstream response. |
| `503` | Service Unavailable | The service is temporarily unable to handle the request. |

A status code is evidence of how the server responded; it does not, by itself, establish a vulnerability.

## 5. Why the same URL can return different responses

The response may depend on more than the URL. Factors can include:

- HTTP method (`GET` versus `HEAD` or `POST`)
- Headers such as `Accept` or `Content-Type`
- Cookies and session state
- Authentication identity and permissions
- Request body or query parameters
- Server-side data or state changing over time
- Caching, rate limits, and other server rules

When comparing responses, change one variable at a time so you can tell which change may have caused the difference.

## 6. Cookies: `Set-Cookie` and `Cookie`

A server can ask a browser to store a cookie using a response header:

```http
Set-Cookie: session=example-value
```

A later request may send the stored cookie back:

```http
Cookie: session=example-value
```

Conceptual flow:

```text
Server response: Set-Cookie
          |
          v
Browser stores cookie according to cookie rules
          |
          v
Later matching request: Cookie
          |
          v
Server processes the request
```

A cookie may be associated with session state, but the cookie's presence alone does not prove who the user is or what permissions they should have. The application must validate the session and enforce authorization.

## 7. Mapping an application

For each endpoint or feature, record:

1. **Method and path:** What request is being made?
2. **Inputs:** Which query parameters, headers, cookies, or body fields are present?
3. **Purpose:** What does the endpoint appear to retrieve or change?
4. **Authentication:** Is an identity/session required?
5. **Authorization:** What access rules should apply?
6. **Observed behavior:** What status, headers, and body did the server return?
7. **Open question:** What still needs to be understood or tested?

Use a table like this in your notes or lab log:

| Method + path | Inputs | Purpose / data | Auth expected? | Authorization question | Observation / next question |
|---|---|---|---|---|---|
| `GET /products` | `sort`, `page` (if supported) | Display products | Depends on design | Is the data meant to be public? | Record actual result |
| `GET /products?id=12` | `id=12` | Request a product | Depends on design | What data does this identifier select? | Record actual result |
| `POST /cart` | Body, cookies (if supported) | Modify a cart | Depends on design | Who is allowed to change this cart? | Record actual result |

These are illustrative examples, not claims about the local static server. Only record authentication or authorization behavior when the target actually implements it.

## 8. Local attack-surface lab

### Project location

Your current naming is sensible:

```text
~/cyber-lab/projects/attack-surface/site/
```

`attack-surface` describes the purpose better than a day-based directory name. Keep `site/` for the files served by the local web server. Store the reusable concepts in `~/cyber-lab/notes/web-security.md`.

Expected project layout:

```text
cyber-lab/
├── notes/
│   └── web-security.md
└── projects/
    └── attack-surface/
        └── site/
            └── index.html
```

### Create the local page

```bash
mkdir -p ~/cyber-lab/projects/attack-surface/site
cd ~/cyber-lab/projects/attack-surface
printf '<!doctype html><html><head><title>Cyber Lab</title></head><body><h1>Cyber Lab</h1><p>Local HTTP testing environment.</p></body></html>\n' > site/index.html
```

### Start the local-only server

Run this from `~/cyber-lab/projects/attack-surface`:

```bash
python3 -m http.server 8000 --bind 127.0.0.1 --directory site
```

Keep this terminal running. Binding to `127.0.0.1` keeps the lab reachable through loopback rather than listening on every network interface.

In a second terminal, run each request separately:

```bash
curl -i http://127.0.0.1:8000/
curl -i http://127.0.0.1:8000/index.html
curl -i 'http://127.0.0.1:8000/?source=day4'
curl -i http://127.0.0.1:8000/missing
```

`curl -i` includes the response headers in the output, followed by the response body.

### What to look for

| Request | Common expected result | What it helps you observe |
|---|---|---|
| `GET /` | `200` when `index.html` is served | How the root path is handled |
| `GET /index.html` | `200` | How the explicit file path compares with `/` |
| `GET /?source=day4` | Usually the same page as `/` | The query string is present, but this static server generally serves the same file; it does not implement custom query logic |
| `GET /missing` | `404` | How the server responds to a missing path |

Treat these as expectations to verify, not a substitute for observing your own output. Response wording and headers can vary by Python version.

### Observation log template

Copy and fill this in after running each request:

```text
Request:
Method:
Path:
Query parameters:
Status:
Interesting response headers:
What changed compared with the previous request?
What does the evidence support?
What remains unknown?
```

## 9. What this lab proves — and does not prove

This lab can help you practise reading methods, paths, query strings, status codes, headers, and response bodies.

It does **not** demonstrate a real login system, user roles, session authorization, a database, or a business workflow. The built-in Python HTTP server is a static-file server, so do not draw conclusions about those features from this lab.

Keep these distinctions clear:

- A parameter existing is not a vulnerability.
- A `404` is an HTTP response, not necessarily a network failure.
- A strange response is not automatically a security finding.
- A security finding needs reproducible evidence of a weakness and a meaningful impact.

## 10. Quick revision

```text
Attack surface → places where input, data, or actions are exposed
Endpoint       → method + path, with relevant inputs documented separately
Query          → URL data after ?
Headers        → request/response metadata
Body           → optional request/response content
Authentication → who the request is associated with
Authorization  → what that identity is allowed to do
Evidence       → what the response actually demonstrates
```

The useful investigation habit is: map what exists, make a clear hypothesis, change one variable at a time, record the response, and avoid claiming more than the evidence supports.

## 11. Burp Suite: Proxy and HTTP history

Burp Suite is an intercepting proxy used to inspect and test traffic between a client (such as a browser) and a web server. In this lab, Burp is used only with the local application at `127.0.0.1:8000`.

### The traffic flow

```text
Burp's built-in browser
        |
        | HTTP request
        v
Burp Proxy listener
        |
        | forwards the request
        v
Local Python HTTP server (127.0.0.1:8000)
        |
        | HTTP response
        v
Burp Proxy
        |
        v
Burp's built-in browser
```

Burp can pause a request before forwarding it, let you inspect or modify it, and then forward or drop it. Its HTTP history is a record of the requests and responses that passed through the proxy.

### Important distinction: `curl` versus Burp's browser

A request made directly by `curl` does **not** automatically pass through Burp. To see a request in Burp's HTTP history, send it through Burp—for this exercise, use Burp's built-in browser. That browser is already configured to use Burp's proxy.

### Start the local target

Keep the local server running in one terminal:

```bash
cd ~/cyber-lab/projects/attack-surface
python3 -m http.server 8000 --bind 127.0.0.1 --directory site
```

Verify in another terminal if needed:

```bash
curl -i http://127.0.0.1:8000/
```

The local target is plain HTTP, so a Burp CA certificate is not needed for this exercise. Do not switch to unrelated or public targets for this lab.

### Open the browser and inspect traffic

1. Start Burp Suite Community Edition.
2. Open **Proxy → Intercept**.
3. Select **Open browser**. Use that browser for the requests below.
4. Initially set **Intercept off** so requests can complete without pausing.
5. Visit `http://127.0.0.1:8000/` and confirm the page loads.
6. Open **Proxy → HTTP history**. Select the request and inspect both the request and response panels.
7. Turn **Intercept on** and visit `http://127.0.0.1:8000/index.html` in the built-in browser. Burp should pause a matching request. Read the request before choosing **Forward** to send it to the server. **Drop** cancels the intercepted request.
8. Turn **Intercept off** again when finished. Traffic can still be recorded in HTTP history while interception is off.

Interface labels can differ slightly between Burp versions. If the request does not appear, check that you used Burp's built-in browser, that the local server is running, and that the target URL is exactly `http://127.0.0.1:8000/`.

### Intercept controls

| Control | Meaning |
|---|---|
| **Intercept on** | Pause matching requests so you can inspect them before they are sent. |
| **Forward** | Send the currently intercepted request onward. |
| **Drop** | Cancel the currently intercepted request instead of sending it. |
| **Intercept off** | Stop pausing requests; the proxy can forward traffic normally. HTTP history can still record it. |

Do not treat an intercepted request as completed until it has been forwarded and you have observed the response.

### HTTP history: what to inspect

For each history item, inspect the request and the corresponding response. Record the evidence that is actually visible.

**Request side**

- Method, such as `GET`
- Path and query string
- Host
- Request headers such as `User-Agent` and `Accept`
- Cookies or body fields, if present (do not publish real secrets or tokens)

**Response side**

- Status code
- Response headers, especially `Content-Type`, `Content-Length`, and `Server` if present
- Response body and whether it resembles the expected page or an error page

HTTP history may also display fields such as status, length, MIME type, and parameters in its table. A missing header is simply an observation; do not infer a vulnerability from its absence alone.

### Five local HTTP exchanges to document

Use Burp's built-in browser with **Intercept off** for these requests so they complete normally. Wait for the page or response, then select the matching entry in **Proxy → HTTP history**.

| # | URL | What to compare |
|---|---|---|
| 1 | `http://127.0.0.1:8000/` | How the server handles the root path. |
| 2 | `http://127.0.0.1:8000/index.html` | Root path versus explicit file path. |
| 3 | `http://127.0.0.1:8000/?source=day4` | Whether the query string is present and whether the response differs. |
| 4 | `http://127.0.0.1:8000/missing` | The response for a path that should not exist. |
| 5 | `http://127.0.0.1:8000/?source=proxy-lab` | Compare a second query value with the first query test. |

The expected results are hypotheses, not completed observations. Record your actual status, headers, and response in Burp. With Python's simple static-file server, the root and `index.html` will commonly return the same page, query strings generally will not alter the static content, and a missing path commonly returns `404`. Verify rather than assume.

### Exchange log template

Copy one block for each of the five exchanges into `~/cyber-lab/notes/web-security.md`:

```markdown
### HTTP Exchange 1 — Root Path
- **Request:** `GET /`
- **Target:** `127.0.0.1:8000`
- **Query parameters:** None
- **Status:** [record the observed status]
- **Content-Type:** [record the observed value, or `Not present`]
- **Other useful headers:** [record actual values]
- **Response body:** [brief description]
- **Observation:** [what you noticed]
- **Conclusion:** [what the evidence supports]
- **Open question:** [what you still do not know]
```

For other exchanges, update the title, method/path, and query parameters as appropriate. Do not fill in status codes or header values from memory; use the actual Burp response.

### Investigation habits

- Compare like with like: inspect the same fields for each exchange.
- Change one variable at a time. For example, compare `/` with `/?source=day4` to investigate the query string while keeping the host and method the same.
- Separate observation from interpretation. “The response status is `404`” is an observation; “the endpoint is vulnerable” is not supported by that fact alone.
- Do not claim a server-side feature exists just because a parameter appears in the URL.
- Use only the local lab target unless you have explicit authorization for another system.
- Keep real credentials, session cookies, authorization headers, and tokens out of committed notes.

## 12. Official references

- [Burp Suite: Getting started](https://portswigger.net/burp/documentation/desktop/getting-started)
- [Intercepting HTTP traffic](https://portswigger.net/burp/documentation/desktop/getting-started/intercepting-http-traffic)
- [Proxy: HTTP history](https://portswigger.net/burp/documentation/desktop/tools/proxy/http-history)
- [Burp's browser](https://portswigger.net/burp/documentation/desktop/tools/burps-browser)

---

## Authentication and Authorization

### Authentication

Authentication verifies the identity of a user or service.

### Authorization

Authorization determines whether an identity may perform a specific action
on a particular resource.

A successful login does not automatically grant access to every record
or operation.

### Key terms

- Identity: the user or service making a request.
- Session: state linking successive requests to an authenticated identity.
- Cookie: browser-managed data that may carry a session identifier.
- Role: a category of permissions.
- Object-level authorization: permission to access a specific object.
- Function-level authorization: permission to perform a specific action.

### Request flow

Browser → Request → Session validation → Identity →
Authorization check → Action → Response

### Security principle

The server must enforce authorization. Client-controlled request values
and hidden interface elements are not proof of permission.

---

# Access Control

## 1. What Is Access Control?

**Access control** is the process of determining which users or systems may access particular resources and perform particular actions.

A web application may contain user profiles, orders, invoices, administrative panels, and account-management functions. Not every user should have permission to access or modify all of them.

For example:
- Alice should be able to view her own profile.
- Alice should not automatically be able to view Bob's private information.
- An ordinary user should not be able to delete other users.
- An administrator may have additional permissions, according to the application's rules.

The central security principle is:

> Every sensitive resource and action must be protected by appropriate authorization checks.

## 2. Authentication vs. Authorization

These concepts are related but different.

### Authentication — Who are you?

Authentication verifies the identity associated with a request.

Common mechanisms include:
- Passwords
- Multi-factor authentication (MFA)
- Session cookies
- Access tokens
- Client certificates

Successful authentication establishes an identity, but it does not automatically grant access to every resource.

### Authorization — What are you allowed to do?

Authorization determines whether an identity is allowed to access a particular resource or perform a particular action.

For example, an application may authenticate Alice successfully but deny her access to Bob's private invoice.

### Request flow

A simplified security flow is:

```text
Incoming request
      |
      v
Authenticate the identity
      |
      v
Determine the requested resource/action
      |
      v
Check authorization
      |
      +---- Denied ----> Reject request
      |
      v
Perform the permitted operation
      |
      v
Return response
```

**Remember:** Authentication establishes identity; authorization enforces permissions.

---

## 3. Horizontal Privilege Escalation

**Horizontal privilege escalation** occurs when a user gains access to another user's resources or functionality at approximately the same privilege level.

Example:

Alice and Bob are ordinary users of a web application.

- Alice can view her own invoices.
- Bob can view his own invoices.
- Alice should not be able to view Bob's invoices.
- A security flaw allows Alice to access Bob's invoice.

Alice has crossed a boundary between users, but she has not necessarily gained administrator privileges.

### Security impact

Depending on the application, horizontal escalation may expose:
- Personal information
- Private messages
- Orders and invoices
- Documents
- Account-specific records

It may also allow modification or deletion of another user's data if the affected operations permit it.

### Key question

**Can this user access another user's resources without permission?**

---

## 4. Vertical Privilege Escalation

**Vertical privilege escalation** occurs when a user gains access to capabilities or permissions intended for a higher privilege level.

Example:

- An ordinary user can view their own profile.
- An administrator can delete user accounts.
- A flaw allows the ordinary user to invoke the account-deletion operation.

The ordinary user has crossed a privilege-level boundary.

### Security impact

Possible consequences include:
- Unauthorized account deletion
- Changes to user roles or permissions
- Modification of administrative settings
- Access to privileged functionality
- Disruption of application operations

The actual impact depends on which permissions are exposed and what the application allows those permissions to do.

### Key question

**Can this user perform an action that requires greater privileges?**

---

## 5. Object-Level Authorization

An **object** is a particular resource or record managed by an application.

Examples include:
- A user profile
- An invoice
- An order
- A document
- A support ticket
- A database record

Object-level authorization determines whether the current user is permitted to access or modify the particular object requested.

For example, an application might receive:

```http
GET /invoices/1002
```

The server must not assume that the user can access invoice `1002` simply because the request contains its identifier.

It must establish whether the authenticated user has permission to access that invoice.

### Important distinction

Knowing an object's identifier is not the same as being authorized to access the object.

Identifiers may be:
- Sequential integers
- Random identifiers
- UUIDs
- Usernames
- Slugs
- Other application-specific references

Changing an identifier is not inherently a vulnerability. The vulnerability exists when the application grants access without the required authorization.

### Key question

**Is this user allowed to access this specific object?**

---

## 6. Function-Level Authorization

A **function** is an operation or capability that an application provides.

Examples include:
- Deleting a user
- Changing account roles
- Issuing a refund
- Exporting sensitive information
- Modifying application configuration
- Viewing administrative reports

Function-level authorization determines whether the current user is allowed to execute the requested operation.

For example, hiding an administrator-only button from ordinary users does not protect the operation itself. A user may still attempt to send the corresponding HTTP request directly.

The server must enforce the permission check when processing the request.

### Key question

**Is this user allowed to perform this particular action?**

---

## 7. IDOR — Insecure Direct Object Reference

**IDOR** is a common access-control vulnerability in which an application uses a user-controlled reference to locate an object but fails to enforce the necessary access check.

Consider the following request:

```http
GET /account?user_id=1001
```

The application uses `user_id` to identify the requested account.

If the current user can change the reference and retrieve another user's private account information without permission, the application may be vulnerable to IDOR.

### How IDOR occurs

A simplified sequence is:

```text
User sends request
       |
       v
Application reads object reference
       |
       v
Application retrieves object
       |
       v
Required authorization check is missing
       |
       v
Unauthorized object access
```

### Common object references

An IDOR may involve:
- Query parameters
- URL path parameters
- Hidden form fields
- JSON request-body fields
- File or document identifiers
- References included in API requests

The parameter's location or naming is not the decisive factor. The important question is whether the application enforces the required permission check.

### IDOR and horizontal escalation

IDOR commonly results in horizontal privilege escalation when a user accesses another user's record at the same privilege level.

However, IDOR and horizontal escalation are not synonyms:

- **IDOR** describes a vulnerability pattern involving object references and missing authorization.
- **Horizontal privilege escalation** describes the resulting access across users at a similar privilege level.

An IDOR can sometimes contribute to more serious privilege escalation, depending on which objects or operations become accessible.

### Key question

**Does the application verify that the authenticated user is allowed to access the object identified by the request?**

---

## 8. How the Concepts Relate

| Concept | What it describes | Main security question |
|---|---|---|
| Horizontal privilege escalation | Access across users at a similar privilege level | Can this user access another user's resources? |
| Vertical privilege escalation | Access to higher-privilege capabilities | Can this user perform a privileged operation? |
| Object-level authorization | Permission for a specific resource | Is this user allowed to access this record? |
| Function-level authorization | Permission for a specific operation | Is this user allowed to perform this action? |
| IDOR | A common object-reference access-control flaw | Is a user-controlled reference accepted without the necessary access check? |

These concepts overlap rather than compete with one another.

For example, an IDOR involving another user's invoice may represent:
- An object-level authorization failure
- An IDOR vulnerability
- Horizontal privilege escalation

The terms describe different aspects of the same underlying security problem.

---

## 9. Why Hiding URLs Is Not Security

An application might hide an administrator link or avoid displaying certain functionality to ordinary users.

That does not establish an access-control boundary.

A user can sometimes discover a route through:
- Public files such as `robots.txt`
- Links elsewhere in the application
- Browser developer tools
- JavaScript files
- Previously observed requests
- Direct requests to known paths

Discovering a route is not automatically a vulnerability. The real issue is whether the server permits an unauthorized user to access the resource or perform the action.

**Security must depend on enforced permissions, not on keeping URLs secret.**

---

## 10. Core Principles for Preventing Access-Control Vulnerabilities

### 10.1 Enforce authorization on the server

Do not rely on a hidden button, a disabled interface element, or a client-controlled field to enforce permissions.

### 10.2 Check every sensitive object

When retrieving or modifying a record, verify that the authenticated user has the necessary permission for that particular resource.

### 10.3 Check every sensitive action

Administrative and other privileged operations must enforce appropriate permissions on the server-side endpoint that performs the action.

### 10.4 Deny access by default

When the application cannot establish the required permission, it should not perform the protected operation.

### 10.5 Do not confuse identifiers with permissions

A sequential ID, random identifier, or UUID identifies a resource; it does not grant permission to access it.

Unpredictable identifiers may make discovery more difficult, but they do not replace authorization checks.

### 10.6 Test different identities and privilege levels

Access-control rules should be considered across:
- Unauthenticated users
- Ordinary authenticated users
- Different users at the same privilege level
- Users with elevated permissions
- Administrators

The application must enforce the intended rules consistently.

---

## 11. Evidence and Vulnerability Reasoning

A suspicious response does not automatically prove an access-control vulnerability.

For example:
- A `200 OK` response does not necessarily mean unauthorized data was exposed.
- A `403 Forbidden` response suggests the server refused the request, but the full context still matters.
- A visible URL does not prove that its functionality is unprotected.
- A predictable object identifier does not prove that IDOR exists.

A sound security conclusion should distinguish:

1. **Observation:** What did the application actually return or permit?
2. **Authorization rule:** What should the user have been allowed to access or do?
3. **Failure:** Which required permission check was missing or ineffective?
4. **Impact:** What information or operation became accessible?
5. **Remediation:** Which server-side check would prevent the unauthorized access?

The goal is to explain the security failure, not simply label a request as suspicious.

---

## 12. Final Mental Model

Use this model when examining an application's access-control design:

```text
Request
   |
   v
Who is making the request?
   |
   v
What resource is being requested?
   |
   v
What operation is being attempted?
   |
   v
Does the identity have permission
for this resource and operation?
   |
   +---- No ----> Reject the operation
   |
   v
Perform the authorized operation
```

The central principle is:

**A user being authenticated does not mean the user is authorized to access every object or execute every function. The server must enforce permissions for the particular resource and action.**

---

## Authentication and Session Investigation

- Lab: Username Enumeration via Different Responses
- Successful login status: `302`
- Login response `Location` header: Present
- Login response `Set-Cookie`: Present
- Cookie on subsequent authenticated request: Present
- Logout response status: `302`
- Logout response `Set-Cookie`: Present
- Cookie expiration directive observed on logout: No
- Fresh account-page request after logout: Access denied

### Conclusion

The login response redirected the browser and included a `Set-Cookie` header. A subsequent request included a `Cookie` header. The logout response also redirected the browser and included `Set-Cookie`. A fresh account-page request after logout was denied.

These observations are consistent with a session-based authentication flow. They do not, by themselves, establish whether logout invalidated the server-side session or whether the original session identifier would be rejected if reused.

### Limitations

- The exact effect of the logout `Set-Cookie` header has not been established.
- Server-side invalidation of the original session has not been independently verified.
- No conclusion about cookie security attributes has been recorded without inspecting them.

---
