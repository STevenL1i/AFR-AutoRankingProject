import csv
import tkinter
from tkinter import filedialog
import dbconnect
from datetime import datetime
import mysql.connector

db = dbconnect.connect_with_conf("server.json", "db")
cursor = db.cursor()

def upload_tt():
    root = tkinter.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename()

    with open(filepath) as tt_data:
        reader = csv.DictReader(tt_data)

        count = 0
        for row in reader:
            count += 1
            print(f'uploading row {count}......')
            drivername = row.get("driverName")
            circuit = row.get("circuit")
            s1 = row.get("sector_1")
            s2 = row.get("sector_2")
            s3 = row.get("sector_3")
            lt_str = row.get("Laptime_str")

            if drivername.replace(" ","") == "" and circuit.replace(" ","") == "" \
            and s1.replace(" ","") == "" and s2.replace(" ","") == "" \
            and s3.replace(" ","") == "" and lt_str.replace(" ","") == "":
                continue

            lt = datetime.strptime(lt_str, '%M:%S.%f')
            lt.microsecond
            lt = lt.minute * 60 + lt.second + lt.microsecond / 1000000

            try:
                query = "INSERT INTO tt VALUES (%s, %s, %s, %s, %s, %s, %s)"
                val = (drivername, circuit, s1, s2, s3, lt, lt_str)
                cursor.execute(query, val)
            except mysql.connector.errors.IntegrityError as e:
                if str(e).find("Duplicate entry") != -1 and str(e).find("tt.PRIMARY") != -1:
                    query = f'UPDATE tt \
                            SET driverName = "{drivername}", \
                                circuit = "{circuit}", \
                                sector_1 = "{s1}", \
                                sector_2 = "{s2}", \
                                sector_3 = "{s3}", \
                                Laptime = "{lt}", \
                                Laptime_str = "{lt_str}" \
                            WHERE driverName = "{drivername}" AND circuit = "{circuit}";'
                    cursor.execute(query)
                else:
                    raise mysql.connector.errors.IntegrityError(e)

        db.commit()

def main():
    upload_tt()

if __name__ == "__main__":
    main()