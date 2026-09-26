# Linux Commands

| Command / Path       | Description                                                                                     | Example                                 |
| -------------------- | ----------------------------------------------------------------------------------------------- | --------------------------------------- |
| `pwd`                | Prints the current working directory                                                            | `pwd`                                   |
| `whoami`             | Displays the username of the current user                                                       | `whoami`                                |
| `id`                 | Displays the current user's UID, GID, and group memberships                                     | `id`                                    |
| `hostname`           | Displays the system's hostname                                                                  | `hostname`                              |
| `uname -a`           | Displays kernel and system information, including kernel version and architecture               | `uname -a`                              |
| `/etc/os-release`    | Contains information identifying the Linux distribution and version                             | `cat /etc/os-release`                   |
| `ip addr`            | Displays network interfaces and their IP addresses                                              | `ip addr`                               |
| `ip route`           | Displays the system's IP routing table, including the default gateway                           | `ip route`                              |
| `ss -tulpn`          | Displays listening TCP/UDP sockets and, when permitted, the processes associated with them      | `sudo ss -tulpn`                        |
| `ps`                 | Displays processes associated with the current terminal/session                                 | `ps`                                    |
| `ps aux`             | Displays detailed information about running processes for all users                             | `ps aux`                                |
| `ps -p`              | Displays information about a specific process ID                                                | `ps -p 3963`                            |
| `ps -p <PID> -o ...` | Displays selected information about a specific process using custom columns                     | `ps -p 3963 -o pid,ppid,user,group,cmd` |
| `top`                | Provides a real-time view of running processes and system resource usage                        | `top`                                   |
| `echo $SHELL`        | Displays the shell configured in the `SHELL` environment variable                               | `echo $SHELL`                           |
| `ls`                 | Lists files and directories                                                                     | `ls`                                    |
| `ls -la`             | Lists all files, including hidden files, with detailed information                              | `ls -la`                                |
| `ls -l`              | Lists files and directories with permissions, ownership, size, and timestamps                   | `ls -l /path/to/directory`              |
| `ls -l /proc/<PID>`  | Lists the process-specific files and directories exposed through `/proc`                        | `ls -l /proc/3963`                      |
| `mkdir`              | Creates a directory                                                                             | `mkdir projects`                        |
| `mkdir -p`           | Creates a directory and any required parent directories                                         | `mkdir -p ~/cyber-lab/notes`            |
| `cd`                 | Changes the current working directory                                                           | `cd /tmp`                               |
| `cat`                | Displays the contents of a file or input stream                                                 | `cat /etc/os-release`                   |
| `head`               | Displays the first lines of a file or command output                                            | `head /proc/3963/maps`                  |
| `grep`               | Searches text for lines matching a specified pattern                                            | `grep "error" logfile.txt`              |
| `grep -E`            | Searches text using extended regular expressions                                                | `grep -E '^(Name\|Pid):' file`          |
| `tr`                 | Translates, replaces, or removes characters from input                                          | `tr '\0' ' ' < /proc/3963/cmdline`      |
| `readlink`           | Displays the target of a symbolic link                                                          | `readlink /proc/3963/exe`               |
| `pstree`             | Displays running processes as a parent-child process tree                                       | `pstree -p 3736`                        |
| `sleep`              | Suspends execution for a specified amount of time; useful for creating a temporary test process | `sleep 60`                              |
| `nano`               | Opens the Nano text editor in the terminal                                                      | `nano ~/cyber-lab/notes/day1.md`        |
| `sudo`               | Executes a command with elevated privileges when the current user is authorized                 | `sudo ss -tulpn`                        |

## `/proc` Process Information

The following are **not commands**. They are files/directories exposed through Linux's `/proc` (procfs) interface and provide information about running processes.

