import csv
import tkinter
from tkinter import filedialog
import datetime
import connectserver

today = datetime.datetime.today().strftime("%Y-%m-%d")

# upload race result
def upload_race():
    db = connectserver.connectserver()
    cursor = db.cursor()

    try:
        root = tkinter.Tk()
        root.withdraw()
        filepath = filedialog.askopenfilename()

        with open(filepath) as result:
            reader = csv.DictReader(result)

            # get the race result
            record = 0
            for row in reader:
                drivergroup = row.get("driverGroup")
                gp = row.get("GP")
                finishposition = row.get("finishPosition")
                drivername = row.get("driverName")
                team = row.get("team")
                startposition = row.get("startPosition")
                gap = row.get("gap")
                driverstatus = row.get("driverStatus")

                if drivergroup == "" and gp == "" and finishposition == "" and drivername == "" and team == "" \
                                     and startposition == "" and driverstatus == "":
                    continue

                record += 1
                print(f'Uploading records {record}......')

                # record the result
                query = "INSERT INTO raceResult VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
                val = (drivergroup, gp, finishposition, drivername, team, startposition, gap, driverstatus)
                cursor.execute(query, val)
        
        db.commit()
        print()
        print("正赛数据上传成功，稍后请记得将文件上传到赛会群备份")

    except Exception as e:
        print(str(e))
        print("数据上传失败，请检查上传文件数据是否正确")
        print("错误提示：" + str(e))

if __name__ == "__main__":
    upload_race()