import os
import time
import subprocess
from decimal import Decimal

file = open("/home/STARTUP_SCRIPTS/startup_scripts_success_check", "a")
file.write("temperature_checker.py successful" + "\n")
file.close()

#code taken from
#http://www.ridgesolutions.ie/index.php/2013/02/22/raspberry-pi-restart-shutdown-your-pi-from-python-code/
#
def restart():
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output
#
#end of copied code
#

def measure_temp():
    temp = os.popen("vcgencmd measure_temp").readline()
    temp = temp.replace("temp=","")
    return (temp.replace("'C", ""))

warning_check_60 = False
warning_check_70 = False

while True:
    temp = measure_temp()
    temp = Decimal(temp)

    if temp >= 60.0 and not warning_check_60:
        subprocess.check_call(["/home/STARTUP_SCRIPTS/functionality_check/broadcast_temp", "60"])
        warning_check_60 = True
    elif temp <= 50.0:
        warning_check_60 = False

    if temp >= 70.0 and not warning_check_70:
        subprocess.check_call(["/home/STARTUP_SCRIPTS/functionality_check/broadcast_temp", "70"])
        warning_check_70 = True
    elif temp <= 60.0:
        warning_check_70 = False

    if temp >= 80.0:
        file = open("/home/STARTUP_SCRIPTS/functionality_check/temperature_reboot", "r")
        reboot_value = file.read()
        file.close()

        if reboot_value != "True" or reboot_value != "True\n":
            subprocess.check_call(["/home/STARTUP_SCRIPTS/functionality_check/broadcast_temp", "80"])
            time_left = 10
            sleep(60)
            while time_left >= 0:
                time.sleep(1)
                subprocess.check_call(["/home/STARTUP_SCRIPTS/functionality_check/broadcast_temp", time_left])
                time_left = time_left - 1

            file = open("/home/STARTUP_SCRIPTS/functionality_check/temperature_reboot", "w")
            file.write("True")
            file.close()

            restart()
        else:
            time.sleep(1800)

    time.sleep(1)
