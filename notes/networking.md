# Networking Notes

## Mental Model

A simplified view of how an application communicates across a network:

```text
    Your Application
           |
        Socket
           |
        TCP / UDP
           |
           IP
           |
    Network Interface
           |
         Gateway
           |
        Internet
           |
       Destination
```

A more complete view:

```text
Application
     ↓
   Socket
     ↓
 TCP / UDP
     ↓
     IP
     ↓
    MAC
     ↓
Network Interface
     ↓
Gateway / Router
     ↓
   Network
     ↓
 Destination
```

DNS is slightly different: it is an application-layer service that helps translate domain names into IP addresses.

---

## IP Address (Internet Protocol Address)

An IP address identifies a network interface/address on an IP network.

### IPv4

Example:

```text
192.168.1.10
```

* Uses **32 bits**
* Still extremely widely used
* Written as four decimal octets
* Each octet ranges from `0` to `255`

### IPv6

Example:

```text
2001:db8:85a3::8a2e:370:7334
```

* Uses **128 bits**
* Provides a vastly larger address space than IPv4
* Designed to address the limitations of IPv4 address availability

### Public IP

A public IP address is routable on the public Internet.

Websites and Internet services can generally see the public IP address from which a connection reaches them.

### Private IP

A private IP address is used inside a private/local network.

Common IPv4 private ranges include:

```text
10.0.0.0/8
172.16.0.0/12
192.168.0.0/16
```

Example:

```text
192.168.1.10
```

Private addresses are not directly routable across the public Internet.

In a typical home network, a router commonly provides or manages private IP addresses using DHCP and provides connectivity to the Internet.

---

## MAC Address

A MAC address is a Layer 2 address associated with a network interface.

Example:

```text
00:0c:29:ff:ed:80
```

MAC addresses are primarily used for communication on the local network.

Think of the difference as:

```text
MAC address → local network addressing
IP address  → IP network addressing
Port        → application/service endpoint
```

A device can have multiple network interfaces, and each interface can have its own MAC address and IP configuration.

---

## Port

A port is a numbered communication endpoint used by TCP or UDP to identify which application or service should receive network traffic.

Port numbers range from:

```text
0 - 65535
```

Examples:

```text
HTTP  → TCP 80
HTTPS → TCP 443
SSH   → TCP 22
DNS   → UDP/TCP 53
```

An IP address identifies the network destination, while a port helps identify the service/application endpoint.

Example:

```text
192.168.1.10:443
```

Here:

```text
IP   = 192.168.1.10
Port = 443
```

---

## Socket

A socket is an operating-system abstraction/API that allows a program to communicate over a network.

A program can use a socket to:

* Create a network endpoint
* Bind to an IP address and port
* Listen for connections
* Accept incoming connections
* Connect to another endpoint
* Send and receive data
* Close the connection

Simplified:

```text
IP + Port + Transport Protocol
              |
           Endpoint
```

For example:

```text
192.168.1.10:50000 + TCP
```

A socket is not simply the physical network connection. It is an interface provided by the operating system through which applications interact with network communication.

---

## Transmission Control Protocol (TCP)

TCP is a transport-layer protocol that provides reliable, ordered communication between applications.

TCP is used underneath protocols such as:

* HTTP/HTTPS
* SSH
* SMTP

### Important TCP properties

TCP provides:

* Reliable delivery
* Ordered delivery
* Retransmission of lost data
* Flow control
* Congestion control
* Connection-oriented communication

### TCP is a byte stream

TCP provides applications with a continuous **byte stream**.

It does not preserve application message boundaries.

The operating system/network stack divides the stream into TCP segments as necessary.

---

### TCP Segment

A TCP segment contains information such as:

* Source port
* Destination port
* Sequence number
* Acknowledgment number
* Flags
* Window information
* Checksum

Important flags include:

```text
SYN
ACK
FIN
RST
```

---

### TCP Three-Way Handshake

TCP establishes a connection using a three-way handshake.

```text
Client                         Server
  │                              │
  │──── SYN ────────────────────>│
  │<─── SYN + ACK ───────────────│
  │──── ACK ────────────────────>│
  │                              │
  │      Connection established  │
```

Simplified meaning:

```text
SYN     → I want to establish a connection.
SYN+ACK → I received your request and agree.
ACK     → I acknowledge your response.
```

---

### TCP Reliable Delivery

TCP uses acknowledgments and sequence numbers to keep track of transmitted data.

If data is lost:

```text
Sender                         Receiver
  │                              │
  │──── Segment 1 ──────────────>│
  │──── Segment 2 ──────X        │  ← lost
  │──── Segment 3 ──────────────>│
  │                              │
  │<──── acknowledgment/recovery │
  │──── Segment 2 ──────────────>│
```

TCP can retransmit missing data.

---

### TCP Keeps Data in Order

Each segment contains sequence information.

This allows the receiver to reconstruct the original byte stream in the correct order even when segments arrive out of order.

---

## User Datagram Protocol (UDP)

UDP is a transport-layer protocol designed for simple, low-overhead communication.

UDP does **not** provide TCP-style guarantees such as:

* Reliable delivery
* Ordered delivery
* Automatic retransmission
* Connection establishment

Applications can implement their own reliability mechanisms when necessary.

### UDP Example

```text
Your Computer                         Server
     │                                  │
     │──── UDP packet ────────────────>│
     │──── UDP packet ────────────────>│
     │──── UDP packet ───────X         │ ← lost
     │──── UDP packet ────────────────>│
```

UDP itself does not automatically retransmit the lost packet.

### UDP Header

A UDP header contains:

```text
Source Port
Destination Port
Length
Checksum
```

The UDP header is small, which contributes to its low overhead.

---

## Router

A router is a network device that forwards packets between different networks.

Example:

```text
Laptop
192.168.1.10
     │
     ▼
┌───────────┐
│  Router   │
└───────────┘
     │
     ▼
  Internet
```

The laptop determines whether the destination is on its local network.

If the destination is on another network, the laptop sends the traffic toward its router/default gateway.

The router then determines where to forward the packet.

---

## Gateway

A gateway is a network point that provides a path to another network.

In a typical home network, the router acts as the **default gateway**.

Example:

```text
Laptop
IP: 192.168.1.10
      │
      ▼
Router / Default Gateway
IP: 192.168.1.1
      │
      ▼
   Internet
```

If a destination is outside the local network, the host normally sends the traffic to its default gateway.

---

## Domain Name System (DNS)

DNS is a distributed system used to translate domain names into information such as IP addresses.

Example:

```text
google.com
     ↓
    DNS
     ↓
IP address
```

Without DNS, users would generally need to remember IP addresses instead of domain names.

