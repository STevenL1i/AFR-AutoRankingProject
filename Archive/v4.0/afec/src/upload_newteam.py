import csv
from logging import root
import tkinter
from tkinter import filedialog
import connectserver

def welcome_newteam():
    db = connectserver.connectserver()
    cursor = db.cursor()

    try:
        root = tkinter.Tk()
        root.withdraw()
        filepath = filedialog.askopenfilename()

        with open(filepath) as newteam:
            reader = csv.DictReader(newteam)

            record = 0
            for row in reader:
                record += 1
                print(f'Uploading records {record}......')

                teamname = row.get("teamName")
                teamcolor = row.get("teamColor")
                transferToken = row.get("transferToken")

                query = "INSERT INTO teamList \
                        (teamName, teamColor, transferToken) VALUES (%s, %s, %s);"
                val = (teamname, teamcolor, transferToken)
                cursor.execute(query, val)

                query = "INSERT INTO constructorsLeaderBoard \
                        (team, driverGroup, totalPoints) VALUES (%s, %s, %s);"
                val = (teamname, "AFEC", 0)
                cursor.execute(query, val)
            
            db.commit()

    except Exception as e:
        print(str(e))
        print("数据上传失败，请检查上传文件数据是否正确")
        print("错误提示：" + str(e))