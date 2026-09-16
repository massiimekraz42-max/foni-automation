import os
from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoAuthenticationException,
    NetmikoTimeoutException,
)

def connect_to_system(system):
    username = os.getenv(system["username_env"])
    password = os.getenv(system["password_env"])

    connection_info = {
        "device_type": system["type"],
        "host": system["host"],
        "username": username,
        "password": password,
    }

    return ConnectHandler(**connection_info)

def create_cisco_loopback(connection):
    commands = [
        "interface Loopback100",
        "description FONI Training Loopback",
        "ip address 192.0.2.100 255.255.255.255",
    ]
    return connection.send_config_set(commands)

def read_cisco_loopback(connection):
    return connection.send_command(
        "show running-config interface Loopback100"
    )

def remove_cisco_loopback(connection):
    return connection.send_config_set([
        "no interface Loopback100"
    ])


connection = None
system = {
    "name": "Cisco Router",
    "type": "cisco_ios",
    "host": "54.90.112.247",
    "username_env": "CISCO_USERNAME",
    "password_env": "CISCO_PASSWORD"
}
try:
    connection = connect_to_system(system)

    print("CREATE")
    print(create_cisco_loopback(connection))

    print("READ AFTER CREATE")
    print(read_cisco_loopback(connection))

    print("REMOVE")
    print(remove_cisco_loopback(connection))

    print("READ AFTER REMOVE")
    print(read_cisco_loopback(connection))

except NetmikoAuthenticationException:
    print(f"{system['name']} -> FAILED: AUTHENTICATION")

except NetmikoTimeoutException:
    print(f"{system['name']} -> FAILED: CONNECTION TIMEOUT")

finally:
    if connection:
        connection.disconnect()

