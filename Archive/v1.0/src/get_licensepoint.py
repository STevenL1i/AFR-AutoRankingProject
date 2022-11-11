import csv
import connectserver

db = connectserver.connectserver()
cursor = db.cursor()

def get_driverlist():
    query = "SELECT * FROM afr_s7.licensePoint \
            ORDER BY CASE driverGroup \
                WHEN 'A1' THEN 1 \
                WHEN 'A2' THEN 2 \
                WHEN 'A3' THEN 3 \
                ELSE 4 \
                END, driverGroup, \
            driverName ASC;"
    cursor.execute(query)

    result = cursor.fetchall()

    file_path = "LicensePoint.csv"
    with open(file_path, "w", newline="") as file:
        header = ["driverName", "driverGroup", "AUS", "BHR", "VNM", "CHN", "NLD", "ESP", 
                "MCO", "AZE", "CAN", "FRA", "AUT", "GBR", "HUN", "BEL", "ITA", "SGP", "RUS", 
                "JPN", "USA", "MEX", "BRA", "UAE", "warning", "totalLicensePoints"]
        writer = csv.DictWriter(file, header)
        writer.writeheader()
        
        for race in result:
            d = list(race)
            race_dict = {}
            for i in range(0,len(header)):
                race_dict[header[i]] = d[i]
            writer.writerow(race_dict)