### Simplified DNS Resolution

```text
Browser / Application
        │
        ▼
 DNS Resolver
        │
        ▼
 Root DNS Server
        │
        ▼
 .com DNS Server
        │
        ▼
Authoritative DNS Server
        │
        ▼
   IP Address
```

This is a simplified model. In practice, a DNS resolver may already have the answer cached.

### What is a DNS Server?

A DNS server is a system/service that handles DNS queries and provides DNS responses.

### DNS Port

Traditional DNS commonly uses:

```text
UDP 53
TCP 53
```

Modern DNS can also use encrypted protocols such as DNS over HTTPS (DoH), which changes the transport details.

---

## Internet Control Message Protocol (ICMP)

ICMP is a network-layer protocol used for network diagnostics, control information, and error reporting.

`ping` commonly uses:

```text
ICMP Echo Request
ICMP Echo Reply
```

Example:

```text
Your Machine
192.168.x.x
      │
      │ ICMP Echo Request
      ▼
   8.8.8.8
      │
      │ ICMP Echo Reply
      ▼
Your Machine
```

### Important

ICMP does **not** use TCP or UDP.

Therefore, an ICMP ping does not have a TCP/UDP port.

ICMP is carried directly inside IP.

For IPv4:

```text
ICMP protocol number = 1
```

This is why Wireshark showed:

```text
ICMP (1)
```

during the packet-capture exercise.

---

## Example: Putting the Concepts Together

Consider a computer accessing an HTTPS website:

```text
Application
   │
   │ HTTPS
   ▼
Socket
   │
   │ TCP
   ▼
TCP
   │
   │ IP
   ▼
IP
   │
   │ MAC
   ▼
Network Interface
   │
   ▼
Default Gateway
   │
   ▼
Internet
   │
   ▼
Web Server
```

Example endpoint:

```text
Client:
192.168.1.10:50000

Server:
142.250.x.x:443
```

The important distinction is:

```text
IP address → Where?
Port        → Which service?
TCP/UDP     → How is transport handled?
Socket      → How does the application interact with networking?
MAC         → Which local-network interface?
```

---

## Practical Observation

During packet analysis, I captured an ICMP ping to:

```text
8.8.8.8
```

The packet showed:

```text
Echo Request
Source:      192.168.x.x
Destination: 8.8.8.8
Protocol:    ICMP (1)
```

The reply reversed the source and destination:

```text
Echo Reply
Source:      8.8.8.8
Destination: 192.168.x.x
Protocol:    ICMP (1)
```

This demonstrated that packet captures expose information that higher-level commands can hide.

---

## Security Perspective

Networking concepts are fundamental to cybersecurity.

An attacker or defender may care about:

* IP addresses
* MAC addresses
* Open ports
* Listening services
* Active connections
* Protocols
* DNS requests
* Routing
* Network interfaces
* Packet contents
* Packet direction

A useful security mindset is:

> Don't just trust the abstraction. Look at what is actually happening on the network.

Tools such as Wireshark allow us to inspect that traffic directly.

# Processes, Sockets & Listening Ports

## Socket

A **socket** is an operating-system abstraction used by programs for network communication.

A process accesses a socket through a file descriptor.

```text
Process
   ↓
File Descriptor
   ↓
Socket
   ↓
TCP/UDP
   ↓
IP
   ↓
Network Interface
```

A socket is not the same thing as:

* an IP address
* a port
* a physical network connection

These concepts work together.

---

# Port

A port identifies a communication endpoint associated with a TCP or UDP service.

Example:

```text
127.0.0.1:8000
```

Here:

```text
127.0.0.1 → IP address
8000      → TCP port
```

The IP address identifies the network endpoint/interface address, while the port identifies the transport-layer service endpoint.

---

# Listening Socket

A server normally creates a socket and puts it into a listening state.

Example:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Then:

```bash
ss -tulpn | grep 8000
```

can show:

```text
tcp LISTEN 0 5 127.0.0.1:8000 0.0.0.0:* users:(("python3",pid=6885,fd=3))
```

Interpretation:

```text
TCP
 ↓
LISTEN
 ↓
127.0.0.1:8000
 ↓
owned by python3
 ↓
PID 6885
 ↓
FD 3
```

---

# `ss`

`ss` is a Linux utility for inspecting sockets.

Common commands:

```bash
ss -tuln
```

Show listening TCP/UDP sockets without resolving names.

```bash
ss -tulpn
```

Additionally show the process owning the socket.

Options:

```text
-t → TCP
-u → UDP
-l → listening
-n → numeric output
-p → process information
```

---

# Process ↔ Socket Relationship

A network service can be traced from the network side to the process side.

For example:

```text
127.0.0.1:8000
       ↓
TCP listening socket
       ↓
python3
       ↓
PID 6885
       ↓
FD 3
```

The process's `/proc` directory can confirm the file descriptor:

```bash
ls -l /proc/6885/fd
```

Result:

```text
3 -> socket:[66597]
```

This gives two complementary views:

### Network view

```bash
ss -tulpn
```

Answers:

> Which process owns this network endpoint?

### Process view

```bash
ls -l /proc/<PID>/fd
```

Answers:

> What resources does this process have open?

Together they provide a powerful way to investigate network activity.

---

# Loopback

IPv4:

```text
127.0.0.1
```

is the loopback address.

Traffic sent to `127.0.0.1` stays within the local machine.

Example:

```text
127.0.0.1:8000
```

means the service is bound to the local machine's loopback interface.

This is different from:

```text
192.168.x.x:8000
```

which may make the service reachable through the machine's network interface, depending on routing and firewall rules.

---

# Security Perspective

When investigating a Linux system, an important question is:

> Which processes are listening for network connections?

A basic investigation can begin with:

```bash
ss -tulpn
```

Then identify the process:

```bash
ps -p <PID> -o pid,ppid,user,cmd
```

Then inspect its resources:

```bash
ls -l /proc/<PID>/fd
```

This creates a useful investigation chain:

```text
Network endpoint
      ↓
Socket
      ↓
Process
      ↓
PID
      ↓
User
      ↓
Process resources
```

This is foundational for later network reconnaissance, incident investigation, and security testing.

A listening port alone does not establish that a service is vulnerable. It identifies an endpoint that can be investigated further.


# TCP, UDP & Wireshark

## TCP Connections

TCP (Transmission Control Protocol) is a connection-oriented transport-layer protocol.

TCP provides:

* Reliable delivery
* Ordered delivery
* Retransmission of lost data
* Error detection
* A byte-stream abstraction
* Connection state between endpoints

A TCP connection can be viewed using its endpoints:

```text
Client IP : Client Port
        ↕
Server IP : Server Port
```

