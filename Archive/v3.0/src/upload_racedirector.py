import csv
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
import connectserver

db = connectserver.connectserver()
cursor = db.cursor()

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
                query = "SELECT caseNumber FROM raceDirector \
                        ORDER BY caseNumber DESC LIMIT 1;"
                cursor.execute(query)
                result = cursor.fetchall()
                result = result[0]
                result = list(result)
                lastcasenumber = result[0]
                number = lastcasenumber[1:]
                number = int(number) + 1
                number = f'{number:03d}'

                casenum = lastcasenumber[0] + number
                today = datetime.today().strftime('%Y-%m-%d')
                drivername = row.get("driverName")
                drivergroup = row.get("driverGroup")
                gp = row.get("GP")
                penalty = row.get("penalty")
                penaltyLP = row.get("penaltyLP")
                penaltywarning = row.get("penaltyWarning")
                qualiban = row.get("qualiBan")
                if qualiban == '':
                    qualiban = 0
                raceban = row.get("raceBan")
                if raceban == '':
                    raceban = 0
                description = row.get("PenaltyDescription")
                
                query = "INSERT INTO raceDirector VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                val = (casenum, today, drivername, drivergroup, gp, penalty, penaltyLP, penaltywarning, qualiban, raceban, description)
                cursor.execute(query, val)

                """
                qualiban = row.get("qualiBan")
                if qualiban == '':
                    qualiban = 0
                raceban = row.get("raceBan")
                if raceban == '':
                    raceban = 0
                warning = row.get("penaltyWarning")
                if warning == '':
                    warning = 0

                query = f'UPDATE licensePoint \
                        SET qualiBan = qualiBan + {qualiban}, \
                        raceBan = raceBan + {raceban}, \
                        warning = warning + {warning} \
                        WHERE driverName = "{drivername}";'
                cursor.execute(query)
                """

            db.commit()
        
        print("判罚数据上传成功，稍后请记得将文件上传到赛会群备份")
        
    except Exception as e:
        print(str(e))
        print("出现错误，请检查输入数据是否有误或联系程序管理员")
        print("没有数据上传到数据库中......")