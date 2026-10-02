# PortPeek

PortPeek is a simple Python port scanner that checks whether one or more TCP ports are open on a target host. It uses Python's built-in `socket` library to attempt outbound TCP connections to a host and port combination.

This project is useful for learning how port scanning works at a basic level and for checking whether common services such as HTTP, SSH, or MySQL are listening on a machine.

## What the script does

The program:

- accepts a target host such as `localhost`, an IP address, or a domain name
- accepts one or more port numbers as command-line arguments
- validates each port value
- connects to each port using a TCP socket
- reports whether the port is open or closed
- prints the socket error name when the port is not open

## Requirements

- Python 3.x
- A machine with network access to the target host

## Usage

```bash
python3 portpeek.py <host> <port1> <port2> <port3> ...
```

Example:

```bash
python3 portpeek.py localhost 22 80 443
```

You can also scan a remote host:

```bash
python3 portpeek.py scanme.nmap.org 22 80 443
```

## How it works

The program starts by checking whether the user supplied enough arguments:

- the script name
- the target host
- at least one port number

If not, it prints usage information and exits.

Then it loops through each port from the command line. For each port:

1. converts the port string into an integer
2. checks that the value is between `1` and `65535`
3. creates a TCP socket
4. sets a 1-second timeout
5. tries to connect to the host and port
6. prints the result
7. closes the socket

## Port validation

The script rejects invalid input such as:

- non-numeric port values
- ports less than `1`
- ports greater than `65535`

Examples:

```bash
python3 portpeek.py localhost abc
```

Output:

```text
Port 'abc' is not a number
```

```bash
python3 portpeek.py localhost 0
```

Output:

```text
Port '0' is out of range
```

## Example output

### Open port

```bash
python3 portpeek.py localhost 22 80 443
```

Example output:

```text
[+] localhost:22 is OPEN
[-] localhost:80 is ECONNREFUSED
[-] localhost:443 is ECONNREFUSED
```

### What the output means

- `[+]` means the port is open and a TCP connection was successful.
- `[-]` means the port is not open or the connection was refused.
- `ECONNREFUSED` usually means the connection was refused,
commonly because no service is listening on the destination port.

## Notes

This script uses a short timeout of `1` second to keep scanning fast. It checks only TCP ports, not UDP ports.

This tool is intended for learning and legitimate network testing. Do not use it against systems you do not own or do not have permission to test.

## Code overview

Key parts of the script:

- `socket.socket(socket.AF_INET, socket.SOCK_STREAM)` creates a TCP socket
- `sock.settimeout(1)` prevents the script from hanging on unresponsive ports
- `sock.connect_ex((target, port))` attempts the connection and returns a status code
- `result == 0` indicates a successful connection, meaning the port is open

## Author

This project was created as a simple port-checking utility for learning Python networking basics.
Currently, PortPeek tests IPv4 TCP connections only.
IPv6 support may be added later.
