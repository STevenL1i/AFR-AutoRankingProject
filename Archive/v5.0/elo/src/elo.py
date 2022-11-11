import math
import convertor

import connectserver

db = connectserver.connectserver()
cursor = db.cursor()

# get season information
seasoninfo = {}
query = f'SELECT * FROM afr_elo.info'
cursor.execute(query)
result = cursor.fetchall()
for record in result:
    seasoninfo[record[0]] = record[1]
afrdb = seasoninfo["afr_db"]
afecdb = seasoninfo["afec_db"]
elodb = seasoninfo["elo_db"]


def updaterank_arg(driverName:str, rank:str):
    query = f'UPDATE {elodb}.elo SET league = "{rank}" \
              WHERE driverName = "{driverName}";'
    cursor.execute(query)
    db.commit()

def updaterank():
    """
    # setting rank for unranked drivers
    query = f'UPDATE {elodb}.elo SET league = "Unranked" \
             WHERE currentpoints = basepoints;'
    cursor.execute(query)
    db.commit()
    """

    # setting rank for drivers
    query = f'SELECT * FROM {elodb}.elo \
              WHERE league = "Ranking" \
              ORDER BY currentpoints DESC;'
    cursor.execute(query)
    result = cursor.fetchall()
    driverlist = result
    drivercount = len(result)

    legend = 5
    champions = int(drivercount * 0.4)
    challenger = int(drivercount * 0.8)

    for i in range(0, legend):
        updaterank_arg(driverlist[i][0], "Legends league")
    for i in range(legend, champions):
        updaterank_arg(driverlist[i][0], "Champions league")
    for i in range(champions, challenger):
        updaterank_arg(driverlist[i][0], "Challenger league")
    for i in range(challenger, drivercount):
        updaterank_arg(driverlist[i][0], "Amateur league")
    
    db.commit()


def resetelo():
    query = f'UPDATE {elodb}.elo \
              SET currentpoints = basepoints, league = "Unranked";'
    cursor.execute(query)
    db.commit()


def recalibration():
    # get race calander
    query = f'SELECT Round, raceDate, GP_ENG, driverGroup \
             FROM {elodb}.raceCalendar ORDER BY raceDate;'
    cursor.execute(query)
    racelist = cursor.fetchall()

    for race in racelist:
        if racelist.index(race) == 0:
            resetelo()
        
        gp = race[2]
        group = race[3]

        if group == "AFEC":
            database = afecdb
        else:
            database = afrdb

        # get quali result
        query = f'SELECT * FROM {database}.qualiResult \
                  WHERE driverGroup = "{group}" AND GP = "{gp}" \
                  ORDER BY position ASC'
        cursor.execute(query)
        qualiresult = cursor.fetchall()

        # get race result
        query = f'SELECT {database}.raceResult.*, {elodb}.elo.currentpoints \
                  FROM {database}.raceResult JOIN {elodb}.elo \
                  ON raceResult.driverName = elo.driverName \
                  WHERE driverGroup = "{group}" AND GP = "{gp}" \
                  ORDER BY raceResult.finishPosition ASC;'
        cursor.execute(query)
        raceresult = cursor.fetchall()

        # determine whether it is unranked race
        # ranked_driver < 2 ==> unranked race, vice versa
        ranked_driver = 0
        for driver in raceresult:
            if driver[-1] != 0:
                ranked_driver += 1

        totalpoints = 0
        
        if group == "A1":
            totalpoints = 30 * len(raceresult)
        elif group == "A2":
            totalpoints = 15 * len(raceresult)
        elif group == "A3":
            totalpoints = 10 * len(raceresult)
        elif group == "AFEC":
            totalpoints = 20 * len(raceresult)
        """
        if ranked_driver < 2:
            if group == "A1":
                totalpoints = 30 * len(raceresult)
            elif group == "A2":
                totalpoints = 15 * len(raceresult)
            elif group == "A3":
                totalpoints = 10 * len(raceresult)
            elif group == "AFEC":
                totalpoints = 20 * len(raceresult)

        elif ranked_driver != len(raceresult):
            pointspool = 0
            for driver in raceresult:
                pointspool += driver[-1]
            totalpoints = (pointspool / ranked_driver) * len(raceresult)

        else:
            for driver in raceresult:
                totalpoints += driver[-1]
        """
        

        




        # allocate elo points by event counter
        # driver counter list = [quali, race, pc, gap]
        drivercounter = {}
        for driver in raceresult:
            drivercounter[driver[3]] = {"counter":{}, "currentpoints":driver[-1]}


        # quali result
        laptime = []
        if len(qualiresult) == 0:
            for driver in raceresult:
                drivercounter[driver[3]]["counter"]["quali"] = 0

        
        for driver in qualiresult:
            if driver[5] == None or driver[5] == "":
                pass
            else:
                laptime.append(convertor.strToLaptime(driver[5]))
        
        for driver in qualiresult:
            try:
                qualicounter = (convertor.strToLaptime(driver[5]) / (sum(laptime) / len(laptime))) - 1
                drivercounter[driver[3]]["counter"]["quali"] = qualicounter
            except AttributeError:
                try:
                    drivercounter[driver[3]]["counter"]["quali"] = -2
                except KeyError:
                    continue
                

            
        

        # race result
        mid = int(len(raceresult) / 2 + 1)
        for driver in raceresult:
            racecounter = 1 + (mid - driver[2]) * 0.1
            drivercounter[driver[3]]["counter"]["race"] = racecounter
        

        # position change
        for driver in raceresult:
            start = driver[5]
            finish = driver[2]
            try:
                upbase = 1 / (start - 1)
            except ZeroDivisionError:
                upbase = 0
            try:
                downbase = 1 / (len(raceresult) - start)
            except ZeroDivisionError:
                downbase = 0

            pc = start - finish
            if pc > 0:
                pccounter = pc * upbase
            elif pc < 0:
                pccounter = pc * downbase
            else:
                pccounter = 1
            
            drivercounter[driver[3]]["counter"]["pc"] = pccounter
        

        # gap (currently not implemented)
        for driver in raceresult:
            drivercounter[driver[3]]["counter"]["gap"] = 0

        


        # calculate total counter
        totalcounter = 0
        totalelo = 0
        for driver in raceresult:
            counter = drivercounter[driver[3]]["counter"]["quali"] * 0.6
            counter += drivercounter[driver[3]]["counter"]["race"] * 3
            counter += drivercounter[driver[3]]["counter"]["pc"] * 1.2
            counter += drivercounter[driver[3]]["counter"]["gap"] * 0.5
            drivercounter[driver[3]]["totalcounter"] = counter
            totalcounter += counter
            totalelo += drivercounter[driver[3]]["currentpoints"]
        
        
        print(f'{race[3]} {race[2]}')
        for driver in raceresult:
            elo_avg = totalelo / len(raceresult)
            counter_ratio = drivercounter[driver[3]]["totalcounter"] / totalcounter
            elo_driver = drivercounter[driver[3]]["currentpoints"]

            if elo_driver > elo_avg:
                elo_ratio = elo_avg / elo_driver
                elo = round(counter_ratio * elo_ratio * totalpoints)
            else:
                elo_ratio = elo_driver / elo_avg
                elo = round(counter_ratio * elo_ratio * totalpoints)
            
            print(f'{driver[3]}: {elo}')
            query = f'UPDATE {elodb}.elo \
                      SET currentpoints = basepoints + {elo}, \
                          league = "Ranking" \
                      WHERE driverName = "{driver[3]}";'
            if racelist.index(race) != 0:
                query = query.replace("basepoints", "currentpoints")
            cursor.execute(query)
            
            db.commit()
        
        
        print()
        if race[2] == "Hungary":
            break


