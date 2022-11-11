import datetime
import csv
import tkinter as tk
from tkinter import filedialog
import connectserver

db = connectserver.connectserver()
cursor = db.cursor()

def transferdriver():
    try:
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()

        with open(file_path) as transferdriver:
            reader = csv.DictReader(transferdriver)
            for row in reader:
                drivername = row.get("driverName")
                team1 = row.get("team1")
                team2 = row.get("team2")
                drivergroup1 = row.get("driverGroup1")
                drivergroup2 = row.get("driverGroup2")
                description = row.get("description")
                tokenused = row.get("tokenUsed")
                status = row.get("driverStatus")

                query = "INSERT INTO driverTransfer VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
                val = (drivername, team1, drivergroup1, team2, drivergroup2,
                        description, datetime.datetime.today().strftime('%Y-%m-%d'), tokenused)
                cursor.execute(query, val)

                query = f'DELETE FROM driverLeaderBoard \
                        WHERE driverName = "{drivername}";'
                cursor.execute(query)

                query = f'UPDATE driverList \
                        SET team = "{team2}", \
                        driverGroup = "{drivergroup2}", \
                        driverStatus = "{status}", \
                        transferToken = transferToken - {tokenused} \
                        WHERE driverName = "{drivername}"'
                cursor.execute(query)

                query = "INSERT INTO driverLeaderBoard (driverName, team, driverGroup, totalPoints) \
                        VALUES (%s, %s, %s, %s);"
                val = (drivername, team2, drivergroup2, 0)
                cursor.execute(query, val)

                query = f'UPDATE licensePoint \
                        SET driverGroup = "{drivergroup2}" \
                        WHERE driverName = "{drivername}"'
                cursor.execute(query)


                db.commit()

        print("车手转会记录上传成功，稍后请记得将文件上传到赛会群备份")

    except Exception as e:
        print(str(e))
        print("出现错误，请检查输入数据是否有误或联系程序管理员")
        print("没有数据上传到数据库中......")