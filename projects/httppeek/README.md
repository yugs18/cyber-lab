# HTTPPeek

HTTPPeek is a small Python HTTP inspection utility built using Python's standard library.

It accepts a target URL, sends an HTTP or HTTPS request, and displays useful information from the server's response, including the status code, common response headers, response time, response size, and whether the request was redirected.

The response body is also saved to a local file based on its reported content type.

The project is intended primarily for learning **HTTP, Python networking, response handling, and basic web reconnaissance concepts**.

---

## Features

HTTPPeek currently:

- accepts exactly one target URL
- validates whether the URL uses `http` or `https`
- sends a request using Python's standard library
- identifies itself with a custom `User-Agent`
- reports the HTTP status code
- displays common response headers
- measures response time
- measures response body size
- detects whether the final URL differs from the original URL
- saves the response body to a file
- handles HTTP and URL-related errors

---

## Requirements

- Python 3.x
- Network connectivity for remote targets

HTTPPeek uses only Python's standard library, so no external Python packages are required.

---

## Usage

```bash
python3 httppeek.py <url>
```

Example:

```bash
python3 httppeek.py http://127.0.0.1:8000
```

HTTPS example:

```bash
python3 httppeek.py https://example.com
```

---

## Local Testing

A simple way to test HTTPPeek safely is to run a local HTTP server.

Start the server:

```bash
python3 -m http.server 8000
```

Then, from another terminal:

```bash
python3 httppeek.py http://127.0.0.1:8000
```

This creates a simple local communication path:

```text
HTTPPeek
    |
    | HTTP Request
    ↓
127.0.0.1:8000
    |
    ↓
Python HTTP Server
    |
    | HTTP Response
    ↓
HTTPPeek
```

Using a local server makes it possible to experiment without depending on a third-party system.

---

## Example Output

A successful request may produce output similar to:

```text
===========================
      HTTPPEEK v0.3
===========================
URL: http://127.0.0.1:8000
HTTP
Status: 200
Server: SimpleHTTP/...
Content-Type: text/html; charset=utf-8
Content-Length: ...
Location: Not present

Response Time: 0.003 sec
Response Size: 1256 bytes
Redirected: False
Response saved to response.html
```

The exact values depend on the server and response.

---

## What the Program Does

### 1. Validate command-line input

HTTPPeek expects exactly one argument after the script name:

```text
python3 httppeek.py <url>
```

If the argument count is incorrect, the program prints usage information and exits.

---

### 2. Parse the URL

The program uses:

```python
urlparse(url)
```

to determine the URL scheme.

Supported schemes are:

```text
http
https
```

Any other scheme causes the program to exit with:

```text
Unknown protocol
```

---

### 3. Create the HTTP request

HTTPPeek creates a request using:

```python
Request(
    url,
    headers={"User-Agent": "CyberLab-httppeek"}
)
```

The custom `User-Agent` identifies the client as:

```text
CyberLab-httppeek
```

This demonstrates that HTTP request headers are supplied by the client.

---

### 4. Send the request

The request is sent using:

```python
urlopen(request, timeout=5)
```

The five-second timeout prevents the program from waiting indefinitely for a response.

The response is handled with a context manager:

```python
with urlopen(request, timeout=5) as response:
```

This ensures the response resource is properly cleaned up after use.

---

### 5. Read the response body

The complete response body is read with:

```python
body = response.read()
```

The body is kept in memory so it can later be measured and saved to disk.

---

### 6. Measure response time

The program uses:

```python
time.perf_counter()
```

to measure elapsed time.

The timer begins before the request and ends after the response body has been read:

```text
Start timer
    ↓
Send request
    ↓
Receive response
    ↓
Read response body
    ↓
Stop timer
```

This gives a measurement of the time taken for the request and response body to be received.

---

### 7. Read the status code

The HTTP status code is obtained from:

```python
response.status
```

Example:

```text
200
```

The status code provides information about the result of the HTTP request.

---

### 8. Read response headers

HTTPPeek extracts these headers:

```text
Server
Content-Type
Content-Length
Location
```

The program uses:

```python
response.headers.get(...)
```

to retrieve them.

If a header is not present, the program displays:

```text
Not present
```

This prevents a missing optional header from causing an unnecessary failure.

---

## Response Size

The size of the response body is calculated with:

```python
response_size = len(body)
```

Because `body` contains bytes, the result represents the number of bytes stored in the response body.

Example:

```text
Response Size: 1256 bytes
```

---

## Redirect Detection

HTTPPeek compares:

```python
final_url = response.url
```

with the original URL:

```python
url
```

Then:

```python
redirected = final_url != url
```

If the final URL is different, the program reports:

```text
Redirected: True
```

Otherwise:

```text
Redirected: False
```

This provides a simple indication that the request ended at a different URL.

---

## Saving the Response

HTTPPeek saves the response body to a local file.

The filename is based on the response's content type:

```python
file_type = response.headers.get_content_type().split('/', 1)[-1]
filename = "response." + file_type
```

Examples:

```text
text/html        → response.html
application/json → response.json
image/png        → response.png
```

