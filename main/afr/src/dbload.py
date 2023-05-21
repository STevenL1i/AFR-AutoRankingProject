import csv
import json
import dbconnect
import deffunc as func
logpath = "log/log.log"

try:
    db = dbconnect.connect_with_conf("server.json", "db")
except Exception:
    db = dbconnect.connect_with_conf("server.json")
cursor = db.cursor()


settingsf = open("settings/settings.json", "r", encoding='utf-8')
settings:dict = json.load(settingsf)
settingsf.close()



def dbload_basic():
    """
    root = tkinter.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename()
    """
    func.logging(logpath, "Initializing database......", end="\n\n")
    print("initializing database......")

    # upload race calendar
    func.logging(logpath, "initializing race calendar......")
    print("initializing race calendar......\n")
    try:
        filename = settings["dbmanager"]["loadingconfig"]["raceCalendar"]
        if filename == 0:
            raise AttributeError("race calendar missing, this must be initialized when started")
        filepath = filename
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
            func.logging(logpath, f'Uploading race: {racedate:<10} {group:<3} {gpchn:<9} {gpeng}.........')
            cursor.execute(query, val)

        func.logging(logpath)
        race.close()

    except FileNotFoundError:
        func.logging(logpath, f'Cannot find file {filepath}, please check your "loadingconfig.json"')
        print(f'Cannot find file {filepath}, please check your "loadingconfig.json"')
        raise AttributeError("race calendar must be initialized")
    except AttributeError:
        raise AttributeError("race calendar must be initialized")
    
    
    
    # upload constructor leader board
    try:
        filename = settings["dbmanager"]["loadingconfig"]["constructorsLeaderBoard"]
        if filename == 0:
            raise AttributeError("User choose not to initialize constructors leaderboard")
        filepath = filename
        driver = open(filepath, "r")
        reader = csv.DictReader(driver)

        for row in reader:
            team = row.get("team")
            group = row.get("driverGroup")
            totalpoints = row.get("totalPoints")

            query = "INSERT INTO constructorsLeaderBoard (team, driverGroup, totalPoints) \
                        VALUES (%s, %s, %s);"
            val = (team, group, totalpoints)
            func.logging(logpath, f'Uploading team: {group:<3} {team}.........')
            cursor.execute(query, val)

        func.logging(logpath)        
        driver.close()
    
    except FileNotFoundError:
        func.logging(logpath, f'Cannot find file {filepath}, please check your "loadingconfig.json"')
        raise FileNotFoundError(f'Cannot find file {filepath}, please check your "loadingconfig.json"')
    except AttributeError as e:
        func.logging(logpath, str(e))
        print(str(e))



    # upload LAN account (optional)
    try:
        filename = settings["dbmanager"]["loadingconfig"]["LANusername"]
        if filename == 0:
            raise AttributeError("User choose not to initialize LANusername table")
        filepath = filename
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
        func.logging(logpath, str(e))
        print(str(e))
    
    
    db.commit()

    # Initialize date
    dbInitialize()
    func.logging(logpath, "season/database initialization complete!!!\n")
    print("season/database initialization complete!!!")


def dbInitialize():
    """
    # Initialize RaceDirector table
    query = "SELECT * FROM raceCalendar WHERE Round = '1' AND driverGroup = 'A2' ORDER BY Round ASC;"
    cursor.execute(query)
    result = cursor.fetchall()
    result = list(result[0])
    gpeng = result[3]
    group = result[4]
    date = result[1]

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
    func.logging(logpath, "initialze driver and constructor leaderboard.........")
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
    gpdict = settings["content"]["gp"]
    for race in result:
        race = list(race)
        gpkey = func.get_key(gpdict, race[2])
        func.logging(logpath, f'inserting column {gpkey}')
        query = f'ALTER TABLE driverLeaderBoard ADD {gpkey} tinyint;'
        cursor.execute(query)
        for i in range(1,3):
            query = f'ALTER TABLE constructorsLeaderBoard ADD {gpkey}_{i} tinyint;'
            cursor.execute(query)
            
        query = f'ALTER TABLE licensePoint ADD {gpkey} tinyint;'
        cursor.execute(query)
    
    func.logging(logpath)

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

    func.logging(logpath, "initialize qualirace FL table.........")
    print("initialize qualirace FL table.........")
    for race in result:
        # race: tuple (GP_ENG, driverGroup)
        query = "INSERT INTO qualiraceFL (GP, driverGroup) VALUES (%s, %s);"
        val = (race[0], race[1])
        cursor.execute(query, val)
    db.commit()
    
    func.logging(logpath)
    
    


def dbload():
    # LANusername
    filename = settings["dbmanager"]["loadingconfig"]["LANusername"]
    if filename != 0:
        filepath = filename
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

