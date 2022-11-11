import csv
import connectserver

db = connectserver.connectserver()
cursor = db.cursor()

def dbload():
    # driverList
    filepath = "src/srcdata_input/s8_driverlist.csv"
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

    filepath = "src/srcdata_input/s8_driverLeaderBoard.csv"
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

    filepath = "src/srcdata_input/s8_constructorsLeaderBoard.csv"
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

    filepath = "src/srcdata_input/s8_licensepoint.csv"
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

    filepath = "src/srcdata_input/s8_racecalendar.csv"
    with open(filepath, "r") as driver:
        reader = csv.DictReader(driver)

        for row in reader:
            round = row.get("Round")
            racedate = row.get("raceDate")
            gpchn = row.get("GP_CHN")
            gpeng = row.get("GP_ENG")
            group = row.get("driverGroup")
            status = row.get("raceStatus")

            query = "INSERT INTO raceCalendar VALUES \
                    (%s, %s, %s, %s, %s, %s);"
            val = (round, racedate, gpchn, gpeng, group, status)
            cursor.execute(query, val)

        db.commit()

    filepath = "src/srcdata_input/s8_lanusername.csv"
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

    filepath = "src/srcdata_input/s8_qualiraceFL.csv"
    with open(filepath, "r") as race:
        reader = csv.DictReader(race)

        for row in reader:
            gp = row.get("GP")
            group = row.get("driverGroup")

            query = "INSERT INTO qualiraceFL (GP, driverGroup) \
                    VALUES (%s, %s);"
            val = (gp, group)
            cursor.execute(query, val)
        
        db.commit()
    
    query = "INSERT INTO raceDirector VALUES \
            (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
    val = ("C000", "2021-07-17", "Linus Sebastian", "A2", "Australia", "None", 0, 0, "header")
    cursor.execute(query,val)
    db.commit()