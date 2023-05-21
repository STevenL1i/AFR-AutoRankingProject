import json, traceback, xlsxwriter
from datetime import datetime

import mysql.connector
import paramiko
import dbconnect
import deffunc as func

# loading all the necessary json settings
# settings
settingsf = open("settings/settings.json", "r", encoding='utf-8')
settings:dict = json.load(settingsf)
settingsf.close()
# format
formatf = open("settings/format.json", "r", encoding='utf-8')
format:dict = json.load(formatf)
formatf.close()
# log
logpath = settings["default"]["log"]





def get_drivergrouplist(db:mysql.connector.MySQLConnection) -> list:
    cursor = db.cursor()

    # get driver group list
    query = "SELECT DISTINCT(driverGroup) FROM raceCalendar \
            ORDER BY CASE driverGroup\n"
    grouplist = settings["drivergroup"]["order"]
    for i in range(0, len(grouplist)):
        query += f'WHEN "{grouplist[i]}" THEN {i+1} \n'
    query += f'ELSE {len(grouplist)+1} \nEND, driverGroup'
    cursor.execute(query)
    result = cursor.fetchall()
    grouplist = []
    for group in result:
        grouplist.append(group[0])
    
    return grouplist



def get_driverlist_data(db:mysql.connector.MySQLConnection) -> dict:
    cursor = db.cursor()

    driverlist_data = {}
    """
    driverlist_data = {
        drivergroup:
        {
            ### for teamed driver ###
            teamcolor:
            {
                "teamname":
                "1st driver":
                "2ed driver":
                "3rd driver":
            }

            ### for rest of the driver ###
            team: [driver0, driver1, ......]
        }
    }
    """
    query = "SELECT * FROM get_driverList;"
    func.logging(logpath, "Fetching all driver list data......")
    print("Fetching all driver list data......")
    cursor.execute(query)
    result = cursor.fetchall()
    func.logging(logpath, f'driver list data fetched: {len(result)} drivers')

    for driver in result:
        group = driver[2]
        drivername = driver[0]
        teamname = driver[1]
        driverstatus = driver[3]
        teamcolor = driver[6]
        if teamcolor is not None:
            try:
                driverlist_data[group][teamcolor][driverstatus] = drivername
            except KeyError:
                try:
                    driverlist_data[group][teamcolor] = {"teamname": teamname, driverstatus: drivername}
                except KeyError:
                    driverlist_data[group] = {}
                    driverlist_data[group][teamcolor] = {"teamname": teamname, driverstatus: drivername}
        
        else:
            try:
                driverlist_data[group][teamname].append(drivername)
            except KeyError:
                try:
                    driverlist_data[group][teamname] = [drivername]
                except KeyError:
                    driverlist_data[group] = {teamname: [drivername]}

    return driverlist_data



def get_raceCalendar_data(db:mysql.connector.MySQLConnection) -> dict:
    cursor = db.cursor()

    racecalendar_data = {}
    """
    racecalendar_data = {
        drivergroup:
        {
            racedate:
            {
                "Round":
                "GP_CHN":
                "status":
            }
        }
    }
    """
    query = "SELECT * FROM get_raceCalendar;"
    func.logging(logpath, "Fetching race calendar data......")
    print("Fetching race calendar data......")
    cursor.execute(query)
    result = cursor.fetchall()
    func.logging(logpath, f'race calendar data fetched: {len(result)} races (including holiday)')

    for race in result:
        group = race[4]
        racedate = race[1]
        round = race[0]
        gpchn = race[2]
        status = race[5]
        try:
            racecalendar_data[group][racedate] = {"Round": round, "GP_CHN": gpchn, "status": status}
        except KeyError:
            racecalendar_data[group] = {}
            racecalendar_data[group][racedate] = {"Round": round, "GP_CHN": gpchn, "status": status}

    return racecalendar_data



def get_shortleaderboard_data(db:mysql.connector.MySQLConnection) -> dict:
    cursor = db.cursor()

    shortleaderboard_data = {}
    """
    shortleaderboard_data = {
        drivergroup:
        {
            "driver":
            {
                drivername:
                {
                    "team":
                    "teamcolor":
                    "totalpoints":
                    "Warning":
                    "QB":
                    "RB":
                    "LP":
                }
            },
            "team":
            {
                teamname:
                {
                    "teamcolor":
                    "totalpoints":
                }
                
            }
        }
    }
    """

    # driver leaderboard short
    query = "SELECT * FROM get_driverleaderboard_short;"
    func.logging(logpath, "Fetching driver short leaderboard data......")
    print("Fetching driver short leaderboard data......")
    cursor.execute(query)
    result = cursor.fetchall()
    func.logging(logpath, f'driver leaderboard data fetched: {len(result)} drivers')

    for driver in result:
        group = driver[3]
        drivername = driver[0]
        team = driver[1]
        teamcolor = driver[2]
        totalpoints = driver[4]
        warning = driver[6]
        qb = driver[7]
        rb = driver[8]
        lp = driver[5]

        try:
            shortleaderboard_data[group]["driver"][drivername] = {
                "team": team, "teamcolor": teamcolor, "totalpoints": totalpoints,
                "Warning": warning, "QB": qb, "RB": rb, "LP": lp
            }
        except KeyError:
            shortleaderboard_data[group] = {"driver": {}}
            shortleaderboard_data[group]["driver"][drivername] = {
                "team": team, "teamcolor": teamcolor, "totalpoints": totalpoints,
                "Warning": warning, "QB": qb, "RB": rb, "LP": lp
            }


    # constrcutors leaderboard short
    query = "SELECT * FROM get_consleaderboard_short;"
    func.logging(logpath, "Fetching constrcutors short leaderboard data......")
    print("Fetching constrcutors short leaderboard data......")
    cursor.execute(query)
    result = cursor.fetchall()
    func.logging(logpath, f'constrcutors leaderboard data fetched: {len(result)} teams', end="\n\n")

    for team in result:
        group = team[2]
        teamname = team[0]
        teamcolor = team[1]
        totalpoints = team[3]

        try:
            shortleaderboard_data[group]["team"][teamname] = {
                "teamcolor": teamcolor, "totalpoints": totalpoints
            }
        except KeyError:
            shortleaderboard_data[group]["team"] = {}
            shortleaderboard_data[group]["team"][teamname] = {
                "teamcolor": teamcolor, "totalpoints": totalpoints
            }

    return shortleaderboard_data



