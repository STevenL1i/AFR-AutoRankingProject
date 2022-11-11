import csv
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
import connectserver

# upload race director result
def upload_racedirector():
    db = connectserver.connectserver("server.json", "league")
    cursor = db.cursor()

    try:
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()

        # get the post-race penalty awarded by stewards
        with open(file_path) as result:
            reader = csv.DictReader(result)

            record = 0
            for row in reader:
                query = "SELECT caseNumber FROM raceDirector \
                        ORDER BY caseNumber DESC LIMIT 1;"
                cursor.execute(query)
                result = cursor.fetchall()
                lastcasenumber = result[0][0]
                number = lastcasenumber[1:]
                number = int(number) + 1
                number = f'{number:03d}'
                
                casenum = lastcasenumber[0] + number
                date = row.get("casedate")
                if date == "" or date == None:
                    date = datetime.today().strftime('%Y-%m-%d')
                drivername = row.get("driverName")
                drivergroup = row.get("driverGroup")
                gp = row.get("GP")
                penalty = row.get("penalty")
                description = row.get("PenaltyDescription")

                if drivername.replace(" ", "") == "" and drivergroup.replace(" ", "") == "" \
                and gp.replace(" ", "") == "" and penalty.replace(" ", "") == "" \
                and description.replace(" ", "") == "":
                    break
                
                record += 1
                print(f'Uploading records {record}......')

                query = "INSERT INTO raceDirector VALUES (%s, %s, %s, %s, %s, %s, %s);"
                val = (casenum, date, drivername, drivergroup, gp, penalty, description)
                cursor.execute(query, val)

            db.commit()

        print()
        print("判罚数据上传成功，稍后请记得将文件上传到赛会群备份")
        
    except Exception as e:
        print(str(e))
        print("数据上传失败，请检查上传文件数据是否正确")
        print("错误提示：" + str(e))
