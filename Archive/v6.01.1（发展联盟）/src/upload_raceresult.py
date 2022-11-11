import csv
import tkinter
from tkinter import filedialog
import connectserver
import deffunc as func

# upload race result
def upload_race():
    db = connectserver.connectserver("server.json", "league")
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
                drivername = row.get("driverName")
                team = row.get("team")
                startposition = row.get("startPosition")
                fl = row.get("fastestLap")
                laps = row.get("laps")
                totaltime = row.get("totaltime")
                penalty = row.get("penalty")
                driverstatus = row.get("driverStatus")

                if drivergroup.replace(" ", "") == "" and gp.replace(" ", "") == "" \
                and drivername.replace(" ", "") == "" and team.replace(" ", "") == "" \
                and startposition.replace(" ", "") == "" and fl.replace(" ", "") == "" \
                and laps.replace(" ", "") == "" and totaltime.replace(" ", "") == "" \
                and penalty.replace(" ", "") == "" and driverstatus.replace(" ", "") == "":
                    break
                
                if fl.replace(" ", "") == "" or fl == "0.000":
                    fl = "9:59.999"

                totaltime_sec = func.laptime_To_second(totaltime)
                
                record += 1
                print(f'Uploading records {record}......')

                # record the result
                try:
                    query = "INSERT INTO raceResult VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                    val = (drivergroup, gp, drivername, team, startposition, fl, laps, totaltime, totaltime_sec, penalty, driverstatus)
                    cursor.execute(query, val)
                except Exception as e:
                    # skipping those whose id are not pass integrity check
                    # which violate the rules of the league
                    # also their result of this race will not be uploaded and counted anymore
                    if str(e).find('raceResult.PRIMARY') != -1:
                        print(str(e))
                    else:
                        raise Exception(str(e))
                
                query = f'UPDATE raceCalendar \
                        SET raceStatus = "FINISHED" \
                        WHERE GP_ENG = "{gp}" AND driverGroup = "{drivergroup}";'
                cursor.execute(query)

        db.commit()
        print()
        print("正赛数据上传成功，稍后请记得将数据整理备份")

    except Exception as e:
        print(str(e))
        print("数据上传失败，请检查上传文件数据是否正确")
        print("错误提示：" + str(e))
