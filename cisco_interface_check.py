from netmiko import ConnectHandler
import os 
device = {
    "device_type": "cisco_ios",
    "host": os.getenv("CISCO_HOST"),
    "username": os.getenv("CISCO_USERNAME"),
    "password": os.getenv("CISCO_PASSWORD")
}
connection = ConnectHandler(**device)
print("Successfully connected to the Cisco device!")
interface_output = connection.send_command("show ip interface brief")
version_output = connection.send_command("show version")
print("Interface Output:")
print(interface_output)
print("Version Output:")
print(version_output)
lines = interface_output.splitlines()
print(" interface name, IP address,  status, protocol")
for line in lines:
    print(line)
    if "loopback" in line:
        data = line.split()
        print(data)
        if data[-2]== "up" and data[-1] == "down":
            print(f"Interface {data[0]} is  operational.")
        else:
            print(f"Interface {data[0]} is checke required.") 

