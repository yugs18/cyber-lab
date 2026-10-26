"""Local-only SQL injection demonstration using fictional SQLite records.

The unsafe_lookup function is intentionally vulnerable for comparison and
must never be used in production code. safe_lookup demonstrates parameterized
queries, which keep supplied input separate from SQL syntax.
"""

import sqlite3


UserRecord = tuple[str, str]


def create_database() -> sqlite3.Connection:
    """Create a fresh in-memory database containing fictional users."""
    conn = sqlite3.connect(":memory:")
    conn.execute(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            display_name TEXT NOT NULL
        )
        """
    )

    fictional_users: list[UserRecord] = [
        ("alice", "Alice Wonderland"),
        ("bob", "Bob Builder"),
        ("charlie", "Charlie Brown"),
        ("o'brien", "O'Brien"),
    ]
    conn.executemany(
        "INSERT INTO users (username, display_name) VALUES (?, ?)",
        fictional_users,
    )
    conn.commit()
    return conn


def unsafe_lookup(conn: sqlite3.Connection, username: str) -> list[UserRecord]:
    """Look up a user by unsafely concatenating input into SQL.

    INTENTIONALLY VULNERABLE: included only for this isolated learning demo.
    """
    query = (
        "SELECT username, display_name FROM users "
        f"WHERE username = '{username}'"
    )
    return conn.execute(query).fetchall()


def safe_lookup(conn: sqlite3.Connection, username: str) -> list[UserRecord]:
    """Look up a user using a parameterized query."""
    query = "SELECT username, display_name FROM users WHERE username = ?"
    return conn.execute(query, (username,)).fetchall()


def run_demo() -> None:
    """Show the same injection-like input against unsafe and safe functions."""
    conn = create_database()
    payload = "' OR 1=1 --"

    try:
        print("=" * 55)
        print("SQL INJECTION: UNSAFE VS PARAMETERIZED")
        print("=" * 55)
        print("\nFictional records in the database:")
        for row in conn.execute(
            "SELECT username, display_name FROM users ORDER BY id"
        ):
            print(row)

        print("\nInput:", repr(payload))
        print("Unsafe query results:", unsafe_lookup(conn, payload))
        print("Parameterized query results:", safe_lookup(conn, payload))
    finally:
        conn.close()


if __name__ == "__main__":
    run_demo()
