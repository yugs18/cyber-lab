import sys
import socket
import getpass
import subprocess

# Get the current machine hostname.
host_name = socket.gethostname()

# Run the system networking command to fetch interface details.
result = subprocess.run(
    ['ip', '-br', 'addr'],
    capture_output=True,
    text=True
)

# Stop if the command fails so the script does not continue with invalid data.
if result.returncode != 0:
    sys.exit("subprocess shows error")

# Parse the output of the IP command into words.
output = result.stdout
fields = output.split()

# Look up the IPv4 address for the ens33 interface in the command output.
ip_address = fields[fields.index('ens33') + 2].split('/')[0]

# Get the username of the currently logged-in user.
user_name = getpass.getuser()

# Display system details to the terminal.
print("Hostname: ", host_name)
print("User Name: ", user_name)
print("IP address: ", ip_address)
