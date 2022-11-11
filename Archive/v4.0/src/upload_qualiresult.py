import csv
import tkinter
from tkinter import filedialog
import connectserver


# upload qualiying results
def upload_quali():
    db = connectserver.connectserver()
    cursor = db.cursor()

    try:
        root = tkinter.Tk()
        root.withdraw()
        filepath = filedialog.askopenfilename()

        with open(filepath) as result:
            reader = csv.DictReader(result)

            record = 0
            for row in reader:
                record += 1
                print(f'Uploading records {record}......')

                drivergroup = row.get("driverGroup")
                gp = row.get("GP")
                position = row.get("position")
                drivername = row.get("driverName")
                team = row.get("team")
                fl = row.get("fastestLap")
                if fl == '':
                    fl = None
                tyre = row.get("tyre")
                if tyre == '':
                    tyre = None
                status = row.get("driverStatus")

                # record the result
                query = "INSERT INTO qualiResult VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
                val = (drivergroup, gp, position, drivername, team, fl, tyre, status)
                cursor.execute(query, val)
            
        db.commit()
        print()
        print("排位赛数据上传成功，稍后请记得将文件上传到赛会群备份")
                
    except Exception as e:
        print(str(e))
        print("数据上传失败，请检查上传文件数据是否正确")
        print("错误提示：" + str(e))

if __name__ == "__main__":
    upload_quali()