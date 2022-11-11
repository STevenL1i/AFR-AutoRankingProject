import sys
import os
import paramiko


server_list = [
                ["guangzhou", "118.89.25.198", "root", "0110@tencent"]
              ]

starttele_cmd = ["/opt/rh/rh-python38/root/usr/bin/python3.8 tele.py -start"]
killtele_cmd = ["/opt/rh/rh-python38/root/usr/bin/python3.8 tele.py -kill"]
checktele_cmd = ["/opt/rh/rh-python38/root/usr/bin/python3.8 tele.py -check"]

print()
print("1.start telemetry")
print("2.close telemetry")
print("3.check telemetry")
choice = input("Your choose: ")
if choice == "1":
    command = starttele_cmd
elif choice == "2":
    command = killtele_cmd
elif choice == "3":
    command = checktele_cmd
else:
    print("choose 1 or 2 or 3")
    input("press <enter> to exit")
    sys.exit(0)

def execcommand(server):
    try:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        print("connecting " + server[0] + ":" + server[1])
        ssh.connect(server[1], 22, server[2], server[3], timeout=5)
        print(server[0] + ":" + server[1] + " connect success!")
        print()
        for cmd in command:
            (stdin, stdout, stderr) = ssh.exec_command(cmd)
        
            for line in stdout.readlines():
                line = line.replace("\n", "")
                print(f'{line}')
        ssh.close()
        print(server[0] + ":" + server[1] + " operation complete!!!")
        print()
    except Exception as e:
        print(str(e))
        sys.exit()


"""
def execcommand(server):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print("connecting " + server[0] + ":" + server[1])
        ssh.connect(server[1], 22, server[2], server[3], timeout=5)
        print(server[0] + ":" + server[1] + " connect success!")
        print()
        
        channel = ssh.get_transport().open_session()
        channel.exec_command("/opt/rh/rh-python38/root/usr/bin/python3.8 tele.py -check \r")
        channel.shutdown_write()

        stdout = channel.makefile().read()
        stderr = channel.makefile_stderr().read()
        exit_code = channel.recv_exit_status()

        channel.close()
        ssh.close()

        print(stdout)
        print()
        print(stderr)
        print()
        print(server[0] + ":" + server[1] + " operation complete!!!")
        print()
    except Exception as e:
        print(str(e))
        sys.exit()
"""




if __name__ == "__main__":
    for server in server_list:
        execcommand(server)
    input("press <enter> to exit")