| Path                  | Description                                                                                                        | Example                   |
| --------------------- | ------------------------------------------------------------------------------------------------------------------ | ------------------------- |
| `/proc/<PID>/cmdline` | Provides the command-line arguments associated with a process                                                      | `cat /proc/3963/cmdline`  |
| `/proc/<PID>/status`  | Provides detailed information about a process, including its state, PID, PPID, UID, GID, memory usage, and threads | `cat /proc/3963/status`   |
| `/proc/<PID>/environ` | Provides the environment variables associated with a process, subject to permission restrictions                   | `cat /proc/3963/environ`  |
| `/proc/<PID>/cwd`     | Symbolic link to the process's current working directory                                                           | `readlink /proc/3963/cwd` |
| `/proc/<PID>/exe`     | Symbolic link to the executable associated with the process                                                        | `readlink /proc/3963/exe` |
| `/proc/<PID>/fd`      | Directory containing symbolic links representing the process's open file descriptors                               | `ls -l /proc/3963/fd`     |
| `/proc/<PID>/maps`    | Shows the process's memory mappings and associated address ranges                                                  | `head /proc/3963/maps`    |

## Filesystem Commands Used

| Command       | Description                                            | Example       |
| ------------- | ------------------------------------------------------ | ------------- |
| `cd /`        | Changes to the root directory of the filesystem        | `cd /`        |
| `ls /`        | Lists the directories and files at the filesystem root | `ls /`        |
| `ls /proc`    | Lists entries exposed through the proc filesystem      | `ls /proc`    |
| `ls /etc`     | Lists system configuration files and directories       | `ls /etc`     |
| `ls /home`    | Lists user home directories                            | `ls /home`    |
| `ls /opt`     | Lists software installed under `/opt`                  | `ls /opt`     |
| `ls /tmp`     | Lists files in the temporary directory                 | `ls /tmp`     |
| `ls /usr`     | Lists the contents of the `/usr` hierarchy             | `ls /usr`     |
| `ls /var`     | Lists variable system/application data                 | `ls /var`     |
| `ls /var/log` | Lists system and application log files                 | `ls /var/log` |

## Useful Syntax / Concepts

| Syntax / Concept | Description                                                                       | Example                  |
| ---------------- | --------------------------------------------------------------------------------- | ------------------------ |
| `<PID>`          | Placeholder representing an actual process ID                                     | `/proc/<PID>/status`     |
| `\|`             | Pipe; sends the output of one command as input to another                         | `ps aux \| grep spotify` |
| `<`              | Input redirection; uses a file as standard input                                  | `cat < file.txt`         |
| `>`              | Output redirection; writes command output to a file                               | `echo "test" > file.txt` |
| `$VARIABLE`      | Expands the value of a shell environment variable                                 | `echo $SHELL`            |
| `.`              | Represents the current directory                                                  | `ls -la`                 |
| `..`             | Represents the parent directory                                                   | `cd ..`                  |
| `/`              | Root of the Linux filesystem when used as the first character of an absolute path | `cd /`                   |
| `~`              | Represents the current user's home directory in the shell                         | `cd ~/cyber-lab`         |

## Security-Relevant Concepts Encountered

### Process Identity

* **PID** — Process ID; identifies a running process.
* **PPID** — Parent Process ID; identifies the process's current parent.
* **UID** — User ID associated with the process.
* **GID** — Group ID associated with the process.

### Process Relationships

Processes form parent-child relationships:

```text
Parent Process
      |
      +-- Child Process
              |
              +-- Another Child Process
```

### Process Investigation

`ps`, `top`, and `/proc/<PID>/` can reveal information about:

* running processes
* process ownership
* process hierarchy
* command-line arguments
* environment
* memory mappings
* open file descriptors
* current working directory
* executable paths

### Network Reconnaissance

`ip addr`, `ip route`, and `ss` can reveal:

* network interfaces
* IP addresses
* routing information
* default gateway
* listening network services
* associated processes, when permissions allow

### Important Principle

> **Don't memorize commands in isolation. Understand what information they expose, why that information exists, and how that information could be useful during security investigation.**


# Processes, File Descriptors & Sockets

## Process Investigation

A **process** is a running instance of a program.

A process has:

* PID — Process ID
* PPID — Parent Process ID
* UID/GID — User and group identity
* Memory
* Environment
* File descriptors
* Other kernel-managed resources

Useful commands:

```bash
ps aux
ps -ef
ps -p <PID>
ps -p <PID> -o pid,ppid,user,stat,cmd
pstree -p <PID>
```

### Current shell process

```bash
echo $$
```

`$$` expands to the PID of the current shell.

The process can then be inspected through:

```bash
ls -l /proc/$$
cat /proc/$$/status
```

---

# `/proc/<PID>`

