# Import the standard library modules needed for HTTP requests,
# URL parsing, timing measurements, and CLI argument handling.
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
import sys
import time


# Validate the command line input before doing anything else.
# The script expects exactly one argument: the target URL.
if len(sys.argv) != 2:
    print(f"Usage: python3 {sys.argv[0]} <url>")
    sys.exit(1)

# Print a simple banner to identify the tool when it runs.
print("===========================\n      HTTPPEEK v0.3       \n===========================")


# Read the URL the user supplied and display it for clarity.
url = sys.argv[1]
print(f"URL: {url}")

# Parse the URL to determine whether it uses HTTP or HTTPS.
# This prevents accidental unsupported protocols from being processed.
scheme = urlparse(url).scheme
if scheme == "https":
    print("HTTPS")
elif scheme == "http":
    print("HTTP")
else:
    print("Unknown protocol")
    sys.exit(1)

# Build an HTTP request object with a custom user-agent string.
# This helps identify the tool when connecting to remote servers.
request = Request(url, headers={"User-Agent": "CyberLab-httppeek"})

try:
    # Measure the request time so the script can report how quickly
    # the server responded to the HTTP request.
    start = time.perf_counter()

    # Send the request and keep the response open only for the duration
    # of the with-block so the connection is cleaned up properly.
    with urlopen(request, timeout=5) as response:

        # Read the full body payload from the server before closing the stream.
        # This preserves the response contents for later saving and analysis.
        body = response.read()

        # Stop the timer after the response is captured.
        end = time.perf_counter()

        # Calculate total elapsed time in seconds.
        response_time = end - start

        # Extract the HTTP status code for quick success/error reporting.
        status = response.status
        print(f"Status: {status}")

        # Pull common headers, replacing missing values with a friendly label.
        # This makes the output more readable when a server omits them.
        server = response.headers.get("Server")
        if server is None:
            server = "Not present"

        content_type = response.headers.get("Content-Type")
        if content_type is None:
            content_type = "Not present"

        length = response.headers.get("Content-Length")
        if length is None:
            length = "Not present"

        location = response.headers.get("Location")
        if location is None:
            location = "Not present"

        # Print the core response metadata collected from the HTTP headers.
        print(f"Server: {server}\nContent-Type: {content_type}\nContent-Length: {length}\nLocation: {location}")

        # Compute the raw size of the response body in bytes.
        response_size = len(body)

        # Check whether the final URL differs from the original input.
        # This indicates a redirect chain was followed by the client.
        final_url = response.url
        redirected = final_url != url

        # Display timing and size information for a quick summary of the response.
        print(f"\nResponse Time: {response_time:.3f} sec\nResponse Size: {response_size} bytes\nRedirected: {redirected}")

        # Determine the file extension based on the response content type,
        # then create a filename like response.html or response.json.
        file_type = response.headers.get_content_type().split('/', 1)[-1]
        filename = "response." + file_type

        # Save the server's raw response body to disk so it can be inspected later.
        with open(filename, "wb") as file:
            file.write(body)

        # Let the user know where the saved copy was written.
        print(f"Response saved to {filename}")

# Handle HTTP-specific failures returned by the remote server, such as 404 or 500.
except HTTPError as e:
    print(f"[HTTP Error] {e.code} {e.reason}")

# Catch lower-level URL problems such as DNS failures, connection timeouts,
# or other transport-level issues that prevent the request from completing.
except URLError as e:
    print(f"URL Error: {e.reason}")

