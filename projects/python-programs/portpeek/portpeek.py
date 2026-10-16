"""Port scanner script.

This script checks whether one or more TCP ports are open on a target host.
It accepts a hostname/IP address and a list of ports from the command line,
then tries to connect to each port using a raw socket connection.

Example:
    python3 portpeek.py scanme.nmap.org 22 80 443
"""

import socket  # Provides low-level networking tools for TCP connections.
import sys  # Allows us to read command-line arguments and exit the program.
import errno  # Provides symbolic socket error names for connection failures.

# Validate command-line arguments.
# We require at least: script name, target host, and one port.
# If not enough arguments are supplied, print a usage example and stop.
if len(sys.argv) < 3:
    print(f"Usage: python3 {sys.argv[0]} <host> <port1> <port2> ...")
    sys.exit(1)

# The first command-line argument after the script name is the host to scan.
target = sys.argv[1]

# Loop through every port passed in by the user.
for port_arg in sys.argv[2:]:
    try:
        # Convert the string like "80" into an integer so we can validate it.
        port = int(port_arg)
    except ValueError:
        # If the port is not a number, tell the user and skip to the next one.
        print(f"Port '{port_arg}' is not a number")
        continue

    # TCP port numbers must be between 1 and 65535 inclusive.
    # Port 0 is reserved and not used for standard services.
    if not 1 <= port <= 65535:
        print(f"Port '{port}' is out of range")
        continue

    # Create an IPv4 TCP socket.
    # socket.AF_INET means use the IPv4 address family.
    # socket.SOCK_STREAM means use TCP (connection-oriented protocol).
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set a short timeout so the script does not hang for too long when a port is closed.
    # A 1-second timeout is a good balance for quick scanning.
    sock.settimeout(1)

    # connect_ex attempts a connection and returns an error code instead of raising an exception.
    # A return value of 0 means the connection succeeded and the port is open.
    result = sock.connect_ex((target, port))

    # If the port is open, print a success message.
    if result == 0:
        print(f"[+] {target}:{port} is OPEN")
    else:
        # For closed or blocked ports, show the socket error name if available.
        # errno.errorcode maps error numbers to text like 'ECONNREFUSED'.
        print(f"[-] {target}:{port} is {errno.errorcode.get(result, 'UNKNOWN')}")

    # Always close the socket so the program does not leak network resources.
    sock.close()