Linux exposes information about processes through the `/proc` pseudo-filesystem.

Example:

```bash
ls -l /proc/<PID>
```

Useful entries:

| Entry     | Meaning                                        |
| --------- | ---------------------------------------------- |
| `cwd`     | Process's current working directory            |
| `exe`     | Executable being run                           |
| `cmdline` | Command-line arguments                         |
| `status`  | Process state, identity, memory, threads, etc. |
| `environ` | Environment variables                          |
| `fd/`     | File descriptors                               |
| `maps`    | Process memory mappings                        |
| `net/`    | Network-related information                    |
| `ns/`     | Namespace information                          |

`/proc` provides evidence about what a process is doing. It does not, by itself, prove that a process is malicious or vulnerable.

---

# File Descriptors

A **file descriptor (FD)** is a small integer used by a process to refer to a resource managed by the kernel.

Common descriptors:

```text
0 → stdin
1 → stdout
2 → stderr
```

Inspect a process's file descriptors:

```bash
ls -l /proc/<PID>/fd
```

Example:

```text
0 -> /dev/pts/1
1 -> /dev/pts/1
2 -> /dev/pts/1
3 -> socket:[66597]
```

This means the process has:

* FD 0 connected to its terminal for input
* FD 1 connected to its terminal for normal output
* FD 2 connected to its terminal for error output
* FD 3 referring to a kernel socket

### Important mental model

```text
Process
   ↓
File Descriptor
   ↓
Kernel-managed resource
```

The resource can be:

* file
* terminal
* pipe
* socket
* device
* other kernel object

Linux uses the file-descriptor interface for many different types of resources.

---

# Pipes

A pipe provides a mechanism for communication between processes.

A pipe may appear in `/proc/<PID>/fd` as:

```text
pipe:[60985]
```

The number identifies the kernel pipe object.

Pipes are commonly used for **inter-process communication (IPC)**.

---

# File Descriptor and Socket

A network socket is represented to a process through a file descriptor.

Example:

```text
FD 3 → socket:[66597]
```

This does not mean the socket is an ordinary file.

Rather, the process uses FD 3 as its handle for communicating with the socket through the kernel.

Mental model:

```text
Process
   ↓
FD 3
   ↓
Socket
   ↓
TCP/UDP networking
```

---

# Finding Which Process Owns a Network Socket

The `ss` command can show network sockets.

```bash
ss -tulpn
```

Important options:

```text
-t  TCP
-u  UDP
-l  listening sockets
-n  don't resolve names
-p  show owning process
```

Example:

```text
tcp LISTEN 0 5 127.0.0.1:8000 0.0.0.0:* users:(("python3",pid=6885,fd=3))
```

This tells us:

```text
Program  = python3
PID      = 6885
FD       = 3
Protocol = TCP
State    = LISTEN
Address  = 127.0.0.1
Port     = 8000
```

We can independently verify the FD:

```bash
ls -l /proc/6885/fd
```

which showed:

```text
3 -> socket:[66597]
```

This connects the process view and network view:

```text
python3
   ↓
PID 6885
   ↓
FD 3
   ↓
socket:[66597]
   ↓
TCP 127.0.0.1:8000
```

---

# Security Perspective

Process and socket investigation is important in security because it allows us to answer questions such as:

* What processes are running?
* Which user owns a process?
* Which process owns a listening port?
* Which network services are exposed?
* Which file descriptors does a process have?
* Is a suspicious process communicating over the network?
* What resources does a process have access to?

A listening port does **not automatically mean a vulnerability exists**.

It tells us that a service is accepting or prepared to accept network connections and gives us something concrete to investigate.

---

# Localhost / Loopback

`127.0.0.1` is the IPv4 loopback address.

A service bound to:

```text
127.0.0.1:8000
```

is listening on the local machine's loopback interface.

It is different from binding to an externally reachable interface such as:

```text
192.168.x.x:8000
```

This distinction matters when determining network exposure.

---

# Core Mental Model

The key relationship learned in this session:

```text
Program
   ↓
Process
   ↓
PID
   ↓
File Descriptor
   ↓
Kernel Resource
   ↓
Socket
   ↓
Network Communication
```

A process does not directly manipulate the physical network.

It interacts with a socket through a file descriptor, while the Linux kernel handles the underlying networking.
