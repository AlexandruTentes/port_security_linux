import os
import time

file = open("/home/STARTUP_SCRIPTS/startup_scripts_success_check", "a")
file.write("ip_connections.py successful\n")
file.close()

def all_connections():
    conn = os.popen("netstat -natp | grep 'ESTABLISHED\|TIME_WAIT'").readlines()
    return conn

def users_connections():
    conn = os.popen("w").readlines()
    return conn

loop = True
secured = False

while loop:
    try:
        server_ip = os.popen("ifconfig | grep 'inet 192'").readline()
        server_ip = server_ip.split()[1]
        loop = False
    except:
        loop = True

while True:

    connections = all_connections()
    users = users_connections()

    for connection in connections:
        split_connection = connection.split()
        connection_type = split_connection[0]
        connection_port = split_connection[3].replace((server_ip + ":"), "")
        connection_ip = split_connection[4].split(":", 1)[0]

        for user in users:
            split_user = user.split()
            user_ip = split_user[2]

            if connection_ip == user_ip:
                try:
                    os.remove("/home/STARTUP_SCRIPTS/security_check/ipaddresses/" + user_ip)
                except:
                    pass

                secured = True

                file = open("/home/STARTUP_SCRIPTS/security_check/whitelisted_ips/" + user_ip, "a")
                file.close()
                break

        if not secured:
            if connection_port == "22" or connection_port == "5900":
                file = open(("/home/STARTUP_SCRIPTS/security_check/ipaddresses/" + connection_ip), "a")
                file.close()

        secured = False

    time.sleep(1)
