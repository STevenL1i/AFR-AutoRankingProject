import csv
import tkinter as tk
from tkinter import filedialog

from mysql.connector.errors import IntegrityError
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
def get_key(my_dict, val):
    for key, value in my_dict.items():
        if val == value:
            return key
    return "key doesn't exist"


# upload qualifying result
def upload_quali():
    try:
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        
        with open(file_path) as result:
            reader = csv.DictReader(result)

            for row in reader:
                drivergroup = row.get("driverGroup")
                gp = row.get("GP")
                position = row.get("position")
                drivername = row.get("driverName")
                team = row.get("team")
                fl = row.get("fastestLap")
                tyre = row.get("tyre")
                driverstatus = row.get("driverStatus")
                if tyre == 'n' or tyre == 'N':
                    tyre = None
                if fl == 'null':
                    fl = None

                query = "INSERT INTO qualiResult VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
                val = (drivergroup, gp, position, drivername, team, fl, tyre, driverstatus)
                cursor.execute(query, val)

                # pass the pole to leaderboard
                gpkey = get_key(gp_dict, gp)
                gpkey += '_pole'
                if position == '1':
                    query = f'UPDATE driverLeaderBoard \
                            SET {gpkey} = 1, \
                            totalPoints = totalPoints + 1 \
                            WHERE driverName = "{drivername}" and driverGroup = "{drivergroup}";'
                    cursor.execute(query)

                    query = f'UPDATE constructorsLeaderBoard \
                            SET totalPoints = totalPoints + 1 \
                            WHERE team = "{team}" and driverGroup = "{drivergroup}";'
                    cursor.execute(query)

            db.commit()
            
        print("排位赛数据上传成功，稍后请记得将文件上传到赛会群备份")

    except Exception as e:
        print(str(e))
        print("出现错误，请检查输入数据是否有误或联系程序管理员")
        print("没有数据上传到数据库中......")

