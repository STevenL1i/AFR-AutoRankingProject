import csv
from datetime import datetime
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
def get_key(my_dict, val):
    for key, value in my_dict.items():
        if val == value:
            return key
    return "key doesn't exist"


# upload race director result
def upload_racedirector():
    try:
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()

        # get the post-race penalty awarded by stewards
        with open(file_path) as result:
            reader = csv.DictReader(result)

            for row in reader:
                casenum = row.get("case#")
                today = datetime.today().strftime('%Y-%m-%d')
                drivername = row.get("driverName")
                drivergroup = row.get("driverGroup")
                gp = row.get("GP")
                penalty = row.get("penalty")
                penaltyLP = row.get("penaltyLP")
                penaltywarning = row.get("penaltyWarning")
                description = row.get("PenaltyDescription")
                
                query = "INSERT INTO raceDirector VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
                val = (casenum, today, drivername, drivergroup, gp, penalty, penaltyLP, penaltywarning, description)
                cursor.execute(query, val)

                gpkey = get_key(gp_dict, gp)
                query = f'UPDATE licensePoint \
                        SET {gpkey} = {penaltyLP}, \
                        totalLicensePoint = totalLicensePoint + {penaltyLP} \
                        WHERE driverName = "{drivername}";'
                cursor.execute(query)

                query = f'UPDATE licensePoint \
                        SET warning = warning + {penaltywarning} \
                        WHERE driverName = "{drivername}";'
                cursor.execute(query)

                qualiban = row.get("qualiban")
                raceban = row.get("raceban")
                if qualiban != '':
                    query = f'UPDATE driverList \
                            SET qualiBan = qualiBan + {qualiban} \
                            WHERE driverName = "{drivername}";'
                    cursor.execute()
                if raceban != '':
                    query = f'UPDATE driverList \
                            SET raceBan = raceBan + {raceban} \
                            WHERE driverName = "{drivername}";'
                    cursor.execute()

            db.commit()
        
        print("判罚数据上传成功，稍后请记得将文件上传到赛会群备份")
        
    except Exception as e:
        print(str(e))
        print("出现错误，请检查输入数据是否有误或联系程序管理员")
        print("没有数据上传到数据库中......")
