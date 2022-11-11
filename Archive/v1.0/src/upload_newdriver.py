import datetime
import random
import csv
import tkinter as tk
from tkinter import filedialog
import connectserver

db = connectserver.connectserver()
cursor = db.cursor()

# upload the new driver profile
def welcome_newdriver():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()

    with open(file_path) as newdriver:
        reader = csv.DictReader(newdriver)

        for row in reader:
            drivername = row.get("driverName")
            team = row.get("team")
            group = row.get("driverGroup")
            status = row.get("driverStatus")

            query = "INSERT INTO driverList VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
            val = (drivername, team, group, status, datetime.datetime.today().strftime('%Y-%m-%d'), 0, 0, 1)
            cursor.execute(query, val)

            query = "INSERT INTO driverLeaderBoard (driverName, team, driverGroup, totalPoints) \
                    VALUES (%s, %s, %s, %s)"
            val = (drivername, team, group, 0)
            cursor.execute(query, val)

            query = "INSERT INTO licensePoint (driverName, driverGroup, warning, totalLicensePoint) \
                    VALUES (%s, %s, %s, %s)"
            val = (drivername, group, 0, 12)
            cursor.execute(query, val)

            # create a LAN account for new driver
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
                
            query = "INSERT INTO LANusername VALUES (%s, %s, %s, %s)"
            val = (drivername, username, password, "STAND BY")
            if group == "A3" and team == "Testing":
                cursor.execute(query, val)

        
        db.commit()

