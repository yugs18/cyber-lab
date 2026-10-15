# HTTPPeek

HTTPPeek is a small command-line HTTP inspection tool written in Python using the standard library. It sends a GET request to an HTTP or HTTPS URL and reports parsed URL details, response metadata, elapsed time, response-body size, and whether the final destination differs from the original URL.

The project is intended for learning HTTP, URL parsing, Python networking, and practical web-security testing against systems you own or are authorized to test.

## Features

- Accepts a URL as a command-line argument.
- Supports `http` and `https` URLs.
- Parses and displays the scheme, hostname, effective port, path, and query parameters.
- Preserves repeated query keys and empty query values when displaying parsed parameters.
- Sends a GET request with the user-agent `CyberLab-httppeek`.
- Supports a configurable request timeout.
- Displays the HTTP status code and reason phrase.
- Displays selected response headers: `Server`, `Content-Type`, `Content-Length`, and `Location`.
- Measures elapsed time through reading the response body.
- Calculates response-body size from the bytes received.
- Reports the final URL and whether it differs from the original destination after URL normalization.
- Handles HTTP error responses (for example, 404) separately from network errors.
- Optionally saves the response body to a file.
- Uses Python's `argparse` for command-line argument parsing and help output.

## Requirements

- Python 3.10 or newer is recommended.
- No third-party Python packages are required.
- Network access to the target is required for requests. The examples below use a local practice server.

## Project layout

A simple layout is:

```text
httppeek/
├── httppeek.py
├── README.md
└── tests/
    ├── test_httppeek.py
    └── test_httppeek_requests.py
```

The two test files are present if you created the unit and integration tests described during development.

## Usage

Run commands from the directory containing `httppeek.py`.

### Show help

```bash
python3 httppeek.py --help
```

### Inspect a URL

```bash
python3 httppeek.py http://127.0.0.1:8000/
```

### Set the timeout

The default timeout is 5 seconds. Pass `--timeout` to use a different positive number of seconds:

```bash
python3 httppeek.py --timeout 10 http://127.0.0.1:8000/
```

A non-positive timeout is rejected by the argument parser.

### Save the response body

```bash
python3 httppeek.py --save-body http://127.0.0.1:8000/
```

With `--save-body`, HTTPPeek writes the received body to a file in the **current working directory**. A successful response uses a name such as `response.html`; an HTTP error response uses a name such as `response-404.html`. The extension is based on the response's MIME subtype, so it should be treated as a convenient label rather than a guarantee about the file's contents.

**Caution:** successful responses with the same MIME subtype use the same filename and can overwrite a previous file. Run separate tests from separate directories or move/rename the saved file between requests if you need to keep multiple response bodies.

## Example output

Output varies with the target server and the actual response. A typical successful request may look like this:

```text
===========================
      HTTPPEEK
===========================
Original URL: http://127.0.0.1:8000/
Scheme: http
Hostname: 127.0.0.1
Port: 8000
Path: /
Query parameters: None

Status: 200 OK
Server: SimpleHTTP/0.6 Python/3.x
Content-Type: text/html
Content-Length: 135
Location: Not present

Response Time: 0.004 sec
Response Size: 135 bytes
Redirected: False
Final Url: http://127.0.0.1:8000/
```

The values above are examples, not fixed expected output. Your server's headers, response size, and timing may differ.

## Run a local test server

For practice, serve a local directory rather than testing an application without permission.

In one terminal:

```bash
cd ~/Desktop/cyber-lab/projects/attack-surface
python3 -m http.server 8000 --bind 127.0.0.1 --directory site
```

Keep the server running. In another terminal, go to the HTTPPeek project directory and run:

```bash
python3 httppeek.py http://127.0.0.1:8000/
python3 httppeek.py http://127.0.0.1:8000/index.html
python3 httppeek.py 'http://127.0.0.1:8000/?source=day4&tag=python'
python3 httppeek.py http://127.0.0.1:8000/missing
python3 httppeek.py --timeout 2 http://127.0.0.1:8000/
```

The missing path will usually produce a 404 response. HTTPPeek displays HTTP error details and returns the response body for optional saving; a network failure such as a refused connection is reported separately.

## URL parsing and validation

HTTPPeek rejects schemes other than HTTP and HTTPS and requires a hostname. If the URL omits a port, the displayed effective port is `80` for HTTP or `443` for HTTPS. An explicitly malformed or out-of-range port is rejected.

For example, the URL:

```text
http://127.0.0.1:8000/search?tag=linux&tag=python&empty=
```

is parsed into:

- Scheme: `http`
- Hostname: `127.0.0.1`
- Port: `8000`
- Path: `/search`
- Query parameters: `[('tag', 'linux'), ('tag', 'python'), ('empty', '')]`

## Error handling

