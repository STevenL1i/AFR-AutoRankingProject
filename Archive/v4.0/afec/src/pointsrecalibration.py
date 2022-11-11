from mysql.connector import connect
import connectserver
import ref_dict as ref


def menu():
    resettable()
    recalibreation()



def resettable():
    db = connectserver.connectserver()
    cursor = db.cursor()

    query = "SELECT Round, GP_CHN, GP_ENG FROM raceCalendar WHERE Round is not null;"
    cursor.execute(query)
    result = cursor.fetchall()

    # reset driverLeaderBorad
    query = f'UPDATE driverLeaderBoard SET '
    for race in result:
        race = list(race)
        gpkey = ref.get_key(ref.gp_dict, race[2])
        query += f'{gpkey} = null, '
    query += "totalPoints = 0"
    cursor.execute(query)
    db.commit()


    # reset constructorsLeaderBorad
    query = f'UPDATE constructorsLeaderBoard SET '
    for race in result:
        race = list(race)
        gpkey = ref.get_key(ref.gp_dict, race[2])
        query += f'{gpkey}_1 = null, {gpkey}_2 = null, '
    query += "totalPoints = 0;"
    cursor.execute(query)
    db.commit()


    # reset licensePoint
    query = f'UPDATE licensePoint SET '
    for race in result:
        race = list(race)
        gpkey = ref.get_key(ref.gp_dict, race[2])
        query += f'{gpkey} = null, '
    query += "totalLicensePoint = 12, qualiBan = 0, raceBan = 0;"
    cursor.execute(query)
    db.commit()


    """
    query = f'UPDATE driverLeaderBoard \
        SET BHR = null, CHN = null, NLD = null, AZE = null, \
        CAN = null, FRA = null, AUT = null, GBR = null, \
        HUN = null, BEL = null, ITA = null, PRT = null, \
        RUS = null, JPN = null, USA = null, SMR = null, \
        BRA = null, UAE = null, totalPoints = 0;'
    
    query = f'UPDATE constructorsLeaderBoard \
        SET BHR_1 = null, BHR_2 = null, CHN_1 = null, CHN_2 = null, \
        NLD_1 = null, NLD_2 = null, AZE_1 = null, AZE_2 = null, \
        CAN_1 = null, CAN_2 = null, FRA_1 = null, FRA_2 = null, \
        AUT_1 = null, AUT_2 = null, GBR_1 = null, GBR_2 = null, \
        HUN_1 = null, HUN_2 = null, BEL_1 = null, BEL_2 = null, \
        ITA_1 = null, ITA_2 = null, PRT_1 = null, PRT_2 = null, \
        RUS_1 = null, RUS_2 = null, JPN_1 = null, JPN_2 = null, \
        USA_1 = null, USA_2 = null, SMR_1 = null, SMR_2 = null, \
        BRA_1 = null, BRA_2 = null, UAE_1 = null, UAE_2 = null, \
        totalPoints = 0;'

    query = f'UPDATE licensePoint \
        SET BHR = null, CHN = null, NLD = null, AZE = null, \
        CAN = null, FRA = null, AUT = null, GBR = null, \
        HUN = null, BEL = null, ITA = null, PRT = null, \
        RUS = null, JPN = null, USA = null, SMR = null, \
        BRA = null, UAE = null, warning = 0, totalLicensePoint = 12, \
        qualiBan = 0, raceBan = 0;'
    """

    del cursor
    del db


