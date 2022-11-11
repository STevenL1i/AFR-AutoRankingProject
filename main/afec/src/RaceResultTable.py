from datetime import datetime
import json
import xlsxwriter
import connectserver
import ref_format

config = "server.json"

db = connectserver.connectserver(config, "afec")
cursor = db.cursor()

today = datetime.today().strftime('%Y-%m-%d')
query = f'SELECT Round, GP_CHN FROM raceCalendar \
        WHERE raceStatus = "FINISHED" \
        ORDER BY raceDate DESC LIMIT 1;'
cursor.execute(query)
result = cursor.fetchall()
try:
    result = list(result[0])
    round = int(result[0])
    race_name = result[1]
    if round < 10:
        round = '0' + str(round)
    else:
        round = str(round)
except Exception:
    round = 0
    race_name = "Pre-Season"

# get season name/number
with open(config, "r") as server:
    servercfg = json.load(server)

seasonname = servercfg["afec"].split("_")[1].upper() 

workbook = xlsxwriter.Workbook(f'AFEC {seasonname} 数据分析（R{round} {race_name}）.xlsx')
# create the worksheet for each race
cursor.execute("SELECT DISTINCT(GP_CHN)FROM raceCalendar WHERE raceStatus != 'SEASON BREAK';")
result = cursor.fetchall()
race = []
for r in result:
    r = list(r)
    race.append(r[0])
raceresult_list = []
for a in range(0,len(race)):
    sheetname = f'R{a+1} {race[a]}'
    raceresult_list.append(workbook.add_worksheet(sheetname))

formatter = ref_format.format(workbook)

def get_raceresulttable():
    round = 0
    for raceresult in raceresult_list:
        # setting row width
        for i in range(0,60):
            raceresult.set_row(i, 20)

        # setting column width
        raceresult.set_column(0,0, 3)
        raceresult.set_column(1,1, 20)
        raceresult.set_column(2,2, 15)
        raceresult.set_column(3,4, 5)
        raceresult.set_column(5,5, 7)

        raceresult.merge_range("A1:E1", "AFEC", formatter.raceresultformat["a1headerf"])
        raceresult.write(1, 1, "车手", formatter.raceresultformat["headerf"])
        raceresult.write(1, 2, "差距", formatter.raceresultformat["headerf"])
        raceresult.write(1, 3, "起跑", formatter.raceresultformat["headerf"])
        raceresult.write(1, 4, "P.C.", formatter.raceresultformat["headerf"])

        round += 1
        query = f'SELECT DISTINCT(GP_ENG) FROM raceCalendar WHERE Round = {round};'
        cursor.execute(query)
        result = cursor.fetchall()
        try:
            result = list(result[0])
            therace = result[0]

            query = f'SELECT raceResult.*, teamList.teamColor, teamList.teamNameAbbr FROM \
                        raceResult JOIN teamList ON \
                        raceResult.team = teamList.teamName \
                        WHERE GP = "{therace}";'
            cursor.execute(query)
            result = cursor.fetchall()

            
            row = 2
            for position in result:
                p = list(position)
                if p[7] == "FINISHED":
                    raceresult.write(row, 0, p[2], formatter.raceresultformat["headerf"])
                elif p[7] == "RETIRED":
                    raceresult.write(row, 0, "RET", formatter.raceresultformat[p[7]])
                else:
                    raceresult.write(row, 0, p[7], formatter.raceresultformat[p[7]])

                raceresult.write(row, 1, f'{p[-1]}.{p[3]}', formatter.driverformat[p[-2]])
                raceresult.write(row, 2, p[6], formatter.raceresultformat["positionhold"])
                raceresult.write(row, 3, p[5], formatter.raceresultformat["headerf"])

                positionchange = p[5] - p[2]
                if positionchange > 0:
                    positionchange = '+' + str(positionchange)
                    raceresult.write(row, +4, positionchange, formatter.raceresultformat["positionup"])
                elif positionchange < 0:
                    positionchange = str(positionchange)
                    raceresult.write(row, 4, positionchange, formatter.raceresultformat["positiondown"])
                else:
                    positionchange = str(positionchange)
                    raceresult.write(row, 4, positionchange, formatter.raceresultformat["positionhold"])
                

                row += 1
            
            

        except Exception:
            pass




def menu():
    get_raceresulttable()
    workbook.close()

menu()