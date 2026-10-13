# Web Security Notes: Attack-Surface Mapping

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
