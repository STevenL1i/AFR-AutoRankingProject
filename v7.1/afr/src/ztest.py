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
import os
try:
    os.mkdir("log")
except FileExistsError:
    pass
f = open("log/test.log", "a")
