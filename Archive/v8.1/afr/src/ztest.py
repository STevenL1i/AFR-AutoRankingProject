import time
import dbconnect

db = dbconnect.connect_with_conf("server.json", "db")
cursor = db.cursor()
t1 = time.perf_counter()

cursor.execute("SELECT * FROM qualiResult;")
result = cursor.fetchall()

cursor.execute("SELECT * FROM raceResult;")
result = cursor.fetchall()

cursor.execute("SELECT * FROM qualiraceFL;")
result = cursor.fetchall()


t2 = time.perf_counter()

print(f'time: {t2-t1} seconds')