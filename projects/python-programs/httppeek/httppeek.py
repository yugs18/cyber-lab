"""HTTPPEEK: a small command-line utility for inspecting HTTP responses.

This script fetches a URL, validates the input, records the HTTP response metadata,
and prints a compact summary for the user. It can also store the response body to a
local file when requested. The implementation is intentionally small and focused, but
it handles several edge cases such as redirect following, HTTP errors, and timeouts.
"""

from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit, parse_qsl
import argparse
import sys
import time


def main():
    """Entry point for the command-line tool.

    The flow is deliberately simple:
    1. Parse CLI arguments.
    2. Validate and normalize the target URL.
    3. Request the URL and collect response metadata.
    4. Optionally save the body to disk.
    5. Print a human-readable summary.
    """
    # Gather all user-provided settings from the command line.
    args = parse_args()

    # Keep the original URL string for display while also validating its structure.
    url = args.url
    scheme, hostname, port, path, query_parameters = parse_and_validate_url(url)

    # Perform the actual HTTP request. This function may return None if the request
    # fails because of a timeout or a network-level error.
    result = fetch_url(url, timeout=args.timeout)

    # If the request failed at the transport level, exit early with an error status.
    if result is None:
        sys.exit(1)

    # Unpack the tuple returned by fetch_url(). The values are ordered to make the
    # caller's work straightforward and to support the optional file-saving behavior.
    (
        status, reason, server, content_type, content_length, location,
        response_size, response_time, final_url, redirected, body, filename
    ) = result

    # Optional feature: write the response body to disk using a generated filename.
    # This is useful when the user wants to inspect payloads outside the terminal.
    if args.save_body:
        with open(filename, "wb") as file:
            file.write(body)

    # Print the response summary in a structured format that includes the original URL,
    # normalized URL parts, and the response metadata collected from the server.
    display_response(
        url, scheme, hostname, port, path, query_parameters,
        status, reason, server, content_type, content_length, location,
        response_size, response_time, final_url, redirected
    )


def parse_args():
    """Build and validate the command-line interface for the tool.

    Returns a namespace with the parsed arguments. The function also enforces a
    positive timeout so the caller cannot accidentally configure a non-working value.
    """
    # argparse centralizes CLI parsing and automatically handles usage text.
    parser = argparse.ArgumentParser(description="A simple inspection tool.")

    # Required positional argument: the URL to request.
    parser.add_argument("url", help="Url to request, e.g. http://127.0.0.1:8000/")

    # Optional timeout (in seconds), defaulting to 5.0 so the tool remains responsive.
    parser.add_argument("--timeout", type=float, default=5.0, help="Request timeout in seconds (default: 5)")

    # Optional flag to persist the response body instead of streaming it only to stdout.
    parser.add_argument("--save-body", action="store_true", help="Save the response body")

    args = parser.parse_args()

    # A timeout of zero or negative seconds would make the tool unusable or misleading,
    # so reject that configuration immediately with argparse's normal error path.
    if args.timeout <= 0:
        parser.error("--timeout must be greater than 0")

    return args


