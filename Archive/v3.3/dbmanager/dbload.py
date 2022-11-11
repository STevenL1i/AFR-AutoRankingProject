from datetime import datetime
import csv
import connectserver

db = connectserver.connectserver()
cursor = db.cursor()

def load_basic():
    ## this part (race calendar) is loaded when created tables

    filepath = "srcdata_input\Preseason_racecalendar.csv"
    with open(filepath, "r") as driver:
        reader = csv.DictReader(driver)

        for row in reader:
            round = row.get("Round")
            racedate = row.get("raceDate")
            gpchn = row.get("GP_CHN")
            gpeng = row.get("GP_ENG")
            group = row.get("driverGroup")
            status = row.get("raceStatus")
            if round == "":
                round = None

            query = "INSERT INTO raceCalendar VALUES \
                    (%s, %s, %s, %s, %s, %s);"
            val = (round, racedate, gpchn, gpeng, group, status)
            cursor.execute(query, val)

        db.commit()
    """
    filepath = "srcdata_input\Preseason_lanusername.csv"
    with open(filepath, "r") as driver:
        reader = csv.DictReader(driver)

        for row in reader:
            drivername = row.get("driverName")
            username = row.get("username")
            password = row.get("password")
            status = row.get("accountStatus")

            query = "INSERT INTO LANusername VALUES \
                    (%s, %s, %s, %s);"
            val = (drivername, username, password, status)
            cursor.execute(query, val)

        db.commit()
    """
    query = "SELECT * FROM raceCalendar WHERE Round != 0 OR Round != null ORDER BY Round ASC;"
    cursor.execute(query)
    result = cursor.fetchall()

    for r in result:
        r = list(r)
        gp = r[3]
        group = r[4]

        query = "INSERT INTO qualiraceFL (GP, driverGroup) \
                    VALUES (%s, %s);"
        val = (gp, group)
        cursor.execute(query, val)

    db.commit()

    filepath = "srcdata_input/Preseason_constructorsLeaderBoard.csv"
    with open(filepath, "r") as driver:
        reader = csv.DictReader(driver)

        for row in reader:
            team = row.get("team")
            group = row.get("driverGroup")
            totalpoints = row.get("totalPoints")

            query = "INSERT INTO constructorsLeaderBoard (team, driverGroup, totalPoints) \
                        VALUES (%s, %s, %s);"
            val = (team, group, totalpoints)
            cursor.execute(query, val)

        db.commit()

    query = "INSERT INTO driverList VALUES (%s, %s, %s, %s, %s, %s);"
    val = ("Race Director", "Reserve", "A3", "reserved driver", "2021-01-01", 0)
    cursor.execute(query, val)
    db.commit()

    query = "INSERT INTO raceDirector VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    val = ("C000", "2021-01-01", "Race Director", "A3", "Bahrain", "prefix", 0, 0, 0, 0, "prefix")
    cursor.execute(query, val)
    db.commit()


def dbload():
    # driverList
    filepath = "src/srcdata_input/driverlist.csv"
    with open(filepath, "r") as driver:
        reader = csv.DictReader(driver)

        for row in reader:
            drivername = row.get("driverName")
            team = row.get("team")
            group = row.get("driverGroup")
            status = row.get("driverStatus")
            jointime = row.get("joinTime")

            query = "INSERT INTO driverList VALUES \
                    (%s, %s, %s, %s, %s, %s);"
            val = (drivername, team, group, status, jointime, 1)
            cursor.execute(query, val)

        db.commit()

    filepath = "src/srcdata_input/driverLeaderBoard.csv"
    with open(filepath, "r") as driver:
        reader = csv.DictReader(driver)

        for row in reader:
            drivername = row.get("driverName")
            team = row.get("team")
            group = row.get("driverGroup")
            totalpoints = row.get("totalPoints")

            query = "INSERT INTO driverLeaderBoard (driverName, team, driverGroup, totalPoints) \
                    VALUES (%s, %s, %s, %s);"
            val = (drivername, team, group, totalpoints)
            cursor.execute(query, val)

        db.commit()

    filepath = "src/srcdata_input/constructorsLeaderBoard.csv"
    with open(filepath, "r") as driver:
        reader = csv.DictReader(driver)

        for row in reader:
            team = row.get("team")
            group = row.get("driverGroup")
            totalpoints = row.get("totalPoints")

            query = "INSERT INTO constructorsLeaderBoard (team, driverGroup, totalPoints) \
                    VALUES (%s, %s, %s);"
            val = (team, group, totalpoints)
            cursor.execute(query, val)

        db.commit()

    filepath = "src/srcdata_input/licensepoint.csv"
    with open(filepath, "r") as driver:
        reader = csv.DictReader(driver)

        for row in reader:
            drivername = row.get("driverName")
            group = row.get("driverGroup")
            warning = row.get("warning")
            totalLP = row.get("totalLicensePoint")

            query = "INSERT INTO licensePoint (driverName, driverGroup, warning, totalLicensePoint, raceBan, qualiBan) \
                    VALUES (%s, %s, %s, %s, %s, %s);"
            val = (drivername, group, warning, totalLP, 0, 0)
            cursor.execute(query, val)

        db.commit()


    query = "INSERT INTO raceDirector VALUES \
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    val = ("C000", "2021-07-17", "Linus Sebastian", "A2", "Australia", "None", 0, 0, 0, 0, "header")
    cursor.execute(query,val)
    db.commit()