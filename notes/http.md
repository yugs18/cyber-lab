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