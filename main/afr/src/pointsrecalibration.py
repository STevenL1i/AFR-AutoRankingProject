import json, traceback, time

import mysql.connector
import dbconnect
import deffunc as func

# loading all the necessary json settings
# settings
settingsf = open("settings/settings.json", "r", encoding='utf-8')
settings:dict = json.load(settingsf)
settingsf.close()
# log
logpath = settings["default"]["log"]




def poleflvalidator(resultlist:list):
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
    poledriver = ""
    poleteam = ""
    for driver in resultlist:
        startposition = driver[5]
        if startposition == 1:
            poledriver = driver[3]
            poleteam = driver[4]

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
    
    return poledriver, poleteam, fldriver, flteam, validation, gp, group






def getResultData(db:mysql.connector.MySQLConnection):
    cursor = db.cursor()

    # fetch all race result record first
    query = f'SELECT * FROM get_raceResult;'
    func.logging(logpath, "Fetching race result data......", end="\n\n")
    print("Fetching race result data......", end="\n\n")
    cursor.execute(query)
    result = cursor.fetchall()


    # classify race result record by GP-group
    raceResultData = {}
    # format: {GP: {group: []}}
    for record in result:
        try:
            raceResultData[record[1]][record[0]].append(record)
        except KeyError:
            try:
                raceResultData[record[1]][record[0]] = [record]
            except KeyError:
                raceResultData[record[1]] = {}
                raceResultData[record[1]][record[0]] = [record]

    
    
    return raceResultData



def getRaceDirectorData(db:mysql.connector.MySQLConnection):
    cursor = db.cursor()

    # fetch all race director record
    query = f'SELECT * FROM get_raceDirector;'
    func.logging(logpath, "Fetching race driector data......", end="\n\n")
    print("Fetching race driector data......", end="\n\n")
    cursor.execute(query)
    result = cursor.fetchall()

    return result





