"""Regression tests for the local SQLite SQL injection demonstration."""

import sqlite3
import unittest

from sqlite_injection_demo import (
    create_database,
    safe_lookup,
    unsafe_lookup,
)


class SQLiteInjectionDemoTests(unittest.TestCase):
    def setUp(self) -> None:
        self.conn = create_database()

    def tearDown(self) -> None:
        self.conn.close()

    def test_ordinary_search_terms_return_expected_records(self) -> None:
        expected_by_username = {
            "alice": [("alice", "Alice Wonderland")],
            "bob": [("bob", "Bob Builder")],
            "charlie": [("charlie", "Charlie Brown")],
        }

        for username, expected in expected_by_username.items():
            with self.subTest(username=username):
                self.assertEqual(safe_lookup(self.conn, username), expected)
                self.assertEqual(unsafe_lookup(self.conn, username), expected)

    def test_unknown_username_returns_no_records(self) -> None:
        self.assertEqual(safe_lookup(self.conn, "nobody"), [])

    def test_empty_input_returns_no_records(self) -> None:
        self.assertEqual(safe_lookup(self.conn, ""), [])
        self.assertEqual(unsafe_lookup(self.conn, ""), [])

    def test_apostrophe_in_valid_username_is_treated_as_data(self) -> None:
        expected = [("o'brien", "O'Brien")]

        # The parameterized query safely matches the fictional username.
        self.assertEqual(safe_lookup(self.conn, "o'brien"), expected)

        # Direct concatenation breaks the quoted SQL string.
        with self.assertRaises(sqlite3.OperationalError):
            unsafe_lookup(self.conn, "o'brien")

    def test_injection_like_input_is_treated_as_data_by_safe_query(self) -> None:
        payload = "' OR 1=1 --"

        # No username equals this complete string, so no rows should match.
        self.assertEqual(safe_lookup(self.conn, payload), [])

    def test_same_injection_like_input_changes_unsafe_query_results(self) -> None:
        payload = "' OR 1=1 --"
        expected = [
            ("alice", "Alice Wonderland"),
            ("bob", "Bob Builder"),
            ("charlie", "Charlie Brown"),
            ("o'brien", "O'Brien"),
        ]

        # The unsafe query interprets the input as SQL and returns every row.
        self.assertEqual(unsafe_lookup(self.conn, payload), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