Example:

```text
127.0.0.1:45122
       ↕
127.0.0.1:8000
```

The server can continue listening on port `8000` while different clients use different ephemeral source ports.

---

## Listening Sockets

A server normally creates a socket and puts it into a listening state.

Example:

```bash
ss -tulpn | grep 8000
```

Example output:

```text
tcp   LISTEN   0   5   127.0.0.1:8000   0.0.0.0:*
users:(("python3",pid=6885,fd=3))
```

Interpretation:

```text
Protocol: TCP
State: LISTEN
Server IP: 127.0.0.1
Server Port: 8000
Process: python3
PID: 6885
File Descriptor: 3
```

This connects the Linux and networking models:

```text
Process
   ↓
File Descriptor
   ↓
Socket
   ↓
TCP endpoint
   ↓
IP + Port
```

---

## TCP Three-Way Handshake

Before normal TCP data exchange, the endpoints establish connection state through a handshake.

The basic sequence is:

```text
Client                         Server

  | -------- SYN ------------> |
  |                            |
  | <------ SYN + ACK -------- |
  |                            |
  | -------- ACK ------------> |
  |                            |
        Connection established
```

### SYN

SYN is a TCP flag used when initiating a connection.

### SYN-ACK

The server acknowledges the client's SYN and sends its own SYN.

### ACK

The client acknowledges the server's SYN.

The handshake establishes the initial state required for the TCP connection.

---

## TCP Flags

Important TCP flags include:

| Flag | Purpose                                                            |
| ---- | ------------------------------------------------------------------ |
| SYN  | Initiates/synchronizes a connection                                |
| ACK  | Acknowledges received TCP information                              |
| FIN  | Indicates an endpoint wants to finish the connection               |
| RST  | Abruptly resets a connection                                       |
| PSH  | Requests that buffered data be passed to the receiving application |
| URG  | Indicates urgent-pointer information                               |

At this stage, focus primarily on:

```text
SYN
ACK
FIN
RST
```

---

## Ephemeral Ports

A client usually does not use the server's well-known/listening port as its source port.

Instead, the operating system assigns a temporary source port called an **ephemeral port**.

Example:

```text
Client: 127.0.0.1:45122
Server: 127.0.0.1:8000
```

Here:

```text
45122 → ephemeral client port
8000  → server listening port
```

This allows many clients to communicate with the same server port.

---

## TCP Connection Termination

TCP connections also maintain state when they are closed.

A simplified view is:

```text
Client                         Server

  | -------- FIN ------------> |
  | <--------- ACK ----------- |
  | <--------- FIN ----------- |
  | -------- ACK ------------> |
```

The exact exchange can vary depending on which side closes first and the connection state.

The important idea is:

> TCP explicitly manages connection state from establishment through termination.

---

# UDP

UDP (User Datagram Protocol) is a transport-layer protocol.

Unlike TCP, UDP does not establish a TCP-style connection before sending data.

UDP provides:

* Datagram-based communication
* No guarantee of delivery
* No guarantee of ordering
* No TCP-style retransmission
* Lower protocol overhead than TCP

UDP itself does not provide the reliability mechanisms that TCP provides.

A useful comparison:

```text
TCP:
Connection → reliable ordered byte stream

UDP:
Datagrams → no delivery/order guarantee from UDP
```

Do not simply remember:

> UDP = faster

The more important distinction is the **guarantees and connection state provided by the protocol**.

---

## TCP vs UDP

| TCP                  | UDP                         |
| -------------------- | --------------------------- |
| Connection-oriented  | Connectionless              |
| Reliable delivery    | No delivery guarantee       |
| Ordered byte stream  | Datagram-based              |
| Retransmission       | No UDP-level retransmission |
| TCP connection state | No TCP-style connection     |
| Three-way handshake  | No TCP handshake            |

---

# DNS Traffic

DNS (Domain Name System) translates domain names into information such as IP addresses.

Example:

```bash
nslookup example.com
```

or:

```bash
dig example.com
```

Traditionally, DNS commonly uses:

```text
UDP port 53
```

DNS can also use TCP, including situations where TCP is required by the DNS protocol or deployment.

A simplified model:

```text
Client
   ↓
DNS query
   ↓
UDP
   ↓
DNS server : 53
```

DNS can be observed in Wireshark using:

```text
dns
```

---

# ICMP and Ping

`ping` normally uses ICMP (Internet Control Message Protocol), not TCP or UDP.

Example:

```bash
ping -c 4 8.8.8.8
```

Typical IPv4 ping traffic:

```text
Echo Request
      ↓
Echo Reply
```

Important:

> ICMP does not use TCP/UDP ports.

Therefore:

```text
HTTP → TCP → port 8000
DNS  → UDP/TCP → commonly port 53
Ping → ICMP → no TCP/UDP port
```

---

# Loopback vs Network Interface

`127.0.0.1` is the IPv4 loopback address.

Traffic sent to:

```text
127.0.0.1
```

is intended for the same host.

The loopback interface is usually:

```text
lo
```

A VM's network interface may instead have an address such as:

```text
192.168.x.x
```

For example:

```text
127.0.0.1:8000
```

means the service is bound to loopback.

Another machine normally cannot reach that service through the VM's normal network interface.

---

# Wireshark

Wireshark allows network packets to be captured and inspected.

A packet can be viewed as a stack of protocol layers.

For example, HTTP over TCP over IPv4:

```text
Ethernet
   ↓
IP
   ↓
TCP
   ↓
HTTP
```

When inspecting a TCP packet, useful fields include:

```text
Source Port
Destination Port
Sequence Number
Acknowledgment Number
TCP Flags
Window
```

---

## Observing a TCP Handshake

For a local HTTP server:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Start Wireshark on:

```text
lo
```

because the server is using `127.0.0.1`.

Then generate traffic:

```bash
curl http://127.0.0.1:8000
```

A useful Wireshark filter is:

```text
tcp.port == 8000
```

The communication should conceptually look like:

```text
TCP handshake
     ↓
HTTP request
     ↓
HTTP response
     ↓
TCP connection termination
```

The handshake should contain:

```text
SYN
SYN-ACK
ACK
```

---

# Reading a Network Packet

When examining traffic, ask:

### 1. Who sent it?

Look at:

```text
Source IP
Source Port
```

### 2. Who received it?

Look at:

```text
Destination IP
Destination Port
```

### 3. Which transport protocol is being used?

```text
TCP
UDP
```

### 4. Is it another network-layer protocol?

For example:

```text
ICMP
```

### 5. Where does the packet fit in the communication?

For example:

```text
SYN
SYN-ACK
ACK
DATA
FIN
```

