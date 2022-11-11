import csv
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
import connectserver


# upload race director result
def upload_racedirector():
    db = connectserver.connectserver("afec")
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
                result = result[0]
                result = list(result)
                lastcasenumber = result[0]
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
                penaltyLP = row.get("penaltyLP")
                penaltywarning = row.get("penaltyWarning")
                qualiban = row.get("qualiBan")
                if qualiban == None or qualiban == '':
                    qualiban = 0
                raceban = row.get("raceBan")
                if raceban == None or raceban == '':
                    raceban = 0
                description = row.get("PenaltyDescription")

                if date == "" and drivername == "" and drivergroup == "" and gp == "" and penalty == "" and penaltyLP == "" \
                              and penaltywarning == "" and qualiban == "" and raceban == "" and description == "":
                    continue

                record += 1
                print(f'Uploading records {record}......')
                
                query = "INSERT INTO raceDirector VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                val = (casenum, date, drivername, drivergroup, gp, penalty, penaltyLP, penaltywarning, qualiban, raceban, description)
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
        print()
        print("判罚数据上传成功，稍后请记得将文件上传到赛会群备份")
        
    except Exception as e:
        print(str(e))
        print("数据上传失败，请检查上传文件数据是否正确")
        print("错误提示：" + str(e))

if __name__ == "__main__":
    upload_racedirector()