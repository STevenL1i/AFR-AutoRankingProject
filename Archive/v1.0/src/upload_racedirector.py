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


# upload race director result
def upload_racedirector():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()

    # get the post-race penalty awarded by stewards
    with open(file_path) as result:
        reader = csv.DictReader(result)

        for row in reader:
            drivername = row.get("driverName")
            drivergroup = row.get("driverGroup")
            gp = row.get("GP")
            penalty = row.get("penalty")
            penaltyLP = row.get("penaltyLP")
            penaltywarning = row.get("penaltyWarning")
            description = row.get("PenaltyDescription")
            
            query = "INSERT INTO raceDirector VALUES (%s, %s, %s, %s, %s, %s, %s);"
            val = (drivername, drivergroup, gp, penalty, penaltyLP, penaltywarning, description)
            cursor.execute(query, val)

            gpkey = get_key(gp_dict, gp)
            query = f'UPDATE licensePoint \
                    SET {gpkey} = {penaltyLP}, \
                    totalLicensePoint = totalLicensePoint - {penaltyLP} \
                    WHERE driverName = "{drivername}";'
            cursor.execute(query)

            query = f'UPDATE licensePoint \
                    SET warning = warning + {penaltywarning} \
                    WHERE driverName = "{drivername}";'
            cursor.execute(query)

            qualiban = row.get("qualiban")
            raceban = row.get("raceban")
            if qualiban != '':
                query = f'UPDATE driverList \
                        SET qualiBan = qualiBan + {qualiban} \
                        WHERE driverName = "{drivername}";'
            if raceban != '':
                query = f'UPDATE driverList \
                        SET raceBan = raceBan + {raceban} \
                        WHERE driverName = "{drivername}";'

        db.commit()