This is more useful than simply identifying the protocol.

---

# Useful Commands

### Show listening TCP/UDP sockets

```bash
ss -tuln
```

### Show processes using sockets

```bash
ss -tulpn
```

### Show established TCP connections

```bash
ss -tn
```

### Generate HTTP traffic

```bash
curl http://127.0.0.1:8000
```

### Generate DNS traffic

```bash
nslookup example.com
```

### Generate ICMP traffic

```bash
ping -c 4 8.8.8.8
```

---

# Security Perspective

Understanding TCP, UDP, ports and sockets is fundamental to network security.

These concepts are used later when studying:

```text
Port scanning
Service enumeration
SYN scanning
Firewall rules
SYN floods
Connection exhaustion
DNS security
Packet filtering
Network monitoring
Intrusion detection
Traffic analysis
Command-and-control traffic
Lateral movement
```

The core mental model is:

```text
Process
   ↓
Socket
   ↓
Port
   ↓
TCP / UDP
   ↓
IP
   ↓
Network Interface
   ↓
Network
```

The goal is to understand what each layer is doing rather than treating networking as a collection of commands.

---

# DNS Fundamentals

## 1. What Is DNS?

**DNS (Domain Name System)** is a distributed naming system that allows applications to look up information associated with domain names.

Humans use hostnames such as `example.com`, while network connections use IP addresses to identify destination hosts.

DNS can provide information such as IPv4 addresses, IPv6 addresses, and aliases to other hostnames.

### Simplified workflow

1. An application needs to contact a hostname.
2. The hostname is resolved through a DNS resolution process.
3. DNS records provide information about the hostname.
4. The application uses the relevant address information to establish a network connection.

**Important:** DNS resolution and establishing a network connection are separate operations.

## 2. DNS Record Types

### A record

Maps a hostname to an IPv4 address.

Example:

```text
example.com → 192.0.2.10
```

The address above is an illustrative documentation address.

### AAAA record

Maps a hostname to an IPv6 address.

Example:

```text
example.com → 2001:db8::10
```

The address above is an illustrative documentation address.

**Security relevance:** An application that checks only IPv4 addresses may overlook prohibited IPv6 destinations.

### CNAME record

Creates an alias from one hostname to another hostname.

Example:

```text
www.example.com → example.com
```

A CNAME points to another name, not directly to an IP address. The target hostname may need further resolution.

## 3. DNS Resolvers

A DNS resolver obtains DNS information for a client.

A simplified process:

1. The client requests DNS information.
2. A resolver checks whether it has a usable cached answer.
3. If necessary, the resolver obtains information from other DNS servers.
4. The resolver returns the answer to the client.

Real resolution can involve operating-system caches, recursive resolvers, authoritative servers, aliases, and multiple addresses.

## 4. TTL and DNS Caching

**TTL (Time To Live)** specifies how long a DNS record may generally be cached before it should be refreshed.

For example:

```text
TTL = 300 seconds
```

This represents five minutes.

TTL does not guarantee that every application will connect to the same IP address for that entire period. Applications and resolvers can have different caching behavior or resolution paths.

## 5. Multiple DNS Answers

One hostname can resolve to multiple IP addresses.

Possible reasons include:

- Load balancing.
- Redundancy and failover.
- Geographic distribution.
- IPv4 and IPv6 support.

A security-sensitive application must evaluate the relevant set of addresses against its destination policy instead of blindly trusting the first result.

---

# DNS and Web Security

## 6. Hostname Validation vs. Destination Validation

These are different checks.

**Hostname validation** determines whether the supplied hostname or URL meets the application's input rules.

**Destination validation** determines whether the network destination is permitted by the application's security policy.

A syntactically valid hostname is not necessarily safe to contact.

A DNS lookup that returns a public address also does not prove that a later connection will use that address.

## 7. TOCTOU: Time of Check to Time of Use

TOCTOU is a class of problem in which a condition changes between the time it is checked and the time it is used.

Consider this simplified workflow:

1. An application resolves a hostname.
2. It checks that the resulting IP address is allowed.
3. The application later makes a network connection.
4. The HTTP client performs another DNS lookup.
5. The new result differs from the previously checked address.

If the actual connection is not constrained by the security check, the earlier validation may no longer protect the application.

**Key lesson:** A security check must enforce the property that matters at the point where the protected operation occurs.

## 8. DNS Rebinding

DNS rebinding is a technique in which a hostname resolves to different IP addresses over time.

In a vulnerable application, changing DNS answers can undermine assumptions made during hostname or destination validation.

### Hypothetical example

1. A hostname resolves to a public IP address.
2. The application allows the hostname.
3. A later lookup returns a prohibited address.
4. The application connects to that address without enforcing its destination policy.

Whether this is exploitable depends on the application's implementation and environment.

### Related risks

- Loopback addresses.
- Private IPv4 and IPv6 addresses.
- Link-local addresses.
- Cloud metadata endpoints.
- Redirects to prohibited destinations.
- IPv4/IPv6 handling inconsistencies.
- Multiple DNS answers containing both allowed and prohibited addresses.

## 9. Redirects and Destination Safety

An HTTP redirect instructs a client to request another URL.

A destination that was allowed initially does not automatically make the redirected destination safe.

A robust implementation must validate each redirect destination before connecting to it.

WebCheck Report currently reports redirects without automatically following them. This reduces redirect-related risk, but does not by itself eliminate DNS-rebinding or connection-time destination risks.

## 10. Secure Connection Design

A robust destination-security design must enforce its policy on the address actually used by the network connection.

It must also preserve normal HTTPS behavior:

- **TLS SNI:** The intended hostname is used during TLS negotiation.
- **Certificate verification:** The certificate is verified against the intended hostname.
- **HTTP Host header:** The request uses the correct hostname.
- **Redirect handling:** Each new destination is validated independently.

Simply replacing a hostname with an IP address in a URL can break TLS verification or change application behavior.

DNS validation alone is not a complete security boundary. Connection-time enforcement and, where appropriate, network egress restrictions may also be necessary.

---

# Practical Commands

These commands will be used in Session 2 to investigate DNS and HTTP behavior.

```bash
dig example.com A
dig example.com AAAA
dig example.com CNAME
curl -v --connect-timeout 5 https://example.com/
```

If `dig` is unavailable on Ubuntu:

```bash
sudo apt update
sudo apt install dnsutils
```

Remember that a separate `dig` lookup does not prove which address `curl` or a Python HTTP client ultimately uses. Different clients may use different resolution paths or cached results.

With Wireshark, DNS and TCP traffic may be observable where the capture point permits it. HTTPS application data is encrypted, so an ordinary packet capture will not reveal the full HTTP response body.

