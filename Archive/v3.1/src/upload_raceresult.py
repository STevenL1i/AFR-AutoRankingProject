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
            for row in reader:
                drivergroup = row.get("driverGroup")
                gp = row.get("GP")
                finishposition = row.get("finishPosition")
                drivername = row.get("driverName")
                team = row.get("team")
                startposition = row.get("startPosition")
                driverstatus = row.get("driverStatus")
                fl = row.get("fastestLap")
                if fl == '':
                    fl = None
                
                # special case: for A2 driver in A1
                # if driver not record in the driverlist, it will be automatically created
                if team == "Team AFR2":
                    query = f'SELECT * FROM driverList \
                            WHERE driverName = "{drivername}" and team = "TEAM AFR2";'
                    cursor.execute(query)
                    result = cursor.fetchall()
                    if len(result) == 0:
                        # update the driverlist
                        query = "INSERT INTO driverList VALUES \
                                (%s, %s, %s, %s, %s, %s);"
                        val = (drivername, team, "A1", "A2 driver", today, 1)
                        cursor.execute(query, val)
                        # update the driverLeaderBoard
                        query = "INSERT INTO driverLeaderBoard \
                                (driverName, team, driverGroup, totalPoints) VALUES (%s, %s, %s, %s);"
                        val = (drivername, team, "A1", 0)
                        cursor.execute(query, val)

                # record the result
                query = "INSERT INTO raceResult VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
                val = (drivergroup, gp, finishposition, drivername, team, startposition, fl, driverstatus)
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