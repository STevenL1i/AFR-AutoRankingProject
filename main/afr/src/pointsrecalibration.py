from functools import update_wrapper
import json, traceback

import mysql.connector
import connectserver
import deffunc as func

# loading all the necessary json settings
# settings
settingsf = open("settings/settings.json", "r", encoding='utf-8')
settings:dict = json.load(settingsf)
settingsf.close()
# log
logpath = settings["default"]["log"]



def raceflvalidator(resultlist:list):
    """
    parameter resultlist came from following query :
    query = f'SELECT driverName, team, driverGroup, GP, \
            startPosition, finishPosition, fastestLap, driverStatus \
            WHERE GP = "{race}" and driverGroup = "{drivergroup}" \
            ORDER BY finishPosition ASC;'
    

    query = f'SELECT driverGroup, GP, finishPosition, driverName, team, \
                     startPosition, fastestLap, gap, driverStatus \
            FROM raceResult \
            WHERE driverGroup = "GROUP" AND GP = "RACE" \
            ORDER BY finishPosition ASC;'
    """

    countdriver = len(resultlist)
    fl_list = resultlist[:int(len(resultlist)/4*3 + 0.8)]
    
    fl = "9:59.999"
    fldriver = ''
    flteam = ''
    validation = 0
    gp = ''
    group = ''

    for driver in fl_list:
        group = driver[0]
        gp = driver[1]
        finishposition = driver[2]
        status = driver[8]
        driverfl = driver[6]
        if driverfl == None:
            driverfl = "9:59.999"

        if driverfl < fl: # driver[6] = thefl
            fl = driver[6]
            fldriver = driver[3]
            flteam = driver[4]
            
            if finishposition < countdriver/2 + 0.5 and status == "FINISHED":
                validation = 1
            else:
                validation = 0
    
    return fldriver, flteam, validation, gp, group



def resettable(db:mysql.connector.MySQLConnection):
    cursor = db.cursor()
    func.logging(logpath, func.delimiter_string(f'Resetting points data', 60), end="\n\n")
    print(func.delimiter_string(f'Resetting points data', 60), end="\n\n")

    # get all the race list (raceCalendar)
    query = "SELECT DISTINCT(Round), GP_CHN, GP_ENG FROM raceCalendar WHERE Round is not null;"
    cursor.execute(query)
    result = cursor.fetchall()

    # reset driverleaderboard
    query = f'UPDATE driverLeaderBoard SET '
    for race in result:
        gpkey = func.get_key(settings["content"]["gp"], race[2])
        query += f'{gpkey} = null, '
    query += "totalPoints = 0"
    func.logging(logpath, f'Resetting driver leaderboard......')
    print(f'Resetting driver leaderboard......')
    cursor.execute(query)
    db.commit()

    # reset constructorsLeaderBorad
    query = f'UPDATE constructorsLeaderBoard SET '
    for race in result:
        race = list(race)
        gpkey = func.get_key(settings["content"]["gp"], race[2])
        query += f'{gpkey}_1 = null, {gpkey}_2 = null, '
    query += "totalPoints = 0;"
    func.logging(logpath, f'Resetting constructors leaderboard......')
    print(f'Resetting constructors leaderboard......')
    cursor.execute(query)
    db.commit()

    # reset licensePoint
    query = f'UPDATE licensePoint SET '
    for race in result:
        race = list(race)
        gpkey = func.get_key(settings["content"]["gp"], race[2])
        query += f'{gpkey} = null, '
    query += "warning = 0.0, totalLicensePoint = 12, qualiBan = 0, raceBan = 0;"
    func.logging(logpath, f'Resetting licensePoint......')
    print(f'Resetting licensePoint......')
    cursor.execute(query)
    db.commit()

    # reset qualirace FL
    query = "DELETE FROM qualiraceFL;"
    func.logging(logpath, f'Resetting qualiraceFL......')
    print(f'Resetting qualiraceFL......')
    cursor.execute(query)
    db.commit()

    func.logging(logpath)
    func.logging(logpath, func.delimiter_string(f'END Reset points data', 60), end="\n\n\n\n\n\n")
    print()
    print(func.delimiter_string(f'END Reset points data', 60), end="\n\n\n\n\n\n")