def compute_points(raceResultData:dict):
    driverLeaderBoard = {}
    """
    driverLeaderBoard = {
        "driverGroup":
        {
            "driverName":
            {
                "GP": {}
                totalpoints: 0
            }
        }
    }
    """
    constructorsLeaderBoard = {}
    """
    constructorsLeaderBoard = {
        "driverGroup":
        {
            "teamName":
            {
                "GP": {},
                "totalpoints: 0
            }
        }
    }
    """
    racePoleFL = {}
    """
    racePoleFL = {
        "driverGroup":
        {
            "GP":
            {
                "poledriver": "",
                "poleteam": "",
                "fldriver": "",
                "flteam": "",
                "flvalidator": 0/1
            }
        }
    }
    """
    for GP in raceResultData.keys():
        for group in raceResultData[GP].keys():
            raceresult = raceResultData[GP][group]
            func.logging(logpath, func.delimiter_string(f'Updating {group}-{GP}', 50), end="\n\n")
            print(f'Updating {group}-{GP}......', end="\n")
            func.logging(logpath, f'Total: {len(raceresult)} drivers', end="\n\n")
            for record in raceresult:
                # record example
                # record = (driverGroup, GP, finishedPosition, driverName, team,
                #           startPosition, fastestLap, gap, driverStatus)
                # record = ('A2', 'Austria', 19, 'DINI', 'A3', 17, '1:09.738', 'DNF', 'RETIRED')
                drivergroup = record[0]
                drivername = record[3]
                team = record[4]
                gp = record[1]
                finishpos = record[2]
                driverstatus = record[8]
                
                gpcode = func.get_key(settings["content"]["gp"], gp)
                if driverstatus == "RETIRED":
                    finishpos = -1
                elif driverstatus == "DNF":
                    finishpos = -2
                elif driverstatus == "DSQ":
                    finishpos = -3
                elif driverstatus == "DNS":
                    finishpos = -4


                # updating driver leaderboard
                func.logging(logpath, f'UPDATE: driverLeaderBoard {group}-{gpcode}-{drivername}......')
                try:
                    driverLeaderBoard[drivergroup][drivername]["GP"][gpcode] = finishpos

                except KeyError:
                    if drivergroup not in driverLeaderBoard.keys():
                        driverLeaderBoard[drivergroup] = {
                            drivername: {
                                "GP": {}
                            }
                        }
                    
                    elif drivername not in driverLeaderBoard[drivergroup].keys():
                        driverLeaderBoard[drivergroup][drivername] = {
                            "GP": {}
                        }

                    driverLeaderBoard[drivergroup][drivername]["GP"][gpcode] = finishpos
                


                # updating constructors leaderboard
                func.logging(logpath, f'UPDATE: constructorsLeaderBoard {group}-{gpcode}-{drivername}......')
                try:
                    if f'{gpcode}_1' in constructorsLeaderBoard[drivergroup][team]["GP"].keys():
                        constructorsLeaderBoard[drivergroup][team]["GP"][f'{gpcode}_2'] = finishpos
                    else:
                        constructorsLeaderBoard[drivergroup][team]["GP"][f'{gpcode}_1'] = finishpos
                
                except KeyError:
                    if drivergroup not in constructorsLeaderBoard.keys():
                        constructorsLeaderBoard[drivergroup] = {
                            team: {
                                "GP": {}
                            }
                        }
                    
                    elif team not in constructorsLeaderBoard[drivergroup].keys():
                        constructorsLeaderBoard[drivergroup][team] = {
                            "GP": {}
                        }
                    

                    if f'{gpcode}_1' in constructorsLeaderBoard[drivergroup][team]["GP"].keys():
                        constructorsLeaderBoard[drivergroup][team]["GP"][f'{gpcode}_2'] = finishpos
                    else:
                        constructorsLeaderBoard[drivergroup][team]["GP"][f'{gpcode}_1'] = finishpos
                

                func.logging(logpath)
            

            # updating pole and fl
            func.logging(logpath, f'UPDATE: poleraceFL {group}-{gpcode}', end="\n")
            poledriver, poleteam, fldriver, flteam, flvalidator, GP, group = poleflvalidator(raceresult)
            func.logging(logpath, f'UPDATE: pole {group}-{gpcode}-{poledriver}-{poleteam}', end="\n")
            func.logging(logpath, f'UPDATE: raceFL {group}-{gpcode}-{fldriver}-{flteam}-{flvalidator}', end="\n\n")
            try:
                racePoleFL[group][GP] = {
                    "poledriver": poledriver,
                    "poleteam": poleteam,
                    "fldriver": fldriver,
                    "flteam": flteam,
                    "flvalidator": flvalidator
                }
            
            except KeyError:
                racePoleFL[group] = {
                    GP: {
                        "poledriver": poledriver,
                        "poleteam": poleteam,
                        "fldriver": fldriver,
                        "flteam": flteam,
                        "flvalidator": flvalidator
                    }
                }

    print()


    ### compute totalpoints for all leaderboard
    # driver leaderboard
    for group in driverLeaderBoard.keys():
        func.logging(logpath, func.delimiter_string(f'Updating {group}-driver points', 50), end="\n\n")
        for driver in driverLeaderBoard[group].keys():
            func.logging(logpath, f'UPDATE: totalpoints {group}-{driver}......')
            print(f'Computing {group}-{driver}......')
            totalpoints = 0
            for gp in driverLeaderBoard[group][driver]["GP"].keys():
                position = driverLeaderBoard[group][driver]["GP"][gp]
                totalpoints += settings["race"]["points"][str(position)]
            
            driverLeaderBoard[group][driver]["totalpoints"] = totalpoints
        
        func.logging(logpath)
        print()


    # constructors leaderboard
    for group in constructorsLeaderBoard.keys():
        func.logging(logpath, func.delimiter_string(f'Updating {group}-constructors points', 50), end="\n\n")
        for team in constructorsLeaderBoard[group].keys():
            func.logging(logpath, f'UPDATE: totalpoints {group}-{team}......')
            print(f'Computing {group}-{team}......')
            totalpoints = 0
            for gp in constructorsLeaderBoard[group][team]["GP"].keys():
                position = constructorsLeaderBoard[group][team]["GP"][gp]
                totalpoints += settings["race"]["points"][str(position)]
            
            constructorsLeaderBoard[group][team]["totalpoints"] = totalpoints
    
        func.logging(logpath)
        print()


    # pole and fl points
    func.logging(logpath, func.delimiter_string("Updating pole race FL points", 50), end="\n\n")
    for group in racePoleFL.keys():
        for gp in racePoleFL[group].keys():
            print(f'Computing poleraceFL {group}-{gp}......')
            poledriver = racePoleFL[group][gp]["poledriver"]
            func.logging(logpath, f'UPDATE: pole {group}-{gp}-{poledriver}......', end="\n")
            driverLeaderBoard[group][poledriver]["totalpoints"] += 1
            
            poleteam = racePoleFL[group][gp]["poleteam"]
            constructorsLeaderBoard[group][poleteam]["totalpoints"] += 1

            fldriver = racePoleFL[group][gp]["fldriver"]
            func.logging(logpath, f'UPDATE: raceFL {group}-{gp}-{fldriver}-{flvalidator}......', end="\n")
            driverLeaderBoard[group][fldriver]["totalpoints"] += racePoleFL[group][gp]["flvalidator"]

            flteam = racePoleFL[group][gp]["flteam"]
            constructorsLeaderBoard[group][flteam]["totalpoints"] += racePoleFL[group][gp]["flvalidator"]
    
        func.logging(logpath)
        print()


    return driverLeaderBoard, constructorsLeaderBoard, racePoleFL



