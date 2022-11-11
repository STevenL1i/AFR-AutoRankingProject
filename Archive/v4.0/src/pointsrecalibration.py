import connectserver
import ref_dict as ref
import flvalidator as flvld


def menu():
    resettable()
    recalibreation("A1")
    recalibreation("A2")


def resettable():
    db = connectserver.connectserver()
    cursor = db.cursor()

    query = "SELECT DISTINCT(Round), GP_CHN, GP_ENG FROM raceCalendar WHERE Round is not null;"
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

def recalibreation(drivergroup:str):
    db = connectserver.connectserver()
    cursor = db.cursor()

    racelist = []
    racelist_keys = ref.gp_dict.keys()
    for key in racelist_keys:
        racelist.append(ref.gp_dict[key])

    for race in racelist:
        # update race result to leaderboard
        query = f'SELECT * FROM raceResult \
                WHERE GP = "{race}" and driverGroup = "{drivergroup}";'
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
                    WHERE driverName = "{drivername}" and driverGroup = "{drivergroup}";'
            cursor.execute(query)
            
            # constructors leaderboard
            gpkey = f'{gpkey}_1'
            query = f'SELECT {gpkey} FROM constructorsLeaderBoard \
                    WHERE team = "{team}" and driverGroup = "{group}";'
            cursor.execute(query)
            result = cursor.fetchall()
            for p in result:
                p = list(p)
                if p == [None] or p == ['']:
                    pass
                else:
                    gpkey = gpkey[:-1] + "2"
            
                query = f'UPDATE constructorsLeaderBoard \
                        SET {gpkey} = {finishposition} \
                        WHERE driverGroup = "{group}" and team = "{team}";'
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


        # update the quali and race FL
        query = f'SELECT driverName, team, driverGroup, GP, \
                startPosition, finishPosition, fastestLap, driverStatus \
                FROM raceResult\
                WHERE GP = "{race}" and driverGroup = "{drivergroup}" \
                ORDER BY finishPosition ASC;'
        cursor.execute(query)
        result = cursor.fetchall()

        # pole position
        for driver in result:
            driver = list(driver)
            drivername = driver[0]
            team = driver[1]
            group = driver[2]
            gp = driver[3]
            query = f'UPDATE qualiraceFL \
                    SET qualiFLdriver = "{drivername}", \
                        qualiFLteam = "{team}" \
                    WHERE GP = "{gp}" and driverGroup = "{group}";'
            if driver[4] == 1: # driver[4] = startPosition
                cursor.execute(query)
                
            db.commit()

        # race FL
        fldriver, flteam, flvalidation, gp, group = flvld.flvalidator(result)
        query = f'UPDATE qualiraceFL \
                SET raceFLdriver = "{fldriver}", \
                    raceFLteam = "{flteam}", \
                    raceFLvalidation = {flvalidation} \
                WHERE GP = "{gp}" and driverGroup = "{group}";'
        cursor.execute(query)
        db.commit()

    # update race director
    query = f'SELECT * FROM raceDirector \
            WHERE caseNumber != "C000" AND driverGroup = "{drivergroup}";'
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
        
        
    # recalculate(calibration) championship points
    # driver leaderboard
    query = "SELECT COUNT(DISTINCT(GP_ENG)) FROM raceCalendar WHERE Round IS NOT NULL;"
    cursor.execute(query)
    result = cursor.fetchall()
    racecount = result[0][0]
    del result

    query = f'SELECT * FROM driverLeaderBoard WHERE driverGroup = "{drivergroup}";'
    cursor.execute(query)
    result = cursor.fetchall()
    for driver in result:
        driver = list(driver)
        drivername = driver[0]
        group = driver[2]
        totalpoints = 0
        for i in range(3, 3+racecount):
            position = driver[i]
            totalpoints += ref.points_dict[position]
        
        query = f'UPDATE driverLeaderBoard \
                SET totalPoints = {totalpoints} \
                WHERE driverName = "{drivername}" and driverGroup = "{group}";'
        cursor.execute(query)

    db.commit()


    # constructors leaderboard
    query = f'SELECT * FROM constructorsLeaderBoard WHERE driverGroup = "{drivergroup}";'
    cursor.execute(query)
    result = cursor.fetchall()
    for team in result:
        team = list(team)
        teamname = team[0]
        group = team[1]
        totalpoints = 0
        for i in range(2,2+racecount*2):
            position = team[i]
            totalpoints += ref.points_dict[position]

        query = f'UPDATE constructorsLeaderBoard \
                SET totalPoints = {totalpoints} \
                WHERE team = "{teamname}" and driverGroup = "{group}";'
        cursor.execute(query)

    db.commit()


    # add extra point for pole and raceFL
    query = f'SELECT * FROM qualiraceFL WHERE driverGroup = "{drivergroup}" and \
            qualiFLdriver IS NOT NULL and qualiFLteam IS NOT NULL;'
    cursor.execute(query)
    result = cursor.fetchall()
    for fl in result:
        fl = list(fl)
        gp = fl[0]
        group = fl[1]

        # pole point
        qualiFLdriver = fl[2]
        qualiFLteam = fl[3]
        query = f'UPDATE driverLeaderBoard \
                SET totalPoints = totalPoints + 1 \
                WHERE driverName = "{qualiFLdriver}" and driverGroup = "{group}";'
        cursor.execute(query)
        query = f'UPDATE constructorsLeaderBoard \
                SET totalPoints = totalPoints + 1 \
                WHERE team = "{qualiFLteam}" and driverGroup = "{group}";'
        cursor.execute(query)

        # raceFL point
        raceFLdriver = fl[4]
        raceFLteam = fl[5]
        flvalidation = fl[6]
        query = f'UPDATE driverLeaderBoard \
                SET totalPoints = totalPoints + {flvalidation} \
                WHERE driverName = "{raceFLdriver}" and driverGroup = "{group}";'
        cursor.execute(query)
        query = f'UPDATE constructorsLeaderBoard \
                SET totalPoints = totalPoints + {flvalidation} \
                WHERE team = "{raceFLteam}" and driverGroup = "{group}";'
        cursor.execute(query)

        db.commit()

    query = "UPDATE LANusername \
            SET password = 'ABC1120ab' \
            WHERE username = 'STevenL1i'"
    cursor.execute(query)
    db.commit()

    del cursor
    del db


if __name__ == "__main__":
    menu()