def recalibreation():
    db = connectserver.connectserver()
    cursor = db.cursor()

    racelist = []
    racelist_keys = ref.gp_dict.keys()
    for key in racelist_keys:
        racelist.append(ref.gp_dict[key])

    for race in racelist:
        # update race result to leaderboard
        query = f'SELECT * FROM raceResult \
                WHERE GP = "{race}";'
        cursor.execute(query)
        result = cursor.fetchall()

        for driver in result:
            driver = list(driver)
            drivername = driver[3]
            team = driver[4]
            group = driver[0]
            gp = driver[1]
            gpkey = ref.get_key(ref.gp_dict, gp)
            finishposition = driver[2]
            status = driver[-1]
            if status == "RETIRED":
                finishposition = '-1'
            elif status == "DNF":
                finishposition = '-2'
            elif status == "DNS":
                finishposition = '-3'
            elif status == "DSQ":
                finishposition = '-4'

            # driver leaderboard
            query = f'UPDATE driverLeaderBoard \
                    SET {gpkey} = {finishposition} \
                    WHERE driverName = "{drivername}";'
            cursor.execute(query)

            # constructor leaderboard
            query = f'SELECT {gpkey}_1, {gpkey}_2 FROM constructorsLeaderBoard \
                    WHERE team = "{team}";'
            cursor.execute(query)
            result = cursor.fetchall()
            for p in result:
                if p[0] == None:
                    gpkey = gpkey + "_1"
                elif p[1] == None:
                    gpkey = gpkey + "_2"
                else:
                    gpkey = gpkey + "_3"
            
                query = f'UPDATE constructorsLeaderBoard \
                        SET {gpkey} = {finishposition} \
                        WHERE team = "{team}";'
                cursor.execute(query)

            gpkey = gpkey[:-2]
            # marking the license point board
            query = f'SELECT {gpkey} FROM licensePoint WHERE driverName = "{drivername}";'
            cursor.execute(query)
            result = cursor.fetchall()
            result = list(result[0])
            templp = result[0]
            query = f'UPDATE licensePoint \
                    SET {gpkey} = 0 \
                    WHERE driverName = "{drivername}";'
            if templp == None:
                cursor.execute(query)
                
        db.commit()

    # update race director
    query = "SELECT * FROM raceDirector \
            WHERE caseNumber != 'C000';"
    cursor.execute(query)
    result = cursor.fetchall()
    for case in result:
        case = list(case)
        drivername = case[2]
        gp = case[4]
        gpkey = ref.get_key(ref.gp_dict, gp)
        plp = case[6]
        pwarning = case[7]
        qualiban = case[8]
        raceban = case[9]
        query = f'SELECT driverName, {gpkey} FROM licensePoint WHERE drivername = "{drivername}";'
        cursor.execute(query)
        result = cursor.fetchall()
        result = list(result[0])
        if result[1] == None or result[1] == '':
            query = f'UPDATE licensePoint SET {gpkey} = 0 WHERE driverName = "{drivername}"'
            cursor.execute(query)
            db.commit()

        query = f'SELECT driverName, driverGroup FROM driverList \
                WHERE driverName = "{drivername}" AND team != "Team AFR2";'
        cursor.execute(query)
        result = cursor.fetchall()
        result = list(result[0])
        group = result[1]
        
        query = f'UPDATE licensePoint \
                SET {gpkey} = {gpkey} + {plp}, \
                    warning = warning + {pwarning}, \
                    totalLicensePoint = totalLicensePoint + {plp}, \
                    qualiBan = qualiBan + {qualiban}, \
                    raceBan = raceBan + {raceban} \
                WHERE driverName = "{drivername}";'
        cursor.execute(query)

    db.commit()


    # recalculate (calibration) championship points
    # driver leaderboard
    query = "SELECT GP_ENG, raceLength FROM raceCalendar ORDER BY Round ASC;"
    cursor.execute(query)
    racelist = cursor.fetchall()

    query = "SELECT * FROM driverLeaderBoard;"
    cursor.execute(query)
    result = cursor.fetchall()
    for driver in result:
        drivername = driver[0]
        totalpoints = 0
        for i in range(3, 3+len(racelist)):
            # racelist[i-3][1] = raceLength
            position = driver[i]
            if racelist[i-3][1] == "HALF":
                totalpoints += ref.points_dict_HALF[position]
            elif racelist[i-3][1] == "FULL":
                totalpoints += ref.points_dict_FULL[position]
        
        query = f'UPDATE driverLeaderBoard \
                SET totalpoints = {totalpoints} \
                WHERE driverName = "{drivername}";'
        cursor.execute(query)
    
    db.commit()



    # constructors leaderboard
    racelist # continute to use from last query

    query = "SELECT team"
    for race in racelist:
        racekey = ref.get_key(ref.gp_dict, race[0])
        query += f', {racekey}_1'
    
    query += " FROM constructorsLeaderBoard;"
    cursor.execute(query)
    result = cursor.fetchall()

    teamdict = {}
    for team in result:
        teamname = team[0]
        totalpoints = 0
        for i in range(1, 1+len(racelist)):
            # racelist[i-1][1] = raceLength
            position = team[i]
            if racelist[i-1][1] == "HALF":
                totalpoints += ref.points_dict_HALF[position]
            elif racelist[i-1][1] == "FULL":
                totalpoints += ref.points_dict_FULL[position]
        
        teamdict[teamname] = totalpoints

    

    query = "SELECT team"
    for race in racelist:
        racekey = ref.get_key(ref.gp_dict, race[0])
        query += f', {racekey}_2'
    
    query += " FROM constructorsLeaderBoard;"
    cursor.execute(query)
    result = cursor.fetchall()

    for team in result:
        teamname = team[0]
        totalpoints = 0
        for i in range(1, 1+len(racelist)):
            # racelist[i-1][1] = raceLength
            position = team[i]
            if racelist[i-1][1] == "HALF":
                totalpoints += ref.points_dict_HALF[position]
            elif racelist[i-1][1] == "FULL":
                totalpoints += ref.points_dict_FULL[position]
        
        teamdict[teamname] += totalpoints


        query = f'UPDATE constructorsLeaderBoard \
                SET totalpoints = {teamdict[teamname]} \
                WHERE team = "{teamname}";'
        cursor.execute(query)

    db.commit()

    
