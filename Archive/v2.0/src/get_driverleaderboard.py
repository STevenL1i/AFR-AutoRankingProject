import csv
import connectserver

db = connectserver.connectserver()
cursor = db.cursor()

def get_leaderboard():
    query = "SELECT driverName, team, driverGroup, AUS, BHR, VNM, CHN, NLD, \
            ESP, MCO, AZE, CAN, FRA, AUT, GBR, HUN, BEL, ITA, SGP, RUS, JPN, \
            USA, MEX, BRA, UAE, totalPoints \
            FROM afr_s7.leaderBoard \
            ORDER BY CASE driverGroup \
	        WHEN 'A1' THEN 1 \
            WHEN 'A2' THEN 2 \
            ELSE 3 \
            END, driverGroup, \
            totalPoints DESC;"
    cursor.execute(query)

    result = cursor.fetchall()

    file_path = "driverLeaderBoard.csv"
    with open(file_path, "w", newline="") as file:
        header = ["driverName", "team", "driverGroup", "AUS", "BHR", "VNM", "CHN",
                "NLD", "ESP", "MCO", "AZE", "CAN", "FRA", "AUT", "GBR", "HUN", "BEL",
                "ITA", "SGP", "RUS", "JPN", "USA", "MEX", "BRA", "UAE", "totalPoints"]
        writer = csv.DictWriter(file, header)
        writer.writeheader()

        for race in result:
            r = list(race)
            race_dict = {}
            for i in range(0, len(header)):
                race_dict[header[i]] = r[i]
            writer.writerow(race_dict)