import getpass
import sys

EXPECTED_POLICY = {
    "admin": {
        "read_own_profile": True,
        "read_other_profiles": True,
        "update_own_profile": True,
        "delete_users": True,
    },
    "user": {
        "read_own_profile": True,
        "read_other_profiles": False,
        "update_own_profile": True,
        "delete_users": False,
    },
    "anonymous": {
        "read_own_profile": False,
        "read_other_profiles": False,
        "update_own_profile": False,
        "delete_users": False,
    },
}

USERS = {
    "admin": {
        "password": "admin123",
        "role": "admin",
    },
    "user1": {
        "password": "user123",
        "role": "user",
    },
    "user2": {
        "password": "user456",
        "role": "user",
    },
}

ROLES = {"admin", "user", "anonymous"}

ACTIONS = {
    "read_own_profile",
    "read_other_profiles",
    "update_own_profile",
    "delete_users",
}


def wanna_login():
    print("Welcome to the Authroization Matrix System!")
    print("Do you want to login? (yes/no)")
    choice = input().strip().lower()
    
    if choice != "yes":
        print("Welcome, Anonymous!")
        return "anonymous"
    
    print("Login to your account: ")
    
    username = input("Username: ")
    password = getpass.getpass("Password: ", echo_char="*")

    if username in USERS and USERS[username]["password"] == password:
        role = USERS[username]['role']
        print(f"Welcome, {username}!")
        return role
    else:
        print("Invalid username or password. Access denied.")
        sys.exit()


def is_allowed(role, action, *, verbose=True):
    if role not in ROLES:
        if verbose:
            print(f"Unknown role: {role}")
        return False

    if action not in ACTIONS:
        if verbose:
            print(f"Unknown action: {action}")
        return False

    if role == "admin":
        allowed = True

    elif role == "user":
        allowed = action in {
            "read_own_profile",
            "update_own_profile",
        }

    else:  # anonymous
        allowed = False

    if verbose:
        decision = "granted" if allowed else "denied"
        print(
            f"Access {decision} for role '{role}' "
            f"to perform action '{action}'."
        )

    return allowed


def check_authorization_matrix():
    failures = 0

    print("\nAuthorization Matrix Check")
    print("-" * 70)

    for role, actions in EXPECTED_POLICY.items():
        for action, expected in actions.items():
            actual = is_allowed(role, action, verbose=False)
            passed = actual == expected

            result = "PASS" if passed else "FAIL"

            print(
                f"{role:10} {action:25} "
                f"expected={str(expected):5} "
                f"actual={str(actual):5} {result}"
            )

            if not passed:
                failures += 1

    print("-" * 70)

    if failures:
        print(f"FAILED: {failures} permission check(s) mismatched.")
        return False

    print("SUCCESS: All permission checks matched.")
    return True


def main():
    role = wanna_login()

    while True:
        print("\nWhat action would you like to perform? (read_own_profile, read_other_profiles, update_own_profile, delete_users)")
        action = input().strip().lower()

        allowed = is_allowed(role, action)

        if not allowed:
            print("Do you want to try a different action? (yes/no)")
            choice = input().strip().lower()
            if choice != "yes":
                print("Exiting the system. Goodbye!")
                break

        if allowed:
            print("Do you want to perform another action? (yes/no)")
            choice = input().strip().lower()
            if choice != "yes":
                print("Exiting the system. Goodbye!")
                break


if __name__ == "__main__":
    if not check_authorization_matrix():
        sys.exit(1)
    # main()
