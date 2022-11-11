import csv
import tkinter
from tkinter import filedialog
import connectserver

db = connectserver.connectserver()
cursor = db.cursor()

# upload qualiying results
def upload_quali():
    try:
        root = tkinter.Tk()
        root.withdraw()
        filepath = filedialog.askopenfilename()

        with open(filepath) as result:
            reader = csv.DictReader(result)

            for row in reader:
                drivergroup = row.get("driverGroup")
                gp = row.get("GP")
                position = row.get("position")
                drivername = row.get("driverName")
                team = row.get("team")
                fl = row.get("fastestLap")
                if fl == '':
                    fl = None
                tyre = row.get("tyre")
                if tyre == '':
                    tyre = None
                status = row.get("driverStatus")

                # record the result
                query = "INSERT INTO qualiResult VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
                val = (drivergroup, gp, position, drivername, team, fl, tyre, status)
                cursor.execute(query, val)
            
        db.commit()
                
    except Exception as e:
        print(str(e))