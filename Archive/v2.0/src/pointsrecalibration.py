import connectserver as connector

db = connector.connectserver()
cursor = db.cursor()

gp_dict = {
    "AUS": "Australia",
    "BHR": "Bahrain",
    "VNM": "Vietnam",
    "CHN": "China",
    "NLD": "Netherlands",
    "ESP": "Spain",
    "MCO": "Monaco",
    "AZE": "Azerbaijan",
    "CAN": "Canada",
    "FRA": "France",
    "AUT": "Austria",
    "GBR": "Britain",
    "HUN": "Hungary",
    "BEL": "Belgium",
    "ITA": "Italy",
    "SGP": "Singapore",
    "RUS": "Russia",
    "JPN": "Japan",
    "USA": "USA",
    "MEX": "Mexico",
    "BRA": "Brazil",
    "UAE": "Abu Dahbi"
}
points_dict = {
    1: 25,
    2: 18,
    3: 15,
    4: 12,
    5: 10,
    6: 8,
    7: 6,
    8: 4,
    9: 2,
    10: 1,
    11: 0,
    12: 0,
    13: 0,
    14: 0,
    15: 0,
    16: 0,
    17: 0,
    18: 0,
    19: 0,
    20: 0,
    -1: 0,
    -2: 0,
    -4: 0,
    'pole': 1,
    'fl': 1,
}
def get_key(my_dict, val):
    for key, value in my_dict.items():
        if val == value:
            return key
    return "key doesn't exist"

racelist = ["Australia", "Bahrain", "Vietnam", "China", "Netherlands", "Spain", "Monaco", "Azerbaijan", "Canada",
            "France", "Austria", "Britain", "Hungary", "Belgium", "Italy", "Singapore", "Russia", "Japan",
            "USA", "Mexico", "Brazil", "Abu Dahbi"]

query = "UPDATE afr_s7.driverLeaderBoard \
    SET AUS = null, AUS_pole = null, AUS_FL = null, \
    BHR = null, BHR_pole = null, BHR_FL = null, \
    VNM = null, VNM_pole = null, VNM_FL = null, \
    CHN = null, CHN_pole = null, CHN_FL = null, \
    NLD = null, NLD_pole = null, NLD_FL = null, \
    ESP = null, ESP_pole = null, ESP_FL = null, \
    MCO = null, MCO_pole = null, MCO_FL = null, \
    AZE = null, AZE_pole = null, AZE_FL = null, \
    CAN = null, CAN_pole = null, CAN_FL = null, \
    FRA = null, FRA_pole = null, FRA_FL = null, \
    AUT = null, AUT_pole = null, AUT_FL = null, \
    GBR = null, GBR_pole = null, GBR_FL = null, \
    HUN = null, HUN_pole = null, HUN_FL = null, \
    BEL = null, BEL_pole = null, BEL_FL = null, \
    ITA = null, ITA_pole = null, ITA_FL = null, \
    SGP = null, SGP_pole = null, SGP_FL = null, \
    RUS = null, RUS_pole = null, RUS_FL = null, \
    JPN = null, JPN_pole = null, JPN_FL = null, \
    USA = null, USA_pole = null, USA_FL = null, \
    MEX = null, MEX_pole = null, MEX_FL = null, \
    BRA = null, BRA_pole = null, BRA_FL = null, \
    UAE = null, UAE_pole = null, UAE_FL = null, \
    totalPoints = 0;"
cursor.execute(query)
db.commit()

query = "UPDATE afr_s7.constructorsLeaderBoard \
    SET AUS_1 = null, AUS_2 = null, BHR_1 = null, BHR_2 = null, \
    VNM_1 = null, VNM_2 = null, CHN_1 = null, CHN_2 = null, \
    NLD_1 = null, NLD_2 = null, ESP_1 = null, ESP_2 = null, \
    MCO_1 = null, MCO_2 = null, AZE_1 = null, AZE_2 = null, \
    CAN_1 = null, CAN_2 = null, FRA_1 = null, FRA_2 = null, \
    AUT_1 = null, AUT_2 = null, GBR_1 = null, GBR_2 = null, \
    HUN_1 = null, HUN_2 = null, BEL_1 = null, BEL_2 = null, \
    ITA_1 = null, ITA_2 = null, SGP_1 = null, SGP_2 = null, \
    RUS_1 = null, RUS_2 = null, JPN_1 = null, JPN_2 = null, \
    USA_1 = null, USA_2 = null, MEX_1 = null, MEX_2 = null, \
    BRA_1 = null, BRA_2 = null, UAE_1 = null, UAE_2 = null, \
    totalPoints = 0;"
cursor.execute(query)
db.commit()



