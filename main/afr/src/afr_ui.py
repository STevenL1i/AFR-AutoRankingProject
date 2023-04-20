import os, json, datetime, traceback
import deffunc as func
import dbconnect
serverconfig = "server.json"
VERSION = "AFR v8.0 (UI)"

settingsf = open("settings/settings.json", "r", encoding='utf-8')
settings:dict = json.load(settingsf)
settingsf.close()
logpath = settings["default"]["log"]
# generating log file
today = datetime.datetime.today()
try:
    os.mkdir("log")
except FileExistsError:
    pass
logf = open(logpath, "a")
logf.write(func.delimiter_string("Program launching", 50) + "\n")
logf.write(func.delimiter_string("Generating log", 50) + "\n")
logf.write(f'Time: {today.strftime("%Y-%m-%d %H:%M:%S")}\n')
logf.write(f'Program Version: {VERSION}\n')
logf.write(func.get_sysinfo() + "\n")
logf.close()

import upload_driverdata
# welcome_newdriver(db):mysql.connector.MySQLConnection         # passed
# welcome_newteam(db:mysql.connector.MySQLConnection)           # passed
# transfer_driver(db:mysql.connector.MySQLConnection)           # passed, but possible unexpected special case

import upload_racedata
# upload_quali(db:mysql.connector.MySQLConnection)              # passed
# upload_race(db:mysql.connector.MySQLConnection)               # passed
# upload_rd(db:mysql.connector.MySQLConnection)                 # passed

import update_racedata
# update_racestatus(db:mysql.connector.MySQLConnection)         # passed
# update_eventresult(db:mysql.connector.MySQLConnection)        # passed
#          this including update quali/race/racedirector data

import pointsrecalibration
import ClassificationTable
import RaceResultTable

def main():
    pass



if __name__ == "__main__":
    main()