import csv
import tkinter as tk
from tkinter import filedialog
import connectserver

db = connectserver.connectserver()
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
    '1': 25,
    '2': 18,
    '3': 15,
    '4': 12,
    '5': 10,
    '6': 8,
    '7': 6,
    '8': 4,
    '9': 2,
    '10': 1,
    '11': 0,
    '12': 0,
    '13': 0,
    '14': 0,
    '15': 0,
    '16': 0,
    '17': 0,
    '18': 0,
    '19': 0,
    '20': 0,
    'pole': 1,
    'fl': 1,
    '-1': 0,
    '-2': 0,
    '-4': 0
}
def get_key(my_dict, val):
    for key, value in my_dict.items():
        if val == value:
            return key
    return "key doesn't exist"


# upload race result
def upload_race():
    try:
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        
        with open(file_path) as result:
            reader = csv.DictReader(result)
            
            fl_list = []
            fl_driver = []
            fl_team = []
            # get the race result
            for row in reader:
                drivergroup = row.get("driverGroup")
                gp = row.get("GP")
                finishposition = row.get("finishPosition")
                drivername = row.get("driverName")
                team = row.get("team")
                startposition = row.get("startPosition")
                driverstatus = row.get("driverStatus")
                fl = row.get("fastestLap")
                if fl == "null" or driverstatus != "FINISHED":
                    fl = None
                    fl_list.append(fl)
                    fl_driver.append(drivername)
                    fl_team.append(team)
                else:
                    fl_list.append(fl)
                    fl_driver.append(drivername)
                    fl_team.append(team)
                
                query = "INSERT INTO raceResult VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
                val = (drivergroup, gp, finishposition, drivername, team, startposition, fl, driverstatus)
                cursor.execute(query, val)

                if driverstatus == "RETIRED" or driverstatus == "DNF":
                    finishposition = '-1'
                elif driverstatus == "DNS":
                    finishposition = '-2'
                elif driverstatus == "DSQ":
                    finishposition = '-4'

                # pass the result to leaderboard and calculate points
                # driver leaderboard
                gpkey = get_key(gp_dict, gp)
                points = points_dict[finishposition]
                query = f'UPDATE driverLeaderBoard \
                        SET {gpkey} = {finishposition}, \
                        totalPoints = totalPoints + {points} \
                        WHERE driverName = "{drivername}" and driverGroup = "{drivergroup}";'
                cursor.execute(query)

                # constructors leaderboard
                gpkey = f'{gpkey}_1'
                query = f'SELECT {gpkey} FROM constructorsLeaderBoard \
                        WHERE team = "{team}" and driverGroup = "{drivergroup}";'
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
                            WHERE team = "{team}" and driverGroup = "{drivergroup}";'
                    cursor.execute(query)
                    query = f'UPDATE constructorsLeaderBoard \
                            SET totalPoints = totalPoints + {points} \
                            WHERE team = "{team}" and driverGroup = "{drivergroup}";'
                    cursor.execute(query)

                # also update the license point at the same time
                # (in case post-race investigation necessary)
                gpkey = get_key(gp_dict, gp)
                query = f'UPDATE licensePoint \
                        SET {gpkey} = 0 \
                        WHERE drivername = "{drivername}";'
                cursor.execute(query)
            
            # find the race fastest lap and validation
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

            # pass the fastest lap to leaderboard
            gpkey = get_key(gp_dict, gp)
            gpkey += '_FL'
            query = f'UPDATE driverLeaderBoard \
                    SET {gpkey} = {flvalidation}, \
                    totalPoints = totalPoints + {flvalidation} \
                    WHERE driverName = "{thedriver}" and driverGroup = "{drivergroup}";'
            cursor.execute(query)

            query = f'UPDATE constructorsLeaderBoard \
                    SET totalPoints = totalPoints + {flvalidation} \
                    WHERE team = "{team}";'
            if team != "Reserve":
                cursor.execute(query)



            # check confrim in race calendar
            query = f'UPDATE raceCalendar \
                    SET raceStatus = "FINISHED" \
                    WHERE GP_ENG = "{gp}";'
            cursor.execute(query)
            db.commit()

            today = datetime.today().strftime('%Y-%m-%d')
            query = f'SELECT Round, GP_ENG FROM raceCalendar \
                    WHERE raceDate >= "{today}" \
                    ORDER BY raceDate ASC LIMIT 0,3;'
            cursor.execute(query)
            result = cursor.fetchall()
            for round in result:
                round = list(round)
                race_name = round[1]

                query = f'UPDATE raceCalendar \
                        SET raceStatus = "ON GOING" \
                        WHERE GP_ENG = "{race_name}";'
                cursor.execute(query)
                db.commit()
            
        print("正赛数据上传成功，稍后请记得将文件上传到赛会群备份")
        
    except Exception as e:
        print(str(e))
        print("出现错误，请检查输入数据是否有误或联系程序管理员")
        print("没有数据上传到数据库中......")

