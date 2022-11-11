import csv
import json
import connectserver
import deffunc as func


try:
    db = connectserver.connectserver("server.json", "db")
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
    print("initializing database......")

    # upload race calendar
    print("initializing race calendar......\n")
    try:
        filename = loadingsetup["raceCalendar"]
        if filename == 0:
            raise AttributeError("race calendar missing, this must be initialized when started")
        filepath = "srcdata_input/" + filename
        race = open(filepath, "r", encoding='utf-8')
        reader = csv.DictReader(race)

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
            print(f'Uploading race: {racedate:<10} {group:<3} {gpchn:<6} {gpeng}.........')
            cursor.execute(query, val)

        
        race.close()

    except FileNotFoundError:
        print(f'Cannot find file {filepath}, please check your "loadingconfig.json"')
        raise AttributeError("race calendar must be initialized")
    except AttributeError:
        raise AttributeError("race calendar must be initialized")
    
    
    # upload constructor leader board
    try:
        filename = loadingsetup["constructorsLeaderBoard"]
        if filename == 0:
            raise AttributeError("User choose not to initialize constructors leaderboard")
        filepath = "srcdata_input/" + filename
        driver = open(filepath, "r")
        reader = csv.DictReader(driver)

        for row in reader:
            team = row.get("team")
            group = row.get("driverGroup")
            totalpoints = row.get("totalPoints")

            query = "INSERT INTO constructorsLeaderBoard (team, driverGroup, totalPoints) \
                        VALUES (%s, %s, %s);"
            val = (team, group, totalpoints)
            print(f'Uploading team: {group:<3} {team}.........')
            cursor.execute(query, val)

        
        driver.close()
    
    except FileNotFoundError:
        raise FileNotFoundError(f'Cannot find file {filepath}, please check your "loadingconfig.json"')
    except AttributeError as e:
        print(str(e))


    # upload LAN account (optional)
    try:
        filename = loadingsetup["LANusername"]
        if filename == 0:
            raise AttributeError("User choose not to initialize LANusername table")
        filepath = "srcdata_input/" + filename
        driver = open(filepath, "r")
        reader = csv.DictReader(driver)

        for row in reader:
            drivername = row.get("driverName")
            username = row.get("username")
            password = row.get("password")
            status = row.get("accountStatus")

            query = "INSERT INTO LANusername VALUES \
                    (%s, %s, %s, %s);"
            val = (drivername, username, password, status)
            print(f'Uploading account: {drivername:<30}: {username:<30} - **********')
            cursor.execute(query, val)

        
        driver.close()
    
    except FileNotFoundError:
        raise FileNotFoundError(f'Cannot find file {filepath}, please check your "loadingconfig.json"')
    except AttributeError as e:
        print(str(e))
    
    db.commit()

    # Initialize date
    dbInitialize()
    print("season/database initialization complete!!!")


def dbInitialize():
    # Initialize RaceDirector table
    query = "SELECT * FROM raceCalendar WHERE Round = '1' AND driverGroup = 'A2' ORDER BY Round ASC;"
    cursor.execute(query)
    result = cursor.fetchall()
    result = list(result[0])
    gpeng = result[3]
    group = result[4]
    date = result[1]

    """
    print("initialize the driverlist (prefix header driver).........")
    query = "INSERT INTO driverList VALUES (%s, %s, %s, %s, %s, %s);"
    val = ("Race Director", "Reserve", "A3", "reserved driver", "2022-01-01", 0)
    cursor.execute(query, val)
    

    # Initialize RaceDirector record
    print("initialize the race director table (prefix header record).........")
    query = "INSERT INTO raceDirector VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    val = ("C000", date, "Race Director", group, gpeng, "prefix", 0, 0, 0, 0, "prefix")
    cursor.execute(query, val)
    """


    # Initialize driver and constructor leaderboard and license point board
    print("initialze driver and constructor leaderboard.........")
    query = "SELECT DISTINCT(Round), GP_CHN, GP_ENG FROM raceCalendar WHERE Round is not null;"
    cursor.execute(query)
    result = cursor.fetchall()
    
    query = "ALTER TABLE driverLeaderBoard DROP COLUMN totalPoints;"
    cursor.execute(query)
    query = "ALTER TABLE constructorsLeaderBoard DROP COLUMN totalPoints;"
    cursor.execute(query)
    query = "ALTER TABLE licensePoint DROP COLUMN warning, DROP COLUMN totalLicensePoint, DROP COLUMN raceBan, DROP COLUMN qualiBan;"
    cursor.execute(query)
    

    # loading gpdict
    gp = open("gp.json", "r")
    gpdict = json.load(gp)
    gp.close()
    for race in result:
        race = list(race)
        gpkey = func.get_key(gpdict, race[2])
        print(f'inserting column {gpkey}')
        query = f'ALTER TABLE driverLeaderBoard ADD {gpkey} tinyint;'
        cursor.execute(query)
        for i in range(1,3):
            query = f'ALTER TABLE constructorsLeaderBoard ADD {gpkey}_{i} tinyint;'
            cursor.execute(query)
            
        query = f'ALTER TABLE licensePoint ADD {gpkey} tinyint;'
        cursor.execute(query)
        

    query = "ALTER TABLE driverLeaderBoard ADD totalPoints smallint;"
    cursor.execute(query)
    query = "ALTER TABLE constructorsLeaderBoard ADD totalPoints smallint;"
    cursor.execute(query)
    query = "ALTER TABLE licensePoint ADD warning decimal(3,1), \
            ADD totalLicensePoint tinyint, ADD raceBan tinyint, ADD qualiBan tinyint;"
    cursor.execute(query)
    

    # Initialize qualiraceFL table
    query = "SELECT GP_ENG, driverGroup FROM raceCalendar WHERE Round is not null \
            ORDER BY Round, driverGroup ASC"
    cursor.execute(query)
    result = cursor.fetchall()

    print("initialize qualirace FL table.........")
    for race in result:
        # race: tuple (GP_ENG, driverGroup)
        query = "INSERT INTO qualiraceFL (GP, driverGroup) VALUES (%s, %s);"
        val = (race[0], race[1])
        cursor.execute(query, val)
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

