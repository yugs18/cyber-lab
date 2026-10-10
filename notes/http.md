# HTTP Notes

## What is HTTP?

HTTP (Hypertext Transfer Protocol) is the application-level protocol used for communication between clients and web servers.

A basic HTTP conversation looks like:

```text
Client
   |
   | HTTP Request
   ↓
Server
   |
   | HTTP Response
   ↓
Client
```

The client sends a request.

The server processes the request and sends a response.

A simplified web architecture is:

```text
Browser
   ↓
HTTP
   ↓
Web Server
   ↓
Application
   ↓
Database
```

HTTP is important to cybersecurity because web vulnerabilities often begin with an attacker-controlled HTTP request being interpreted by an application.

A simplified security flow is:

```text
Attacker controls input
        ↓
HTTP request
        ↓
Application interprets it
        ↓
Unexpected behavior
        ↓
Security impact
```

Understanding HTTP is therefore a prerequisite for understanding web security.

---

# HTTP Request

An HTTP request is sent by a client to a server.

A simplified example:

```http
GET / HTTP/1.1
Host: example.com
User-Agent: ...
Accept: ...
```

An HTTP request can contain:

```text
Method
Target / URL
Path
Query parameters
Headers
Body
```

---

## Method

The HTTP method indicates the type of operation the client is requesting.

Example:

```http
GET / HTTP/1.1
```

Here:

```text
GET → HTTP method
```

Common HTTP methods include:

```text
GET
POST
PUT
PATCH
DELETE
HEAD
OPTIONS
```

The method is part of the HTTP request and is one of the things the server uses when determining how to handle the request.

---

# Path

The path identifies the resource being requested.

Example:

```http
GET /users HTTP/1.1
```

Here:

```text
/users
```

is the path.

Another example:

```http
GET /users/42 HTTP/1.1
```

Here:

```text
/users/42
```

is the path.

---

# Query Parameters

Query parameters are values included in the request target, usually after `?`.

Example:

```text
https://example.com/users?id=42
```

Conceptually:

```text
https://example.com/users?id=42
│       │           │    │
│       │           │    └── query parameter
│       │           └────── path
│       └────────────────── host
└────────────────────────── scheme
```

Here:

```text
Scheme → https
Host   → example.com
Path   → /users
Query  → id=42
```

A query can contain one or more parameters.

Example:

```text
/search?q=cat&page=2
```

Conceptually:

```text
q    → cat
page → 2
```

---

# Headers

HTTP headers carry metadata and control information about a request or response.

Examples include:

```text
Host
User-Agent
Accept
Content-Type
Content-Length
Authorization
Cookie
Set-Cookie
Location
Referer
Origin
Cache-Control
```

Headers are extremely important in web security because they can carry information about:

```text
the target host
the client
accepted formats
request/response content
authentication
sessions
redirects
cross-origin behavior
caching
```

---

# HTTP Response

An HTTP response is sent by the server back to the client.

Example:

```http
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: ...

<html>...
```

An HTTP response contains:

```text
Status code
Headers
Body
```

The response status tells the client the result of processing the request.

The headers provide metadata and control information.

The body contains the response content when a body is present.

---

# Request vs Response

### Request

Sent:

```text
Client → Server
```

Contains things such as:

```text
Method
Path
Query parameters
Headers
Body
```

### Response

Sent:

```text
Server → Client
```

Contains:

```text
Status code
Headers
Body
```

Mental model:

```text
Client
   |
   | Request
   ↓
Server
   |
   | Response
   ↓
Client
```

---

# HTTP Methods

## GET

Normally used to retrieve a resource.

Example:

```http
GET /users/42 HTTP/1.1
```

Conceptually:

```text
Retrieve this resource.
```

---

## POST

Commonly used to submit data or request that the server perform an operation that creates or otherwise changes server-side state.

Example:

```http
POST /users HTTP/1.1
Content-Type: application/json

{"name":"Alice"}
```

Conceptually:

```text
Send this data and process it.
```

---

## PUT

Commonly used to replace or create a representation at a target resource.

Conceptually:

```text
Set this resource to this representation.
```

---

## PATCH

Used for partial modification of a resource.

Conceptually:

```text
Change part of this resource.
```

---

## DELETE

Requests deletion of a resource.

Example:

```http
DELETE /users/42 HTTP/1.1
```

Conceptually:

```text
Delete this resource.
```

---

## HEAD

Similar to `GET`, but requests the response headers without the response body.

This can be useful when only metadata about a resource is needed.

---

## OPTIONS

Used to discover communication options supported for a target resource or server.

It becomes especially useful later when studying browser behavior and cross-origin requests.

---

# Security Question About HTTP Methods

HTTP methods have normal meanings and assumptions.

For security, ask:

> What happens if an application does not enforce the assumptions normally associated with the method?

For example, developers may conceptually expect:

```text
GET    → read
POST   → submit/change
DELETE → delete
```

But the method itself does not automatically enforce authorization.

The server still has to enforce the application's security rules.

This becomes important when studying authorization and business logic.

---

# HTTP Status Codes

HTTP status codes communicate the result of processing a request.

The five broad categories are:

```text
1xx → Informational
2xx → Success
3xx → Redirection
4xx → Client/request-related error
5xx → Server-side failure
```

---

# 1xx — Informational

Indicates informational responses.

Individual 1xx status codes do not need to be memorized at this stage.

---

# 2xx — Success

Indicates that the request was successfully processed.

Important examples:

```text
200 OK
201 Created
204 No Content
```

### 200 OK

The request was successfully processed.

### 201 Created

A resource was successfully created.

### 204 No Content

The request was successfully processed without a response body.

---

# 3xx — Redirection

Indicates that the client may need to perform another action, often involving another resource.

Important examples:

```text
301 Moved Permanently
302 Found
304 Not Modified
```

### 301

The resource has been permanently moved.

### 302

Indicates a redirection.

### 304

Indicates that a cached representation can be reused.

---

# 4xx — Client / Request Problems

Indicates a problem involving the request or the client's ability to perform the requested operation.

Important examples:

```text
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
405 Method Not Allowed
429 Too Many Requests
```

---

## 400 Bad Request

The server could not process the request because the request was invalid or malformed.

---

## 401 Unauthorized

Indicates that authentication is required or the supplied authentication credentials are not valid.

Mental model:

```text
Who are you?
```

---

## 403 Forbidden

Indicates that the server understood the request but refuses to allow it.

Mental model:

```text
You are not allowed to do this.
```

---

## 404 Not Found

The requested resource was not found.

---

## 405 Method Not Allowed

The requested method is not supported for the target resource.

---

## 429 Too Many Requests

Indicates that the client has sent too many requests within a given period.

---

# 5xx — Server Errors

Indicates that the server or an intermediary encountered a problem while processing the request.

Important examples:

```text
500 Internal Server Error
502 Bad Gateway
503 Service Unavailable
```

---

## 500 Internal Server Error

A general server-side error occurred.

---

## 502 Bad Gateway

A server acting as a gateway or proxy received an invalid response from an upstream server.

---

## 503 Service Unavailable

The server is currently unable to handle the request.

---

# 401 vs 403

This distinction is extremely important.

```text
401
 ↓
Authentication problem
 ↓
Who are you?
```