---

# Key Takeaways

1. DNS maps names to information such as IP addresses and aliases.
2. A records represent IPv4 addresses; AAAA records represent IPv6 addresses.
3. CNAME records point to other hostnames.
4. TTL controls DNS record caching, not the lifetime of a network connection.
5. A hostname can have multiple IP addresses.
6. Hostname validation and destination validation are different.
7. DNS answers can change between a security check and a connection.
8. DNS rebinding can exploit unsafe assumptions about hostname resolution.
9. Redirects must be treated as new destinations.
10. A robust security policy must constrain the actual connection while preserving TLS verification.

## Review Questions

1. What is the difference between an A record and an AAAA record?
2. What does a CNAME point to?
3. What does DNS TTL control?
4. Why might a hostname resolve to multiple addresses?
5. Explain TOCTOU in the context of DNS resolution.
6. What is DNS rebinding?
7. Why is checking a DNS answer once insufficient to guarantee destination safety?
8. Why must HTTPS certificate verification remain enabled when connecting to a validated IP?
9. Why must redirect destinations be validated independently?
10. What must a secure HTTP client enforce at connection time?

---


---

# Practical Investigation: DNS, HTTPS and Wireshark

This section records a practical investigation using `dig`, `curl`, and Wireshark. Keep observed results separate from interpretation, and update the evidence record if a later run returns different addresses, TTLs, or headers.

## 1. DNS Lookups with `dig`

### Commands used

```bash
dig -v
dig example.com A +noall +answer
dig example.com AAAA +noall +answer
dig www.example.com CNAME +noall +answer
```

The installed version reported:

```text
DiG 9.18.39-0ubuntu0.24.04.8-Ubuntu
```

### Observed A records

```text
example.com.        5    IN    A    172.66.147.243
example.com.        5    IN    A    104.20.23.154
```

`A` records provide IPv4 address information. Two IPv4 answers were returned in this run.

### Observed AAAA records

```text
example.com.        5    IN    AAAA    2606:4700:10::6814:179a
example.com.        5    IN    AAAA    2606:4700:10::ac42:93f3
```

`AAAA` records provide IPv6 address information. Two IPv6 answers were returned in this run.

### Interpreting the answer fields

For this record:

```text
example.com.    5    IN    A    172.66.147.243
```

- `example.com.` is the record name.
- `5` is the record TTL, in seconds, at the time of the query.
- `IN` is the Internet DNS class.
- `A` is the record type.
- `172.66.147.243` is the IPv4 address in that answer.

The displayed TTL was `5` seconds for the records shown. DNS answers and TTLs can change, so treat these as observations from this run, not permanent values.

The CNAME command produced no answer in the displayed output. That alone does not prove a DNS failure; the queried name may not have a CNAME record. If needed, inspect the full `dig` response and its status separately.

## 2. HTTPS Request with `curl`

### Command used

```bash
curl -v --connect-timeout 5 https://example.com/ -o /dev/null
```

- `-v` displays verbose connection and protocol information.
- `--connect-timeout 5` sets a five-second connection timeout.
- `-o /dev/null` discards the response body instead of saving it.

### Relevant observed lines

```text
Host example.com:443 was resolved.
Trying 104.20.23.154:443...
Connected to example.com (104.20.23.154) port 443
TLSv1.3
SSL certificate verify ok.
using HTTP/2
< HTTP/2 200
```

Interpretation:

1. `curl` obtained address information for `example.com`.
2. It attempted to connect to `104.20.23.154` on port `443`.
3. The connection succeeded.
4. TLS version 1.3 was negotiated.
5. Certificate verification succeeded according to `curl`, including a hostname match for `example.com`.
6. The request used HTTP/2 and received a successful HTTP response with status `200`.

This does not prove the website is free of vulnerabilities. It documents the connection and response observed in this test.

### Response headers

A second command was used to display response headers without printing the body:

```bash
curl -sS -D - -o /dev/null https://example.com/
```

Some observed headers were:

```text
HTTP/2 200
content-type: text/html; charset=utf-8
server: cloudflare
last-modified: Tue, 13 Oct 2026 22:05:48 GMT
allow: GET, HEAD
accept-ranges: bytes
cf-cache-status: HIT
alt-svc: h3=":443"; ma=86400
```

Headers can vary between requests. `content-type: text/html; charset=utf-8` declares HTML content encoded as UTF-8. The `200` status indicates a successful HTTP response; neither the status nor the headers establish that the application is secure.

## 3. Wireshark Capture: DNS Query and Response

### Capture setup

- Capture interface: `ens33`
- Display filter used: `dns`
- Test hostname: `example.com`

The `dns` filter showed four rows:

1. One A query.
2. One A response.
3. One AAAA query.
4. One AAAA response.

This is two DNS question-and-answer pairs. It does not mean the website was contacted twice; DNS lookup and HTTP communication are separate activities.

### Wireshark panes

1. **Packet List:** The top pane. Start by checking Time, Source, Destination, Protocol, Length, and Info.
2. **Packet Details:** The middle pane. Select a row and expand protocol sections to inspect decoded fields.
3. **Packet Bytes:** The bottom pane. Shows raw bytes in hexadecimal and a text representation where possible. It is not necessary to interpret this pane during the first DNS exercise.

### Inspect a DNS query

Apply this display filter:

```text
dns
```

Select the A query and expand **Domain Name System (query)**. Inspect:

- **Queries → Name:** the queried hostname.
- **Queries → Type:** the requested record type, such as `A` or `AAAA`.
- **Transaction ID:** useful for correlating a query with its response.
- **Flags:** query-related information and options.

Then select the AAAA query and confirm its requested record type.

### Inspect a DNS response

Select the response matching the query and expand **Domain Name System (response)**. Inspect:

- **Transaction ID:** compare it with the query.
- **Response Code:** whether the resolver reported a DNS error.
- **Answers:** returned records, if present.
- **Record Type and address/name value:** what the response returned.
- **Time to live (TTL):** the TTL attached to each answer.
- **Answer count:** how many answer records are included.

Useful response-code interpretation:

- `NOERROR`: no DNS error was reported; an answer is not guaranteed to exist.
- `NXDOMAIN`: the queried name does not exist according to that DNS response.

**Evidence still to fill in:** the exact Name, Type, Response Code, answer values, and TTLs from the selected Wireshark packets have not yet been recorded in this note. Read these fields from the capture rather than assuming the Wireshark values match a separate `dig` query.

## 4. Wireshark Fields for Other Protocols

### Packet list fields