def parse_and_validate_url(url):
    """Parse the URL and reject malformed or unsupported inputs.

    This function normalizes the URL into a consistent tuple that the rest of the tool
    can use: scheme, hostname, port, path, and parsed query parameters. It exits the
    process with a status code of 2 for invalid URLs so callers can treat it as an
    input-validation failure rather than a runtime error.
    """
    # urlsplit() is the standard library parser for URLs and is robust enough for this
    # simple CLI utility. We catch ValueError so invalid input can be reported cleanly.
    try:
        result = urlsplit(url)
    except ValueError as e:
        print(f"Invalid URL: {e}")
        sys.exit(2)

    # HTTP and HTTPS are the only supported schemes for this tool.
    scheme = result.scheme.lower()
    if scheme not in ("http", "https"):
        print("URL must use HTTP or HTTPS")
        sys.exit(2)

    # A hostname is required; without it, the URL is not usable for requests.
    if not result.netloc or not result.hostname:
        print("URL must include a hostname")
        sys.exit(2)

    hostname = result.hostname

    # result.port may raise ValueError for an invalid numeric port, such as a value
    # greater than 65535 or a negative number.
    try:
        explicit_port = result.port
    except ValueError as e:
        print(f"Invalid port number: {e}")
        sys.exit(2)

    # Use the default HTTP/HTTPS port when the URL omitted an explicit port.
    if explicit_port is None:
        port = 80 if scheme == "http" else 443
    else:
        port = explicit_port

    # An empty path is legal in HTTP URLs and should be treated as the root path.
    path = result.path or "/"

    # Parse query parameters as a list of key/value pairs. keep_blank_values=True keeps
    # parameters like "?empty=" instead of silently dropping them.
    query_parameters = (
        parse_qsl(result.query, keep_blank_values=True)
        if result.query
        else None
    )

    return scheme, hostname, port, path, query_parameters


def comparable_url(url):
    """Normalize a URL so redirect comparisons are stable and semantically correct.

    Redirect detection must ignore the fragment (which is not resent in HTTP requests)
    and treat the default port as equivalent to the same host without an explicit port.
    The function returns a tuple that can be compared across URLs without being fooled by
    formatting differences like uppercase hostnames or default-port notation.
    """
    # Parse the URL again so we can inspect each component separately.
    parts = urlsplit(url)

    # Hostnames are case-insensitive, so lowercase them to avoid false mismatches.
    scheme = parts.scheme.lower()
    hostname = (parts.hostname or "").lower()

    # If the URL includes an invalid port number, we cannot normalize it reliably, so
    # fall back to a raw string comparison rather than crashing.
    try:
        port = parts.port
    except ValueError:
        return url

    # HTTP and HTTPS default ports should not count as a real difference when comparing
    # the original URL to the final URL after a redirect.
    if (scheme == "http" and port == 80) or \
       (scheme == "https" and port == 443):
        port = None

    # IPv6 literals need square brackets when rendered as a host:port string.
    if ":" in hostname:
        hostname = f"[{hostname}]"

    # Preserve any userinfo (such as username:password) if present, but remove it from
    # the comparison unless the user explicitly included it in the URL.
    userinfo = ""
    if "@" in parts.netloc:
        userinfo = parts.netloc.rsplit("@", 1)[0] + "@"

    netloc = userinfo + hostname

    if port is not None:
        netloc += f":{port}"

    # Paths are significant for redirects; a change from /old to /new should count as a
    # true redirect in the comparison, even if the hostname is otherwise the same.
    path = parts.path or "/"

    return scheme, netloc, path, parts.query


