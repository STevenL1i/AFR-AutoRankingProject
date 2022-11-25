import json

import connectserver
import deffunc as func

config = "server.json"
gpdict = {}
with open("format/gp.json") as gp:
    gpdict = json.load(gp)
pointsdict = {}
with open("format/points.json") as points:
    pointsdict = json.load(points)

def main():
    db = connectserver.connectserver(config, "league")
    cursor = db.cursor()
    
    resettable(db, cursor)

    query = "SELECT DISTINCT(driverGroup) FROM raceCalendar;"
    cursor.execute(query)
    result = cursor.fetchall()
    for group in result:
        recalibreation(group[0], db, cursor)


def resettable(db:object, cursor:object):
    query = "SELECT DISTINCT(GP_CHN), GP_ENG FROM raceCalendar WHERE Round is not null;"
    cursor.execute(query)
    result = cursor.fetchall()

    # reset driverLeaderBoard
    query = f'UPDATE driverLeaderBoard SET '
    for race in result:
        gpkey = func.get_key(gpdict, race[1])
        query += f'{gpkey} = null, '
    query += "totalPoints = 0;"
    cursor.execute(query)
    db.commit()


def recalibreation(drivergroup:str, db:object, cursor:object):
    # get the list of the race which have been marked as finished
    # notice: ponits of the race which not been marked as "FINISHED" will not be calculated
    query = f'SELECT GP_ENG FROM raceCalendar \
            WHERE driverGroup = "{drivergroup}" AND raceStatus = "FINISHED";'
    cursor.execute(query)
    result = cursor.fetchall()
    race_list = []
    racekey_list = []
    for race in result:
        race_list.append(race[0])
        racekey_list.append(func.get_key(gpdict, race[0]))
    
    
    # creating a temp table for calculation
    # get DDL of raceResult table
    query = "SHOW CREATE TABLE raceResult;"
    cursor.execute(query)
    result = cursor.fetchall()

    # create temporary table
    try:
        createquery = result[0][1].replace("raceResult", "tempraceResult")
        cursor.execute(createquery)
    except:
        pass

    # calculating points of every race
    for i in range(0, len(race_list)):
        print(f'recalibrating {race_list[i]}......')
        # firstly clear all the record at tempraceResult table
        query = "DELETE FROM tempraceResult;"
        cursor.execute(query)
        db.commit()
        
        race = race_list[i]
        racekey = racekey_list[i]
        
        # get the original result of the race (raw result)
        query = f'SELECT * FROM raceResult \
                WHERE GP = "{race}" AND driverGroup = "{drivergroup}";'
        cursor.execute(query)
        result = cursor.fetchall()

        # copy into temp table
        for r in result:
            totaltime_sec = r[8]
            penalty = r[9]
            # also adding in-game penalty to totaltime
            realtotaltime_sec = totaltime_sec + penalty
            realtotaltime = func.second_To_laptime(realtotaltime_sec)

            query = "INSERT INTO tempraceResult VALUES \
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            val = (r[0], r[1], r[2], r[3], r[4], r[5], r[6], realtotaltime, realtotaltime_sec, 0, r[10])
            cursor.execute(query, val)
        db.commit()

        # marked driver leaderborad of this race
        # get possible post-game penalty and adding time to driver's result
        query = f'SELECT driverName, penalty FROM raceDirector \
                WHERE driverGroup = "{drivergroup}" AND GP = "{race}";'
        cursor.execute(query)
        result = cursor.fetchall()
        for penalty in result:
            penaltytime = int(penalty[1].replace("s", "").replace("S", ""))
            query = f'UPDATE tempraceResult \
                    SET totaltime_sec = totaltime_sec + {penaltytime} \
                    WHERE driverName = "{penalty[0]}";'
            cursor.execute(query)
            db.commit()
        
        # get the final result after both in-game and post-game penalty
        query = "SELECT * FROM tempraceResult \
                ORDER BY CASE driverStatus \
                    WHEN 'DNF' THEN 1 \
                    WHEN 'RETIRED' THEN 2 \
                    WHEN 'DSQ' THEN 3 \
                    WHEN 'DNS' THEN 4 \
                END, driverStatus, \
                laps DESC, totaltime_sec ASC;"
        cursor.execute(query)
        result = cursor.fetchall()

        # marked driver leaderborad of this race
        for i in range(0, len(result)):
            driver = result[i]
            driverstatus = driver[10]
            if driverstatus == "FINISHED":
                finishcode = i+1
            elif driverstatus == "RETIRED":
                finishcode = -1
            elif driverstatus == "DNF":
                finishcode = -2
            elif driverstatus == "DSQ":
                finishcode = -3
            elif driverstatus == "DNS":
                finishcode = -4
            else:
                finishcode = None
            
            query = f'UPDATE driverLeaderBoard \
                    SET {racekey} = {finishcode} \
                    WHERE driverName = "{driver[2]}";'
            cursor.execute(query)
        db.commit()

    # calculate driver's totalpoints (by race key)
    for racekey in racekey_list:
        query = f'SELECT driverName, {racekey} FROM driverLeaderBoard;'
        cursor.execute(query)
        result = cursor.fetchall()

        for driver in result:
            query = f'UPDATE driverLeaderBoard \
                    SET totalPoints = totalPoints + {pointsdict[str(driver[1])]} \
                    WHERE driverName = "{driver[0]}" AND driverGroup = "{drivergroup}";'
            cursor.execute(query)
        
    db.commit()



    # delete the temp table
    query = "DROP TABLE tempraceResult;"
    cursor.execute(query)
