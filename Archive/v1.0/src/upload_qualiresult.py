import csv
import tkinter as tk
from tkinter import filedialog
import connectserver

db = connectserver.connectserver()
cursor = db.cursor()


gp_dict = {
    "AUS": "Australia",
    "BHR": "Bahrain",
    "VNM": "Vietnam",
    "CHN": "China",
    "NLD": "Netherlands",
    "ESP": "Spain",
    "MCO": "Monaco",
    "AZE": "Azerbaijan",
    "CAN": "Canada",
    "FRA": "France",
    "AUT": "Austria",
    "GBR": "Britain",
    "HUN": "Hungary",
    "BEL": "Belgium",
    "ITA": "Italy",
    "SGP": "Singapore",
    "RUS": "Russia",
    "JPN": "Japan",
    "USA": "USA",
    "MEX": "Mexico",
    "BRA": "Brazil",
    "UAE": "Abu Dahbi"
}
def get_key(my_dict, val):
    for key, value in my_dict.items():
        if val == value:
            return key
    return "key doesn't exist"


# upload qualifying result
def upload_quali():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    
    with open(file_path) as result:
        reader = csv.DictReader(result)

        for row in reader:
            drivergroup = row.get("driverGroup")
            gp = row.get("GP")
            position = row.get("position")
            drivername = row.get("driverName")
            team = row.get("team")
            fl = row.get("fastestLap")
            tyre = row.get("tyre")
            driverstatus = row.get("driverStatus")
            if tyre == 'n':
                tyre = None
            if fl == 'null':
                fl = None

            query = "INSERT INTO qualiResult VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
            val = (drivergroup, gp, position, drivername, team, fl, tyre, driverstatus)
            cursor.execute(query, val)

            # pass the pole to leaderboard
            gpkey = get_key(gp_dict, gp)
            gpkey += '_pole'
            if position == '1':
                query = f'UPDATE driverLeaderBoard \
                        SET {gpkey} = 1, \
                        totalPoints = totalPoints + 1 \
                        WHERE driverName = "{drivername}";'
                cursor.execute(query)

                query = f'UPDATE constructorsLeaderBoard \
                        SET totalPoints = totalPoints + 1 \
                        WHERE team = "{team}" and driverGroup = "{drivergroup}";'
                cursor.execute(query)

        db.commit()