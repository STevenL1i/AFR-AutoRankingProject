import mysql.connector
import csv
import connectserver

db = connectserver.connectserver()
cursor = db.cursor()

def get_driverlist():
    query = "SELECT driverName, team, driverGroup, driverStatus \
            FROM afr_s7.driverList \
            ORDER BY CASE driverGroup \
                WHEN 'A1' THEN 1 \
                WHEN 'A2' THEN 2 \
                WHEN 'A3' THEN 3 \
                ELSE 4 \
                END, driverGroup, \
            CASE team \
                WHEN 'Mercedes' THEN 1 \
                WHEN 'Ferrari' THEN 2 \
                WHEN 'Red Bull Racing' THEN 3 \
                WHEN 'McLaren' THEN 4 \
                WHEN 'Racing Point' THEN 5 \
                WHEN 'Renault' THEN 6 \
                WHEN 'Alpha Tauri' THEN 7 \
                WHEN 'Alfa Romeo' THEN 8 \
                WHEN 'Williams' THEN 9 \
                WHEN 'Haas' THEN 10 \
                ELSE 11 \
                END, team, \
            driverStatus ASC;"
    cursor.execute(query)

    result = cursor.fetchall()

    file_path = "DirverList.csv"
    with open(file_path, "w", newline="") as driver:
        header = ["driverName", "team", "driverGroup", "driverStatus"]
        writer = csv.DictWriter(driver, header)
        writer.writeheader()
        
        for driver in result:
            d = list(driver)
            driver_dict = {}
            for i in range(0,len(header)):
                driver_dict[header[i]] = d[i]
            writer.writerow(driver_dict)