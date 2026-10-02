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