def update_leaderboard(db:mysql.connector.MySQLConnection, race):
    cursor = db.cursor()
    group = race[3]; gp = race[2]
    """
    race = 'SELECT Round, GP_CHN, GP_ENG, driverGroup, raceStatus \
            FROM raceCalendar \
            WHERE driverGroup = "GROUP" AND raceStatus = "STATUS" AND Round is not null \
            ORDER BY Round ASC;'
    """

    func.logging(logpath, func.delimiter_string(f'Updating {group}-{gp}', 50), end="\n\n")
    print(func.delimiter_string(f'Updating {group}-{gp}', 50), end="\n\n")
    gpkey = func.get_key(settings["content"]["gp"], gp)

    # get the race result of the race
    f = open("bin/get_result_race_gp_group.sql", "r")
    query = f.read().replace("GROUP", group).replace("RACE", gp)
    f.close()
    func.logging(logpath, f'FETCH: race result data {group}-{gp}......')
    print(f'Fetching race result data {group}-{gp}......\n')
    cursor.execute(query)
    result = cursor.fetchall()
    func.logging(logpath, f'Total: {len(result)} drivers', end="\n\n")
    
    print(f'Updating leaderboard for {group}-{gp}......\n')
    for driver in result:
        drivername = driver[3]; team = driver[4]; status = driver[8]
        if status == "FINISHED":
            finishpos = driver[2]
        elif status == "RETIRED":
            finishpos = -1
        elif status == "DNF":
            finishpos = -2
        elif status == "DSQ":
            finishpos = -3
        elif status == "DNS":
            finishpos = -4
        
        # test whether need to add new driverleaderboard record for cross-group driver
        try:
            query = f'INSERT INTO driverLeaderBoard \
                    (driverName, team, driverGroup, totalPoints) \
                    VALUES ("{drivername}", (SELECT driverGroup FROM driverList WHERE driverName = "{drivername}"), "{group}", 0);'
            cursor.execute(query)
            db.commit()
        except mysql.connector.errors.IntegrityError as e:
            # Duplicate entry '188066-A1' for key 'driverLeaderBoard.PRIMARY'
            if str(e).find("Duplicate entry") != -1 and str(e).find("driverLeaderBoard.PRIMARY") != -1:
                pass
            else:
                raise mysql.connector.errors.IntegrityError(e)


        # 1. update/mark driverleaderboard
        query = f'UPDATE driverLeaderBoard \
                SET {gpkey} = {finishpos} \
                WHERE driverName = "{drivername}" AND driverGroup = "{driver[0]}";'
        func.logging(logpath, f'UPDATE: driverleaderboard {group}-{gpkey}-{drivername}......')
        cursor.execute(query)
        db.commit()


        # 2. update/mark constructorleaderboard
        query = f'SELECT {gpkey}_1 FROM constructorsLeaderBoard \
                WHERE team = "{team}" and driverGroup = "{group}";'
        cursor.execute(query)
        testkey = cursor.fetchall()
        
        try:
            if testkey[0][0] == None:
                gpk = f'{gpkey}_1'
            else:
                gpk = f'{gpkey}_2'
        
            query = f'UPDATE constructorsLeaderBoard \
                    SET {gpk} = {finishpos} \
                    WHERE driverGroup = "{group}" and team = "{team}";'
            func.logging(logpath, f'UPDATE: constructorleaderboard {group}-{gpkey}-{drivername}......')
            cursor.execute(query)
            db.commit()
        
        except IndexError:
            pass


        # 3. update/mark licensepoint
        query = f'UPDATE licensePoint \
                SET {gpkey} = 0 \
                WHERE driverName = "{drivername}";'
        func.logging(logpath, f'UPDATE: licensepoint {group}-{gpkey}-{drivername}......')
        cursor.execute(query)
        db.commit()

        func.logging(logpath)

    func.logging(logpath)



def update_qualiracefl(db:mysql.connector.MySQLConnection, race):
    cursor = db.cursor()
    group = race[3]; gp = race[2]

    # get the race result of the race
    f = open("bin/get_result_race_gp_group.sql", "r")
    query = f.read().replace("GROUP", group).replace("RACE", gp)
    f.close()
    # print(f'Fetching race result data {race[3]}-{race[2]}......')
    cursor.execute(query)
    result = cursor.fetchall()

    try:
        query = "INSERT INTO qualiraceFL (GP, driverGroup) \
                VALUES (%s, %s);"
        val = (gp, group)
        cursor.execute(query, val)
        db.commit()
    except mysql.connector.errors.IntegrityError as e:
        # Duplicate entry 'Bahrain-A1' for key 'qualiraceFL.PRIMARY'
        if str(e).find("Duplicate entry") != -1 and str(e).find("qualiraceFL.PRIMARY") != -1:
            pass
        else:
            raise mysql.connector.errors.IntegrityError(e)


    # 2. update pole (qualiraceFL)
    for driver in result:
        if driver[5] != 1:
            continue
        
        group = driver[0]; gp = driver[1]; drivername = driver[3]; team = driver[4]
        query = f'UPDATE qualiraceFL \
                SET qualiFLdriver = "{drivername}", \
                    qualiFLteam = "{team}" \
                WHERE driverGroup = "{group}" AND GP = "{gp}";'
        func.logging(logpath, f'UPDATE pole position {group}-{gp}-{drivername}......')
        cursor.execute(query)
    db.commit()


    # 3. update race FL (qualiraceFL)
    fldriver, flteam, flvalidation, gp, group = raceflvalidator(result)
    query = f'UPDATE qualiraceFL \
            SET raceFLdriver = "{fldriver}", \
                raceFLteam = "{flteam}", \
                raceFLvalidation = {flvalidation} \
            WHERE driverGroup = "{group}" AND GP = "{gp}";'
    func.logging(logpath, f'UPDATE: race fastestlap {group}-{gp}-{fldriver}-{flvalidation}......', end="\n\n")
    cursor.execute(query)
    db.commit()

    func.logging(logpath)






