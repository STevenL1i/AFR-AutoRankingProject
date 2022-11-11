import csv
import tkinter
from tkinter import filedialog
import connectserver

# upload qualiying results
def upload_quali():
    db = connectserver.connectserver("server.json", "league")
    cursor = db.cursor()

    try:
        root = tkinter.Tk()
        root.withdraw()
        filepath = filedialog.askopenfilename()

        with open(filepath) as result:
            reader = csv.DictReader(result)

            record = 0
            for row in reader:
                drivergroup = row.get("driverGroup")
                gp = row.get("GP")
                drivername = row.get("driverName")
                team = row.get("team")
                fl = row.get("fastestLap")
                status = row.get("driverStatus")

                if drivergroup.replace(" ", "") == "" and gp.replace(" ", "") == "" \
                and drivername.replace(" ", "") == "" and team.replace(" ", "") == "" \
                and fl.replace(" ", "") == "" and status.replace(" ", "") == "":
                    break
                
                if fl.replace(" ", "") == "" or fl == "0.000":
                    fl = "9:59.999"
                
                record += 1
                print(f'Uploading records {record}......')

                # record the result
                try:
                    query = "INSERT INTO qualiResult VALUES (%s, %s, %s, %s, %s, %s);"
                    val = (drivergroup, gp, drivername, team, fl, status)
                    cursor.execute(query, val)
                except Exception as e:
                    # skipping those whose id are not pass integrity check
                    # which violate the rules of the league
                    # also their result of this race will not be uploaded and counted anymore
                    if str(e).find('qualiResult.PRIMARY') != -1:
                        print(str(e))
                    else:
                        raise Exception(str(e))
            
            db.commit()
            
        print()
        print("排位赛数据上传成功，稍后请记得将数据整理备份")

    except Exception as e:
        print(str(e))
        print("数据上传失败，请检查上传文件数据是否正确")
        print("错误提示：" + str(e))
