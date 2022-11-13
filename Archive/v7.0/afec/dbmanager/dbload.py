import csv
import json
from datetime import datetime
import tkinter
from tkinter import filedialog
import connectserver
import ref_dict

try:
    db = connectserver.connectserver("server.json", "afec")
except Exception:
    db = connectserver.connectserver("server.json")
cursor = db.cursor()


with open("loadingconfig.json") as config:
    loadingsetup = json.load(config)
    item = loadingsetup.keys()



def dbload_basic():
    """
    root = tkinter.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename()
    """

    # upload race calendar
    filepath = "srcdata_input/" + loadingsetup["raceCalendar"]
    with open(filepath, "r") as race:
        reader = csv.DictReader(race)

        for row in reader:
            round = row.get("Round")
            racedate = row.get("raceDate")
            gpchn = row.get("GP_CHN")
            gpeng = row.get("GP_ENG")
            length = row.get("raceLength")
            status = row.get("raceStatus")
            if round == "":
                round = None

            query = "INSERT INTO raceCalendar VALUES \
                    (%s, %s, %s, %s, %s, %s);"
            val = (round, racedate, gpchn, gpeng, length, status)
            cursor.execute(query, val)

        db.commit()


    # Initialize date
    dbInitialize()




def dbInitialize():
    # Initialize RaceDirector table
    query = "SELECT * FROM raceCalendar WHERE Round = '1' ORDER BY Round ASC;"
    cursor.execute(query)
    result = cursor.fetchall()
    result = list(result[0])
    gpeng = result[3]
    date = result[1]


    query = "INSERT INTO driverList VALUES (%s, %s, %s, %s, %s, %s);"
    val = ("Race Director", "Reserve", "AFEC", "reserved driver", "2022-01-01", 0)
    cursor.execute(query, val)
    db.commit()

    # Initialize RaceDirector record
    query = "INSERT INTO raceDirector VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    val = ("C000", date, "Race Director", "AFEC", gpeng, "prefix", 0, 0, 0, 0, "prefix")
    cursor.execute(query, val)
    db.commit()


    # Initialize driver and constructor leaderboard and license point board
    query = "SELECT DISTINCT(Round), GP_CHN, GP_ENG FROM raceCalendar WHERE Round is not null;"
    cursor.execute(query)
    result = cursor.fetchall()
    
    query = "ALTER TABLE driverLeaderBoard DROP COLUMN totalPoints;"
    cursor.execute(query)
    query = "ALTER TABLE constructorsLeaderBoard DROP COLUMN totalPoints;"
    cursor.execute(query)
    query = "ALTER TABLE licensePoint DROP COLUMN warning, DROP COLUMN totalLicensePoint, DROP COLUMN raceBan, DROP COLUMN qualiBan;"
    cursor.execute(query)
    db.commit()

    for race in result:
        race = list(race)
        gpkey = ref_dict.get_key(ref_dict.gp_dict, race[2])
        query = f'ALTER TABLE driverLeaderBoard ADD {gpkey} tinyint;'
        cursor.execute(query)
        for i in range(1,4):
            query = f'ALTER TABLE constructorsLeaderBoard ADD {gpkey}_{i} tinyint;'
            cursor.execute(query)
            
        query = f'ALTER TABLE licensePoint ADD {gpkey} tinyint;'
        cursor.execute(query)
        db.commit()

    query = "ALTER TABLE driverLeaderBoard ADD totalPoints smallint;"
    cursor.execute(query)
    query = "ALTER TABLE constructorsLeaderBoard ADD totalPoints float;"
    cursor.execute(query)
    query = "ALTER TABLE licensePoint ADD warning decimal(3,1), \
            ADD totalLicensePoint tinyint, ADD raceBan tinyint, ADD qualiBan tinyint;"
    cursor.execute(query)
    db.commit()
    
    


def dbload():
    # LANusername
    filepath = "srcdata_input/" + loadingsetup["LANusername"]
    if filepath != 0:
        with open(filepath, "r") as lanacct:
            reader = csv.DictReader(lanacct)

            for row in reader:
                # driverName username password accountStatus
                drivername = row.get("driverName")
                usrname = row.get("username")
                pwd = row.get("password")
                acctstatus = row.get("accountStatus")

                query = "INSERT INTO LANusername VALUES \
                        (%s, %s, %s, %s);"
                val = (drivername, usrname, pwd, acctstatus)
                cursor.execute(query, val)

            db.commit()