def get_raceDirector(db:mysql.connector.MySQLConnection) -> list:
    cursor = db.cursor()

    racedirector_data = []
    query = "SELECT * FROM get_raceDirector;"
    func.logging(logpath, f'Fetching race director data......')
    print(f'Fetching race director data......')
    cursor.execute(query)
    result = cursor.fetchall()
    func.logging(logpath, f'race director data fetched: {len(result)} records')
    for record in result:
        racedirector_data.append(record)

    return racedirector_data







def driverlist(workbook:xlsxwriter.Workbook, db:mysql.connector.MySQLConnection):
    cursor = db.cursor()
    func.logging(logpath, func.delimiter_string("Exporting driverlist", length=60), end="\n\n")
    print(func.delimiter_string("Exporting driverlist", length=60), end="\n\n")
    driverlist = workbook.add_worksheet("车手名单")


    # fetching driver list data
    driverlist_data = get_driverlist_data(db)
    func.logging(logpath)
    print()
    
    # get driver group list
    grouplist = get_drivergrouplist(db)

    # getting team list order (setting by user)
    teamlist = settings["content"]["teamorder"]
    
    # getting driver list by each group
    # and writing into the table
    colcursor = 0
    for group in grouplist:
        func.logging(logpath, f'Writing driverlist of {group}......', end="\n\n")
        print(f'Writing driverlist of {group}......')
        """
        # setting column width and writing header
        # using different layout when 
        driverlist.set_column(colcursor+0, colcursor+0, 18)
        driverlist.set_column(colcursor+1, colcursor+1, 20)
        driverlist.set_column(colcursor+2, colcursor+2, 3)
        driverlist.set_column(colcursor+3, colcursor+3, 20)
        driverlist.set_column(colcursor+4, colcursor+4, 3)
        """

        # if team is enabled (in settings/settings.json)
        if settings["drivergroup"]["enable_team"][group] == True:
            # setting header row height and column width for teamed driver
            driverlist.set_row(0, 16)
            driverlist.set_column(colcursor+0, colcursor+0, 18)
            driverlist.set_column(colcursor+1, colcursor+1, 20)
            driverlist.set_column(colcursor+2, colcursor+2, 3)
            # writing header
            driverlist.merge_range(0, colcursor, 0, colcursor+1, settings["content"]["codename"][group], workbook.add_format(format["default"]["header_12"]))
            driverlist.write(0, colcursor+3, "Reserve", workbook.add_format(format["default"]["default_11"]))


            ### getting teamed driver ###
            rowcursor = 1
            for team in teamlist:
                # team name header
                func.logging(logpath, f'Writing team header: {group}-{team}......')
                driverlist.write(rowcursor, colcursor, team, workbook.add_format(format["driverformat"][team]))
                driverlist.write(rowcursor+1, colcursor, settings["content"]["codename"][team], workbook.add_format(format["driverformat"][team]))
                try:
                    driverlist.write(rowcursor+2, colcursor, driverlist_data[group][team]["teamname"], workbook.add_format(format["driverformat"][team]))
                except KeyError:
                    driverlist.write(rowcursor+2, colcursor, None, workbook.add_format(format["driverformat"][team]))

                # 1st driver (if exist)
                try:
                    func.logging(logpath, f'Writing driver: {group}-{driverlist_data[group][team]["teamname"]}-{driverlist_data[group][team]["1st driver"]}')
                    driverlist.write(rowcursor, colcursor+1, driverlist_data[group][team]["1st driver"], workbook.add_format(format["driverformat"][team]))
                except KeyError:
                    driverlist.write(rowcursor, colcursor+1, None, workbook.add_format(format["driverformat"][team]))
                
                # 2ed driver (if exist)
                try:
                    func.logging(logpath, f'Writing driver: {group}-{driverlist_data[group][team]["teamname"]}-{driverlist_data[group][team]["2ed driver"]}')
                    driverlist.write(rowcursor+1, colcursor+1, driverlist_data[group][team]["2ed driver"], workbook.add_format(format["driverformat"][team]))
                except KeyError:
                    driverlist.write(rowcursor+1, colcursor+1, None, workbook.add_format(format["driverformat"][team]))

                # 3rd driver (if exist)
                try:
                    func.logging(logpath, f'Writing driver: {group}-{driverlist_data[group][team]["teamname"]}-{driverlist_data[group][team]["3rd driver"]}')
                    driverlist.write(rowcursor+2, colcursor+1, driverlist_data[group][team]["3rd driver"], workbook.add_format(format["driverformat"][team]))
                except KeyError:
                    driverlist.write(rowcursor+2, colcursor+1, None, workbook.add_format(format["driverformat"][team]))
                
                rowcursor += 3
            
            colcursor += 3
            ### END getting teamed driver ###


        ### getting reserve driver ###
        # setting column width for reserve driver
        driverlist.set_column(colcursor+0, colcursor+0, 20)
        driverlist.set_column(colcursor+1, colcursor+1, 3)
        # writing header
        if settings["drivergroup"]["enable_team"][group] == False:
            driverlist.write(0, colcursor, settings["content"]["codename"][group], workbook.add_format(format["default"]["header_12"]))
        else:
            driverlist.write(0, colcursor, "Reserve", workbook.add_format(format["default"]["default_11"]))

        # writing reserved driver
        rowcursor = 1
        try:
            for driver in driverlist_data[group]["Reserve"]:
                func.logging(logpath, f'Writing driver: {group}-Reserve-{driver}')
                driverlist.write(rowcursor, colcursor, driver, workbook.add_format(format["driverformat"]["Reserve"]))
                rowcursor += 1
        except KeyError:
            pass
        
        try:
            for driver in driverlist_data[group]["Retired"]:
                func.logging(logpath, f'Writing driver: {group}-Retired-{driver}')
                driverlist.write(rowcursor, colcursor, driver, workbook.add_format(format["driverformat"]["Retired"]))
                rowcursor += 1
        except KeyError:
            pass

        colcursor += 2
        ### END getting reserve driver ###

        func.logging(logpath, end="\n\n")
        print()

    func.logging(logpath, func.delimiter_string("END driverlist", length=60), end="\n\n\n\n\n\n")
    print(func.delimiter_string("END driverlist", length=60), end="\n\n\n\n\n\n")