def fetch_url(url, timeout=5):
    """Send an HTTP request and return a rich tuple of response metadata.

    This function wraps urllib's request machinery to make the HTTP interaction easier
    to inspect in one place. It captures the status, headers, body, final URL, timing,
    and redirect state. On HTTP errors (4xx/5xx), urllib raises HTTPError, which is
    handled separately so the script can still report the server response.
    """
    # Build a custom request with a user-agent string to identify the tool to servers.
    request = Request(url, headers={"User-Agent": "CyberLab-httppeek"})

    start = time.perf_counter()
    try:
        # urlopen() follows redirects automatically, which is exactly what we want for a
        # tool that checks the final response after redirection.
        with urlopen(request, timeout=timeout) as response:

            # Read the entire body before closing the response to ensure we have the
            # complete payload for display or optional file saving.
            body = response.read()

            end = time.perf_counter()

            response_time = end - start

            status = response.status

            # Response headers are case-insensitive; using .get() simplifies extraction.
            server = response.headers.get("Server")
            if server is None:
                server = "Not present"

            content_type = response.headers.get("Content-Type")
            if content_type is None:
                content_type = "Not present"

            content_length = response.headers.get("Content-Length")
            if content_length is None:
                content_length = "Not present"

            location = response.headers.get("Location")
            if location is None:
                location = "Not present"

            response_size = len(body)

            final_url = response.url

            # Compare the normalized original and final URLs to decide whether the request
            # was redirected at some point during the fetch.
            redirected = (
                comparable_url(final_url) != comparable_url(url)
            )

            # Generate a simple filename based on the response content type, e.g.:
            # "response.json" or "response.html".
            file_type = response.headers.get_content_type().split('/', 1)[-1]
            filename = "response." + file_type

            return (status, response.reason, server, content_type, content_length, location, response_size, response_time, final_url, redirected, body, filename)

    except HTTPError as e:
        # HTTP status codes such as 404 or 500 are not fatal in this tool; they still
        # carry a valid response body and headers, so we capture those details.
        body = e.read()
        response_time = time.perf_counter() - start

        status = e.code
        headers = e.headers

        server = headers.get("Server") or "Not present"
        content_type = headers.get("Content-Type") or "Not present"
        content_length = headers.get("Content-Length") or "Not present"
        location = headers.get("Location") or "Not present"

        response_size = len(body)

        final_url = e.url

        redirected = (
            comparable_url(final_url) != comparable_url(url)
        )

        # Some servers may not supply a useful Content-Type, so fall back to a plain
        # extension when needed.
        if headers:
            file_type = headers.get_content_type().split("/", 1)[-1]
        else:
            file_type = "plain"

        filename = f"response-{status}.{file_type}"

        return (
            status,
            e.reason,
            server,
            content_type,
            content_length,
            location,
            response_size,
            response_time,
            final_url,
            redirected,
            body,
            filename,
        )

    except TimeoutError:
        # This exception is raised when the underlying socket times out before a
        # response is received. Display a user-friendly message and return None so the
        # caller can exit without a traceback.
        print(f"[Timeout] Request exceeded the configured timeout of {timeout:g} seconds")
        return None

    except URLError as e:
        # A URLError can wrap either a timeout or a broader network failure such as DNS
        # resolution, connection refusals, or unreachable hosts.
        if isinstance(e.reason, TimeoutError):
            print(
                f"[Timeout] Request exceeded the configured timeout "
                f"of {timeout:g} seconds"
            )
        else:
            print(f"[Network Error] {e.reason}")

        return None


def display_response(url, scheme, hostname, port, path, query_parameters, status, reason, server, content_type, content_length, location, response_size, response_time, final_url, redirected):
    """Print a well-structured summary of the HTTP response to the terminal.

    The output is intentionally formatted to resemble a simple inspection report:
    request details first, then server response details, followed by timing and redirect
    information. This makes the output easy to scan while debugging network behavior.
    """
    # Banner header to visually separate the tool output from other console messages.
    print("===========================\n      HTTPPEEK       \n===========================")

    print(f"Original URL: {url}")

    # Show the normalized request components so the user sees exactly what the tool
    # parsed from the input URL.
    print(f"Scheme: {scheme}\nHostname: {hostname}\nPort: {port}\nPath: {path}\nQuery parameters: {query_parameters}")

    print(f"\nStatus: {status} {reason}")

    # Print the most common headers that are relevant for diagnosis: server identity,
    # media type, content length, and redirect location (if any).
    print(f"Server: {server}\nContent-Type: {content_type}\nContent-Length: {content_length}\nLocation: {location}")

    # Timing and size are helpful in figuring out whether the server was slow or returned
    # a large payload. Redirect information helps confirm whether urlopen() followed a
    # redirect chain before landing on the final resource.
    print(f"\nResponse Time: {response_time:.3f} sec\nResponse Size: {response_size} bytes\nRedirected: {redirected}")

    print(f"Final Url: {final_url}")


if __name__ == "__main__":
    main()