The body is written in binary mode:

```python
with open(filename, "wb") as file:
    file.write(body)
```

The saved file can then be inspected separately.

---

## Error Handling

HTTPPeek handles two main categories of errors.

### HTTP Errors

```python
except HTTPError as e:
```

This handles HTTP-specific error responses such as:

```text
404 Not Found
500 Internal Server Error
```

The program displays:

```text
[HTTP Error] <status> <reason>
```

For example:

```text
[HTTP Error] 404 Not Found
```

---

### URL / Network Errors

```python
except URLError as e:
```

This handles URL-related or lower-level problems that prevent the request from completing normally.

The program displays:

```text
URL Error: <reason>
```

---

# Program Flow

The overall flow of HTTPPeek is:

```text
Command-line URL
        ↓
Validate input
        ↓
Parse URL scheme
        ↓
Create Request
        ↓
Add User-Agent
        ↓
Start timer
        ↓
urlopen()
        ↓
Receive HTTP response
        ↓
Read response body
        ↓
Stop timer
        ↓
Extract status
        ↓
Extract headers
        ↓
Calculate response size
        ↓
Check final URL
        ↓
Save response body
        ↓
Display results
```

---

# Technologies Used

HTTPPeek uses only Python's standard library.

Main modules:

```python
urllib.request
urllib.error
urllib.parse
sys
time
```

### `urllib.request`

Used for:

- creating HTTP requests
- sending requests
- receiving responses

### `urllib.error`

Used for:

- handling `HTTPError`
- handling `URLError`

### `urllib.parse`

Used for:

- parsing URLs
- identifying the URL scheme

### `sys`

Used for:

- reading command-line arguments
- exiting the program

### `time`

Used for:

- measuring response time

---

# HTTPPeek and the Network Stack

HTTPPeek operates at the HTTP/application layer, but its communication still depends on the lower networking layers.

Conceptually:

```text
HTTPPeek
    ↓
HTTP
    ↓
TCP
    ↓
IP
    ↓
Network Interface
```

This connects HTTPPeek with the networking concepts explored in the earlier `PortPeek` project.

`PortPeek` asks:

```text
Can I establish a TCP connection?
```

HTTPPeek goes one layer higher:

```text
Can I communicate using HTTP,
and what did the server return?
```

---

# Security Relevance

HTTPPeek is intentionally simple, but it introduces concepts used in web reconnaissance and security testing.

The tool begins collecting information such as:

```text
HTTP status
Server header
Content-Type
Content-Length
Location
Response size
Response time
```

These observations can provide clues about how a web server behaves.

The broader progression is:

```text
HTTP request
      ↓
HTTP response
      ↓
Headers
      ↓
Server behavior
      ↓
Application clues
      ↓
Reconnaissance
```

The project is not a vulnerability scanner and does not attempt to exploit the target.

---

# Security Mindset

When analyzing an HTTP response, ask:

```text
What exactly did the server return?
What does this information tell me?
What does it NOT tell me?
What assumptions would be unsafe to make?
```

For example:

```text
Server: ...
```

may provide information about the server software, but the presence of that header alone does not prove the exact software version or identify a vulnerability.

Similarly:

```text
404 Not Found
```

is an HTTP response, not necessarily a network failure.

The goal is to distinguish:

```text
Observation
    ↓
Evidence
    ↓
Interpretation
```

rather than immediately treating an observation as proof of a vulnerability.

---

# Current Limitations

HTTPPeek currently:

- supports one URL per execution
- supports HTTP and HTTPS
- uses the standard library only
- does not perform concurrent requests
- does not crawl links
- does not enumerate directories
- does not identify technologies automatically
- does not perform vulnerability scanning
- does not perform authentication testing
- does not analyze cookies in depth
- does not inspect security headers as a dedicated feature
- saves the response using a simple content-type-based filename

These limitations are intentional.

The project is designed to build HTTP and Python networking fundamentals before moving into more advanced web-security tooling.

---

# Future Improvements

Possible future versions could include:

```text
v0.4
├── detailed redirect information
├── custom request headers
├── configurable timeout
└── improved response-file naming

v0.5
├── selected response-header analysis
├── cookie inspection
├── security-header checks
└── more structured output

Future
├── multiple targets
├── endpoint discovery
├── technology identification
└── integration with larger reconnaissance tooling
```

These features should only be added as the underlying concepts become understood.

---

# Responsible Use

HTTPPeek can make requests to remote systems.

Only test systems that you own or systems for which you have explicit permission to perform testing.

For learning, a local target such as:

```text
127.0.0.1
```

is preferred.

---

# Project Purpose

HTTPPeek is part of a progressive cybersecurity learning environment.

The current project progression is:

```text
sysprobe
    ↓
System information

portpeek
    ↓
TCP connectivity

httppeek
    ↓
HTTP inspection
```

This progression builds the following mental model:

```text
Program
   ↓
Process
   ↓
Socket
   ↓
TCP
   ↓
HTTP
   ↓
Web Server
   ↓
Application
```

The long-term goal is to understand what is happening underneath security tools rather than relying on them as black boxes.