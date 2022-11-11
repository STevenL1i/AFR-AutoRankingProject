import datetime
import random
import csv
import tkinter
from tkinter import filedialog
import connectserver

db = connectserver.connectserver()
cursor = db.cursor()

# upload the new driver profile
def welcome_newdriver():
    root = tkinter.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename()

    with open(filepath) as newdriver:
        reader = csv.DictReader(newdriver)
        
        for row in reader:
            drivername = row.get("driverName")
            team = row.get("team")
            group = row.get("driverGroup")
            status = row.get("driverStatus")
            jointime = row.get("joinTime")
            raceban = row.get("raceBan")
            qualiban = row.get("qualiBan")

            try:
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
                
                # update the driverlist
                query = "INSERT INTO driverList VALUES \
                        (%s, %s, %s, %s, %s, %s, %s, %s);"
                val = (drivername, team, group, status, jointime, raceban, qualiban, 1)
                cursor.execute(query, val)

                # update the driverLeaderBoard
                query = "INSERT INTO driverLeaderBoard \
                        (driverName, team, driverGroup, totalPoints) VALUES (%s, %s, %s, %s);"
                val = (drivername, team, group, 0)
                cursor.execute(query, val)

                # update the driver license point
                query = "INSERT INTO licensePoint (driverName, driverGroup, warning, totalLicensePoint) \
                    VALUES (%s, %s, %s, %s);"
                val = (drivername, group, 0, 12)
                cursor.execute(query, val)
                
                # create a LAN account for the new driver
                # firstly check if the driver already had an account
                query = f'SELECT * FROM LANusername WHERE driverName = {drivername};'
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
                        
                    query = "INSERT INTO LANusername VALUES (%s, %s, %s, %s);"
                    val = (drivername, username, password, "STAND BY")
                    cursor.execute(query, val)

                db.commit()

            except Exception as e:
                print(str(e))