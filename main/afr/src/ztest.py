import connectserver


"""
config = "server.json"
db = connectserver.connectserver(config, "db")
cursor = db.cursor()

query = 'SELECT BHR_1 FROM constructorsLeaderBoard \
                    WHERE team = "CodeMaster Sucks" and driverGroup = "A1";'
cursor.execute(query)
result = cursor.fetchall()

print(result)
"""

a = 'SELECT driverLeaderBoard.*, teamList.teamColor \
    FROM driverLeaderBoard LEFT JOIN teamList \
    ON driverLeaderBoard.team = teamList.teamName \
    AND driverLeaderBoard.driverGroup = teamList.driverGroup \
    WHERE driverLeaderBoard.driverGroup = "GROUP" \
    ORDER BY totalPoints DESC;'

a = a.replace(", teamList.teamColor", "")
a = a[:a.index("LEFT JOIN")] + a[a.index("WHERE"):]
print(a)