def racecalendar(workbook:xlsxwriter.Workbook, db:mysql.connector.MySQLConnection):
    cursor = db.cursor()
    func.logging(logpath, func.delimiter_string("Exporting race calendar", length=60), end="\n\n")
    print(func.delimiter_string("Exporting race calendar", length=60), end="\n\n")
    racecalendar = workbook.add_worksheet("赛程安排")

    # fetching race calendar data
    racecalendar_data = get_raceCalendar_data(db)
    func.logging(logpath)
    print()

    # get driver group list
    grouplist = get_drivergrouplist(db)

    # get and write race calendar of each group
    colcursor = 0
    for group in grouplist:
        func.logging(logpath, f'Writing race calendar of {group}......', end="\n\n")
        print(f'Writing race calendar of {group}......')

        # setting header row height and column width
        racecalendar.set_row(0, 33)
        racecalendar.set_row(1, 31)
        racecalendar.set_column(colcursor+0, colcursor+0, 17)
        racecalendar.set_column(colcursor+1, colcursor+2, 15)
        racecalendar.set_column(colcursor+3, colcursor+3, 9)

        # writing header
        racecalendar.merge_range(0, colcursor, 0, colcursor+2, settings["content"]["codename"][group], workbook.add_format(format["racecalendar"]["bigheader"]))
        racecalendar.write(1, colcursor+0, "日期", workbook.add_format(format["racecalendar"]["smallheader"]))
        racecalendar.write(1, colcursor+1, "分站", workbook.add_format(format["racecalendar"]["smallheader"]))
        racecalendar.write(1, colcursor+2, "天气", workbook.add_format(format["racecalendar"]["smallheader"]))

        # writing race calendar
        rowcursor = 2
        for racedate in sorted(list(racecalendar_data[group].keys())):
            round = racecalendar_data[group][racedate]["Round"]
            gpchn = racecalendar_data[group][racedate]["GP_CHN"]
            status = racecalendar_data[group][racedate]["status"]

            # setting row height
            racecalendar.set_row(rowcursor, 31)

            # wrting content
            func.logging(logpath, f'Writing GP {racedate.strftime("%Y-%m-%d"):<10} {group}-{gpchn}......')
            racecalendar.write(rowcursor, colcursor, racedate, workbook.add_format(format["racecalendar"][status]))
            racecalendar.write(rowcursor, colcursor+1, gpchn, workbook.add_format(format["racecalendar"][status]))
            if round is not None:
                racecalendar.write(rowcursor, colcursor+2, "动态", workbook.add_format(format["racecalendar"][status]))
            else:
                racecalendar.write(rowcursor, colcursor+2, "晴朗", workbook.add_format(format["racecalendar"][status]))
            
            rowcursor += 1

        colcursor += 4
        
        func.logging(logpath, end="\n\n")
        print()

    func.logging(logpath, func.delimiter_string("END race calendar", length=60), end="\n\n\n\n\n\n")
    print(func.delimiter_string("END race calendar", length=60), end="\n\n\n\n\n\n")



