import sqlite3

def create_database():
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

    fictional_users = [
        ("alice", "Alice Wonderland"),
        ("bob", "Bob Builder"),
        ("charlie", "Charlie Brown"),
    ]

    conn.executemany(
        "INSERT INTO users (username, display_name) VALUES (?, ?)",
        fictional_users,
    )

    conn.commit()
    return conn


def unsafe_lookup (conn, username):
    query = (
        "SELECT username, display_name FROM users "
        f"WHERE username = '{username}'"
    )

    print(f"\n[UNSAFE] Executing query: {query}")
    return conn.execute(query).fetchall()


def safe_lookup(conn, username):
    query = "SELECT username, display_name FROM users WHERE username = ?"

    print(f"\n[SAFE] Executing query: {query} with parameter: {username}")
    return conn.execute(query, (username,)).fetchall()


def run_demo():
    conn = create_database()

    try:
        payload = "' OR 1=1 --"

        print("=" * 55)
        print("SQL INJECTION: UNSAFE VS PARAMETERIZED")
        print("=" * 55)

        print("\nFictional records in the database:")
        for row in conn.execute(
            "SELECT username, display_name FROM users"
        ):
            print(row)

        print("\nInput:", repr(payload))

        unsafe_results = unsafe_lookup(conn, payload)
        print("Unsafe results:", unsafe_results)

        safe_results = safe_lookup(conn, payload)
        print("Safe results:", safe_results)

    finally:
        conn.close()

if __name__ == "__main__":
    run_demo()