# adding effect of attendance to elo
def floatingattendance():
    # get all the driver that have valid elo
    query = f'SELECT * FROM {elodb}.elo \
              WHERE currentpoints != basepoints;'
    cursor.execute(query)
    result = cursor.fetchall()

    for driver in result:
        drivername = driver[0]
        elo_delta = driver[2] - driver[1]

        print(f'recalibrating {drivername}......')
        query = f'SELECT COUNT(*) FROM {afrdb}.raceResult \
                  WHERE driverName = "{drivername}";'
        cursor.execute(query)
        result = cursor.fetchall()
        afrcount = result[0][0]

        query = f'SELECT COUNT(*) FROM {afecdb}.raceResult \
                  WHERE driverName = "{drivername}";'
        cursor.execute(query)
        result = cursor.fetchall()
        afeccount = result[0][0]

        query = f'SELECT distinct(GP_ENG) FROM {elodb}.raceCalendar \
                  WHERE {elodb}.raceCalendar.raceDate >= \
                        (SELECT distinct(joinTime) \
                         FROM {afrdb}.driverList \
                         WHERE driverName = "h0") \
                  and {elodb}.raceCalendar.raceDate <= CURDATE();'
        query2 = f'SELECT DISTINCT({elodb}.raceCalendar.GP_ENG) \
                  FROM {elodb}.raceCalendar \
                  WHERE raceDate <= CURDATE();'
        cursor.execute(query)
        result = cursor.fetchall()
        totalracecount = len(result)

        driverracecount = afrcount # + afeccount
        
        # sigmoid function
        # elo_recalibrate = round(elo_delta * (-1 / (1 + pow(math.e, -driverracecount*0.5 + totalracecount))) * 0.5 + 0.7)

        # normal distribution
        elo_recalibrate = round(elo_delta * (pow(1 / math.sqrt(math.pi * 2) * math.e, -pow((driverracecount - totalracecount)*0.8, 2) / 2) * 0.45 + 0.75))
        """
        try:
            elo_recalibrate = elo_delta * ((racecount-1) / racecount)
        except ZeroDivisionError:
            elo_recalibrate = 0
        """

        query = f'UPDATE {elodb}.elo \
                  SET currentpoints = basepoints + {elo_recalibrate} \
                  WHERE driverName = "{drivername}";'
        cursor.execute(query)

    db.commit()





def main():
    recalibration()
    floatingattendance()
    updaterank()

if __name__ == "__main__":
    main()