for race in racelist:
    # race
    query = f'SELECT * FROM raceResult WHERE GP = "{race}";'
    cursor.execute(query)
    result = cursor.fetchall()
    for driver in result:
        d = list(driver)
        drivername = d[3]
        team = d[4]
        group = d[0]
        gp = d[1]
        gpkey = get_key(gp_dict, gp)
        position = d[2]
        status = d[-1]
        if status == "RETIRED" or status == "DNF":
            position = -1
        elif status == "DNS":
            position = -2
        elif status == "DSQ":
            position = -4

        # driver leaderboard
        query = f'UPDATE driverLeaderBoard \
                SET {gpkey} = {position} \
                WHERE driverGroup = "{group}" and driverName = "{drivername}";'
        cursor.execute(query)
        db.commit()

        # constructor leaderboard
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
                SET {gpkey} = {position}, \
                totalPoints = totalPoints + {points_dict[position]} \
                WHERE driverGroup = "{group}" and team = "{team}";'
        cursor.execute(query)
        db.commit()



    # qualifying
    query = f'SELECT * FROM qualiResult \
            WHERE GP ="{race}" and position = 1;'
    cursor.execute(query)
    result = cursor.fetchall()
    for driver in result:
        d = list(driver)
        drivername = d[3]
        team = d[4]
        group = d[0]
        gp = d[1]
        gpkey = get_key(gp_dict, gp)

        query = f'UPDATE driverLeaderBoard \
                SET {gpkey}_pole = 1 \
                WHERE driverGroup = "{group}" and driverName = "{drivername}";'
        cursor.execute(query)
        db.commit()
        query = f'UPDATE constructorsLeaderBoard \
                SET totalPoints = totalPoints + 1 \
                WHERE driverGroup = "{group}" and team = "{team}";'
        cursor.execute(query)
        db.commit()


    # race fastest lap (need to be done group by group)
    for i in range(1,4):
        gp = race
        gpkey = get_key(gp_dict, gp)
        fl_list = []
        fl_driver = []
        fl_team = []
        query = f'SELECT driverName, team, driverGroup, fastestLap \
                FROM raceResult WHERE GP = "{race}" and driverGroup = "A{i}";'
        cursor.execute(query)
        result = cursor.fetchall()
        for driver in result:
            d = list(driver)
            if d[3] == None:
                fl = "9:59.999"
            else:
                fl = d[3]
            fl_list.append(fl)
            fl_driver.append(d[0])
            fl_team.append(d[1])
            group = d[2]

        count_driver = len(fl_list)
        fl = "9:59.999"
        flvalidation = 0
        thedriver = ''
        fl_list = fl_list[:int(count_driver/4*3 + 1)]
        for index in range(0, len(fl_list)):
            if fl_list[index] != None:
                if fl_list[index] < fl:
                    fl = fl_list[index]
                    driver = fl_driver[index]
                    thedriver = driver
                    team = fl_team[index]
                    if (index + 1) < count_driver/2 + 1:
                        flvalidation = 1
                    else:
                        flvalidation = 0

        query = f'UPDATE driverLeaderBoard \
                SET {gpkey}_FL = {flvalidation} \
                WHERE driverName = "{thedriver}" and driverGroup = "A{i}";'
        cursor.execute(query)
        db.commit()

        query = f'UPDATE constructorsLeaderBoard \
                SET totalPoints = totalPoints + {flvalidation} \
                WHERE team = "{team}" and driverGroup = "A{i}";'
        cursor.execute(query)
        db.commit()


    
query = "SELECT driverName, AUS, BHR, VNM, CHN, NLD, ESP, MCO, AZE, CAN, \
        FRA, AUT, GBR, HUN, BEL, ITA, SGP, RUS, JPN, USA, MEX, BRA, UAE, driverGroup \
        FROM driverLeaderBoard;"
cursor.execute(query)
result = cursor.fetchall()

for driver in result:
    d = list(driver)
    drivername = d[0]
    group = d[-1]
    totalpoints = 0
    for i in range(1,23):
        if d[i] != None:
            totalpoints += points_dict[d[i]]
    
    query = f'UPDATE driverLeaderBoard \
            SET totalPoints = {totalpoints} \
            WHERE driverName = "{drivername}" and driverGroup = "{group}";'
    cursor.execute(query)
    db.commit()




query = "SELECT driverName, AUS_pole, BHR_pole, VNM_pole, CHN_pole, NLD_pole, ESP_pole, \
        MCO_pole, AZE_pole, CAN_pole, FRA_pole, AUT_pole, GBR_pole, HUN_pole, BEL_pole, \
        ITA_pole, SGP_pole, RUS_pole, JPN_pole, USA_pole, MEX_pole, BRA_pole, UAE_pole, driverGroup \
        FROM driverLeaderBoard;"
cursor.execute(query)
result = cursor.fetchall()

for driver in result:
    d = list(driver)
    drivername = d[0]
    group = d[-1]
    query = f'UPDATE driverLeaderBoard \
            SET totalPoints = totalPoints + 1 \
            WHERE driverName = "{drivername}" and driverGroup = "{group}";'
    for i in range(1,23):
        if d[i] != None:
            cursor.execute(query)
            db.commit()



query = "SELECT driverName, AUS_FL, BHR_FL, VNM_FL, CHN_FL, NLD_FL, ESP_FL, \
        MCO_FL, AZE_FL, CAN_FL, FRA_FL, AUT_FL, GBR_FL, HUN_FL, BEL_FL, \
        ITA_FL, SGP_FL, RUS_FL, JPN_FL, USA_FL, MEX_FL, BRA_FL, UAE_FL, driverGroup \
        FROM driverLeaderBoard;"
cursor.execute(query)
result = cursor.fetchall()

for driver in result:
    d = list(driver)
    drivername = d[0]
    group = d[-1]
    query = f'UPDATE driverLeaderBoard \
            SET totalPoints = totalPoints + 1 \
            WHERE driverName = "{drivername}" and driverGroup = "{group}";'
    for i in range(1,23):
        if d[i] == 1:
            cursor.execute(query)
            db.commit()
            


        


    