def calculate_driver(db:mysql.connector.MySQLConnection, group:str):
    cursor = db.cursor()
    func.logging(logpath, func.delimiter_string(f'{group} driver points', 50), end="\n\n")

    # get full driverleaderboard
    f = open("bin/get_leaderboard_driver_group.sql", "r")
    query = f.read().replace("GROUP", group)
    f.close()
    func.logging(logpath, f'FETCH: driver leaderboard of {group}......', end="\n\n")
    print(f'Fetching driver leaderboard of {group}......\n')
    cursor.execute(query)
    result = cursor.fetchall()
    
    print(f'Calculating driver points {group}......')
    for driver in result:
        drivername = driver[0]
        totalpoints = 0
        for i in range(3, len(driver)):
            try:
                totalpoints += settings["race"]["points"][str(driver[i])]
            except KeyError:
                pass
        
        query = f'UPDATE driverLeaderBoard \
                SET totalPoints = {totalpoints} \
                WHERE driverName = "{drivername}" AND driverGroup = "{group}";'
        func.logging(logpath, f'UPDATE: driverleaderboard {group}-{drivername}-{totalpoints}......')
        cursor.execute(query)
    db.commit()



def calculate_constructors(db:mysql.connector.MySQLConnection, group:str):
    cursor = db.cursor()
    func.logging(logpath, func.delimiter_string(f'{group} constructors points', 50), end="\n\n")

    # get full constructorsleaderboard
    f = open("bin/get_leaderboard_constructors_group.sql", "r")
    query = f.read().replace("GROUP", group)
    f.close()
    func.logging(logpath, f'FETCH: constructors leaderboard of {group}......', end="\n\n")
    print(f'Fetching constructors leaderboard of {group}......', end="\n\n")
    cursor.execute(query)
    result = cursor.fetchall()

    print(f'Calculating constructors points {group}......')
    for team in result:
        teamname = team[0]
        totalpoints = 0
        for i in range(2, len(team)):
            try:
                totalpoints += settings["race"]["points"][str(team[i])]
            except KeyError:
                pass
        
        query = f'UPDATE constructorsLeaderBoard \
                SET totalPoints = {totalpoints} \
                WHERE team = "{teamname}" AND driverGroup = "{group}";'
        func.logging(logpath, f'UPDATE: constructorsleaderboard {group}-{teamname}-{totalpoints}......')
        cursor.execute(query)
    db.commit()



def calculate_licensepoint(db:mysql.connector.MySQLConnection, group:str):
    cursor = db.cursor()
    func.logging(logpath, func.delimiter_string(f'{group} license points', 50), end="\n\n")

    # get race director record
    f = open("bin/get_racedirector_gp_group.sql", "r")
    query = f.read().replace("GROUP", group).replace(" AND GP = \"RACE\"", "")
    f.close()
    func.logging(logpath, f'FETCH: race director data {group}......', end="\n\n")
    print(f'Fetching race director data {group}......\n')
    cursor.execute(query)
    result = cursor.fetchall()

    print(f'Calculating license point {group}......')
    for record in result:
        gpkey = func.get_key(settings["content"]["gp"], record[3])
        name = record[1]; lp = record[4]; warning = record[5]; qb = record[6]; rb = record[7]
        query = f'UPDATE licensePoint \
                SET {gpkey} = {gpkey} + {lp}, \
                    warning = warning + {warning}, \
                    totalLicensePoint = totalLicensePoint + {lp}, \
                    qualiBan = qualiBan + {qb}, \
                    raceBan = raceBan + {rb} \
                WHERE driverName = "{name}";'
        func.logging(logpath, f'UPDATE: race director {record[0]}-{group}-{name}......')
        cursor.execute(query)
    db.commit()



