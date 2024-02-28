import csv
import tkinter
from tkinter import filedialog
import dbconnect
from datetime import datetime
import mysql.connector

db = dbconnect.connect_with_conf("server.json", "db")
cursor = db.cursor()

def upload_eval():
    root = tkinter.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename()

    with open(filepath) as eval_data:
        reader = csv.DictReader(eval_data)

        count = 0
        for row in reader:
            count += 1
            print(f'uploading row {count}......')
            drivername = row.get("driverName")
            lap = row.get("Lap")
            lt_str = row.get("Laptime_str")
            tyre = row.get("Tyre")
            status = row.get("Status")

            if drivername.replace(" ","") == "" and lap.replace(" ","") == "" \
            and lt_str.replace(" ","") == "" and tyre.replace(" ","") == "" \
            and status.replace(" ","") == "":
                continue

            lt = datetime.strptime(lt_str, '%M:%S.%f')
            lt.microsecond
            lt = lt.minute * 60 + lt.second + lt.microsecond / 1000000

            try:
                query = "INSERT INTO evalrace VALUES (%s, %s, %s, %s, %s, %s)"
                val = (drivername, lap, lt, lt_str, tyre, status)
                cursor.execute(query, val)
            except mysql.connector.errors.IntegrityError as e:
                if str(e).find("Duplicate entry") != -1 and str(e).find("evalrace.PRIMARY") != -1:
                    query = f'UPDATE evalrace \
                            SET driverName = "{drivername}", \
                                Lap = "{lap}", \
                                Laptime = "{lt}", \
                                Laptime_str = "{lt_str}", \
                                tyre = "{tyre}", \
                                status = "{status}" \
                            WHERE driverName = "{drivername}" AND Lap = "{lap}";'
                    cursor.execute(query)
                else:
                    raise mysql.connector.errors.IntegrityError(e)

        db.commit()


def main():
    upload_eval()

if __name__ == "__main__":
    main()