| Field | What it tells you |
|---|---|
| Time | When the packet was captured; useful for ordering events |
| Source | Source address shown for the packet |
| Destination | Destination address shown for the packet |
| Protocol | Protocol Wireshark recognizes |
| Length | Packet length in bytes |
| Info | Brief protocol-specific summary |

One packet is only one piece of evidence. A field that looks unusual is not automatically proof of malicious activity.

### IP fields

Filters:

```text
ip.version == 4
ipv6
```

Inspect Source Address, Destination Address, TTL (IPv4) or Hop Limit (IPv6), and Protocol/Next Header. These fields help identify endpoints and the next protocol carried by the packet.

### TCP fields

Filter:

```text
tcp
```

Inspect:

- Source Port and Destination Port.
- Flags, particularly SYN, ACK, FIN, and RST.
- Sequence Number and Acknowledgment Number.
- Window Size.
- Retransmission indicators, if Wireshark reports them.

A typical TCP handshake is `SYN` → `SYN, ACK` → `ACK`. A missing packet in a capture does not necessarily mean a handshake failed; the capture may have started late or missed traffic.

Useful filters:

```text
tcp.flags.syn == 1 && tcp.flags.ack == 0
tcp.flags.reset == 1
tcp.analysis.retransmission
tcp.port == 443
```

The first filter displays initial SYN packets without ACK. The second displays TCP reset packets. The third displays packets Wireshark identifies as retransmissions. The last displays TCP packets with port 443 as either source or destination.

### UDP fields

Filter:

```text
udp
```

Inspect Source Port, Destination Port, Length, and Checksum. Traditional DNS commonly uses UDP port 53, though DNS can also use TCP and other transport mechanisms.

For DNS-over-UDP packets:

```text
dns && udp
```

### TLS fields

Filter:

```text
tls
```

When visible, inspect Client Hello, Server Hello, handshake message type, supported versions, Server Name Indication (SNI), and TLS alerts.

TLS 1.3 encrypts most handshake messages after Server Hello. A normal capture may not expose the certificate or all handshake details. HTTPS application data is encrypted, so the HTTP request and response contents generally cannot be read from the capture without suitable decryption material.

### HTTP fields

Filter:

```text
http
```

This works when Wireshark can recognize visible HTTP traffic. Ordinary HTTPS traffic is encrypted, so this filter may not show the HTTP messages from an HTTPS request.

For visible HTTP, inspect Request Method, Host, Request URI, Status Code, Content-Type, User-Agent, Location (if a redirect is returned), and Content-Length (when present). HTTP/2 uses pseudo-headers such as `:method`, `:path`, and `:authority`; these are normally encrypted when HTTP/2 is carried over HTTPS.

## 5. Useful Display Filters Reference

Display filters affect which packets are shown, not whether the packets remain in the capture.

| Purpose | Filter |
|---|---|
| DNS | `dns` |
| IPv4 | `ip.version == 4` |
| IPv6 | `ipv6` |
| TCP | `tcp` |
| UDP | `udp` |
| TLS | `tls` |
| Visible HTTP | `http` |
| DNS over UDP | `dns && udp` |
| Traffic to or from one IPv4 address | `ip.addr == 192.0.2.10` |
| TCP traffic using port 443 | `tcp.port == 443` |
| Initial TCP SYN packets | `tcp.flags.syn == 1 && tcp.flags.ack == 0` |
| TCP reset packets | `tcp.flags.reset == 1` |
| TCP retransmissions recognized by Wireshark | `tcp.analysis.retransmission` |

`192.0.2.10` is a documentation example; replace it with an address from your own capture if needed.

## 6. Repeatable Packet Investigation Workflow

For a small capture, use this order:

1. Identify the interface and the action that generated the traffic.
2. Look at Time, Source, Destination, Protocol, Length, and Info in the Packet List.
3. Select a relevant packet and expand the matching protocol in Packet Details.
4. For DNS, compare a query with its response and record the requested name/type, response code, answer and TTL.
5. For TCP, check ports, flags, and whether the handshake is visible.
6. For TLS, note which handshake metadata is visible and remember that much of TLS 1.3 is encrypted.
7. For HTTP, inspect methods, paths, headers, and status codes only when the content is visible.
8. Write down what you actually observed separately from your interpretation.
9. Record missing information and capture limitations instead of guessing.

## 7. Experiment Record — Current Findings

**Environment:** Ubuntu environment

**Capture interface:** `ens33`

**Target:** `example.com`

### Confirmed from terminal output

- The `dig` version was `9.18.39-0ubuntu0.24.04.8-Ubuntu`.
- Two A answers and two AAAA answers were returned by the displayed DNS queries.
- The displayed TTL for the records was 5 seconds at the time of those queries.
- The CNAME lookup for `www.example.com` printed no answer in the displayed output.
- `curl` connected to `104.20.23.154` on port 443.
- TLS 1.3 was negotiated and certificate verification succeeded for `example.com`.
- The HTTP response was `HTTP/2 200`.
- A response header declared `content-type: text/html; charset=utf-8`.

### Confirmed from Wireshark

- Interface: `ens33`.
- With display filter `dns`, four rows appeared: one A query and response, and one AAAA query and response.

### To complete after inspecting Packet Details

- A query: Name and Type.
- A response: Transaction ID, Response Code, answer values and TTL.
- AAAA query: Name and Type.
- AAAA response: Transaction ID, Response Code, answer values and TTL.
- If visible, record the TCP handshake packets and port 443 endpoints for the HTTPS request.
- Record which TLS details were visible in the capture.

## 8. Security Notes

- DNS resolution and establishing a network connection are separate operations.
- A hostname can resolve to multiple IPv4 and IPv6 addresses.
- A DNS answer does not guarantee which address a client ultimately connects to.
- A pre-connection DNS check alone does not eliminate DNS-rebinding or time-of-check-to-time-of-use (TOCTOU) risks if a client resolves the hostname again at connection time.
- Each redirect is a new destination and should be checked independently by security-sensitive HTTP clients.
- Secure destination enforcement must apply to the actual connection while preserving TLS SNI, certificate verification for the intended hostname, and the correct HTTP Host/authority value.
- An HTTP 200 response, a valid TLS certificate, or a successful connection does not prove that the target website is free of vulnerabilities.
- Use captures only on networks and systems where you have authorization. Captures can contain sensitive addresses and metadata; avoid publishing them unnecessarily.

---

# SSRF, DNS Rebinding & Safe URL Fetching

## 1. Server-Side Request Forgery (SSRF)

**SSRF (Server-Side Request Forgery)** is a vulnerability in which a user can influence an application or server to make a request to an unintended destination.

A common example is a website-preview feature:

1. A user submits a URL.
2. The application server fetches that URL.
3. The server returns information about the page.