```text
403
 ↓
Authorization / permission problem
 ↓
Are you allowed to do this?
```

A useful conceptual distinction:

```text
Authentication
      ↓
Who are you?

Authorization
      ↓
What are you allowed to do?
```

This distinction becomes important later when studying access-control vulnerabilities.

---

# Important HTTP Headers

## Host

Example:

```http
Host: example.com
```

Identifies the host the request is intended for.

A server may host multiple websites, so the requested host is important when determining which site or virtual host should handle the request.

---

# User-Agent

Example:

```http
User-Agent: Mozilla/5.0
```

Provides information about the client software making the request.

It can be used for:

```text
logging
analytics
compatibility
client-specific behavior
```

The value is supplied by the client and should not automatically be treated as trustworthy security information.

---

# Accept

Example:

```http
Accept: application/json
```

Indicates what response media types the client can accept.

This becomes especially useful when working with APIs and content negotiation.

---

# Content-Type

Describes the media type of the message body.

Examples:

```http
Content-Type: application/json
```

```http
Content-Type: application/x-www-form-urlencoded
```

```http
Content-Type: text/html
```

This is important when applications parse incoming data.

---

# Content-Length

Indicates the size of the message body when applicable.

Example:

```http
Content-Length: 42
```

---

# Authorization

Carries authentication-related credentials.

Example:

```http
Authorization: Bearer <token>
```

This can be associated with:

```text
authentication
tokens
identity
access control
```

It becomes very important when studying authentication and authorization.

---

# Cookie

Cookies allow a client, commonly a browser, to send stored state to a server.

Example:

```http
Cookie: session=abc123
```

A common session flow is:

```text
Server
   ↓
Set-Cookie
   ↓
Browser stores cookie
   ↓
Browser sends Cookie
   ↓
Server identifies associated state/session
```

Cookies are therefore highly important for understanding web sessions.

---

# Set-Cookie

A server can send:

```http
Set-Cookie: session=abc123
```

in a response.

Conceptually:

```text
Server
   ↓
HTTP Response
   ↓
Set-Cookie
   ↓
Browser stores cookie
```

A later request can contain:

```http
Cookie: session=abc123
```

---

# Location

Used commonly with redirects.

Example:

```http
HTTP/1.1 302 Found
Location: /login
```

The client can use the `Location` value to determine where the redirect points.

---

# Referer

Can indicate the page or resource from which a request originated.

Example:

```http
Referer: https://example.com/account
```

It can be useful for analytics and application behavior.

Because it is part of an HTTP request, client-supplied values should not automatically be treated as trusted security controls.

---

# Origin

Indicates the origin associated with a request in contexts such as cross-origin requests.

Example:

```http
Origin: https://example.com
```

This becomes important later when studying:

```text
CORS
CSRF
browser security
same-origin policy
```

---

# Cache-Control

Controls caching behavior.

Example:

```http
Cache-Control: no-cache
```

Caching can affect application behavior and can become relevant to security and privacy.

---

# Client-Controlled HTTP Data

An important security observation is:

> The client controls a surprising amount of the HTTP request.

The client can provide or influence things such as:

```text
method
path
query parameters
headers
body
User-Agent
Cookie
Authorization
Origin
```

This does **not** mean the client should be trusted.

The server and application must enforce their own security rules.

This becomes a central idea in web security:

```text
Client input
      ↓
HTTP request
      ↓
Server/application
      ↓
validation
      ↓
authentication
      ↓
authorization
      ↓
business logic
```

---

# HTTP and Web Security

Web vulnerabilities often involve an interaction between:

```text
attacker-controlled input
        ↓
HTTP request
        ↓
application
        ↓
unexpected interpretation or behavior
        ↓
security impact
```

Therefore, understanding HTTP is not optional for serious web-security work.

Before learning specific vulnerabilities, you should be able to read a request and identify:

```text
method
path
query
headers
body
```

and read a response and identify:

```text
status
headers
body
```

---

# Browser / Web Server Model

A simplified architecture:

```text
                  Internet
                     |
                     ↓
                  Browser
                     |
                   HTTP
                     |
                     ↓
                Web Server
                     |
                     ↓
                Application
                     |
                     ↓
                  Database
```

A request may travel through several components before a response reaches the browser.

Later, this architecture can be expanded to include:

```text
Reverse Proxy
API
Cache
Database
Authentication
Authorization
Business Logic
```

The important idea for now is that HTTP is the communication layer connecting the client to the web application's server side.

---

# HTTP Over TCP

HTTP itself operates at the application layer.

A simplified relationship is:

```text
HTTP
 ↓
TCP
 ↓
IP
 ↓
Network Interface
```

This connects today's learning to Day 2.

On Day 2 you learned:

```text
Process
   ↓
Socket
   ↓
TCP
   ↓
IP
```

Now:

```text
Web application
   ↓
HTTP
   ↓
TCP
   ↓
IP
```

So the browser's HTTP request is carried through the lower-level networking stack you studied previously.

---

# HTTP Mental Model

When reading an HTTP request, ask:

```text
Who is the client?
      ↓
What method is being used?
      ↓
What resource is being requested?
      ↓
What path is being requested?
      ↓
Are there query parameters?
      ↓
What headers are present?
      ↓
Is there a body?
```

When reading the response, ask:

```text
What status was returned?
      ↓
What headers were returned?
      ↓
Is there a response body?
      ↓
What does the body contain?
```

---

# Security Questions

When examining an HTTP interaction, eventually ask:

### Who am I?

Authentication.

### What am I allowed to do?

Authorization.

### What can I control?

Input.

### Where does my input go?

Application flow.

### What does the application trust?

Trust boundaries.

### What happens when I violate assumptions?

Error handling.

### What data can I access?

Access control.

### What happens on the backend?

Backend/API behavior.

These questions are more valuable than memorizing isolated attack payloads.

---

# Practical HTTP Observation

A basic HTTP request can be observed with tools such as `curl`.

Example:

```bash
curl -v https://example.com
```

Verbose output can help reveal the HTTP request and response.

In `curl -v` output:

```text
>
```

generally marks request-related output.

```text
<
```

generally marks response-related output.

Another useful command:

```bash
curl -I https://example.com
```

This requests response headers without retrieving the normal response body.

---

# Local HTTP Lab

A local web server can be used for safe experimentation.

Start a server:

```bash
python3 -m http.server 8000
```

Then from another terminal:

```bash
curl -v http://127.0.0.1:8000
```

The basic flow becomes:

```text
curl
 ↓
TCP connection
 ↓
HTTP request
 ↓
local web server
 ↓
HTTP response
 ↓
curl
```

This allows both sides of the communication to be controlled during learning.

---

# Wireshark and HTTP

HTTP traffic can be observed using Wireshark when the traffic is visible to the selected capture interface.

For a local server bound to:

```text
127.0.0.1
```

the relevant interface is normally:

```text
lo
```

The conceptual sequence is:

```text
TCP connection
      ↓
HTTP request
      ↓
HTTP response
```

This connects:

```text
Day 2:
TCP / sockets
       ↓
Day 3:
HTTP
```

---

# HTTP Security Roadmap

HTTP fundamentals lead into:

```text
HTTP
 ↓
Web architecture
 ↓
Authentication
 ↓
Authorization
 ↓
Input handling
 ↓
Business logic
 ↓
Web security
```

Eventually this foundation is used for understanding areas such as:

```text
Broken Access Control
Injection
Authentication Failures
XSS
SQL Injection
IDOR
SSRF
API security
Business logic flaws
```

The correct order is to understand the underlying web communication before attempting vulnerability exploitation.

---

# Quick Reference

## Request

```text
Method
Path
Query
Headers
Body
```

## Response

```text
Status
Headers
Body
```

## Methods

```text
GET
POST
PUT
PATCH
DELETE
HEAD
OPTIONS
```

## Status categories

```text
1xx → Informational
2xx → Success
3xx → Redirection
4xx → Client/request problems
5xx → Server errors
```

## Important status codes

```text
200 → OK
201 → Created
204 → No Content

301 → Moved Permanently
302 → Found
304 → Not Modified

400 → Bad Request
401 → Unauthorized
403 → Forbidden
404 → Not Found
405 → Method Not Allowed
429 → Too Many Requests

500 → Internal Server Error
502 → Bad Gateway
503 → Service Unavailable
```

## Important headers

```text
Host
User-Agent
Accept
Content-Type
Content-Length
Authorization
Cookie
Set-Cookie
Location
Referer
Origin
Cache-Control
```

---

# Core Mental Model

```text
Browser / Client
       ↓
HTTP Request
       ↓
Web Server
       ↓
Application
       ↓
Database
       ↓
HTTP Response
       ↓
Browser / Client
```

And beneath HTTP:

```text
HTTP
 ↓
TCP
 ↓
IP
 ↓
Network Interface
```

The overall model from your first three days is now:

```text
Program
   ↓
Process
   ↓
Socket
   ↓
TCP
   ↓
IP
   ↓
HTTP
   ↓
Web Server
   ↓
Application
   ↓
Database
```

This is the foundation for understanding how web applications work before moving into web-security testing.

---

# HTTP — Practical Observation with curl and Wireshark

## Purpose

The goal of this section is to move from understanding HTTP theoretically to actually observing it.

Instead of only reading about:

```text
HTTP Request
HTTP Response
Headers
Status Codes
```

we use tools such as `curl` and Wireshark to observe what is actually exchanged between a client and a server.

The core idea is:

```text
Client
   ↓
TCP connection
   ↓
HTTP request
   ↓
Server
   ↓
HTTP response
   ↓
Client
```

This connects the HTTP layer learned on Day 3 with the TCP/socket concepts learned previously.

---

# 1. `curl`

`curl` is a command-line tool that can make network requests.

It is particularly useful for learning HTTP because it lets us make requests without relying on a graphical browser.

Instead of:

```text
Browser
   ↓
HTTP
```

we can explicitly perform:

```text
Terminal
   ↓
curl
   ↓
HTTP
```

This gives us more visibility and control over the request.

---

# 2. Verbose Mode: `curl -v`

Run:

```bash
curl -v https://example.com
```

The `-v` option enables verbose output.

The output can look complicated, but the important objective is to identify the request and response.

In verbose output:

```text
>
```

generally indicates request-related output.

```text
<
```

generally indicates response-related output.

A request may look conceptually like:

```http
> GET / HTTP/1.1
> Host: example.com
> User-Agent: curl/...
> Accept: */*
```

A response may look conceptually like:

```http
< HTTP/...
< Content-Type: ...
< ...
<
<html>...
```

The exact headers and values returned can vary.

---

# 3. Reading a Request with `curl -v`

When looking at a verbose request, identify:

```text
Method
Path
Headers
Body, if present
```

For example:

```http
GET / HTTP/1.1
Host: example.com
User-Agent: curl/...
Accept: */*
```

Breakdown:

```text
GET
 ↓
method

/
 ↓
path

Host: example.com
 ↓
target host

User-Agent: ...
 ↓
client information

Accept: */*
 ↓
acceptable response type
```

This is the same HTTP structure studied previously, but now it is being observed directly.

---

# 4. Reading a Response with `curl -v`

When reading the response, identify:

```text
Status code
Response headers
Response body
```

Example:

```http
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: ...

<html>...
```

Breakdown:

```text
200 OK
 ↓
status

Content-Type
 ↓
response metadata

Content-Length
 ↓
body-size information

<html>...
 ↓
response body
```

The important habit is:

> Read the request and response structurally rather than treating verbose output as random terminal text.

---

# 5. `curl -I`

Run:

```bash
curl -I https://example.com
```

This performs a `HEAD` request.

The purpose is to retrieve response headers without the normal response body.

Compare:

```bash
curl https://example.com
```

with:

```bash
curl -I https://example.com
```

Conceptually:

```text
GET
 ↓
request a resource and normally receive its body
```

while:

```text
HEAD
 ↓
request the response headers without the normal body
```

This makes `curl -I` useful for examining response metadata.

Look for headers such as:

```text
Content-Type
Content-Length
Location
Cache-Control
Server
```

---

# 6. HTTP and HTTPS

Compare:

```bash
curl -v http://example.com
```

with:

```bash
curl -v https://example.com
```

At a high level:

```text
HTTP
 ↓
HTTP communication over the network

HTTPS
 ↓
HTTP protected using TLS
```

The important observation for this stage is not the details of TLS.

The goal is to recognize that HTTPS changes how HTTP data is protected while travelling across the network.

---

# 7. Observing Redirects

When accessing an HTTP resource, the server may return a redirect.

Conceptually:

```text
Client
   ↓
HTTP request
   ↓
Server
   ↓
3xx response
   ↓
Location header
   ↓
Client requests another location
```

Example:

```http
HTTP/1.1 302 ...
Location: https://example.com/
```

Important pieces:

```text
302
 ↓
redirect status

Location
 ↓
destination
```

When using:

```bash
curl -v http://example.com
```

pay attention to whether the response contains a `3xx` status and a `Location` header.

The exact redirect behavior depends on the server.

---

# 8. `curl -X`

You can explicitly specify the HTTP method with:

```bash
curl -v -X GET https://example.com
```

Here:

```text
-X
 ↓
choose the request method

GET
 ↓
method
```

This demonstrates that the HTTP method is part of the request and can be deliberately selected by the client.

At this stage, the purpose is observation rather than exploitation.

---

# 9. Changing HTTP Headers

One of the most important practical observations is that the client can control many parts of the HTTP request.

The `-H` option allows a header to be supplied.

Example:

```bash
curl -v -H "User-Agent: CyberLab" https://example.com
```

The resulting request can contain:

```http
User-Agent: CyberLab
```

Compare this with the normal request from `curl`.

The important observation is:

> The client can supply its own header values.

This is a foundational security concept because applications should not blindly trust client-controlled data.

---

# 10. Changing `Accept`

Try:

```bash
curl -v -H "Accept: application/json" https://example.com
```

This sends:

```http
Accept: application/json
```

The client is expressing that it can accept a JSON representation.

This becomes particularly useful when working with APIs and applications that support different response formats.

The broader lesson is:

```text
Client
   ↓
controls request fields
   ↓
Server
   ↓
interprets those fields
```

---

# 11. Client-Controlled Data

