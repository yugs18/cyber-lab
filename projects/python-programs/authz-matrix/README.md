# Authorization Matrix

A small Python cybersecurity project that models role-based access control (RBAC), generates an authorization matrix, and tests whether an authorization function follows an explicitly defined security policy.

This project was built as a hands-on exercise in access-control concepts, policy enforcement, and security regression testing.

## Overview

Web applications often have different permissions for anonymous visitors, ordinary users, and administrators. A security flaw occurs when an application allows an identity to perform an action that it should not be permitted to perform.

This project represents a fictional application's authorization rules in Python and checks the actual authorization decisions against the expected policy.

**The main objective is to make authorization rules explicit, testable, and easy to review.**

## Features

- Models three identities: `anonymous`, `user`, and `admin`.
- Defines four protected actions.
- Maintains an expected authorization policy separately from the authorization logic.
- Implements an independent authorization function.
- Generates a readable authorization matrix.
- Compares expected and actual permission decisions.
- Reports mismatches between policy and implementation.
- Includes automated tests for allowed and denied decisions.
- Denies unknown roles and actions by default.
- Runs locally without connecting to a real website or external service.

## Technology Stack

- **Language:** Python 3
- **Testing:** Python's built-in `unittest` module
- **External dependencies:** None required for the authorization matrix and tests

## Authorization Model

The project uses three identities:

| Identity | Description |
|---|---|
| `anonymous` | A visitor who is not authenticated |
| `user` | An ordinary authenticated user |
| `admin` | An administrator with elevated permissions |

It models four actions:

| Action | Description |
|---|---|
| `read_own_profile` | Read the current user's profile |
| `read_other_profiles` | Read another user's profile |
| `update_own_profile` | Update the current user's profile |
| `delete_users` | Delete user accounts |

## Expected Authorization Policy

The fictional application's expected permissions are:

| Identity | Read own profile | Read other profiles | Update own profile | Delete users |
|---|---|---|---|---|
| Anonymous | DENY | DENY | DENY | DENY |
| User | ALLOW | DENY | ALLOW | DENY |
| Admin | ALLOW | ALLOW | ALLOW | ALLOW |

These rules are assumptions for this educational exercise, not universal authorization rules for every application.

## How It Works

The project separates the expected policy from the function responsible for making authorization decisions.

### 1. Expected policy

`EXPECTED_POLICY` stores the expected result for each identity-action combination.

It acts as the reference against which the implementation is checked.

### 2. Authorization function

`is_allowed(role, action)` independently determines whether a role may perform a particular action.

Unknown roles and unknown actions are denied by default.

### 3. Matrix checker

The matrix checker iterates through every identity-action combination, compares the expected result with the authorization function's result, and reports whether each check passed.

If the implementation disagrees with the expected policy, the checker reports a failure and returns an unsuccessful exit status.

### 4. Automated tests

The test suite checks that authorization decisions match the expected policy and verifies representative allowed and denied cases.

This helps detect accidental permission changes during future modifications.

## Project Structure

```text
authz-matrix/
├── authz_matrix.py
├── test_authz_matrix.py
└── README.md
```

- `authz_matrix.py` — Expected policy, authorization function, and matrix checker.
- `test_authz_matrix.py` — Automated tests for authorization behavior.
- `README.md` — Project documentation.

## Getting Started

### Prerequisites

Install Python 3. No third-party packages are required for this exercise.

Check your Python version:

```bash
python3 --version
```

### Run the authorization matrix

From the project directory, execute:

```bash
python3 authz_matrix.py
```

The program evaluates the expected permissions against the actual authorization decisions and prints the result of each check.

A successful run should end with:

```text
SUCCESS: All permission checks matched.
```

### Run the automated tests

Execute:

```bash
python3 -m unittest -v test_authz_matrix.py
```

The test runner reports which tests passed or failed.

## Example Output

A successful matrix check displays each identity-action combination, its expected decision, its actual decision, and the comparison result.

For example:

```text
admin      read_own_profile          expected=True  actual=True  PASS
admin      delete_users              expected=True  actual=True  PASS
user       read_other_profiles       expected=False actual=False PASS
user       delete_users              expected=False actual=False PASS
anonymous  read_own_profile          expected=False actual=False PASS

SUCCESS: All permission checks matched.
```

The exact output contains all 12 combinations.

## Security Testing Exercise

An important part of this project is checking whether the tests detect an incorrect authorization rule.

To verify this:

1. Temporarily introduce an incorrect permission into the authorization function.
2. Run the matrix checker and automated tests.
3. Confirm that the mismatch is detected and the relevant test fails.
4. Restore the intended authorization rule.
5. Run the checker and tests again to confirm they pass.

This demonstrates how regression tests can detect unintended changes in access-control behavior.

## Security Concepts Practiced

This project reinforces the following concepts:

- **Authentication vs. authorization:** Establishing an identity does not automatically grant every permission.
- **Role-based access control (RBAC):** Permissions are assigned according to an identity's role.
- **Least privilege:** Users should receive only the permissions required for their intended responsibilities.
- **Default deny:** Unknown roles and actions should not receive permission by default.
- **Authorization testing:** Expected security rules should be checked against the actual implementation.
- **Security regression testing:** Automated tests help identify when a code change introduces an authorization failure.

## Limitations

This is a local educational simulation, not a production authorization system.

- It does not connect to a web server or database.
- It does not implement real profile reading, profile updates, or account deletion.
- It does not provide production authentication, session management, or secure password storage.
- Its policy is simplified and does not model permissions for individual records, ownership relationships, or complex business rules.

In a real application, authorization must be enforced on the server for the specific resource and action being requested. A role-based decision alone may not be sufficient for object-level authorization.

## Future Improvements

Possible extensions include:

- Add more roles and actions.
- Add tests for unknown roles and unknown actions.
- Add object-level authorization based on resource ownership.
- Represent permissions using explicit policy data structures.
- Add command-line options for running the matrix checker or interactive simulator.
- Generate a machine-readable JSON report of authorization decisions.
- Add continuous integration to run the test suite automatically.

## Key Takeaway

**Authorization rules should be explicit, independently implemented, and automatically tested.**

This project demonstrates how a small Python program can model a security policy and detect differences between expected and actual authorization decisions.