import datetime
import random
import csv
import tkinter
from tkinter import filedialog
import connectserver

# upload the new driver profile
def welcome_newdriver():
    db = connectserver.connectserver("server.json", "afec")
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
                status = row.get("driverStatus")
                jointime = row.get("joinTime")
                raceban = row.get("raceBan")
                qualiban = row.get("qualiBan")

                if drivername == "" and team == "" and group == "" and status == "" and jointime == "" and raceban == "" and qualiban == "":
                    break

                if jointime == '':
                    jointime = datetime.datetime.today().strftime('%Y-%m-%d')
                
                if qualiban == '':
                    qualiban = 0
                else:
                    qualiban = int(qualiban)
                
                if raceban == '':
                    raceban = 0
                else:
                    raceban = int(raceban)

                record += 1
                print(f'Uploading records {record}......')
                
                # update the driverlist
                query = "INSERT INTO driverList VALUES \
                        (%s, %s, %s, %s, %s, %s);"
                val = (drivername, team, group, status, jointime, 1)
                cursor.execute(query, val)

                # update the driverLeaderBoard
                query = "INSERT INTO driverLeaderBoard \
                        (driverName, team, driverGroup, totalPoints) VALUES (%s, %s, %s, %s);"
                val = (drivername, team, group, 0)
                cursor.execute(query, val)

                # update the driver license point
                query = "INSERT INTO licensePoint (driverName, driverGroup, warning, totalLicensePoint, raceBan, qualiBan) \
                    VALUES (%s, %s, %s, %s, %s, %s);"
                val = (drivername, group, 0, 12, raceban, qualiban)
                cursor.execute(query, val)



            db.commit()
        print()
        print("新车手数据上传成功，稍后请记得将文件上传到赛会群备份")

    except Exception as e:
        print(str(e))
        print("数据上传失败，请检查上传文件数据是否正确")
        print("错误提示：" + str(e))

if __name__ == "__main__":
    welcome_newdriver()