def leaderboard_short(workbook:xlsxwriter.Workbook, db:mysql.connector.MySQLConnection):
    cursor = db.cursor()
    func.logging(logpath, func.delimiter_string("Exporting leaderboard (short)", length=60), end="\n\n")
    print(func.delimiter_string("Exporting leaderboard (short)", length=60), end="\n\n")

    # fetch short leaderboard data
    shortleaderboard_data = get_shortleaderboard_data(db)
    func.logging(logpath)
    print()

    # get driver group list
    grouplist = get_drivergrouplist(db)

    # preparing variables
    warning_dict = settings["content"]["warning"]
    licensepoint_dict = func.get_LPdict(settings["race"]["licensepoint"])

    for group in grouplist:
        leaderboard = workbook.add_worksheet(f'{group}积分榜')
        func.logging(logpath, f'Writing driver leaderboard (short) of {group}......', end="\n\n")
        print(f'Writing driver leaderboard (short) of {group}......')
        

        ### driver leaderboard ###
        # setting header row height and column width
        leaderboard.set_row(0, 31)
        leaderboard.set_column(0,0, 3)
        leaderboard.set_column(1,1, 20)
        leaderboard.set_column(2,4, 9)
        leaderboard.set_column(5,5, 20)
        leaderboard.set_column(6,6, 3)

        # writing header
        leaderboard.write(0,0, "Pos.", workbook.add_format(format["default"]["header_11"]))
        leaderboard.write(0,1, "Driver", workbook.add_format(format["default"]["header_11"]))
        leaderboard.write(0,3, "Points", workbook.add_format(format["default"]["header_11"]))
        leaderboard.write(0,4, "LP", workbook.add_format(format["default"]["header_11"]))


        # writing driver leaderboard data
        drivers = sorted(shortleaderboard_data[group]["driver"].items(), key=lambda x: -x[1]["totalpoints"])
        pos = 1
        for driver in drivers:
            drivername = driver[0]
            driver = shortleaderboard_data[group]["driver"][drivername]
            func.logging(logpath, f"Writing driver: {pos}-{group}-{drivername}......")
            
            # setting row height
            leaderboard.set_row(pos, 18)
            # writing column header (Pos.)
            leaderboard.write(pos, 0, pos, workbook.add_format(format["default"]["header_11"]))

            # drivername (with warning appended in front)
            # format warning string
            warning = float(driver["Warning"])
            warning_str = ""
            for wkey in sorted(warning_dict.keys(), reverse=True):
                try:
                    warning_str += int(warning // float(wkey)) * warning_dict[wkey]
                    warning -= int(warning // float(wkey)) * float(wkey)
                except ZeroDivisionError:
                    continue
            
            # writing drivername
            try:
                if settings["drivergroup"]["enable_team"][group] == True:
                    leaderboard.write(pos, 1, f'{warning_str}{drivername}',
                                                workbook.add_format(format["driverformat"][driver["teamcolor"]]))
                else:
                    leaderboard.write(pos, 1, f'{warning_str}{drivername}',
                                                workbook.add_format(format["driverformat"]["Reserve"]))
            except KeyError:
                if driver["team"] == "Reserve":
                    driver["team"] = "Reserve_leaderboard"
                leaderboard.write(pos, 1, f'{warning_str}{drivername}',
                                                workbook.add_format(format["driverformat"][driver["team"]]))
            

            # writing totalpoints
            leaderboard.write(pos, 3, driver["totalpoints"], workbook.add_format(format["default"]["header_11"]))
            
            # writing licensepoint
            leaderboard.write(pos, 4, driver["LP"],
                                        workbook.add_format(format["pointsformat"][licensepoint_dict[driver["LP"]]]))

            # writing quali/race ban (if driver has)
            if driver["RB"] > 0:
                leaderboard.write(pos, 5, f'Race to be DSQ x{driver["RB"]}',
                                            workbook.add_format(format["pointsformat"]["trigger"]))
            elif driver["QB"] > 0:
                leaderboard.write(pos, 5, f'Qualiying to be DSQ x{driver["QB"]}',
                                            workbook.add_format(format["pointsformat"]["trigger"]))

            pos += 1

        func.logging(logpath, end="\n")
        print()



        ### constructors leaderboard ###
        # (if teams enabled in the group)
        if settings["drivergroup"]["enable_team"][group] == False:
            func.logging(logpath, f'Team feature has been disabled in drivergroup {group}', end="\n\n")
            continue

        # setting column width
        leaderboard.set_column(7,7, 3)
        leaderboard.set_column(8,8, 20)
        leaderboard.set_column(9,10, 9)

        # writing header
        leaderboard.write(0, 7, "Pos.", workbook.add_format(format["default"]["header_11"]))
        leaderboard.write(0, 8, "Team", workbook.add_format(format["default"]["header_11"]))
        leaderboard.write(0, 10, "Points", workbook.add_format(format["default"]["header_11"]))


        # writing constrcutors leaderboard data
        teams = sorted(shortleaderboard_data[group]["team"].items(), key=lambda x: -x[1]["totalpoints"])
        pos = 1
        for team in teams:
            teamname = team[0]
            team = shortleaderboard_data[group]["team"][teamname]
            func.logging(logpath, f'Writing team: {pos}-{group}-{teamname}......')

            # setting row height
            leaderboard.set_row(pos, 18)
            # writing column header (Pos.)
            leaderboard.write(pos, 7, pos, workbook.add_format(format["default"]["header_11"]))

            # writing teamname
            leaderboard.write(pos, 8, teamname, workbook.add_format(format["driverformat"][team["teamcolor"]]))
            # writing totalpoints
            leaderboard.write(pos, 10, team["totalpoints"], workbook.add_format(format["default"]["header_11"]))

            pos += 1


    func.logging(logpath, func.delimiter_string("END leaderboard (short)", length=60), end="\n\n\n\n\n\n")
    print(func.delimiter_string("END leaderboard (short)", length=60), end="\n\n\n\n\n\n")



def leaderboard_driver(workbook:xlsxwriter.Workbook, db:mysql.connector.MySQLConnection):
    cursor = db.cursor()
    func.logging(logpath, func.delimiter_string("Exporting driver leaderboard", length=60), end="\n\n")
    print(func.delimiter_string("Exporting driver leaderboard", length=60), end="\n\n")

    # get driver group list
    grouplist = get_drivergrouplist(db)

    for group in grouplist:
        leaderboard = workbook.add_worksheet(f'{group}车手积分榜')
        func.logging(logpath, f'Writing driver leaderboard of {group}......', end="\n\n")
        print(f'Writing driver leaderboard of {group}......')

        # preparing variables
        racedonelist = []

        # setting header row and height and column width
        leaderboard.set_row(0, 31)
        leaderboard.set_column(0,0, 3)
        leaderboard.set_column(1,1, 20)

        # writing header
        leaderboard.write(0,0, "Pos.", workbook.add_format(format["default"]["header_11"]))
        leaderboard.write(0,1, "Driver", workbook.add_format(format["default"]["header_11"]))

            # writing flag header, and setting column width based on race calendar
        query = f'SELECT * FROM get_raceCalendar WHERE driverGroup = "{group}";'
        cursor.execute(query)
        result = cursor.fetchall()
        colcursor = 2
        for race in result:
            if race[0] == None or race[5] == "CANCELLED":
                continue
            if race[5] == "FINISHED":
                racedonelist.append(race[3])
            
            leaderboard.set_column(colcursor, colcursor, 9)
            leaderboard.insert_image(0, colcursor, settings["content"]["flags"][race[3]], {'x_scale':0.96, 'y_scale':0.98})

            colcursor += 1
        
        # continue on writing header
        leaderboard.set_column(colcursor, colcursor, 9)
        leaderboard.write(0, colcursor, "Points", workbook.add_format(format["default"]["header_11"]))


        # get full driver leaderboard
        query = f'SELECT * FROM get_leaderboard_driver \
                WHERE driverGroup = "{group}";'
        cursor.execute(query)
        func.logging(logpath, f'Fetching driverleaderboard of {group}......')
        result = cursor.fetchall()

        # get driver's pole and raceFL
        query = f'SELECT GP, driverGroup, qualiFLdriver \
                FROM qualiraceFL \
                WHERE driverGroup = "{group}";'
        cursor.execute(query)
        poleresult = cursor.fetchall()

        query = f'SELECT GP, driverGroup, raceFLdriver, raceFLvalidation \
                FROM qualiraceFL \
                WHERE driverGroup = "{group}";'
        cursor.execute(query)
        raceFLresult = cursor.fetchall()


        for i in range(0, len(result)):
            driver = list(result[i])
            func.logging(logpath, f'Writing driver: {i+1}-{driver[1]}-{driver[0]}......')

            # setting row height
            leaderboard.set_row(i+1, 18)
            # writing column header (Pos.)
            leaderboard.write(i+1, 0, i+1, workbook.add_format(format["default"]["header_11"]))
            try:
                if settings["drivergroup"]["enable_team"][group] == True:
                    leaderboard.write(i+1, 1, driver[0], workbook.add_format(format["driverformat"][driver[-1]]))
                else:
                    leaderboard.write(i+1, 1, driver[0], workbook.add_format(format["driverformat"]["Reserve"]))
            except KeyError:
                if driver[1] == "Reserve":
                    driver[1] = "Reserve_leaderboard"
                leaderboard.write(i+1, 1, driver[0], workbook.add_format(format["driverformat"][driver[1]]))

            # writing result of every race
            colcursor = 2
            for j in range(3, 3+len(racedonelist)):
                race = racedonelist[j-3]
                f = None

                if driver[j] == None:
                    f = workbook.add_format(format["pointsformat"]["dna"])
                    driver[j] = "DNA"
                elif driver[j] == 1:
                    f = workbook.add_format(format["pointsformat"]["P1"])
                elif driver[j] == 2:
                    f = workbook.add_format(format["pointsformat"]["P2"])
                elif driver[j] == 3:
                    f = workbook.add_format(format["pointsformat"]["P3"])
                elif settings["race"]["points"][str(driver[j])] > 0 and driver[j] > 0:
                    f = workbook.add_format(format["pointsformat"]["points"])
                elif settings["race"]["points"][str(driver[j])] == 0 and driver[j] > 0:
                    f = workbook.add_format(format["pointsformat"]["outpoint"])
                elif driver[j] == -1:
                    f = workbook.add_format(format["pointsformat"]["retired"])
                    driver[j] = "RET"
                elif driver[j] == -2:
                    f = workbook.add_format(format["pointsformat"]["dnf"])
                    driver[j] = "DNF"
                elif driver[j] == -3:
                    f = workbook.add_format(format["pointsformat"]["dsq"])
                    driver[j] = "DSQ"
                elif driver[j] == -4:
                    f = workbook.add_format(format["pointsformat"]["dns"])
                    driver[j] = "DNS"

                # marking pole
                for pole in poleresult:
                    if pole[0] == race and pole[2] == driver[0]:
                        f.set_bold(True)
                
                # marking raceFL
                for raceFL in raceFLresult:
                    if raceFL[0] == race and raceFL[2] == driver[0]:
                        f.set_italic(True)

                        if raceFL[3] == 0:
                            f.set_underline(True)



                leaderboard.write(i+1, colcursor, driver[j], f)
                
                colcursor += 1

            # writing totalpoints
            leaderboard.write(i+1, len(driver)-3, driver[-2], workbook.add_format(format["default"]["header_11"]))

        func.logging(logpath, end="\n\n")
        print()
    
    func.logging(logpath, func.delimiter_string("END driver leaderboard", 60), end="\n\n\n\n\n\n")
    print(func.delimiter_string("END driver leaderboard", 60), end="\n\n\n\n\n\n")



def leaderboard_constructors(workbook:xlsxwriter.Workbook, db:mysql.connector.MySQLConnection):
    cursor = db.cursor()
    func.logging(logpath, func.delimiter_string("Exporting constructors leaderboard", length=60), end="\n\n")
    print(func.delimiter_string("Exporting constructors leaderboard", length=60), end="\n\n")

    # get driver group list
    grouplist = get_drivergrouplist(db)

    for group in grouplist:
        if settings["drivergroup"]["enable_team"][group] == False:
            continue

        leaderboard = workbook.add_worksheet(f'{group}车队积分榜')
        func.logging(logpath, f'Writing constructors leaderboard of {group}......', end="\n\n")
        print(f'Writing constructors leaderboard of {group}......')

        # preparing variables
        racedonelist = []

        # setting header row and height and column width
        leaderboard.set_row(0, 31)
        leaderboard.set_column(0,0, 3)
        leaderboard.set_column(1,1, 20)

        # writing header
        leaderboard.write(0,0, "Pos.", workbook.add_format(format["default"]["header_11"]))
        leaderboard.write(0,1, "Team", workbook.add_format(format["default"]["header_11"]))

            # writing flag header, and setting column width based on race calendar
        query = f'SELECT * FROM get_raceCalendar WHERE driverGroup = "{group}";'
        cursor.execute(query)
        func.logging(logpath, f'Fetching constructorsleaderboard of {group}......')
        result = cursor.fetchall()
        colcursor = 2
        for race in result:
            if race[0] == None or race[5] == "CANCELLED":
                continue
            if race[5] == "FINISHED":
                racedonelist.append(race)
            
            leaderboard.set_column(colcursor, colcursor+1, 4)
            leaderboard.insert_image(0, colcursor, settings["content"]["flags"][race[3]], {'x_scale':0.96, 'y_scale':0.98})

            colcursor += 2
        
        # continue on writing header
        leaderboard.set_column(colcursor, colcursor, 9)
        leaderboard.write(0, colcursor, "Points", workbook.add_format(format["default"]["header_11"]))


        # get full constructors leaderboard
        query = f'SELECT * FROM get_leaderboard_constructors \
                WHERE driverGroup = "{group}";'
        cursor.execute(query)
        result = cursor.fetchall()

        for i in range(0, len(result)):
            team = list(result[i])
            func.logging(logpath, f'Writing team: {i+1}-{team[1]}-{team[0]}......')

            # setting row height
            leaderboard.set_row(i+1, 23)
            # writing column header (Pos.)
            leaderboard.write(i+1, 0, i+1, workbook.add_format(format["default"]["header_11"]))
            leaderboard.write(i+1, 1, team[0], workbook.add_format(format["teamformat"][team[-1]]))

            # writing result of every race
            colcursor = 2
            for j in range(2, 2+len(racedonelist*2)):
                if team[j] == None:
                    leaderboard.write(i+1, colcursor, "DNA", workbook.add_format(format["pointsformat"]["dna"]))
                elif team[j] == 1:
                    leaderboard.write(i+1, colcursor, team[j], workbook.add_format(format["pointsformat"]["P1"]))
                elif team[j] == 2:
                    leaderboard.write(i+1, colcursor, team[j], workbook.add_format(format["pointsformat"]["P2"]))
                elif team[j] == 3:
                    leaderboard.write(i+1, colcursor, team[j], workbook.add_format(format["pointsformat"]["P3"]))
                elif settings["race"]["points"][str(team[j])] > 0 and team[j] > 0:
                    leaderboard.write(i+1, colcursor, team[j], workbook.add_format(format["pointsformat"]["points"]))
                elif settings["race"]["points"][str(team[j])] == 0 and team[j] > 0:
                    leaderboard.write(i+1, colcursor, team[j], workbook.add_format(format["pointsformat"]["outpoint"]))
                elif team[j] == -1:
                    leaderboard.write(i+1, colcursor, "RET", workbook.add_format(format["pointsformat"]["retired"]))
                elif team[j] == -2:
                    leaderboard.write(i+1, colcursor, "DNF", workbook.add_format(format["pointsformat"]["dnf"]))
                elif team[j] == -3:
                    leaderboard.write(i+1, colcursor, "DSQ", workbook.add_format(format["pointsformat"]["dsq"]))
                elif team[j] == -4:
                    leaderboard.write(i+1, colcursor, "DNS", workbook.add_format(format["pointsformat"]["dns"]))

                colcursor += 1

            # writing totalpoints
            leaderboard.write(i+1, len(team)-2, team[-2], workbook.add_format(format["default"]["header_11"]))

        func.logging(logpath, end="\n\n")
        print()

    func.logging(logpath, func.delimiter_string("END constructors leaderboard", length=60), end="\n\n\n\n\n\n")
    print(func.delimiter_string("END constructors leaderboard", length=60), end="\n\n\n\n\n\n")



def licensepoint(workbook:xlsxwriter.Workbook, db:mysql.connector.MySQLConnection):
    cursor = db.cursor()
    func.logging(logpath, func.delimiter_string("Exporting license point", length=60), end="\n\n")
    print(func.delimiter_string("Exporting license point", length=60), end="\n\n")
    lpboard = workbook.add_worksheet(f'车手驾照分')

    # get driver group list
    grouplist = get_drivergrouplist(db)

    rowcursor = 1
    for group in grouplist:
        func.logging(logpath, f'Writing license point of {group}......', end="\n\n")
        print(f'Writing license point of {group}......')

        # preparing variables
        racedonelist = []
        licensepoint_dict = func.get_LPdict(settings["race"]["licensepoint"])

        # setting header row and height and column width
        lpboard.set_row(0, 31)
        lpboard.set_column(0,0, 3)
        lpboard.set_column(1,1, 20)

        # writing header
        lpboard.write(0,1, "Driver", workbook.add_format(format["default"]["header_11"]))

            # writing flag header, and setting column width based on race calendar
        query = f'SELECT * FROM get_raceCalendar WHERE driverGroup = "{group}";'
        cursor.execute(query)
        result = cursor.fetchall()
        colcursor = 2
        for race in result:
            if race[0] == None or race[5] == "CANCELLED":
                continue
            if race[5] == "FINISHED":
                racedonelist.append(race)
            
            lpboard.set_column(colcursor, colcursor, 9)
            lpboard.insert_image(0, colcursor, settings["content"]["flags"][race[3]], {'x_scale':0.96, 'y_scale':0.98})

            colcursor += 1
        
        # continue on writing header
        lpboard.set_column(colcursor, colcursor, 9)
        lpboard.write(0, colcursor, "Points", workbook.add_format(format["default"]["header_11"]))

        # get full license point
        query = f'SELECT * FROM get_licensepoint WHERE driverGroup = "{group}";'
        func.logging(logpath, f'Fetching license point of {group}......')
        cursor.execute(query)
        result = cursor.fetchall()

        for i in range(0, len(result)):
            driver = list(result[i])
            func.logging(logpath, f'Writing driver: {i+1}-{driver[1]}-{driver[0]}......')

            # setting row height
            lpboard.set_row(rowcursor, 18)
            lpboard.write(rowcursor, 1, driver[0], workbook.add_format(format["driverformat"][driver[1]]))
            
            colcursor = 2
            for j in range(2, len(driver)-4):
                if driver[j] != None:
                    lpboard.write(rowcursor, colcursor, driver[j], workbook.add_format(format["default"]["header_11"]))
                colcursor += 1

            if driver[-3] >= 0:
                lpboard.write(rowcursor, colcursor, driver[-3], workbook.add_format(format["pointsformat"][licensepoint_dict[driver[-3]]]))
            else:
                lpboard.write(rowcursor, colcursor, 0, workbook.add_format(format["pointsformat"][licensepoint_dict[0]]))

            rowcursor += 1
        
        func.logging(logpath, end="\n\n")
        print()

    func.logging(logpath, func.delimiter_string("END license point", length=60), end="\n\n\n\n\n\n")
    print(func.delimiter_string("END license point", length=60), end="\n\n\n\n\n\n")



def seasonstats(workbook:xlsxwriter.Workbook, db:mysql.connector.MySQLConnection):
    cursor = db.cursor()



def racedirector(workbook:xlsxwriter.Workbook, db:mysql.connector.MySQLConnection):
    cursor = db.cursor()
    func.logging(logpath, func.delimiter_string("Exporting race director", length=60), end="\n\n")
    print(func.delimiter_string("Exporting race director", length=60), end="\n\n")
    rdboard = workbook.add_worksheet(f'判罚记录')

    # set header row height
    rdboard.set_row(0, 16)
    # set column width and writing header
    colcursor = 0
    rdboard.set_column(colcursor,colcursor, 13)
    rdboard.write(0,colcursor, "案件编号", workbook.add_format(format["default"]["header_11"]))
    colcursor += 1
    rdboard.set_column(colcursor,colcursor, 14)
    rdboard.write(0,colcursor, "日期", workbook.add_format(format["default"]["header_11"]))
    colcursor += 1
    rdboard.set_column(colcursor,colcursor, 20)
    rdboard.write(0,colcursor, "车手", workbook.add_format(format["default"]["header_11"]))
    colcursor += 1
    rdboard.set_column(colcursor,colcursor, 5)
    rdboard.write(0,colcursor, "组别", workbook.add_format(format["default"]["header_11"]))
    colcursor += 1
    rdboard.set_column(colcursor,colcursor, 12)
    rdboard.write(0,colcursor, "比赛", workbook.add_format(format["default"]["header_11"]))
    colcursor += 1
    rdboard.set_column(colcursor,colcursor, 40)
    rdboard.write(0,colcursor, "处罚", workbook.add_format(format["default"]["header_11"]))
    colcursor += 1
    rdboard.set_column(colcursor,colcursor, 7)
    rdboard.write(0,colcursor, "驾照分", workbook.add_format(format["default"]["header_11"]))
    colcursor += 1
    rdboard.set_column(colcursor,colcursor, 5)
    rdboard.write(0,colcursor, "警告", workbook.add_format(format["default"]["header_11"]))
    colcursor += 1
    rdboard.set_column(colcursor,colcursor, 7)
    rdboard.write(0,colcursor, "禁排位", workbook.add_format(format["default"]["header_11"]))
    colcursor += 1
    rdboard.set_column(colcursor,colcursor, 5)
    rdboard.write(0,colcursor, "禁赛", workbook.add_format(format["default"]["header_11"]))
    colcursor += 1
    rdboard.set_column(colcursor,colcursor, 70)
    rdboard.write(0,colcursor, "大致描述", workbook.add_format(format["default"]["header_11"]))
    colcursor += 1


    # fetch race director data
    racedirector_data = get_raceDirector(db)
    func.logging(logpath)
    print()

    print(f'Writing race director data......\n')
    rowcursor = 1
    for i in range(0, len(racedirector_data)):
        rdboard.set_row(rowcursor, 16)
        record = racedirector_data[i]

        func.logging(logpath, f'Writing {record[0]}......')
        rdboard.write(rowcursor, 0, record[0], workbook.add_format(format["default"]["default_11"]))
        rdboard.write(rowcursor, 1, record[1], workbook.add_format(format["default"]["default_11_date"]))
        rdboard.write(rowcursor, 2, record[2], workbook.add_format(format["default"]["default_11"]))
        rdboard.write(rowcursor, 3, record[3], workbook.add_format(format["default"]["default_11"]))
        rdboard.write(rowcursor, 4, record[4], workbook.add_format(format["default"]["default_11"]))
        rdboard.write(rowcursor, 5, record[5], workbook.add_format(format["default"]["default_11"]))
        rdboard.write(rowcursor, 6, record[6], workbook.add_format(format["default"]["default_11"]))
        rdboard.write(rowcursor, 7, record[7], workbook.add_format(format["default"]["default_11"]))
        rdboard.write(rowcursor, 8, record[8], workbook.add_format(format["default"]["default_11"]))
        rdboard.write(rowcursor, 9, record[9], workbook.add_format(format["default"]["default_11"]))
        rdboard.write(rowcursor, 10, record[10], workbook.add_format(format["default"]["default_11"]))

        rowcursor += 1
    
    func.logging(logpath)
    func.logging(logpath, func.delimiter_string("END race director", length=60), end="\n\n\n\n\n\n")
    print()
    print(func.delimiter_string("END race director", length=60), end="\n\n\n\n\n\n")



# this funcion is disabled for current context
def lanuserlist(db:mysql.connector.MySQLConnection):
    try:
        cursor = db.cursor()

        # seperate LAN userlist table
        func.logging(logpath, func.delimiter_string("User downloading LAN userlist Table", 60), end="\n\n")

        filename = f'{settings["default"]["leaguename"]} LAN账号列表.xlsx'
        func.logging(logpath, f'Exporting LAN userlist table to file "{filename}"......', end="\n\n")
        print(f'Exporting LAN userlist table to file "{filename}"......\n')
        workbook = xlsxwriter.Workbook(filename)

        # lanuserlist(lanworkbook, db)

        lanlist = workbook.add_worksheet("LAN列表")
        func.logging(logpath, func.delimiter_string("Exporting LAN userlist", 60), end="\n\n")
        print(func.delimiter_string("Exporting LAN userlist", 60), end="\n\n")

        # setting header row height and column width
        lanlist.set_column(0,2, 22)

        # writing header
        lanlist.write(0,0, "游戏id", workbook.add_format(format["default"]["header_12"]))
        lanlist.write(0,1, "LAN用户名", workbook.add_format(format["default"]["header_12"]))
        lanlist.write(0,2, "密码", workbook.add_format(format["default"]["header_12"]))

        # fetch LAN account list
        query = "SELECT * FROM afr_db.LANusername ORDER BY username ASC;"
        func.logging(logpath, "Fetching LAN userlist......", end="\n\n")
        print("Fetching LAN userlist......\n")
        cursor.execute(query)
        result = cursor.fetchall()

        # writing LAN userlist
        print("Writing LAN userlist......")
        rowcursor = 1; colcursor = 0
        for account in result:
            status = account[3]
            func.logging(logpath, f'Writing LAN user {account[1]}-{status}......')
            for i in range(0,3):
                lanlist.write(rowcursor, colcursor+i, account[i], workbook.add_format(format["LANusername"][status]))
            rowcursor += 1

        func.logging(logpath)
        func.logging(logpath, func.delimiter_string("END LAN userlist", 60), end="\n\n\n\n\n\n")
        print()
        print(func.delimiter_string("END LAN userlist", 60), end="\n\n")


        workbook.close()
        func.logging(logpath, f'LAN userlist table save to file "{filename}" complete', end="\n\n\n\n\n\n")
        print(f'LAN userlist table save to file "{filename}" complete')

    
    except Exception as e:
        func.logging(logpath, traceback.format_exc())
        func.logging(logpath, "Error: " + str(e), end="\n\n")
        print("错误提示：" + str(e))
        print("LAN账号列表下载失败，推荐咨询管理员寻求解决......")



def registlist(db:mysql.connector.MySQLConnection):
    try:
        cursor = db.cursor()

        func.logging(logpath, func.delimiter_string("User downloading registration of today's race", 60), end="\n\n")

        func.logging(logpath, "Searching for race event information......", end="\n\n")
        print("正在查找比赛信息......", end="\n\n")

        today = datetime.today()
        # today = datetime(2023, 4, 22, 19, 00, 00)     # --- this is for testing --- #
        today_date = today.strftime("%Y-%m-%d")
        today_time = today.strftime("%H:%M")

        
        # looking for the race event TODAY
        query = f'SELECT * FROM get_raceCalendar \
                WHERE raceDate = "{today_date}";'
        cursor.execute(query)
        race = cursor.fetchall()
        if len(race) == 0:
            func.logging(logpath, "Unable to find race event of today", end="\n\n\n\n\n\n")
            print("没有找到在今日进行的比赛，请在比赛当天再试")
            return -1
        
        func.logging(logpath, f'Today\'s race: R{race[0][0]:02}-{race[0][4]}-{race[0][3]}', end="\n\n")
        print(f'今日比赛：R{race[0][0]:02}-{race[0][4]}-{race[0][2]}', end="\n\n")
        

        # check registration deadline
        query = f'SELECT * FROM afr_db.League_Info \
                WHERE field = "regist_DL_time";'
        cursor.execute(query)
        result = cursor.fetchall()
        regDLtime = result[0][1]

        if regDLtime > today_time:
            func.logging(logpath, "WARNING: Currently still ahead of regist deadline time", end="\n\n")
            print("注意：当前时间未到达报名截止时间......", end="\n\n")
        

        test = input("请按Enter以下载今日比赛报名表，输入q回到主菜单 ")
        if test == 'q' or test == "Q":
            func.logging(logpath, "", end="\n\n\n\n")
            return 0
        print()

        filename = f'{settings["default"]["leaguename"]} R{race[0][0]}-{race[0][4]}-{race[0][2]} 报名表.xlsx'
        func.logging(logpath, f'Exporting registration to file {filename}', end="\n\n")
        print(f'Exporting registration to file {filename}', end="\n\n")
        


        # writing registration to file
        workbook = xlsxwriter.Workbook(filename)
        reglist = workbook.add_worksheet(f'R{race[0][0]:02}-{race[0][4]}-{race[0][3]}')
        func.logging(logpath, func.delimiter_string("Exporting registration data", 60), end="\n\n")
        print(func.delimiter_string("Exporting registration data", 60), end="\n\n")

        # setting row height and column width
        reglist.set_column(0,1, 14)
        for i in range(0, 50):
            reglist.set_row(i, 15)
        
        # writing header
        reglist.merge_range(0,0, 0,1, f'{race[0][2]}', workbook.add_format(format["default"]["header_11"]))
        reglist.write(0,2, "server", workbook.add_format(format["default"]["header_11"]))


        
        # writing team column header
        func.logging(logpath, "Writing team column header")
        print("Writing team column header")

        rowcursor = 1
        colcursor = 0
        teamlist = settings["content"]["teamorder"]

        driverlist_data = get_driverlist_data(db)
        for team in teamlist:
            reglist.write(rowcursor, colcursor, settings["content"]["codename"][team],
                                                workbook.add_format(format["driverformat"][team]))
            try:
                reglist.write(rowcursor+1, colcursor, driverlist_data[race[0][4]][team]["teamname"],
                                                workbook.add_format(format["driverformat"][team]))
            except KeyError:
                reglist.write(rowcursor+1, colcursor, None,
                                                workbook.add_format(format["driverformat"][team]))
            rowcursor += 2

        reglist.write(rowcursor, colcursor, "Race Director", workbook.add_format(format["default"]["default_11"]))
        reglist.write(rowcursor+1, colcursor, "OB", workbook.add_format(format["default"]["default_11"]))
        reglist.write(rowcursor+2, colcursor, "OB", workbook.add_format(format["default"]["default_11"]))
        rowcursor += 4
        


        # writing registration data
        func.logging(logpath, "Writing registration data......")
        print("Writing registration data......")


        query = f'SELECT * FROM get_registration \
                WHERE raceGroup = "{race[0][4]}" AND GP = "{race[0][3]}";'
        cursor.execute(query)
        result = cursor.fetchall()

        i = 1
        for reg in result:
            func.logging(logpath, f'Writing regist: {i}-{reg[0]}-{reg[4]}......')
            i += 1

            try:
                reglist.write(rowcursor, colcursor, reg[2], workbook.add_format(format["driverformat"][reg[3]]))
            except KeyError:
                reglist.write(rowcursor, colcursor, reg[2], workbook.add_format(format["default"]["default_11"]))
            
            if reg[6] != 0:
                reglist.write(rowcursor, colcursor+1, reg[0], workbook.add_format(format["registformat"]["rb"]))
            elif reg[5] != 0:
                reglist.write(rowcursor, colcursor+1, reg[0], workbook.add_format(format["registformat"]["qb"]))
            elif race[0][4] != reg[1]:
                reglist.write(rowcursor, colcursor, reg[1], workbook.add_format(format["default"]["default_11"]))
                reglist.write(rowcursor, colcursor+1, reg[0], workbook.add_format(format["registformat"]["crossgroup"]))
            elif reg[2] == "Reserve":
                reglist.write(rowcursor, colcursor+1, reg[0], workbook.add_format(format["registformat"]["reserved"]))
            else:
                reglist.write(rowcursor, colcursor+1, reg[0], workbook.add_format(format["default"]["default_11"]))
            
            rowcursor += 1

        
        func.logging(logpath)
        func.logging(logpath, func.delimiter_string("END registration data", 60), end="\n\n\n\n\n\n")
        print()
        print(func.delimiter_string("END registration data", 60), end="\n\n")

        workbook.close()
        func.logging(logpath, f'Registration save to file "{filename}" complete', end="\n\n\n\n\n\n")
        print(f'Registration save to file "{filename}" complete')
    


    except Exception as e:
        func.logging(logpath, traceback.format_exc())
        func.logging(logpath, "Error: " + str(e), end="\n\n")
        print("错误提示：" + str(e))
        print("今日比赛报名表下载失败，推荐咨询管理员寻求解决......")


    

    


def main(db:mysql.connector.MySQLConnection):
    try:
        # connect database
        cursor = db.cursor()

        # logging
        func.logging(logpath, func.delimiter_string("User downloading Classification Table", 60), end="\n\n")

        # get latest race date
        today = datetime.today().strftime('%Y-%m-%d')
        query = f'SELECT GP_CHN, raceDate FROM raceCalendar \
                WHERE raceStatus = "ON GOING" OR raceDate = {today} \
                ORDER BY raceDate ASC;'
        cursor.execute(query)
        result = cursor.fetchall()

        if len(result) == 0:
            query = f'SELECT GP_CHN, raceDate FROM raceCalendar \
                WHERE raceStatus = "FINISHED" AND raceDate <= "{today}" \
                ORDER BY raceDate DESC'
            cursor.execute(query)
            result = cursor.fetchall()

        try:
            result = list(result[0])
            race_name = result[0]
            date_name = result[1].strftime('%m.%d')
        except Exception:
            race_name = "Pre-Season"
            date_name = datetime.today().strftime('%m.%d')

        if date_name[3] == '0':
            date_name = date_name[0:3] + date_name[-1]
        if date_name[0] == '0':
            date_name = date_name[1:]

        
        # get season name/number
        leaguename = settings["default"]["leaguename"]
        seasonname = settings["default"]["seasonname"]

        # create the excel file
        print()
        filename = f'{leaguename} {seasonname}【{date_name}】{race_name}.xlsx'
        func.logging(logpath, f'Exporting Classification table to file "{filename}"......', end="\n\n")
        print(f'Exporting Classification table to file "{filename}"......\n')
        workbook = xlsxwriter.Workbook(filename)



        # writing table
        driverlist(workbook, db)                    # passed
        racecalendar(workbook, db)                  # passed
        leaderboard_short(workbook, db)             # passed
        leaderboard_driver(workbook, db)            # new version under development (pause)
        leaderboard_constructors(workbook, db)      # new version under development (pause)
        licensepoint(workbook, db)                  # new version under development (pause)
        # seasonstats(workbook, db)                 # not develop for now
        racedirector(workbook, db)                  # passed

        workbook.close()
        func.logging(logpath, f'Classification table save to file "{filename}" complete', end="\n\n\n\n\n\n")
        print(f'Classification table save to file "{filename}" complete')


    except Exception as e:
        func.logging(logpath, traceback.format_exc())
        func.logging(logpath, "Error: " + str(e), end="\n\n")
        print("错误提示：" + str(e))
        print("积分表下载失败，推荐咨询管理员寻求解决......")


"""
if __name__ == "__main__":
    main(dbconnect.connect_with_conf("server.json", "db"))
"""