This is a normal feature when appropriately restricted. It becomes an SSRF risk if an attacker can make the server contact destinations the feature should not reach.

### Why SSRF can be dangerous

The request is made by the application server, not directly by the user's browser. The server may have network access to internal services or resources unavailable to an ordinary Internet user.

Examples of destinations a security-sensitive URL fetcher may need to prohibit include:

- The server itself through a loopback address.
- Private-network services.
- Link-local addresses and cloud metadata services.
- Other special-purpose or otherwise prohibited IPv4/IPv6 destinations.

A request to an internal address is not automatically a vulnerability. The risk depends on the application's access, its behavior, and the security policy it is supposed to enforce.

## 2. Understanding Internal Destinations

### Loopback

IPv4 loopback includes `127.0.0.1`. It refers to the same machine that makes the request.

If a URL-fetching application running on a remote server requests `127.0.0.1`, that address refers to the application server itself—not the user's laptop.

### Private IPv4 addresses

Common private IPv4 ranges include:

```text
10.0.0.0/8
172.16.0.0/12
192.168.0.0/16
```

These addresses are commonly used inside private networks.

### Link-local addresses

`169.254.0.0/16` is the IPv4 link-local range. Cloud environments may expose metadata services at link-local addresses; a vulnerable server-side URL fetcher might be able to reach such services.

### IPv6 and special-purpose addresses

A URL-fetching security policy must consider IPv6 as well as IPv4. Checking only private IPv4 ranges is insufficient. The policy should account for loopback, link-local, private/local, multicast, unspecified, and other special-purpose addresses as appropriate to the application.

**Important:** An address classification policy should be based on a reliable IP-address library and a clearly defined security policy, rather than ad-hoc string comparisons.

## 3. URL Validation vs. Destination Validation

These are separate checks.

- **URL validation:** Determines whether the input is a syntactically valid URL and follows the application's accepted URL rules.
- **Destination validation:** Determines whether the IP destination is allowed by the application's policy.
- **Connection-time enforcement:** Ensures the actual network connection uses a destination permitted by that policy.

A URL being syntactically valid does not mean it is safe to fetch. A hostname resolving to a public IP during one lookup does not guarantee a later connection will use that same address.

### Limit accepted schemes

For a tool intended to check web URLs, accept only the schemes it needs:

```text
http://
https://
```

Reject unsupported schemes such as `file://` and any other scheme not deliberately supported. Do not enable extra client capabilities that the application does not require.

HTTP is unencrypted in transit; HTTPS uses TLS. Supporting HTTP does not remove the need for destination validation.

## 4. DNS Rebinding

**DNS rebinding** is a technique in which a hostname is made to resolve to different IP addresses over time. In some applications, this can undermine assumptions made during URL or destination validation.

A simplified hypothetical sequence:

1. An application resolves a hostname.
2. The first DNS answer contains a permitted public address.
3. The application approves that answer.
4. Later, the HTTP client resolves the same hostname again.
5. The later answer differs and contains a prohibited address.
6. If the HTTP client connects without re-enforcing the destination policy, the earlier check may not protect the connection.

This is related to **TOCTOU (Time Of Check to Time Of Use)**: a relevant condition changes between the time it is checked and the time it is used.

DNS rebinding is not automatically an exploitable SSRF vulnerability. Exploitability depends on the client's implementation, the timing and resolution behavior, and the server's network access.

## 5. Multiple DNS Answers

One hostname can resolve to multiple IPv4 or IPv6 addresses. This may be used for redundancy, load balancing, or other legitimate reasons.

A security-sensitive URL fetcher should:

1. Resolve the hostname to the relevant IPv4 and IPv6 addresses.
2. Classify every returned address against its destination policy.
3. Apply a clearly defined rule to mixed responses.
4. Ensure the actual connection uses only an address that passed the policy.

A conservative policy is to reject the hostname when any returned address is prohibited, rather than let the HTTP client choose an unchecked address from a mixed result. A different design must still ensure no connection can be made to a prohibited address.

Checking only the first address, or checking only IPv4, can leave gaps.

## 6. The Actual Connection Must Enforce the Policy

A DNS lookup and an HTTP connection are separate operations. A common risk is:

1. The application resolves a hostname and checks the result.
2. The HTTP client performs a separate lookup during connection establishment.
3. The client connects to a different result from the address that was checked.

The central defensive principle is:

> Do not merely check an address before connecting. Ensure the actual connection uses a validated, permitted address.

The networking implementation must avoid unchecked re-resolution changing the destination between validation and connection. Connection retries and address-selection/fallback behavior must also remain within the same policy.

A pre-connection DNS check alone is not a complete security boundary.

## 7. Preserve HTTPS Hostname Verification

Destination IP and website identity are different concepts. If a client connects to a validated IP for `example.com`, it must still preserve the intended hostname for HTTPS.

| Item | Purpose |
|---|---|
| Validated IP address | Determines the network destination |
| TLS SNI hostname | Indicates the intended hostname during the TLS handshake, when SNI is used |
| Certificate verification hostname | The hostname against which the TLS certificate is verified |
| HTTP `Host` header / HTTP/2 `:authority` | Identifies the intended hostname at the HTTP layer |

For a request to `https://example.com/`, the intended hostname remains `example.com` even if the connection is directed to a validated IP address.

Do **not** solve destination validation by disabling TLS certificate verification. That would remove an important protection and could expose the client to interception or impersonation.

## 8. Redirects Are New Destinations

An HTTP redirect can instruct a client to request a different URL, commonly through the `Location` response header.

For example, a response might contain:

```text
HTTP/1.1 302 Found
Location: https://another-site.example/
```

If an HTTP client follows redirects automatically, it may make a second request to the new destination. A destination that passed the first check does not make the redirected destination safe.

A security-sensitive implementation should validate each new destination before connecting. It should also ensure redirect handling cannot bypass scheme rules, DNS checks, or connection-time enforcement.

WebCheck Report currently reports redirects without automatically following them. That avoids making the redirected request automatically, but it does not by itself eliminate DNS-rebinding or other destination risks in the initial request.

## 9. Allowlisting vs. Blocklisting

### Allowlist

An allowlist permits only specifically approved destinations, for example a small set of known API hostnames. It is well suited to applications that only need to contact a fixed set of services.

### Blocklist

A blocklist rejects known prohibited destinations while allowing other destinations. It may fit a general-purpose public URL checker better than a tiny hostname allowlist, but it can be incomplete if it misses an address category or edge case.

For a tool designed to check many public websites, destination block rules still need robust IP classification and connection-time enforcement. Neither an allowlist nor a blocklist should be treated as a substitute for ensuring that the actual connection obeys the policy.

