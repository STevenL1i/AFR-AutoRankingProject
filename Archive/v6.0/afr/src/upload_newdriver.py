import datetime
import random
import csv
import tkinter
from tkinter import filedialog
import connectserver
import mysql.connector

# upload the new driver profile
def welcome_newdriver():
    db = connectserver.connectserver("server.json", "afr")
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
                pwd = row.get("password")
                if drivername == "" and team == "" and group == "" and status == "" \
                and jointime == "" and raceban == "" and qualiban == "" and pwd == "":
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
                
                # create a LAN account for the new driver
                """
                # firstly check if the driver already had an account
                query = f'SELECT * FROM LANusername WHERE driverName = "{drivername}";'
                cursor.execute(query)
                result = cursor.fetchall()
                # creating account if driver doesnt have
                if len(result) == 0:
                    randomcode = random.randint(0,9999)
                    if randomcode < 10:
                        randomcode = '000' + str(randomcode)
                    elif randomcode < 100:
                        randomcode = '00' + str(randomcode)
                    elif randomcode < 1000:
                        randomcode = '0' + str(randomcode)
                    else:
                        randomcode = str(randomcode)
                    
                    username = ""
                    for c in drivername:
                        if c == ',' or c == '.' or c == ' ' or c == '-' or c == '_':
                            pass
                        else:
                            username += c
                    
                    password = username + randomcode
                """
                username = drivername.replace(",", "").replace(".", "").replace(" ", "").replace("-", "").replace("_", "")
                try:
                    query = "INSERT INTO afr_elo.LANusername VALUES (%s, %s, %s, %s);"
                    val = (drivername, username, pwd, "STANDBY")
                    cursor.execute(query, val)
                except mysql.connector.errors.IntegrityError:
                    query = f'UPDATE afr_elo.LANusername SET password = "{pwd}" WHERE username = "{username}";'
                    cursor.execute(query)




            db.commit()
        print()
        print("新车手数据上传成功，稍后请记得将文件上传到赛会群备份")

    except Exception as e:
        print(str(e))
        print("数据上传失败，请检查上传文件数据是否正确")
        print("错误提示：" + str(e))

if __name__ == "__main__":
    welcome_newdriver()