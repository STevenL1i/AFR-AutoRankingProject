import csv
import connectserver

db = connectserver.connectserver()
cursor = db.cursor()

def get_lanusername():
    query = "SELECT * FROM afr_s7.LANusernames \
            ORDER BY username ASC;"
    cursor.execute(query)

    result = cursor.fetchall()

    file_path = "LANUsername.csv"
    with open(file_path, "w", newline="") as file:
        header = ["driverName", "username", "password", "accountStatus"]
        writer = csv.DictWriter(file, fieldnames=header)

        writer.writeheader()
        for account in result:
            a = list(account)
            account_dict = {}
            for i in range(0,len(header)):
                account_dict[header[i]] = a[i]
            writer.writerow(account_dict)