A client can influence many parts of an HTTP request, including:

```text
Method
URL
Path
Query parameters
Headers
Body
```

Examples of client-supplied headers include:

```text
User-Agent
Accept
Cookie
Authorization
Origin
```

This leads to an important security principle:

> **Anything supplied by the client should be treated as potentially untrusted input unless the application has a reason and mechanism to validate it.**

The client can say:

```http
User-Agent: CyberLab
```

but that does not mean the server should treat:

```text
CyberLab
```

as a trusted identity.

Likewise, the client may provide other values that the application must validate and interpret correctly.

---

# 12. Why Client Control Matters to Security

The practical observation is:

```text
Client controls request
        ↓
Request reaches server
        ↓
Application interprets request
        ↓
Application makes decisions
```

Security problems can occur when an application makes unsafe assumptions about that input.

A useful security model is:

```text
Client-controlled input
        ↓
HTTP request
        ↓
Validation
        ↓
Authentication
        ↓
Authorization
        ↓
Business logic
        ↓
Response
```

This does not mean that every client-controlled field is automatically dangerous.

The key idea is that **the server must enforce its own rules**.

---

# 13. Build a Local HTTP Lab

One of the best ways to learn networking is to control both endpoints.

Start a simple local HTTP server:

```bash
python3 -m http.server 8000
```

This starts a Python HTTP server listening on port `8000`.

Then, from another terminal:

```bash
curl -v http://127.0.0.1:8000
```

Now both sides are under your control:

```text
curl
 ↓
127.0.0.1:8000
 ↓
Python HTTP server
```

This makes the environment excellent for experimentation because there is no need to depend on the behavior of a third-party server.

---

# 14. Why `127.0.0.1`?

`127.0.0.1` is the IPv4 loopback address.

Traffic sent to it stays on the local host.

The corresponding interface is normally:

```text
lo
```

So:

```text
127.0.0.1:8000
```

means:

```text
local machine
+
port 8000
```

This is why the local lab is particularly useful for learning.

---

# 15. Connecting This to Day 2

Previously we observed:

```text
Python HTTP server
      ↓
Process
      ↓
PID
      ↓
File Descriptor
      ↓
Socket
      ↓
TCP
      ↓
127.0.0.1:8000
```

Now we have a client:

```text
curl
      ↓
HTTP request
      ↓
TCP connection
      ↓
127.0.0.1:8000
      ↓
Python HTTP server
```

Put both together:

```text
curl
 ↓
HTTP
 ↓
TCP
 ↓
Socket
 ↓
Server Process
```

This is the connection between the Linux/process concepts from Day 2 and the web concepts from Day 3.

---

# 16. HTTP Request Over TCP

At a simplified networking level:

```text
HTTP
 ↓
TCP
 ↓
IP
 ↓
Network Interface
```

For a local HTTP connection:

```text
HTTP request
     ↓
TCP connection
     ↓
127.0.0.1
     ↓
loopback interface
```

Before HTTP data can normally be exchanged over TCP, TCP establishes its connection.

Conceptually:

```text
SYN
 ↓
SYN-ACK
 ↓
ACK
 ↓
HTTP request
 ↓
HTTP response
```

Therefore, HTTP is operating on top of the lower-level networking mechanisms you have already studied.

---

# 17. Wireshark

Wireshark allows network traffic to be captured and examined.

For the local server:

```text
127.0.0.1
```

capture on the loopback interface:

```text
lo
```

Then generate traffic:

```bash
curl http://127.0.0.1:8000
```

The target sequence is:

```text
TCP connection
      ↓
HTTP request
      ↓
HTTP response
```

This lets you see the relationship between the transport layer and the application layer.

---

# 18. What to Look for in Wireshark

When observing the local request, don't try to understand every field.

Focus on the communication sequence.

Look for:

```text
SYN
SYN-ACK
ACK
```

Then:

```text
HTTP request
```

Then:

```text
HTTP response
```

Finally, the TCP connection may be closed.

So the overall sequence is:

```text
1. TCP connection establishment
2. HTTP request
3. HTTP response
4. TCP connection termination
```

---

# 19. Wireshark Mental Model

When you inspect a packet, think in layers:

```text
Network Interface
       ↓
IP
       ↓
TCP
       ↓
HTTP
```

The packet you observe isn't just "an HTTP packet."

It is better understood as a stack of protocols.

For example:

```text
Ethernet / Link Layer
       ↓
IP
       ↓
TCP
       ↓
HTTP
```

The exact lower-layer details depend on the environment and capture interface.

---

# 20. HTTP vs HTTPS in Wireshark

A major practical difference is visibility.

For ordinary HTTP:

```text
HTTP
 ↓
TCP
```

the HTTP content may be visible directly in a packet capture.

For HTTPS:

```text
HTTP
 ↓
TLS
 ↓
TCP
```

the HTTP application data is protected by TLS during transmission.

Therefore, the HTTP request itself is not normally exposed as readable plaintext in the network capture.

At this stage, the important thing is simply understanding the layering:

```text
HTTP
 ↓
TLS
 ↓
TCP
```

---

# 21. Local Lab Experiment

A useful sequence is:

### Terminal 1

```bash
python3 -m http.server 8000
```

### Terminal 2

```bash
curl -v http://127.0.0.1:8000
```

### Wireshark

Capture on:

```text
lo
```

Then observe:

```text
TCP handshake
      ↓
HTTP request
      ↓
HTTP response
```

This is one of the most valuable experiments of the session because it combines several concepts you have learned separately.

---

# 22. What `curl` Is Teaching You

`curl` is not just a convenience tool.

It gives you an explicit way to think about HTTP as data being exchanged.

You can manipulate:

```text
method
headers
URL
path
query
```

and observe:

```text
status
headers
response body
redirects
```

This starts developing the habit of reading HTTP traffic as a security researcher would.

Instead of seeing:

```text
"the website loaded"
```

you begin seeing:

```text
request
 ↓
server processing
 ↓
response
```

---

# 23. Practical Security Mindset

When examining any HTTP request, ask:

```text
What is the client sending?
        ↓
Which parts are client-controlled?
        ↓
What does the server do with them?
        ↓
What assumptions is the server making?
        ↓
What does the response reveal?
```

This mindset is more important than memorizing a collection of payloads.

Eventually, the same approach will be applied to:

```text
authentication
authorization
sessions
APIs
input validation
business logic
```

---

# 24. Important Observations from This Session

## Observation 1 — HTTP is visible

With `curl -v`, the request and response can be inspected directly.

```text
Client
 ↓
HTTP Request
 ↓
Server
 ↓
HTTP Response
```

---

## Observation 2 — HTTP is structured

A request isn't just text.

It contains meaningful components:

```text
Method
Path
Headers
Body
```

A response contains:

```text
Status
Headers
Body
```

---

## Observation 3 — The client has significant control

The client can construct many request fields.

For example:

```bash
curl -H "User-Agent: CyberLab" ...
```

This demonstrates that request headers can be supplied by the client.

---

## Observation 4 — HTTP depends on the lower network stack

The request does not magically reach the server.

The conceptual chain is:

```text
HTTP
 ↓
TCP
 ↓
IP
 ↓
Interface
```

---