def compute_LP(raceDirectorData:list):
    licensepoint = {}
    """
    licensepoint = {
        "driverName": {
            "GP": {},
            "QB": 0,
            "RB": 0,
            "Warning": 0,
            "totalLP": 12
        }
    }
    """
    for record in raceDirectorData:
        # record example
        # record = (CaseNumber, CaseDate, driverName, driverGroup, GP,
        #           penalty, penaltyLP, penaltyWarning, qualiBan, raceBan, PenaltyDescription)
        # record = ('A1-AUS-C01', datetime.date(2023, 2, 12), 'bomber-20', 'A1', 'Australia',
        #           '10 Second time penalty', -2, 0.0, 0, 0, 'Causing a severe collision')
        drivername = record[2]
        gp = record[4]
        gpcode = func.get_key(settings["content"]["gp"], gp)
        penaltyLP = record[6]
        warning = record[7]
        qualiban = record[8]
        raceban = record[9]

        if drivername not in licensepoint.keys():
            licensepoint[drivername] = {
                "GP": {},
                "QB": 0,
                "RB": 0,
                "Warning": 0.0,
                "totalLP": 12
            }
        
        try:
            licensepoint[drivername]["GP"][gpcode] += penaltyLP
        except KeyError:
            licensepoint[drivername]["GP"][gpcode] = penaltyLP

        licensepoint[drivername]["Warning"] += warning
        licensepoint[drivername]["QB"] += qualiban
        licensepoint[drivername]["RB"] += raceban
        licensepoint[drivername]["totalLP"] += penaltyLP
    

    return licensepoint





def resettable(db:mysql.connector.MySQLConnection):
    cursor = db.cursor()

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
    print()



def updatedb(db:mysql.connector.MySQLConnection, 
             driverLeaderBoard:dict, constructorsLeaderBoard:dict, racePoleFL:dict, licensepoint:dict):
    cursor = db.cursor()
    
    # update driver leaderboard
    # func.logging(logpath, func.delimiter_string("Updating driverLeaderBoard", 50), end="\n\n")
    print("Updating driverLeaderBoard......", end="\n\n")
    for group in driverLeaderBoard.keys():
        for driver in driverLeaderBoard[group].keys():
            # test whether need to add new driver record for cross-group driver
            try:
                query = f'INSERT INTO driverLeaderBoard \
                        (driverName, team, driverGroup, totalPoints) \
                        VALUES ("{driver}", (SELECT driverGroup FROM driverList WHERE driverName = "{driver}"), "{group}", 0);'
                cursor.execute(query)
                db.commit()
            except mysql.connector.errors.IntegrityError as e:
                # Duplicate entry '188066-A1' for key 'driverLeaderBoard.PRIMARY'
                if str(e).find("Duplicate entry") != -1 and str(e).find("driverLeaderBoard.PRIMARY") != -1:
                    pass
                else:
                    raise mysql.connector.errors.IntegrityError(e)


            query = f'UPDATE driverLeaderBoard SET '
            for gp in driverLeaderBoard[group][driver]["GP"].keys():
                query += f'{gp} = {driverLeaderBoard[group][driver]["GP"][gp]}, '

            query += f'totalPoints = {driverLeaderBoard[group][driver]["totalpoints"]} '
            query += f'WHERE driverName = "{driver}" AND driverGroup = "{group}";'
            func.logging(logpath, f'UPDATE: driverLeaderBoard {group}-{driver}-{driverLeaderBoard[group][driver]["totalpoints"]}......')
            cursor.execute(query)
    func.logging(logpath)


    # update constructors leaderboard
    # func.logging(logpath, func.delimiter_string("Updating constructorsLeaderBoard", 50), end="\n\n")
    print("Updating constructorsLeaderBoard......", end="\n\n")
    for group in constructorsLeaderBoard.keys():
        for team in constructorsLeaderBoard[group].keys():
            # query example
            # UPDATE driverLeaderBoard SET AUS = 1, SAU = 1, totalPoints = 12
            # WHERE driverName = "625" AND driverGroup = "A1"
            query = f'UPDATE constructorsLeaderBoard SET '
            for gp in constructorsLeaderBoard[group][team]["GP"].keys():
                query += f'{gp} = {constructorsLeaderBoard[group][team]["GP"][gp]}, '

            query += f'totalPoints = {constructorsLeaderBoard[group][team]["totalpoints"]} '
            query += f'WHERE team = "{team}" AND driverGroup = "{group}";'
            func.logging(logpath, f'UPDATE: constructorsLeaderBoard {group}-{driver}-{constructorsLeaderBoard[group][team]["totalpoints"]}......')
            cursor.execute(query)
    func.logging(logpath)
    

    # update pole and fl table
    # func.logging(logpath, func.delimiter_string("Updating qualiraceFL", 50), end="\n\n")
    print("Updating qualiraceFL......", end="\n\n")
    for group in racePoleFL.keys():
        val = []
        for gp in racePoleFL[group].keys():
            val.append((gp, group, racePoleFL[group][gp]["poledriver"], racePoleFL[group][gp]["poleteam"],
                        racePoleFL[group][gp]["fldriver"], racePoleFL[group][gp]["flteam"], racePoleFL[group][gp]["flvalidator"]))

        query = f'INSERT INTO qualiraceFL VALUES (%s, %s, %s, %s, %s, %s, %s);'
        func.logging(logpath, f'UPDATE: qualiraceFL {group}......')
        cursor.executemany(query, val)
    func.logging(logpath)


    # update license point table
    # func.logging(logpath, func.delimiter_string("Updating licensepoint", 50), end="\n\n")
    print("Updating licensepoint......", end="\n\n")
    for driver in licensepoint.keys():
        if licensepoint[driver]["totalLP"] < 0:
            licensepoint[driver]["totalLP"] = 0

        query = f'UPDATE licensePoint SET '
        for gp in licensepoint[driver]["GP"].keys():
            query += f'{gp} = {licensepoint[driver]["GP"][gp]}, '
        
        query += f'warning = {licensepoint[driver]["Warning"]}, '
        query += f'totalLicensePoint = {licensepoint[driver]["totalLP"]}, '
        query += f'raceBan = {licensepoint[driver]["RB"]}, qualiBan = {licensepoint[driver]["QB"]} '
        query += f'WHERE driverName = "{driver}";'
        
        func.logging(logpath, f'UPDATE: licensepoint {driver}-{licensepoint[driver]["totalLP"]}......')
        cursor.execute(query)
    func.logging(logpath)


    db.commit()





