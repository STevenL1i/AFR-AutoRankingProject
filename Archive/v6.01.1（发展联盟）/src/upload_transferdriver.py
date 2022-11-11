import datetime
import csv
import tkinter as tk
from tkinter import filedialog
import connectserver


def transferdriver():
    db = connectserver.connectserver("server.json", "league")
    cursor = db.cursor()

    try:
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()

        with open(file_path) as transferdriver:
            reader = csv.DictReader(transferdriver)

            record = 0
            for row in reader:
                drivername = row.get("driverName")
                team1 = row.get("team1")
                team2 = row.get("team2")
                drivergroup1 = row.get("driverGroup1")
                drivergroup2 = row.get("driverGroup2")
                description = row.get("description")
                transfertime = row.get("transferTime")
                if transfertime == '':
                    transfertime = datetime.datetime.today().strftime('%Y-%m-%d')
                
                if drivername.replace(" ","") == "" and team1.replace(" ","") == "" and team2.replace(" ","") == "" \
                and drivergroup1.replace(" ","") == "" and drivergroup2.replace(" ","") == "" \
                and description.replace(" ","") == "":
                    break

                record += 1
                print(f'Uploading records {record}......')

                query = "INSERT INTO driverTransfer VALUES (%s, %s, %s, %s, %s, %s, %s);"
                val = (drivername, team1, drivergroup1, team2, drivergroup2,
                        description, transfertime)
                cursor.execute(query, val)

                query = f'DELETE FROM driverLeaderBoard \
                        WHERE driverName = "{drivername}";'
                cursor.execute(query)
                
                query = f'UPDATE driverList \
                        SET team = "{team2}", \
                        driverGroup = "{drivergroup2}" \
                        WHERE driverName = "{drivername}" AND driverGroup = "{drivergroup1}";'
                cursor.execute(query)

                query = "INSERT INTO driverLeaderBoard (driverName, team, driverGroup, totalPoints) \
                        VALUES (%s, %s, %s, %s);"
                val = (drivername, team2, drivergroup2, 0)
                cursor.execute(query, val)
        
            db.commit()
        print()
        print("车手转会记录上传成功，稍后请记得将数据整理备份")
    
    except Exception as e:
        print(str(e))
        print("数据上传失败，请检查上传文件数据是否正确")
        print("错误提示：" + str(e))
