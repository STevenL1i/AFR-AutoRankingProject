import datetime
import csv
import tkinter as tk
from tkinter import filedialog
import connectserver


def transferdriver():
    db = connectserver.connectserver()
    cursor = db.cursor()

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
                status = row.get("driverStatus")
                description = row.get("description")
                transfertime = row.get("transferTime")
                if transfertime == '':
                    transfertime = datetime.datetime.today().strftime('%Y-%m-%d')
                tokenused = row.get("tokenUsed")
                

                query = "INSERT INTO driverTransfer VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
                val = (drivername, team1, drivergroup1, team2, drivergroup2,
                        description, transfertime, tokenused)
                cursor.execute(query, val)

                query = f'DELETE FROM driverLeaderBoard \
                        WHERE driverName = "{drivername}";'
                cursor.execute(query)
                
                query = f'UPDATE driverList \
                        SET team = "{team2}", \
                        driverGroup = "{drivergroup2}", \
                        driverStatus = "{status}", \
                        transferToken = transferToken - {tokenused} \
                        WHERE driverName = "{drivername}" AND driverGroup = "{drivergroup1}"'
                cursor.execute(query)

                query = f'UPDATE licensePoint \
                        SET driverGroup = "{drivergroup2}" \
                        WHERE driverName = "{drivername}"'
                cursor.execute(query)

                query = "INSERT INTO driverLeaderBoard (driverName, team, driverGroup, totalPoints) \
                        VALUES (%s, %s, %s, %s);"
                val = (drivername, team2, drivergroup2, 0)
                cursor.execute(query, val)

                db.commit()
        print()
        print("车手转会记录上传成功，稍后请记得将文件上传到赛会群备份")

    except Exception as e:
        print(str(e))
        print("数据上传失败，请检查上传文件数据是否正确")
        print("错误提示：" + str(e))

if __name__ == "__main__":
    transferdriver()