def main(db:mysql.connector.MySQLConnection):
    try:
        cursor = db.cursor()

        # logging
        func.logging(logpath, func.delimiter_string("User recalibrating leaderboard", 60), end="\n\n")


        # fetching event data (race result, race director record)
        func.logging(logpath, func.delimiter_string("Fetching event result data", length=60), end="\n\n")
        print(func.delimiter_string("Fetching event result data", length=60), end="\n\n")
        raceResultData = getResultData(db)
        raceDirectorData = getRaceDirectorData(db)
        func.logging(logpath, func.delimiter_string("END fetching data", length=60), end="\n\n\n\n")
        print(func.delimiter_string("END fetching data", length=60), end="\n\n\n\n")

        # compute leaderboard points on local machine
        func.logging(logpath, func.delimiter_string("Compute points", length=60), end="\n\n")
        print(func.delimiter_string("Compute points", length=60), end="\n\n")
        driverLeaderBoard, constructorsLeaderBoard, racePoleFL = compute_points(raceResultData)
        licensepoint = compute_LP(raceDirectorData)
        func.logging(logpath, func.delimiter_string("END Compute points", length=60), end="\n\n\n\n")
        print(func.delimiter_string("END Compute points", length=60), end="\n\n\n\n")

        # update leaderboard to database
        func.logging(logpath, func.delimiter_string("Updating to database", length=60), end="\n\n")
        print(func.delimiter_string("Updating to database", length=60), end="\n\n")
        resettable(db)
        updatedb(db, driverLeaderBoard, constructorsLeaderBoard, racePoleFL, licensepoint)
        func.logging(logpath, func.delimiter_string("END Updating to database", length=60), end="\n\n\n\n")
        print(func.delimiter_string("END Updating to database", length=60), end="\n\n\n\n")


        func.logging(logpath, func.delimiter_string("END recalibrating leaderboard", 60), end="\n\n\n\n")


    except Exception as e:
        func.logging(logpath, traceback.format_exc())
        func.logging(logpath, "Error: " + str(e), end="\n")
        print("错误提示：" + str(e))
        print("积分校准失败，推荐查看日志咨询管理员寻求解决......")


"""
if __name__ == "__main__":
    main(dbconnect.connect_with_conf("server.json", "db"))
"""