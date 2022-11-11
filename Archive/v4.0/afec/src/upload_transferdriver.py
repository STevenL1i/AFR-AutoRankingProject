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

            record = 0
            for row in reader:
                record += 1
                print(f'Uploading records {record}......')

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
                teamtokenused = row.get("teamtokenUsed")
                

                query = "INSERT INTO driverTransfer VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
                val = (drivername, team1, drivergroup1, team2, drivergroup2,
                        description, transfertime, tokenused, teamtokenused)
                cursor.execute(query, val)

                
                query = f'UPDATE driverList \
                        SET team = "{team2}", \
                        driverGroup = "{drivergroup2}", \
                        driverStatus = "{status}", \
                        transferToken = transferToken - {tokenused} \
                        WHERE driverName = "{drivername}";'
                cursor.execute(query)


                if status == "1st driver":
                    driverPos = "driver_1"
                elif status == "2ed driver":
                    driverPos = "driver_2"
                elif status == "3rd driver":
                    driverPos = "driver_3"
                elif status == "4th driver":
                    driverPos = "driver_4"

                query = f'UPDATE teamList \
                        SET {driverPos} = "{drivername}" \
                        WHERE teamName = "{team2}";'
                cursor.execute(query)


            db.commit()
        
        print()
        print("车手转会记录上传成功，稍后请记得将文件上传到赛会群备份")

    except Exception as e:
        print(str(e))
        print("数据上传失败，请检查上传文件数据是否正确")
        print("错误提示：" + str(e))

if __name__ == "__main__":
    transferdriver()