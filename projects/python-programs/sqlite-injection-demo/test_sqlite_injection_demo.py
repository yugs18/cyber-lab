import sqlite3
import unittest

from sqlite_injection_demo import create_database, unsafe_lookup, safe_lookup # type: ignore


class SQLiteInjectionDemoTests(unittest.TestCase):
    def setUp(self):
        self.conn = create_database()

    def tearDown(self):
        self.conn.close()

    def test_normal_username_works_in_both_ways(self):
        expected = [("alice", "Alice Wonderland")]

        self.assertEqual(unsafe_lookup(self.conn, "alice"), expected)
        self.assertEqual(safe_lookup(self.conn, "alice"), expected)

    def test_injection_changes_unsafe_query_meaning(self):
        payload = "' OR 1=1 --"

        unsafe_results = unsafe_lookup(self.conn, payload)

        self.assertEqual(len(unsafe_results), 3)

    def test_parameterized_query_treats_payload_as_data(self):
        payload = "' OR 1=1 --"

        safe_results = safe_lookup(self.conn, payload)

        self.assertEqual(safe_results, [])

    def test_apostrophe_is_handled_as_data(self):
        payload = "O'Brien"

        self.assertEqual(safe_lookup(self.conn, payload), [])

        with self.assertRaises(sqlite3.OperationalError):
            unsafe_lookup(self.conn, payload)


if __name__ == "__main__":
    unittest.main()