def calculate_qualiraceFL(db:mysql.connector.MySQLConnection, group:str):
    cursor = db.cursor()
    func.logging(logpath, func.delimiter_string(f'{group} pole & raceFL points', 50), end="\n\n")

    query = f'SELECT GP, driverGroup, qualiFLdriver, qualiFLteam, \
            raceFLdriver, raceFLteam, raceFLvalidation \
            FROM qualiraceFL \
            WHERE driverGroup = "{group}";'
    func.logging(logpath, f'FETCH: qualiraceFL data......', end="\n\n")
    print(f'Fetching qualiraceFL data......\n')
    cursor.execute(query)
    result = cursor.fetchall()

    print(f'Calculating pole & raceFL points {group}......')
    for race in result:
        query = f'UPDATE driverLeaderBoard \
                SET totalPoints = totalPoints + 1 \
                WHERE driverName = "{race[2]}" AND driverGroup = "{race[1]}";'
        func.logging(logpath, f'UPDATE: pole points {race[1]}-{race[0]}-{race[2]}......')
        cursor.execute(query)

        query = f'UPDATE constructorsLeaderBoard \
                SET totalPoints = totalPoints + 1 \
                WHERE team = "{race[3]}" AND driverGroup = "{race[1]}";'
        func.logging(logpath, f'UPDATE: pole points {race[1]}-{race[0]}-{race[3]}......')
        cursor.execute(query)

        query = f'UPDATE driverLeaderBoard \
                SET totalPoints = totalPoints + {race[6]} \
                WHERE driverName = "{race[4]}" AND driverGroup = "{race[1]}";'
        func.logging(logpath, f'UPDATE: raceFL points {race[1]}-{race[0]}-{race[4]}-{race[6]}......')
        cursor.execute(query)

        query = f'UPDATE constructorsLeaderBoard \
                SET totalPoints = totalPoints + {race[6]} \
                WHERE team = "{race[5]}" AND driverGroup = "{race[1]}";'
        func.logging(logpath, f'UPDATE: raceFL points {race[1]}-{race[0]}-{race[5]}-{race[6]}......')
        cursor.execute(query)

        func.logging(logpath)
    
    db.commit()





def recalibration(db:mysql.connector.MySQLConnection, group:str):
    cursor = db.cursor()
    func.logging(logpath, func.delimiter_string(f'Recalibrating points {group}', 70), end="\n\n")
    print(func.delimiter_string(f'Recalibrating points {group}', 70), end="\n\n")

    # get the race list
    # (only will calculate the points which raceStatus = "FINISHED")
    f = open("bin/get_racelist_group_status.sql", "r")
    query = f.read().replace("GROUP", group).replace("STATUS", "FINISHED")
    f.close()
    func.logging(logpath, "FETCH: finished race list......", end="\n\n")
    print("Fetching finished race list......\n")
    cursor.execute(query)
    donerace = cursor.fetchall()
    # '''
    # marking data for every race
    for race in donerace:
        # 1. update / marking driverleaderboard, constructorleaderboard, licensepoint
        # (just marking the table, add points later on)
        update_leaderboard(db, race)
        # 2. update / marking qualiraceFL
        # (also just recording, add points later on)
        update_qualiracefl(db, race)

        print()
    
    # calculate totalpoints for every table
    # driverleaderboard, constructorleaderboard, licensepoint
    func.logging(logpath, func.delimiter_string("Calculating total points", 60), end="\n\n")
    print(func.delimiter_string("Calculating total points", 60), end="\n\n")
    # 1. driver total points
    calculate_driver(db, group)
    func.logging(logpath)
    print()

    # 2. constructor total points
    calculate_constructors(db, group)
    func.logging(logpath)
    print()

    # 3. pole & racefl extra points
    calculate_qualiraceFL(db, group)
    func.logging(logpath)
    print()

    # 4. update & calculate license points
    calculate_licensepoint(db, group)
    func.logging(logpath)
    print("\n")
    
    func.logging(logpath, func.delimiter_string(f'END Recalibration {group}', 70), end="\n\n\n\n")
    print(func.delimiter_string(f'END Recalibration {group}', 70), end="\n\n\n\n")


def main(db:mysql.connector.MySQLConnection):
    try:
        cursor = db.cursor()

        resettable(db)
        
        # get grouplist
        query = "SELECT DISTINCT(driverGroup) FROM raceCalendar;"
        cursor.execute(query)
        result = cursor.fetchall()
        for group in result:
            recalibration(db, group[0])


    except Exception as e:
        func.logging(logpath, traceback.format_exc())
        func.logging(logpath, "Error: " + str(e), end="\n")
        print("错误提示：" + str(e))
        print("积分校准失败，推荐查看日志咨询管理员寻求解决......")


"""
if __name__ == "__main__":
    main(connectserver.connectserver("server.json", "db"))
"""