## Observation 5 — HTTPS changes visibility

HTTP:

```text
HTTP
 ↓
TCP
```

HTTPS:

```text
HTTP
 ↓
TLS
 ↓
TCP
```

TLS protects the HTTP data while it is being transmitted.

---

# 25. Important Commands

### Verbose request

```bash
curl -v https://example.com
```

### HEAD request

```bash
curl -I https://example.com
```

### Explicit GET

```bash
curl -v -X GET https://example.com
```

### Custom User-Agent

```bash
curl -v -H "User-Agent: CyberLab" https://example.com
```

### Custom Accept header

```bash
curl -v -H "Accept: application/json" https://example.com
```

### Local server

```bash
python3 -m http.server 8000
```

### Local request

```bash
curl -v http://127.0.0.1:8000
```

---

# 26. Questions for Revision

Try to answer these without looking at the notes.

### `curl`

1. What does `curl -v` show?
2. What do `>` and `<` generally indicate in verbose output?
3. What does `curl -I` do?
4. Why might `HEAD` be useful?

### Requests

5. What parts of an HTTP request can the client control?
6. What does `-H` do?
7. Why should client-supplied headers not automatically be trusted?

### Redirects

8. What is a redirect?
9. Which status-code family represents redirects?
10. Which header commonly tells the client where to go?

### Local server

11. Why is `127.0.0.1` useful for the lab?
12. What interface normally handles `127.0.0.1` traffic?
13. What happens when `curl` connects to `127.0.0.1:8000`?

### Wireshark

14. What happens before the HTTP request?
15. What does the TCP handshake look like?
16. What comes after the HTTP request?
17. Why can ordinary HTTP be visible in a capture while HTTPS protects the HTTP data?

---

# 27. Complete Mental Model

The most important model from this session is:

```text
User
 ↓
curl
 ↓
HTTP Request
 ├── Method
 ├── Path
 ├── Query
 ├── Headers
 └── Body
      ↓
     TCP
      ↓
      IP
      ↓
Network Interface
      ↓
Server
      ↓
Application
      ↓
HTTP Response
 ├── Status
 ├── Headers
 └── Body
```

For your local lab:

```text
curl
 ↓
HTTP
 ↓
TCP
 ↓
127.0.0.1:8000
 ↓
Python HTTP server
 ↓
HTTP response
 ↓
curl
```

---

# Security Mental Model

The most important security lesson from this session is:

> **The client constructs the request, but the server is responsible for enforcing security.**

Therefore:

```text
Client-controlled input
        ↓
HTTP request
        ↓
Server
        ↓
Application
        ↓
Security checks
        ↓
Business logic
        ↓
Response
```

This is the foundation for the next stages of your roadmap.

You are not learning random `curl` commands.

You are learning to **see HTTP as an attack surface**.

---

# Session 2 Checkpoint

You have completed the practical foundation when you can:

```text
curl -v
   ↓
read request
   ↓
read response
```

and:

```text
curl -H ...
   ↓
change request
   ↓
observe what changed
```

and:

```text
local HTTP server
   ↓
curl
   ↓
Wireshark
   ↓
TCP handshake
   ↓
HTTP request
   ↓
HTTP response
```

At that point, the progression becomes:

```text
HTTP theory
     ↓
HTTP observation
     ↓
HTTP programming
     ↓
httppeek
     ↓
web architecture
     ↓
Burp Suite
     ↓
web security testing
```

---

# Web Architecture & Security Thinking

## Why This Matters

Understanding HTTP syntax is only the beginning of web security.

A browser sends an HTTP request, but that request may pass through several layers before the application's business logic processes it.

A simplified model is:

```text
Browser
   ↓
HTTP
   ↓
Reverse Proxy
   ↓
Web Application
   ↓
Database
```

The goal is to understand:

- what each component does
- where application decisions happen
- where authentication happens
- where authorization happens
- where user-controlled input goes
- what the application trusts
- how business logic processes requests

This creates the foundation for later web-security testing.

---

# 1. Web Application Architecture

A simplified web architecture can look like:

```text
                    Internet
                        |
                        ↓
                     Browser
                        |
                      HTTP
                        |
                        ↓
                  Reverse Proxy
                        |
                        ↓
                  Web Application
                   /      |      \
                  ↓       ↓       ↓
             Database   Cache     API
```

This is a conceptual model.

Not every real application has exactly these components or exactly this arrangement.

The purpose of the model is to give a mental map for understanding where requests travel and where security decisions may occur.

---

# 2. Browser

The browser is the client-side environment through which users interact with web applications.

At an introductory level, important browser concepts include:

```text
HTML
JavaScript
Cookies
DOM
Same-Origin Policy
Local Storage
Session Storage
```

The browser receives content from the server and interprets it.

A simplified model is:

```text
Server
   ↓
HTML + JavaScript + other resources
   ↓
Browser
   ↓
User interaction
   ↓
Additional HTTP requests
```

Modern web applications can therefore involve many HTTP requests rather than a single request for a single page.

---

# 3. HTML

HTML defines the structure of web content.

Example:

```html
<h1>Hello</h1>
<p>Welcome.</p>
```

The browser parses HTML and turns it into structures that it can display and work with.

Conceptually:

```text
HTML
 ↓
Browser parses HTML
 ↓
Rendered document
```

HTML becomes security-relevant because applications may place user-controlled data into HTML content.

For now, the important idea is simply:

> HTML is part of the content that the browser receives and interprets.

---

# 4. JavaScript

JavaScript provides client-side program logic.

A browser can execute JavaScript to perform tasks such as:

- respond to user actions
- modify page content
- interact with the DOM
- communicate with servers
- make additional HTTP requests
- manage application behavior

A simplified flow:

```text
Server
   ↓
HTML + JavaScript
   ↓
Browser
   ↓
JavaScript executes
   ↓
Additional requests / page changes
```

JavaScript is therefore another major part of the browser-side web environment.

---

# 5. DOM

DOM stands for:

> Document Object Model

The browser creates a representation of a document that scripts can interact with.

Conceptually:

```text
HTML
 ↓
Browser parses document
 ↓
DOM
 ↓
JavaScript interacts with DOM
```

For example:

```html
<p id="message">Hello</p>
```

The browser represents this document structure internally so that JavaScript can interact with it.

For now, the important idea is:

> The browser does not merely display HTML as raw text. It creates a document model that scripts can work with.

---

# 6. Cookies

Cookies provide a mechanism for storing client-side state associated with a website.

A common flow is:

```text
Server
   ↓
Set-Cookie
   ↓
Browser stores cookie
   ↓
Later request
   ↓
Cookie
   ↓
Server
```

Example response:

```http
Set-Cookie: session=abc123
```

Later request:

```http
Cookie: session=abc123
```

Cookies are commonly used for maintaining application state and sessions.

This creates an important chain:

```text
HTTP
 ↓
Cookie
 ↓
Session state
 ↓
Authentication
```

Cookies therefore become very important when studying web authentication.

---

# 7. Local Storage

Local Storage is browser-side storage available to web applications.

Conceptually:

```text
Web Application
      ↓
Browser
      ↓
Local Storage
```

It differs from cookies in an important practical way:

> Data stored in Local Storage is not automatically attached to every HTTP request in the way cookies can be.

