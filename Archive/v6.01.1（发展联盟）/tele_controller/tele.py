import os
import sys


def main():
    if sys.argv[1] == "-start":
        start_tele()
    elif sys.argv[1] == "-kill":
        kill_tele()
    elif sys.argv[1] == "-check":
        check_tele()



def start_tele():
    os.system("./tele.sh")
    print("telemetry started")


def kill_tele():
    os.system("ps -ef | grep a.out > temp")
    f = open("temp", "r")

    stdout = f.read()
    stdout = stdout.split("\n")
    for line in stdout:
        if line.find("./a.out 20777") != -1:
            tokenlist = line.split(" ")
            for token in tokenlist:
                try:
                    taskid = int(token)
                    os.system(f'kill -9 {taskid}')
                    print(f'telemetry process ({taskid} killed success)')
                    break
                except ValueError:
                    continue

    f.close()
    os.system("rm -rf temp")


def check_tele():
    os.system("ps -ef | grep a.out > temp")
    f = open("temp", "r")
    stdout = f.read()

    print(f'{"Service":<20}{"Status"}')
    if stdout.find("./a.out 20777") != -1:
        print(f'{"telemetry":<20}{"ACTIVE"}')
    else:
        print(f'{"telemetry":<20}{"OFFLINE"}')
    print()

    f.close()
    os.system("rm -rf temp")


if __name__ == "__main__":
    main()