"""Unit tests for URL parsing and redirect comparison helpers.

These tests focus on the validation and normalization logic inside httppeek rather than
network I/O. They verify that malformed URLs are rejected, default ports are handled
consistently, query strings are parsed correctly, and redirect comparisons ignore
irrelevant differences such as case and fragments.
"""

import unittest
from contextlib import redirect_stdout
from io import StringIO

from httppeek import parse_and_validate_url, comparable_url


class TestURLParsing(unittest.TestCase):
    """Validate the input-validation contract for user-provided URLs."""

    def test_http_default_port(self):
        """HTTP URLs without an explicit port should resolve to port 80."""
        result = parse_and_validate_url("http://example.com")

        self.assertEqual(
            result,
            ("http", "example.com", 80, "/", None),
        )

    def test_https_default_port(self):
        """HTTPS URLs without an explicit port should resolve to port 443."""
        result = parse_and_validate_url("https://example.com")

        self.assertEqual(
            result,
            ("https", "example.com", 443, "/", None),
        )

    def test_explicit_port_and_path(self):
        """Explicit ports and non-root paths should be preserved exactly."""
        result = parse_and_validate_url(
            "http://127.0.0.1:8000/test"
        )

        self.assertEqual(
            result,
            ("http", "127.0.0.1", 8000, "/test", None),
        )

    def test_query_parameters(self):
        """Query strings should be parsed into a list of key/value pairs."""
        result = parse_and_validate_url(
            "http://example.com/?tag=linux&tag=python&empty="
        )

        self.assertEqual(
            result[4],
            [("tag", "linux"), ("tag", "python"), ("empty", "")],
        )

    def assert_invalid_url(self, url):
        """Shared helper for asserting that invalid inputs terminate with exit code 2."""
        # Some invalid URL inputs cause the parser to print a message and exit via
        # SystemExit, so tests capture stdout to keep output clean.
        with redirect_stdout(StringIO()):
            with self.assertRaises(SystemExit) as error:
                parse_and_validate_url(url)

        self.assertEqual(error.exception.code, 2)

    def test_rejects_unsupported_scheme(self):
        """Only HTTP and HTTPS are allowed, so FTP should be rejected."""
        self.assert_invalid_url("ftp://example.com")

    def test_rejects_missing_hostname(self):
        """A URL without a hostname is not a valid endpoint for this tool."""
        self.assert_invalid_url("http:///path")

    def test_rejects_invalid_port(self):
        """An out-of-range port should fail input validation before a request is made."""
        self.assert_invalid_url("http://example.com:99999")

    def test_rejects_non_url_input(self):
        """Gibberish strings should not be accepted as URLs."""
        self.assert_invalid_url("not-a-url")


class TestURLComparison(unittest.TestCase):
    """Check whether two URLs are effectively identical for redirect detection."""

    def test_hostname_case_and_default_port(self):
        """Case differences and default-port notation should not look like a redirect."""
        self.assertEqual(
            comparable_url("http://EXAMPLE.com"),
            comparable_url("http://example.com:80/"),
        )

    def test_ignores_fragment(self):
        """Fragments are not part of the HTTP request and therefore should be ignored."""
        self.assertEqual(
            comparable_url("http://example.com/#section"),
            comparable_url("http://example.com/"),
        )

    def test_different_paths_are_not_equal(self):
        """A move from one path to another should count as a redirect change."""
        self.assertNotEqual(
            comparable_url("http://example.com/old"),
            comparable_url("http://example.com/new"),
        )

    def test_different_queries_are_not_equal(self):
        """A changed query string means the client reached a different resource."""
        self.assertNotEqual(
            comparable_url("http://example.com/?page=1"),
            comparable_url("http://example.com/?page=2"),
        )


if __name__ == "__main__":
    unittest.main()