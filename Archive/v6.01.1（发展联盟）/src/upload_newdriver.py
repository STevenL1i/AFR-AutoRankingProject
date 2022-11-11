import datetime
import csv
from pickletools import read_unicodestringnl
import tkinter
from tkinter import filedialog
import mysql.connector
import connectserver

# upload new driver profile
def welcome_newdriver():
    db = connectserver.connectserver("server.json", "league")
    cursor = db.cursor()

    try:
        root = tkinter.Tk()
        root.withdraw()
        filepath = filedialog.askopenfilename()

        with open(filepath) as newdriver:
            reader = csv.DictReader(newdriver)

            record = 0
            for row in reader:
                drivername = row.get("driverName")
                team = row.get("team")
                group = row.get("driverGroup")
                jointime = row.get("joinTime")
                
                if drivername.replace(" ", "") == "" and team.replace(" ", "") == "" \
                    and group.replace(" ", "") == "" and jointime.replace(" ", "") == "":
                    break

                if jointime == '':
                    jointime = datetime.datetime.today().strftime('%Y-%m-%d')

                record += 1
                print(f'Uploading records {record}......')
                
                # update the driverlist
                query = "INSERT INTO driverList VALUES \
                        (%s, %s, %s, %s);"
                val = (drivername, team, group, jointime)
                cursor.execute(query, val)

                # update the driverLeaderBoard
                query = "INSERT INTO driverLeaderBoard \
                        (driverName, team, driverGroup, totalPoints) VALUES (%s, %s, %s, %s);"
                val = (drivername, team, group, 0)
                cursor.execute(query, val)
            
            db.commit()
        print()
        print("新车手数据上传成功，稍后请记得将数据整理备份")

    except Exception as e:
        print(str(e))
        print("数据上传失败，请检查上传文件数据是否正确")
        print("错误提示：" + str(e))