At this stage, remember its architectural role rather than studying its security properties deeply.

---

# 8. Session Storage

Session Storage is another browser-side storage mechanism.

A simplified comparison:

```text
Local Storage
→ browser-side persistent storage

Session Storage
→ browser-side storage associated with a browser session/tab context
```

These mechanisms allow client-side applications to maintain state locally.

---

# 9. Same-Origin Policy

The Same-Origin Policy is a fundamental browser security mechanism.

At a high level:

> It restricts how scripts associated with one origin can interact with resources associated with another origin.

An origin is associated with:

```text
scheme
host
port
```

For example:

```text
https://example.com:443
```

and:

```text
http://example.com:80
```

represent different origins because the scheme and port differ.

Conceptually:

```text
Origin A
   ↓
JavaScript
   ↓
Browser security rules
   ↓
Can it interact with Origin B?
```

The important idea is:

> Browsers place security restrictions around cross-origin interactions.

This will matter later when learning concepts such as:

```text
CORS
CSRF
cross-origin requests
browser security
```

Do not try to master those topics yet.

---

# 10. Reverse Proxy

A reverse proxy sits between clients and backend applications.

Simplified:

```text
Browser
   ↓
HTTP
   ↓
Reverse Proxy
   ↓
Application
```

A reverse proxy can receive incoming requests and forward them to backend services.

The important security lesson is:

> The component receiving an HTTP request may not be the component containing the actual application logic.

A request can therefore pass through infrastructure before it reaches the application.

Conceptually:

```text
Client
 ↓
Reverse Proxy
 ↓
Application
```

This becomes relevant when interpreting:

- routing
- headers
- redirects
- errors
- authentication behavior
- backend responses

---

# 11. Web Application

The web application contains the logic that processes requests and performs the application's intended operations.

A simplified flow is:

```text
Request
   ↓
Routing
   ↓
Authentication
   ↓
Authorization
   ↓
Business Logic
   ↓
Database
   ↓
Response
```

This flow is one of the most important security models to remember.

---

# 12. Routing

Routing determines which application component should handle a request.

For example:

```http
GET /login
```

might be routed to a login handler.

Another request:

```http
GET /profile
```

might be routed to a profile handler.

Conceptually:

```text
HTTP Request
      ↓
Path
      ↓
Router
      ↓
Application handler
```

This is one reason application endpoints become important during security testing.

---

# 13. Authentication

Authentication answers:

> **Who am I?**

It is the process by which the application determines an identity associated with a request.

Examples can include:

```text
username + password
session cookie
token
```

Conceptually:

```text
Request
   ↓
Authentication
   ↓
Identity
```

For example:

```text
Request
   ↓
authentication
   ↓
Alice
```

The application may now associate the request with Alice's account.

---

# 14. Authorization

Authorization answers:

> **What am I allowed to do?**

It is different from authentication.

Authentication:

```text
Who are you?
```

Authorization:

```text
What are you allowed to do?
```

Example:

```text
Authentication
      ↓
You are Alice.

Authorization
      ↓
Alice may view her profile.
Alice may not access administrative functions.
```

The distinction can be visualized as:

```text
Identity
   ↓
Authentication
   ↓
Who is the user?

Permission
   ↓
Authorization
   ↓
What can the user do?
```

This distinction is fundamental to understanding access-control security.

---

# 15. Authentication vs Authorization

Keep this distinction extremely clear:

```text
Authentication
→ establishes identity

Authorization
→ determines permissions
```

A user can be successfully authenticated while still being unauthorized to perform a particular action.

For example:

```text
Alice logs in successfully
        ↓
Authentication succeeds
        ↓
Application knows Alice's identity
        ↓
Alice requests admin operation
        ↓
Authorization check
        ↓
Allowed or denied
```

Authentication alone is not permission.

---

# 16. Business Logic

Business logic is the set of rules that implement what the application is actually supposed to do.

Examples include:

```text
create an account
place an order
transfer money
upload a file
change a profile
create a post
delete a resource
```

Conceptually:

```text
Request
   ↓
Authentication
   ↓
Authorization
   ↓
Business Logic
   ↓
Result
```

Business logic is important because an application can have technically valid code while still implementing an unsafe rule.

The key security question is:

> What assumptions does the application make while performing an operation?

---

# 17. Database

The application may use a database to store persistent information.

Examples of stored information might include:

```text
users
profiles
orders
messages
accounts
```

A simplified flow:

```text
HTTP Request
      ↓
Application
      ↓
Database operation
      ↓
Database result
      ↓
Application
      ↓
HTTP Response
```

This means user-controlled HTTP input can sometimes travel through application logic and eventually influence database operations.

At this point, the important thing is understanding the **data flow**.

Do not study injection techniques yet.

---

# 18. API

An API is an interface through which software components communicate.

A modern application may use HTTP APIs between the browser and backend services.

For example:

```text
Browser
   ↓
HTTP
   ↓
API
   ↓
Backend
```

A frontend might request:

```text
/api/profile
/api/orders
/api/users
```

The backend then processes the request.

Conceptually:

```text
Browser
   ↓
API
   ↓
Application logic
   ↓
Database
```

The API may therefore be another important boundary for authentication, authorization, input handling, and business logic.

---

# 19. Cache

A cache stores information so it can be retrieved more efficiently.

A simplified architecture is:

```text
Application
    |
    ↓
  Cache
    |
    ↓
Database
```

A cache can reduce the need to retrieve information repeatedly from the database.

For now, remember:

> A cache is another component that can influence how a web application behaves.

Its security implications can be studied later.

---

# 20. The Complete Server-Side Flow

Put the major concepts together:

```text
HTTP Request
      ↓
Reverse Proxy
      ↓
Routing
      ↓
Authentication
      ↓
Authorization
      ↓
Business Logic
      ↓
API / Cache / Database
      ↓
HTTP Response
```

This is a conceptual flow rather than a strict requirement for every application.

The value of the model is that it gives you places to ask security questions.

---

# 21. The Hacker's Questions

When looking at a web application, eventually you want to ask:

```text
Who am I?

What am I allowed to do?

What can I control?

Where does my input go?

What does the application trust?

What happens when I violate assumptions?

What data can I access?

What happens on the other side of the API?
```

These are investigation questions.

They are more valuable than memorizing isolated attack payloads.

---

# 22. Question 1 — Who Am I?

This is the authentication question.

```text
Who am I?
    ↓
Authentication
    ↓
Identity
```

You want to understand how the application associates a request with an identity.

Possible mechanisms include:

```text
credentials
sessions
cookies
tokens
```

The exact mechanism depends on the application.

---

# 23. Question 2 — What Am I Allowed to Do?

This is the authorization question.

```text
Who am I?
    ↓
What permissions do I have?
    ↓
What resources/actions are allowed?
```

For example:

```text
User
 ↓
regular account
 ↓
view own data
 ↓
cannot perform administrative actions
```

This is fundamentally about permissions.

---

# 24. Question 3 — What Can I Control?

This is the input question.

A client can influence many parts of an HTTP request.

For example:

```text
URL
Path
Query parameters
Headers
Cookies
Authorization data
Body
```

Conceptually:

