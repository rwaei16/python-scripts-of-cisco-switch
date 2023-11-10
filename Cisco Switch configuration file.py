import getpass
import paramiko
import time

# List of IP addresses
HOSTS = ["10.40.10.23", "10.40.10.24", "10.40.10.25", "10.40.10.26", "10.40.10.27"]
port = 22  # SSH port
user = input("Enter your SSH username: ")
password = getpass.getpass("Enter your SSH password: ")

try:
    for host in HOSTS:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password)

        # You can now send your VLAN configuration commands
        remote_conn = ssh.invoke_shell()

        remote_conn.send("enable\n")
        remote_conn.send("conf t\n")
        remote_conn.send("banner motd #\n"
        "*****************************************************************************\n"
        "* My test Company.                                  *\n"
        "*                                                                           *\n"
        "*****************************************************************************\n"
        "*                                                                           *\n"
        "* !Please log out immediately if you are not an authorized administrator!!  *\n"
        "*****************************************************************************\n"
        "#\n")
        remote_conn.send("username Mohammed privilege 15 secret mohammed@123\n")
        remote_conn.send("ip domain name test.sa\n")
        remote_conn.send("ip default-gateway 10.40.10.1\n")
        remote_conn.send("interface range tenGigabitEthernet 1/1/1-4\n")
        remote_conn.send("switchport mode trunk\n")
        remote_conn.send("exit\n")
        remote_conn.send("service password-encryption\n")
        remote_conn.send("vlan 10\n")
        remote_conn.send("name Management\n")
        remote_conn.send("vlan 20\n")
        remote_conn.send("name IT\n")
        remote_conn.send("vlan 30\n")
        remote_conn.send("name FA\n")
        remote_conn.send("end\n")
        
        # Wait for a brief moment to ensure the configuration is applied
        time.sleep(2)  # Adjust as needed

        # Save the configuration to memory
        remote_conn.send("write memory\n")

        # Wait briefly after writing to memory
        time.sleep(1)  # Adjust as needed

        output = remote_conn.recv(65535).decode('ascii')
        print(output)

        # Close the SSH connection for each device
        ssh.close()

    print("Configuration completed successfully for all devices.")

except Exception as e:
    print("An error occurred during the SSH session:", e)

