🔒 Netmiko-Fortinet Automation Scripts
This repository contains Python scripts designed for Network Automation tasks on Fortinet FortiGate devices using the powerful Netmiko library.

The scripts facilitate reliable SSH connections, execution of command lists, configuration management, and data retrieval, making routine network operations faster and less prone to manual error. This project is specifically useful for bulk configuration changes, such as enabling logging across multiple firewall policies.

✨ Features
Secure Connection: Establishes secure SSH connections to Fortinet devices.

Command Execution: Runs single or multiple CLI commands.

Configuration Management: Allows pushing configuration changes to the device (e.g., policy updates).

Data Parsing: Uses Regular Expressions (Regex) to extract specific configuration parameters (like Policy IDs) from command output.

Log Management: Automates the process of enabling full traffic logging (set logtraffic all) on multiple firewall policies.

🚀 Getting Started
Prerequisites
To run these scripts, you need:

Python 3.x installed.

Netmiko library.

SSH access enabled and configured on your target FortiGate device(s).

Installation
Install the Netmiko library using pip:

Bash

pip install netmiko
Configuration (Device Credentials)
For security, connection parameters should be stored separately (e.g., in a secure .yml or a separate file). The required parameters are:

Parameter	Description	Required Value
device_type	Always set to the Netmiko platform name.	'fortinet'
host	The IP address or hostname of the device.	IP_ADDRESS
username	Your FortiGate SSH username.	user
password	Your FortiGate SSH password.	password

Export to Sheets
💡 Usage Example (Policy Log Automation)
This example demonstrates how to extract all existing Policy IDs from the configuration and then apply a change—specifically enabling full traffic logging—to each one.

1. Define Logic and Connection
Python

from netmiko import ConnectHandler
import re

# --- 1. Define Device Connection Details ---
fortigate_device = {
    "device_type": "fortinet",
    "host": "YOUR_FORTIGATE_IP",
    "username": "YOUR_SSH_USERNAME",
    "password": "YOUR_SSH_PASSWORD",
}

# --- 2. Define Command List Generator ---
def generate_log_config(policy_id):
    """Generates FortiGate CLI commands to enable logging on a firewall policy."""
    return [
        'config vdom',
        'edit root',  # IMPORTANT: Change 'root' to your target VDOM name if different
        'config firewall policy',
        f'edit {policy_id}',
        'set logtraffic all',  # Enables logging of all traffic for this policy
        'end',
        'end',
    ]

# --- 3. Execution Logic ---
try:
    print(f"Connecting to {fortigate_device['host']}...")
    net_connect = ConnectHandler(**fortigate_device)
    
    # 3.1 Retrieve Current Policy Configuration
    print("Retrieving current firewall policy configuration...")
    # Get the configuration output for all policies
    receive_config = net_connect.send_command("show firewall policy")

    # 3.2 Extract Policy IDs using Regex
    # Find all policyid values (e.g., policyid: 1, policyid: 20, etc.)
    policyid_pattern = re.findall("policyid:\s(\d*)", receive_config)
    print(f"Extracted Policy IDs: {policyid_pattern}")

    # 3.3 Apply Logging Configuration to Each Policy ID
    if policyid_pattern:
        print("\nStarting configuration changes to enable logging on policies...")
        
        for pid in policyid_pattern:
            config_commands = generate_log_config(pid)
            
            # Send the configuration commands to the device
            net_connect.send_config_set(config_commands)
            print(f"  -> Log enabled on Policy ID {pid}")
            
    else:
        print("No firewall policies found to update.")

    # Close the connection
    net_connect.disconnect()
    print("\nConnection closed successfully.")

except Exception as e:
    print(f"An error occurred: {e}")
Explanation of Key Code
show firewall policy: The command used to pull the configuration data from the FortiGate.

re.findall("policyid:\s(\d*)", receive_config): This Regular Expression is the core of the automation. It searches the output for the literal string "policyid:", followed by any whitespace (\s), and then captures one or more digits ((\d*)), returning them as a clean list of strings (e.g., ['1', '2', '3']).

generate_log_config(policy_id): Dynamically creates the necessary CLI steps (config vdom, config firewall policy, edit <id>) for each policy ID found.

set logtraffic all: The specific configuration command used to turn on logging for all sessions matching that policy.

net_connect.send_config_set(): Pushes the configuration changes to the device efficiently.

🤝 Contribution
Feel free to fork this repository, submit bug fixes, or add more specialized FortiGate automation scripts via Pull Requests!
