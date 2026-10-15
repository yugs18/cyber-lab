"""Integration tests for the HTTP request helper used by httppeek.

These tests exercise the real network behavior of fetch_url() against a tiny local
HTTP server. They validate the important success cases (200 OK, redirect handling,
HTTP error responses, and request timeouts) without relying on external network access.
"""

import time
import unittest
from contextlib import redirect_stdout
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import StringIO
from threading import Thread

from httppeek import fetch_url


class TestHandler(BaseHTTPRequestHandler):
    """Local test server that mimics a handful of simple HTTP responses.

    The server is kept intentionally tiny: it answers a normal successful request,
    a redirect, a missing resource, and a deliberately slow endpoint to trigger timeouts.
    The handler is a minimal implementation that only supports GET requests because the
    tests only need to validate fetch_url() for basic HTTP fetching behavior.
    """

    def do_GET(self):
        """Dispatch to the proper canned response based on the request path."""
        # Redirect path: verifies that urllib follows a Location header automatically.
        if self.path == "/redirect":
            self.send_response(302)
            self.send_header("Location", "/ok")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return

        # Missing resource path: should trigger an HTTPError in fetch_url() and return
        # the response body plus status 404.
        if self.path == "/missing":
            status = 404
            body = b"missing test resource"

        # Slow path: introduces a delay longer than the test timeout so fetch_url()
        # catches a timeout and returns None.
        elif self.path == "/slow":
            # Longer than the timeout used by the test.
            time.sleep(0.5)
            status = 200
            body = b"slow test response"

        # Default case: a healthy 200 OK response with a plain text payload.
        else:
            status = 200
            body = b"hello from local test server"

        self.send_response(status)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

        try:
            self.wfile.write(body)
        except OSError:
            # The client may have disconnected after a timeout.
            pass

    def log_message(self, format, *args):
        # Keep routine server logs out of the test output.
        pass


class TestFetchURL(unittest.TestCase):
    """Exercise fetch_url() against realistic HTTP responses.

    Each test validates a specific contract of the helper: successful data retrieval,
    HTTP error handling, redirect tracking, and timeout behavior.
    """

    @classmethod
    def setUpClass(cls):
        """Create a temporary local web server for the whole test class."""
        # Bind to an ephemeral port (0) so the test server chooses an available port.
        cls.server = ThreadingHTTPServer(
            ("127.0.0.1", 0),
            TestHandler,
        )

        # Run the server in a background thread so tests can send requests while the
        # server stays alive for the duration of the test suite.
        cls.server_thread = Thread(
            target=cls.server.serve_forever,
            daemon=True,
        )
        cls.server_thread.start()

        # Store the base URL used for all test requests.
        cls.base_url = (
            f"http://127.0.0.1:{cls.server.server_port}"
        )

    @classmethod
    def tearDownClass(cls):
        """Stop the test server cleanly after all tests finish."""
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join()

    def fetch_silently(self, path, timeout=2):
        """Issue a request while suppressing expected console output from fetch_url().

        Some error conditions (such as timeouts or network failures) print messages to
        stdout, but the tests are specifically checking the returned values, not the log
        output. Suppressing stdout keeps the test results easy to read and avoids noisy
        failures unrelated to logic.
        """
        url = self.base_url + path

        # Suppress expected error messages during tests.
        with redirect_stdout(StringIO()):
            result = fetch_url(url, timeout=timeout)

        return url, result

    def test_successful_response(self):
        """A normal 200 OK response should yield the expected status and payload."""
        url, result = self.fetch_silently("/ok")

        self.assertIsNotNone(result)
        self.assertEqual(result[0], 200)       # Status code
        self.assertEqual(result[1], "OK")      # HTTP reason phrase
        self.assertEqual(result[3], "text/plain")
        self.assertEqual(result[6], len(
            b"hello from local test server"
        ))
        self.assertGreaterEqual(result[7], 0)  # Elapsed time should be non-negative
        self.assertEqual(result[8], url)       # Final URL should match the requested URL
        self.assertFalse(result[9])            # No redirect happened
        self.assertEqual(
            result[10],
            b"hello from local test server",
        )

    def test_http_404_response(self):
        """HTTPError responses should still return the body and status metadata."""
        url, result = self.fetch_silently("/missing")

        self.assertIsNotNone(result)
        self.assertEqual(result[0], 404)
        self.assertEqual(
            result[10],
            b"missing test resource",
        )
        self.assertEqual(result[6], len(
            b"missing test resource"
        ))
        self.assertGreaterEqual(result[7], 0)
        self.assertEqual(result[8], url)
        self.assertFalse(result[9])

    def test_redirect_is_followed(self):
        """urllib should automatically follow redirects and report the final URL."""
        url, result = self.fetch_silently("/redirect")

        self.assertIsNotNone(result)
        self.assertEqual(result[0], 200)
        self.assertTrue(result[9])
        self.assertEqual(result[8], self.base_url + "/ok")
        self.assertEqual(
            result[10],
            b"hello from local test server",
        )

    def test_timeout_returns_no_result(self):
        """If the response takes too long, fetch_url() should fail gracefully."""
        url = self.base_url + "/slow"

        with redirect_stdout(StringIO()):
            result = fetch_url(url, timeout=0.1)

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()