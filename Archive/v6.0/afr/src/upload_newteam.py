import csv
from logging import root
import tkinter
from tkinter import filedialog
import connectserver

def welcome_newteam():
    db = connectserver.connectserver("server.json", "afr")
    cursor = db.cursor()

    try:
        root = tkinter.Tk()
        root.withdraw()
        filepath = filedialog.askopenfilename()

        with open(filepath) as newteam:
            reader = csv.DictReader(newteam)

            record = 0
            for row in reader:
                teamname = row.get("teamName")
                teamcolor = row.get("teamColor")
                group = row.get("driverGroup")

                if teamname == "" and teamcolor == "" and group == "":
                    break

                record += 1
                print(f'Uploading records {record}......')

                query = "INSERT INTO teamList \
                        (teamName, teamColor, driverGroup) VALUES (%s, %s, %s);"
                val = (teamname, teamcolor, group)
                cursor.execute(query, val)

                query = "INSERT INTO constructorsLeaderBoard \
                        (team, driverGroup, totalPoints) VALUES (%s, %s, %s);"
                val = (teamname, group, 0)
                cursor.execute(query, val)
            
            db.commit()

    except Exception as e:
        print(str(e))
        print("数据上传失败，请检查上传文件数据是否正确")
        print("错误提示：" + str(e))