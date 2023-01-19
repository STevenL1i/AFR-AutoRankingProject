import json, traceback, xlsxwriter
from datetime import datetime

import mysql.connector
import connectserver
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



def driverlist(workbook:xlsxwriter.Workbook, db:mysql.connector.MySQLConnection):
    cursor = db.cursor()

    func.logging(logpath, func.delimiter_string("Exporting driverlist", length=60), end="\n\n")
    print(func.delimiter_string("Exporting driverlist", length=60), end="\n\n")
    driverlist = workbook.add_worksheet("车手名单")
    
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
                # get driverlist of this team
                f = open("bin/get_driverlist_group-team.sql", "r")
                query = f.read().replace("GROUP", group).replace("THETEAM",team)
                f.close()
                func.logging(logpath, f'Fetching driverlist data of {group}-{team}......')
                cursor.execute(query)
                result = cursor.fetchall()
                
                func.logging(logpath, f'Writing team title: {group}-{team}......')
                driverlist.write(rowcursor, colcursor, team, workbook.add_format(format["driverformat"][team]))
                driverlist.write(rowcursor+1, colcursor, settings["content"]["codename"][team], workbook.add_format(format["driverformat"][team]))
                try:
                    driverlist.write(rowcursor+2, colcursor, result[0][2], workbook.add_format(format["driverformat"][team]))
                except IndexError:
                    driverlist.write(rowcursor+2, colcursor, None, workbook.add_format(format["driverformat"][team]))
                
                for i in range(0, 3):
                    # setting row height
                    driverlist.set_row(rowcursor, 16)
                    try:
                        func.logging(logpath, f'Writing driver: {group}-{result[i][2]}-{result[i][0]}......')
                        driverlist.write(rowcursor, colcursor+1, result[i][0], workbook.add_format(format["driverformat"][team]))
                    except IndexError:
                        driverlist.write(rowcursor, colcursor+1, None, workbook.add_format(format["driverformat"][team]))
                    rowcursor += 1
                
                for i in range(3, len(result)):
                    # setting row height
                    driverlist.set_row(rowcursor, 16)
                    func.logging(logpath, f'Writing driver: {group}-{result[i][2]}-{result[i][0]}......')
                    driverlist.write(rowcursor, colcursor, None, workbook.add_format(format["driverformat"][team]))
                    driverlist.write(rowcursor, colcursor+1, result[i][0], workbook.add_format(format["driverformat"][team]))
                    rowcursor += 1

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


        # get reserve driverlist
        f = open("bin/get_driverlist_group-reserve.sql", "r")
        query = f.read().replace("GROUP", group)
        f.close()
        cursor.execute(query)
        result = cursor.fetchall()

        rowcursor = 1
        for driver in result:
            func.logging(logpath, f'Writing driver: {group}-{driver[2]}-{driver[0]}......')
            driverlist.write(rowcursor, colcursor, driver[0], workbook.add_format(format["driverformat"][driver[2]]))
            rowcursor += 1
        
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

        # get the race calendar of this group
        f = open("bin/get_racecalendar_group.sql", "r")
        query = f.read().replace("GROUP", group)
        f.close()
        cursor.execute(query)
        result = cursor.fetchall()

        # write the race calendar
        rowcursor = 2
        for race in result:
            func.logging(logpath, f'Writing GP {race[1].strftime("%Y-%m-%d"):<10} {group}-{race[2]}......')

            # setting row height
            racecalendar.set_row(rowcursor, 31)

            # writing content
            racecalendar.write(rowcursor, colcursor+0, race[1], workbook.add_format(format["racecalendar"][race[5]]))
            racecalendar.write(rowcursor, colcursor+1, race[2], workbook.add_format(format["racecalendar"][race[5]]))
            if race[0] != "" and race[0] != None:
                racecalendar.write(rowcursor, colcursor+2, "动态", workbook.add_format(format["racecalendar"][race[5]]))
            else:
                racecalendar.write(rowcursor, colcursor+2, "晴朗", workbook.add_format(format["racecalendar"][race[5]]))
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

    # get driver group list
    grouplist = get_drivergrouplist(db)

    # preparing variables
    warning_dict = settings["content"]["warning"]
    warning_key = list(warning_dict.keys())
    warning_key.sort(reverse=True)

    licensepoint_dict = func.get_LPdict(settings["race"]["licensepoint"])

    for group in grouplist:
        leaderboard = workbook.add_worksheet(f'{group}积分榜')
        func.logging(logpath, f'Writing driver leaderboard (short) of {group}......', end="\n\n")
        print(f'Writing driver leaderboard (short) of {group}......')
        
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

        # get driverleaderboard (+ licensepoint)
        f = open("bin/get_leaderboard_short_group.sql", "r")
        query = f.read().replace("GROUP", group)
        f.close()
        func.logging(logpath, f'Fetching driverleaderboard of {group}......')
        cursor.execute(query)
        result = cursor.fetchall()

        for i in range(0, len(result)):
            driver = list(result[i])
            func.logging(logpath, f'Writing driver: {i+1}-{driver[1]}-{driver[0]}......')

            # setting row height
            leaderboard.set_row(i+1, 18)
            # writing column header (Pos.)
            leaderboard.write(i+1, 0, i+1, workbook.add_format(format["default"]["header_11"]))

            # writing driverleaderboard data
                # drivername ( + warning appened to front)
                    # format warning string
            warning = float(driver[6])
            warning_string = ""
            for wkey in warning_key:
                try:
                    warning_string += int(warning // float(wkey)) * warning_dict[wkey]
                    warning -= int(warning // float(wkey)) * float(wkey)
                except ZeroDivisionError:
                    continue
            
                    # write drivername
            try:
                if settings["drivergroup"]["enable_team"][group] == True:
                    leaderboard.write(i+1, 1, f'{warning_string}{driver[0]}', workbook.add_format(format["driverformat"][driver[2]]))
                else:
                    leaderboard.write(i+1, 1, f'{warning_string}{driver[0]}', workbook.add_format(format["driverformat"]["Reserve"]))
            except KeyError:
                if driver[1] == "Reserve":
                    driver[1] = "Reserve_leaderboard"
                leaderboard.write(i+1, 1, f'{warning_string}{driver[0]}', workbook.add_format(format["driverformat"][driver[1]]))
                # write totalpoints
            leaderboard.write(i+1, 3, driver[4], workbook.add_format(format["default"]["header_11"]))
                # write licensepoint
            leaderboard.write(i+1, 4, driver[5], workbook.add_format(format["pointsformat"][licensepoint_dict[driver[5]]]))

                # write quali/race ban (if driver has)
            if driver[8] > 0:
                leaderboard.write(i+1, 5, f'Race to be DSQ x{driver[8]}', workbook.add_format(format["pointsformat"]["trigger"]))
            elif driver[7] > 0:
                leaderboard.write(i+1, 5, f'Qualiying to be DSQ x{driver[7]}', workbook.add_format(format["pointsformat"]["trigger"]))

        func.logging(logpath, end="\n")
        print()

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

        # get constructorleaderboard
        f = open("bin/get_leaderboard_constructors_group.sql", "r")
        query = f.read().replace("GROUP", group)
        f.close()
        func.logging(logpath, f'Fetching constructorsleaderboard of {group}......')
        cursor.execute(query)
        result = cursor.fetchall()

        for i in range(0, len(result)):
            team = result[i]
            func.logging(logpath, f'Writing team: {i+1}-{team[1]}-{team[0]}......')

            # setting row height
            leaderboard.set_row(i+1, 18)
            # writing column header (Pos.)
            leaderboard.write(i+1, 7, i+1, workbook.add_format(format["default"]["header_11"]))

            leaderboard.write(i+1, 8, team[0], workbook.add_format(format["driverformat"][team[-1]]))
            leaderboard.write(i+1, 10, team[-2], workbook.add_format(format["default"]["header_11"]))

        func.logging(logpath, end="\n\n")
    
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
        f = open("bin/get_racecalendar_group.sql", "r")
        query = f.read().replace("GROUP", group)
        f.close()
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
        f = open("bin/get_leaderboard_driver_group.sql", "r")
        query = f.read().replace("GROUP", group)
        f.close()
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
        f = open("bin/get_racecalendar_group.sql", "r")
        query = f.read().replace("GROUP", group)
        f.close()
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
        f = open("bin/get_leaderboard_constructors_group.sql", "r")
        query = f.read().replace("GROUP", group)
        f.close()
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
        f = open("bin/get_racecalendar_group.sql", "r")
        query = f.read().replace("GROUP", group)
        f.close()
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
        f = open("bin/get_licensepoint_group.sql", "r")
        query = f.read().replace("GROUP", group)
        f.close()
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

            lpboard.write(rowcursor, colcursor, driver[-3], workbook.add_format(format["pointsformat"][licensepoint_dict[driver[-3]]]))

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


    # get race director record
    f = open("bin/get_racedirector_all.sql", "r")
    query = f.read()
    f.close()
    func.logging(logpath, f'Fetching race director data......\n')
    print(f'Fetching race director data......\n')
    cursor.execute(query)
    result = cursor.fetchall()

    print(f'Writing race director data......\n')
    rowcursor = 1
    for i in range(0, len(result)):
        rdboard.set_row(rowcursor, 16)
        record = result[i]

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
        query = "SELECT * FROM afr_elo.LANusername ORDER BY username ASC;"
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
        leaderboard_driver(workbook, db)            # passed, pole & fl unmarked
        leaderboard_constructors(workbook, db)      # passed
        licensepoint(workbook, db)                  # passed
        # seasonstats(workbook, db)                 # not develop for now   
        racedirector(workbook, db)                  # passed

        workbook.close()
        func.logging(logpath, f'Classification table save to file "{filename}" complete', end="\n\n\n\n\n\n")
        print(f'Classification table save to file "{filename}" complete\n\n')


    except Exception as e:
        func.logging(logpath, traceback.format_exc())
        func.logging(logpath, "Error: " + str(e), end="\n\n")
        print("错误提示：" + str(e))
        print("积分表下载失败，推荐咨询管理员寻求解决......")


"""
if __name__ == "__main__":
    main(connectserver.connectserver("server.json", "db"))
"""
