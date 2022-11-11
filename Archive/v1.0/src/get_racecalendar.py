import csv
import connectserver

db = connectserver.connectserver()
cursor = db.cursor()

def get_racecalendar():
    query = "SELECT raceDate, GP_CHN, driverGroup, raceStatus \
            FROM afr_s7.raceCalendar \
            ORDER BY CASE driverGroup \
                WHEN 'A1' THEN 1 \
                WHEN 'A2' THEN 2 \
                WHEN 'A3' THEN 3 \
                ELSE 4 \
            END, driverGroup, \
            raceDate ASC;"
    cursor.execute(query)

    result = cursor.fetchall()

    file_path = "RaceCalendar.csv"
    with open(file_path, "w", newline="") as calendar:
        header = ["raceDate", "GP_CHN", "driverGroup", "raceStatus"]
        writer = csv.DictWriter(calendar, fieldnames=header)

        writer.writeheader()
        for race in result:
            r = list(race)
            race_dict = {}
            for i in range(0,len(header)):
                race_dict[header[i]] = r[i]
            writer.writerow(race_dict)