```text
Client-controlled input
        ↓
HTTP Request
        ↓
Application
```

This is one of the foundations of web security.

---

# 25. Question 4 — Where Does My Input Go?

Finding where data travels through the application is extremely important.

Suppose the request contains:

```text
name=Alice
```

That input might travel through:

```text
HTTP Request
      ↓
Router
      ↓
Application
      ↓
Business Logic
      ↓
Database
```

Or:

```text
HTTP Request
      ↓
Application
      ↓
HTML Response
```

Or:

```text
HTTP Request
      ↓
API
      ↓
Another backend service
```

The important question is:

> What does the application eventually do with this value?

---

# 26. Question 5 — What Does the Application Trust?

A web client can supply many values.

For example:

```http
User-Agent: CyberLab
```

The server receives this value from the client.

The application should not automatically treat client-supplied information as trustworthy.

Conceptually:

```text
Untrusted Client
      ↓
HTTP Request
      ↓
Trust Boundary
      ↓
Application
```

Security decisions should be enforced by the server/application rather than relying on the client's cooperation.

---

# 27. Question 6 — What Happens When I Violate Assumptions?

Applications are designed around assumptions.

For example:

```text
username should be a valid identifier
age should be numeric
user should access only permitted resources
request should contain required fields
```

A useful investigation question is:

> What happens when those assumptions are not satisfied?

The application might:

```text
reject the request
return an error
return a 4xx response
handle the condition incorrectly
produce unexpected behavior
```

This is closely connected to exceptional-condition handling and application robustness.

---

# 28. Question 7 — What Data Can I Access?

This is closely related to access control.

Conceptually:

```text
Identity
   ↓
Requested resource
   ↓
Permission check
   ↓
Allow / deny
```

The important question is:

> Does the application correctly enforce which resources a particular user may access?

This will become very important when studying Broken Access Control.

For now, do not try to exploit it.

Understand the architecture.

---

# 29. Question 8 — What Happens on the Other Side of the API?

A frontend is not necessarily the entire application.

A browser may communicate with an API:

```text
Browser
   ↓
HTTP
   ↓
API
   ↓
Backend
```

The backend may then communicate with:

```text
database
cache
other services
```

Therefore:

> A visible webpage may only be one part of a much larger application.

This is important when thinking about application architecture and future reconnaissance.

---

# 30. Trust Boundaries

A trust boundary is a conceptual boundary between components or contexts that should not automatically trust one another.

For web applications:

```text
Client
  ↓
HTTP
  ↓
Server
```

The client is under the user's control.

The server therefore needs to treat incoming data appropriately.

Another example:

```text
Browser
   ↓
API
   ↓
Backend service
```

Each component may have different responsibilities and trust assumptions.

The key mindset is:

> **Ask what each component assumes about the data it receives.**

---

# 31. Client vs Server Responsibility

A useful distinction:

```text
Client
→ sends requests

Server
→ enforces application rules
```

The client can provide:

```text
method
path
query
headers
body
```

But it should not be responsible for enforcing its own permissions.

For example, a client saying:

```text
I am an administrator
```

does not make the user an administrator.

The server must determine the identity and permissions according to its own trusted mechanisms.

---

# 32. Input Flow

A useful general model is:

```text
Client
   ↓
HTTP Request
   ↓
Input
   ↓
Application
   ↓
Validation
   ↓
Authentication
   ↓
Authorization
   ↓
Business Logic
   ↓
Backend
   ↓
HTTP Response
```

The exact order may differ between applications.

The important thing is to understand that data can travel through multiple layers.

---

# 33. Why Input Matters

A web application accepts data from clients because that's how users interact with it.

Examples:

```text
login credentials
search terms
profile information
file uploads
IDs
URLs
API parameters
```

The application then interprets that data.

Security problems can arise when the application interprets attacker-controlled input in an unsafe way.

This is why the basic model:

```text
Input
 ↓
Application
 ↓
Unexpected behavior
 ↓
Security impact
```

is so important.

---

# 34. Business Logic Security

Not every security problem involves memory corruption or a malformed packet.

An application can have a perfectly valid request and still make a bad decision.

For example, conceptually:

```text
User
 ↓
legitimate request
 ↓
application
 ↓
incorrect business rule
 ↓
undesired result
```

This is why understanding what the application is **supposed to do** matters.

Business logic security asks questions about application assumptions and rules.

---

# 35. Web Security as Data Flow

A useful way to think about web vulnerabilities is as data-flow problems.

```text
Input
  ↓
Processing
  ↓
Decision
  ↓
Action
```

More specifically:

```text
HTTP input
   ↓
Application
   ↓
Validation
   ↓
Authentication
   ↓
Authorization
   ↓
Business logic
   ↓
Database / API / output
```

When studying a vulnerability later, ask:

```text
Where did the input originate?
Where did it travel?
How was it interpreted?
What security checks were performed?
What did the application eventually do?
```

---

# 36. Authentication and Authorization in the Architecture

A common misconception is that:

```text
login successful
    =
everything is allowed
```

That is incorrect.

The architecture is better represented as:

```text
Request
   ↓
Authentication
   ↓
Identity
   ↓
Authorization
   ↓
Permission decision
   ↓
Business operation
```

Successful authentication establishes identity.

Authorization determines whether that identity may perform the requested action.

---

# 37. HTTP Headers and Trust

You learned earlier that a client can supply headers.

Examples:

```text
User-Agent
Cookie
Authorization
Origin
```

This means:

```text
Client
 ↓
Header
 ↓
Server
```

A header's presence does not automatically make its contents trustworthy.

The application must determine:

```text
Which values are security-sensitive?
Which values can be modified by the client?
Which values must be validated?
```

This is particularly important for authentication and authorization.

---

# 38. A Request Through the Whole Architecture

Take this example:

```http
GET /profile?id=42 HTTP/1.1
Host: example.com
Cookie: session=abc123
```

Think about the request like this:

```text
Browser
   ↓
HTTP request
   ↓
Reverse Proxy
   ↓
Routing
   ↓
Authentication
   ↓
Authorization
   ↓
Business Logic
   ↓
Database
   ↓
HTTP Response
```

Now ask:

```text
Who is the user?
What resource are they requesting?
Why should they be allowed to access it?
Where does id=42 go?
What does the session identify?
What happens if the requested resource belongs to another user?
```

Again, we're not exploiting anything.

We're learning how to think about the request.

---

# 39. A Request With an API

Imagine:

```http
GET /api/profile HTTP/1.1
Host: example.com
Authorization: Bearer <token>
```

Conceptually:

```text
Browser
   ↓
HTTP
   ↓
API
   ↓
Authentication
   ↓
Authorization
   ↓
Business Logic
   ↓
Database
   ↓
JSON response
```

The important observation is that the visible browser interface may only be the front end of a much larger system.

---

# 40. Security Questions as a Workflow

When examining an application, think:

```text
1. What is the request?

2. Who is making it?

3. What identity is associated with it?

4. What can the client control?

5. What resource/action is being requested?

6. What authorization decision should happen?

7. Where does the input go?

8. What does the application trust?

9. What business logic is executed?

10. What does the response reveal?
```

This is an investigation framework rather than a list of attacks.

---

# 41. OWASP Connection