HTTPPeek distinguishes these categories:

- **HTTP error response:** The server returned an HTTP status such as `404`. HTTPPeek reports the status and reason, records available response headers and body size, and can save the error response body with `--save-body`.
- **Network error:** A request could not be completed because of a connection or other URL/network problem. HTTPPeek prints a network-error message and exits with status `1`.
- **Timeout:** The request exceeded the configured timeout. HTTPPeek prints a timeout message and exits with status `1`.
- **Invalid input:** Unsupported schemes, missing hostnames, invalid ports, or a non-positive timeout are rejected before the request is made. URL validation exits with status `2`; `argparse` also uses status `2` for command-line argument errors.

## Tests

If the `tests/` files have been created, run them from the project root:

```bash
python3 -m unittest discover -s tests -v
```

The unit tests cover URL parsing, input validation, and URL comparison. The integration tests use a small local HTTP server to check successful responses, 404 responses, redirects, and timeout behavior. The tests should not need an external website.

## How it works

The program is organized around four main stages:

1. `parse_args()` reads the URL, timeout, and optional body-saving flag.
2. `parse_and_validate_url()` checks URL structure and returns the parsed components for display.
3. `fetch_url()` sends the GET request, measures elapsed time, gathers response metadata, detects a changed final destination, and returns the response body and filename.
4. `display_response()` prints the request URL details and response summary.

`comparable_url()` normalizes URL components used to compare the original URL with the final URL. It ignores fragments, lowercases scheme and hostname, treats default ports as equivalent to omitted ports, and supplies `/` for an empty path. The current implementation reports whether the final destination differs; it does not list every intermediate redirect.

## Current limitations

- HTTPPeek currently sends GET requests only; it does not let the user select another HTTP method.
- It prints selected response headers rather than every header.
- `--save-body` writes to the current directory and does not accept a custom output path.
- A successful response may overwrite an earlier `response.<subtype>` file with the same MIME subtype.
- The chosen filename extension is inferred from the MIME subtype and does not guarantee the response is a valid file of that type.
- Redirect reporting identifies a change in the final destination, not the number of redirects or intermediate locations.
- The reported response time includes reading the response body; it is not strictly the time until the first response byte arrives.
- The response body is read into memory before it is displayed or saved, so very large responses can consume significant memory.
- The tool is an educational inspection utility, not a full vulnerability scanner or proof that a target is secure.

## Safe use

Use HTTPPeek against your own services, local labs, or targets for which you have explicit authorization. Keep authentication tokens, cookies, sensitive response bodies, and private data out of committed evidence and screenshots.

---

## Testing

`httppeek` uses Python's built-in `unittest` framework to test URL parsing, URL comparison, HTTP responses, redirects, and timeout handling.

### Run the test suite

From the project root, run:

```bash
python3 -m unittest discover -s tests -v
```

The command discovers and runs the test files in the `tests/` directory and displays each test result.

### Unit tests

The unit tests verify URL parsing, validation, and comparison logic without making HTTP requests.

**URL parsing and validation**

The tests check that:

- HTTP URLs default to port `80`.
- HTTPS URLs default to port `443`.
- Explicit ports and URL paths are parsed correctly.
- Repeated query parameters and empty parameter values are preserved.
- Unsupported schemes, missing hostnames, invalid ports, and non-URL inputs are rejected with exit code `2`.

**URL comparison**

The tests verify that:

- Hostname capitalization and explicit default ports do not create false differences.
- URL fragments are ignored during comparison.
- Different paths and query strings are recognized as different destinations.

### HTTP integration tests

The integration tests run against a small local HTTP server bound to `127.0.0.1`, using an automatically assigned available port. They do not require access to external websites.

The tests cover:

| Test | Expected behavior |
|---|---|
| Successful response | Returns status `200`, response metadata, body, size, elapsed time, and final URL. |
| HTTP 404 response | Preserves the error status, response body, size, and timing information. |
| Redirect handling | Follows a local redirect and reports the final URL and redirect status. |
| Timeout handling | Returns no result when the request exceeds the configured timeout. |

The test server is shut down after the integration tests finish.

### Test organization

The tests can be kept in separate files:

```text
httppeek/
├── httppeek.py
├── README.md
└── tests/
    ├── test_httppeek.py
    └── test_httppeek_requests.py
```

- `test_httppeek.py` contains unit tests for URL parsing, validation, and comparison.
- `test_httppeek_requests.py` contains integration tests for HTTP responses, redirects, and timeouts.

### Limitations

These tests do not yet verify the command-line interface's complete behavior, including `--save-body`, the exact contents of saved files, or output formatting from `display_response()`. Those behaviors require additional tests.

Passing the test suite establishes that the tested cases behave as expected; it does not guarantee that every possible URL, server response, or network condition is handled correctly.
