import connectserver

db = connectserver.connectserver()
cursor = db.cursor()

query = "SELECT * FROM driverLeaderBoard"
cursor.execute(query)
result = cursor.fetchall()

for driver in result:
    driver = list(driver)
    