The Day 3 roadmap uses the OWASP Top 10:2025 as its current reference.

The areas highlighted for the later learning path include:

```text
Broken Access Control
Injection
Authentication Failures
```

The broader 2025 list in the study plan also includes:

```text
Security Misconfiguration
Software Supply Chain Failures
Cryptographic Failures
Insecure Design
Software/Data Integrity Failures
Logging & Alerting Failures
Mishandling of Exceptional Conditions
```

The important thing for this session is not memorizing the entire list.

The goal is seeing how today's architectural concepts eventually connect to security categories.

---

# 42. From Architecture to Vulnerabilities

Your learning path is intentionally:

```text
HTTP
 ↓
Web Architecture
 ↓
Authentication
 ↓
Authorization
 ↓
Input
 ↓
Injection
 ↓
Business Logic
 ↓
Real Vulnerabilities
```

The dependency matters.

For example, to understand an authorization vulnerability, you first need to understand:

```text
identity
 ↓
permissions
 ↓
resource
 ↓
authorization decision
```

To understand an injection vulnerability, you need to understand:

```text
input
 ↓
application
 ↓
interpretation
 ↓
backend
```

The goal is to understand the underlying mechanism instead of memorizing payloads.

---

# 43. The Most Important Mental Model

Keep this model in your head:

```text
                   INTERNET
                       |
                       ↓
                    Browser
                       |
                     HTTP
                       |
                       ↓
                  Reverse Proxy
                       |
                       ↓
                  Web Application
                       |
            ┌──────────┼──────────┐
            ↓          ↓          ↓
       Authentication Authorization Business Logic
            |          |          |
            └──────────┼──────────┘
                       ↓
                  API / Cache
                       |
                       ↓
                    Database
                       |
                       ↓
                  HTTP Response
```

This is not a literal implementation of every website.

It is your **security map**.

---

# 44. The Full Data-Flow Model

Another useful model is:

```text
Client
  ↓
Request
  ↓
Input
  ↓
Server
  ↓
Authentication
  ↓
Authorization
  ↓
Business Logic
  ↓
Backend Systems
  ↓
Response
  ↓
Client
```

At every stage ask:

```text
What data is moving?
Who controls it?
What is trusted?
What is validated?
What decision is being made?
```

---

# 45. Security Researcher Mindset

A beginner often asks:

```text
"What payload should I try?"
```

A stronger approach begins with:

```text
"What does this application do?"
```

Then:

```text
Who am I?
What can I do?
What can I control?
Where does my input go?
What does the application trust?
What assumptions does it make?
What happens when those assumptions change?
What data can I access?
```

This leads to understanding instead of memorization.

---

# 46. What We Are NOT Doing Yet

Do not jump directly into:

```text
SQL Injection
XSS
IDOR
SSRF
Burp attacks
Payload collections
```

The purpose of this session is to understand the architecture that makes those vulnerabilities meaningful.

The Day 3 plan deliberately postpones vulnerability exploitation until after the HTTP and architecture foundations are established.

---

# 47. Revision Examples

## Example 1 — Profile Request

```http
GET /profile?id=42 HTTP/1.1
Host: example.com
Cookie: session=abc123
```

Ask:

```text
Method?
GET

Path?
/profile

Query?
id=42

Authentication/session data?
Cookie

What identity does the session represent?

What resource is being requested?

What authorization check should happen?

Where does id=42 go?
```

---

## Example 2 — API Request

```http
GET /api/orders HTTP/1.1
Host: example.com
Authorization: Bearer <token>
```

Think:

```text
Browser
 ↓
API
 ↓
Authentication
 ↓
Authorization
 ↓
Business Logic
 ↓
Database
 ↓
JSON response
```

---

## Example 3 — Client-Controlled Header

```http
User-Agent: CyberLab
```

Ask:

```text
Who supplied this?
```

Answer:

```text
The client.
```

Then ask:

```text
Should the server treat it as a trusted identity?
```

Answer:

```text
No automatic assumption of trust.
```

---

# 48. Core Definitions

### Browser

Client-side software used to interact with web applications.

### Web Server

Server-side infrastructure that receives and responds to web requests.

### Reverse Proxy

An intermediary that receives client requests and forwards them to backend systems.

### Application

Software implementing the application's behavior and business logic.

### Database

A system used to store and retrieve persistent application data.

### API

An interface through which software components communicate.

### Cache

A component that stores data for more efficient retrieval.

### Authentication

Determining or establishing the identity associated with a request.

### Authorization

Determining what an authenticated identity is allowed to access or perform.

### Business Logic

The rules and operations implementing what the application is designed to do.

### Trust Boundary

A conceptual boundary across which data should not automatically be trusted.

---

# 49. Quick Comparison

```text
Authentication
→ Who are you?

Authorization
→ What are you allowed to do?

Input
→ What can the client control?

Routing
→ Which application component handles the request?

Business Logic
→ What operation does the application perform?

Database
→ Where can persistent application data be stored?

API
→ How can software components communicate?

Reverse Proxy
→ What intermediary receives and forwards requests?

Browser
→ Where client-side web behavior occurs?
```

---

# 50. Final Mental Model

When you encounter a web application, visualize:

```text
                    USER
                     |
                     ↓
                  BROWSER
                     |
                     | HTTP Request
                     ↓
               REVERSE PROXY
                     |
                     ↓
                  ROUTING
                     |
                     ↓
              AUTHENTICATION
                     |
                     ↓
              AUTHORIZATION
                     |
                     ↓
               BUSINESS LOGIC
                     |
            ┌────────┼────────┐
            ↓        ↓        ↓
           API     CACHE   DATABASE
            |                 |
            └────────┬────────┘
                     ↓
                HTTP Response
                     |
                     ↓
                  BROWSER
```

Now ask at every boundary:

```text
Who controls this?
What is trusted?
What is validated?
What identity is associated with this?
What permissions are required?
Where does the data go?
What happens if an assumption is wrong?
```

---

# 51. Key Takeaways

1. A web application is more than a webpage.

2. A request may pass through reverse proxies, routing, authentication, authorization, application logic, APIs, caches, and databases.

3. Authentication answers:

```text
Who am I?
```

4. Authorization answers:

```text
What am I allowed to do?
```

5. The client controls significant parts of an HTTP request.

6. Client-controlled data should not automatically be trusted.

7. Input can travel through multiple layers of an application.

8. Business logic determines how the application performs its intended operations.

9. The browser has its own security mechanisms, including the Same-Origin Policy.

10. Understanding architecture is more valuable than memorizing isolated attack payloads.

11. Web security is fundamentally about understanding:

```text
input
 ↓
processing
 ↓
trust
 ↓
identity
 ↓
authorization
 ↓
business logic
 ↓
data
 ↓
output
```

---

# Security Mindset

When you meet a web application, don't immediately think:

```text
"What vulnerability can I try?"
```

Start with:

```text
How does this application work?
```

Then investigate:

```text
Who am I?

What am I allowed to do?

What can I control?

Where does my input go?

What does the application trust?

What happens when I violate assumptions?

What data can I access?

What happens behind the API?
```

Those questions give you the map.

Later, when you start using Burp Suite and security labs, the goal will be to use that map to investigate what the application actually does.

---