## 10. Fail Closed

**Fail closed** means refusing the protected operation when a required security check cannot be completed.

For example, if the application cannot resolve or classify a destination well enough to determine that it is permitted, it should not make the request anyway.

Failing closed does not mean assuming every network error is malicious. It means not proceeding when a required security condition remains unverified.

## 11. Defense in Depth

Defense in depth uses multiple protective controls because each addresses a different failure mode.

For a server-side URL checker, layers may include:

1. Validate the URL syntax and allow only intended schemes.
2. Resolve and classify all relevant IPv4/IPv6 addresses.
3. Apply a clear policy to prohibited and mixed DNS answers.
4. Enforce the policy on the actual connection and all retry/fallback paths.
5. Do not automatically follow redirects unless every new destination is validated.
6. Preserve TLS SNI and certificate verification for the intended hostname, plus the correct HTTP Host/authority value.
7. Where appropriate, use network egress controls to restrict what the application server can reach.
8. Test expected and adversarial cases; document what the tests do and do not demonstrate.

Passing a unit-test suite is useful evidence, but it does not by itself prove production security.

## 12. Applying This to WebCheck Report

### Behaviors already established from earlier project work

- The tool accepts URLs for HTTP/HTTPS diagnostics.
- It validates URL inputs.
- It resolves hostnames and rejects non-public IP addresses according to its existing network-safety check.
- It reports redirects without automatically following them.
- Automated tests were previously reported as passing, but passing tests alone do not establish complete SSRF resistance.

### Important concern still requiring verification

The existing design was identified as potentially vulnerable to a time-of-check-to-time-of-use gap: the application checks DNS answers, but the HTTP client may resolve the hostname again when connecting. This concern has not been confirmed through an exploit test in this note, and no complete fix is claimed here.

Before describing the tool as hardened, inspect and test whether the actual connection is guaranteed to use only a validated address while preserving hostname-based TLS verification and HTTP Host/authority behavior. Also test IPv4/IPv6 handling, mixed DNS answers, redirects, and relevant retry/fallback behavior.

### Safe development approach

- Use mock resolvers and controlled local test fixtures to test policy decisions.
- Add tests for public addresses, prohibited address classes, mixed answers, DNS errors, and redirect behavior.
- Verify which address the connection actually uses, rather than inferring it only from an earlier DNS lookup.
- Keep TLS certificate verification enabled.
- Document implementation limitations and avoid production-security claims until the relevant behavior is verified.

Only test against systems and networks you own or have explicit permission to assess.

## 13. Review Questions

1. What is SSRF, and why does the request's server-side origin matter?
2. If a server-side application requests `127.0.0.1`, which machine does that address refer to?
3. How are URL validation, destination validation, and connection-time enforcement different?
4. What is DNS rebinding?
5. What does TOCTOU mean in the context of DNS resolution?
6. Why must a URL checker consider both IPv4 and IPv6?
7. Why can multiple DNS answers create a destination-validation challenge?
8. Why must every redirect destination be checked separately?
9. What are the differences between allowlisting and blocklisting?
10. What does fail closed mean?
11. Why should TLS certificate verification remain enabled when connecting to a validated IP?
12. What still needs to be verified in WebCheck Report before claiming that its destination handling is hardened?

## Key Takeaway

SSRF prevention is not just about rejecting suspicious URL strings. A secure URL-fetching service must control where the server is actually allowed to connect, account for DNS answers and changes, validate each redirect destination, preserve HTTPS hostname verification, and fail safely when required security checks cannot be completed.

---

# SSRF and Localhost

## Server-Side Request Forgery (SSRF)

**Definition:** SSRF is a vulnerability in which user-influenced input causes a server-side application to make a request to an unintended destination. The destination may be an internal service, the application itself, or an external system.

### Client-side vs server-side perspective

- When my browser requests `http://localhost/...`, `localhost` normally refers to the machine running my browser.
- When a vulnerable application on a remote server requests `http://localhost/...` on my behalf, `localhost` refers to the machine or network namespace making that server-side connection.
- Therefore, in an SSRF test, `localhost` can reach a service local to the vulnerable server even though it does not point to my own computer.

### Lab example: `stockApi`

In PortSwigger's **Basic SSRF against the local server** lab, the product stock-check request was `POST /product/stock`. Its `stockApi` parameter controlled the URL that the application fetched.

Observed experiments:

| Input | Observation | Interpretation |
|---|---|---|
| `https://host/admin` | `401` | Unauthorized response for that attempt; not enough on its own to identify the exact cause. |
| `https://local/admin` | `500` | Server error; the status alone did not explain what failed. |
| `http://localhost/admin` | `200` plus admin HTML | The response body showed that the local admin interface had been reached through the stock-check feature. |
| `http://localhost/admin/delete?username=carlos` | `302`, followed by the lab's solved message | The lab confirmed that the delete action succeeded. A redirect status alone is not proof of success. |

The important clue was the combination of a user-controlled URL parameter and a response containing the internal admin page. The server performed the request; the browser was only sending the stock-check request to the vulnerable application.

### Common SSRF risk areas

- URL importers, image fetchers, webhooks, document previewers, stock checks, and other features that fetch user-supplied URLs.
- Internal-only admin pages or services that trust requests from local interfaces.
- Redirects that lead to a different destination after the initial URL is validated.
- DNS names that resolve to multiple addresses or change between validation and connection.

### Defense concepts to remember

1. Restrict URL schemes, hosts, and ports to what the feature actually requires; prefer a strict allowlist when feasible.
2. Resolve and validate all relevant IPv4 and IPv6 destinations, and prohibit loopback, private, link-local, multicast, unspecified, and other disallowed address ranges.
3. Enforce the destination policy at connection time, not only during an earlier DNS lookup; preserve TLS certificate verification and hostname/SNI behavior.
4. Disable redirects where they are not needed or revalidate every redirect destination.
5. Use outbound network controls to prevent the application from reaching sensitive internal networks and services.
6. Require authentication and authorization for administrative actions even when requests originate locally.

### Connection to DNS and TOCTOU

A DNS name can resolve to one IP during validation and a different IP when the HTTP client connects. This is a time-of-check/time-of-use (TOCTOU) risk and can contribute to DNS-rebinding-style SSRF. A robust defense must ensure that the actual peer address is permitted, not merely that an earlier DNS result looked safe. Mixed A/AAAA answers and redirects also need consistent policy enforcement.

### Testing habit

Change one input at a time and compare both the response status and response body. A `200`, `302`, `401`, or `500` is evidence, but none should be interpreted in isolation. Confirm the application behavior and, in a training lab, the platform's success indicator.

---
