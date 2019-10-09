import os
import time
import subprocess
import threading

file = open("/home/STARTUP_SCRIPTS/startup_scripts_success_check", "a")
file.write("ban_addresses.py successful\n")
file.close()

def get_trials(ip):
    conn = os.popen("grep 'Failed password' /var/log/auth.log | grep \'" + ip + "\' | cut -d' ' -f3").readlines()
    return conn

print(get_trials("5.9.23.67"))

def get_ips(folder):
    ips = os.popen("ls /home/" + folder).readlines()
    return ips

def check_ip_trials(ip):
    start = time.time()
    time.clock()
    ip_trials = get_trials(ip)
    is_whitelisted = False

    while len(ip_trials) < 3:
        if time.time() - start > 15:
            break

        ip_trials = get_trials(ip)
        whitelisted_ips = get_ips("STARTUP_SCRIPTS/security_check/whitelisted_ips")

        for whitelisted_ip in whitelisted_ips:
            whitelisted_ip = whitelisted_ip.replace("\n", "")

            if whitelisted_ip == ip:
                is_whitelisted = True
                break

        if is_whitelisted:
            break

        time.sleep(1)

    if not is_whitelisted:
        subprocess.check_call(['/home/STARTUP_SCRIPTS/security_check/ban_ip', ip])
    else:
        try:
            os.remove("/home/STARTUP_SCRIPTS/security_check/ipaddresses/" + ip)
        except:
            pass

is_whitelisted = False

while True:
    ips = get_ips("STARTUP_SCRIPTS/security_check/ipaddresses")
    whitelisted_ips = get_ips("STARTUP_SCRIPTS/security_check/whitelisted_ips")

    for ip in ips:
        ip = ip.replace("\n", "")

        for whitelisted_ip in whitelisted_ips:
            whitelisted_ip = whitelisted_ip.replace("\n", "")

            if whitelisted_ip == ip:
                is_whitelisted = True
                break

        if not is_whitelisted:
            file = open("/home/STARTUP_SCRIPTS/security_check/ipaddresses/" + ip, "r+")
            ip_mode = file.read()

            if ip_mode != "used":
                file.seek(0)
                file.write("used")
                file.truncate()
                ip_thread = threading.Thread(target=check_ip_trials, args=(ip, ))
                ip_thread.daemon = True
                ip_thread.start()

            file.close()
        else:
            try:
                os.remove("/home/STARTUP_SCRIPTS/security_check/ipaddresses/" + ip)
            except:
                pass

        is_whitelisted = False

    time.sleep(1)
