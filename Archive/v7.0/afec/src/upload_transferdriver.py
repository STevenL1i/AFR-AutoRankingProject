import datetime
import csv
import tkinter as tk
from tkinter import filedialog
import connectserver


def transferdriver():
    db = connectserver.connectserver("server.json", "afec")
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
                status = row.get("driverStatus")
                description = row.get("description")
                transfertime = row.get("transferTime")
                if transfertime == '':
                    transfertime = datetime.datetime.today().strftime('%Y-%m-%d')
                tokenused = row.get("tokenUsed")
                teamtokenused = row.get("teamtokenUsed")

                if drivername == "" and team1 == "" and team2 == "" and drivergroup1 == "" and drivergroup2 == "" and status == "" \
                                    and description == "" and transfertime == "" and tokenused == "" and teamtokenused == "":
                    break
                
                record += 1
                print(f'Uploading records {record}......')

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

                query = f'UPDATE teamList \
                        SET transferToken = transferToken - {teamtokenused} \
                        WHERE teamName = "{team2}";'
                cursor.execute(query)

            db.commit()

        # update driver in teamlist
        query = "UPDATE teamList \
                SET driver_1 = null, driver_2 = null, \
                    driver_3 = null, driver_4 = null;"
        cursor.execute(query)
        db.commit()

        query = 'SELECT driverName, team, driverStatus, teamColor, teamNameAbbr \
                FROM driverList JOIN teamList ON team = teamName \
                ORDER BY teamName ASC, \
                        case driverStatus \
                            WHEN "1st driver" THEN 1 \
                            WHEN "2ed driver" THEN 2 \
                            WHEN "3rd driver" THEN 3 \
                            WHEN "4th driver" THEN 4 \
                            ELSE 5 \
                            END, driverStatus;'
        cursor.execute(query)
        result = cursor.fetchall()

        for driver in result:
            driverPos = ""
            if driver[2] == "1st driver":
                driverPos = "driver_1"
            elif driver[2] == "2ed driver":
                driverPos = "driver_2"
            elif driver[2] == "3rd driver":
                driverPos = "driver_3"
            elif driver[2] == "4th driver":
                driverPos = "driver_4"
            
            query = f'UPDATE teamList \
                    SET {driverPos} = "{driver[0]}" \
                    WHERE teamName = "{driver[1]}";'
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