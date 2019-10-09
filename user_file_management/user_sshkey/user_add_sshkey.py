import os
import time
import subprocess

file = open("/home/STARTUP_SCRIPTS/startup_scripts_success_check", "a")
file.write("user_add_sshkey successful\n")
file.close()

def get_users():
    users = os.popen("cat /etc/passwd | grep '/home/' | sed 's/:.*//'").readlines()
    return users

def get_checked_users(folder):
    users = os.popen("ls " + folder).readlines()
    return users

def add_file(user):
    user = user.replace("\n", "")
    check = get_checked_users("-a /home/" + user + " 2>/dev/null")

    if len(check) != 0:
        subprocess.check_call(["/home/STARTUP_SCRIPTS/user_file_management/user_sshkey/add_files", user])

is_checked = False
was_equal = False
found_user = "@"
i = 1

while True:
    try:
        users = get_users()
        checked_users = get_checked_users("/home/STARTUP_SCRIPTS/user_file_management/user_sshkey/users_checked")

    except Exception as e:
        raise Exception(" Error at loading 'users' in /home/STARTUP_SCRIPTS/user_file_management/user_sshkey : {err}".format(err = repr(e)))

    if len(users) == len(checked_users):
        was_equal = True
        time.sleep(1)
        continue

    if len(users) < len(checked_users):
        was_equal = False
        for checked_user in checked_users:
            checked_user = checked_user.replace("\n", "")
            output = get_checked_users("/home/" + checked_user + " 2>/dev/null")
            if len(output) == 0:
                subprocess.check_call(["/home/STARTUP_SCRIPTS/user_file_management/user_sshkey/remove_files", checked_user])

    if not was_equal:
        for user in users:
            for checked_user in checked_users:
                if user == checked_user:
                    user_found = True
                    break

            if not user_found:
                add_file(user)

            user_found = False
    else:
        was_equal = False

        for checked_user in checked_users:
            if checked_user == users[len(users) - i]:
                found_user = "@"

                if i < len(users) - 2:
                    i = i + 1

                break

            found_user = users[len(users) - i]

        if found_user != "@":
            i = 1
            add_file(found_user)
            found_user = "@"

    time.sleep(1)
