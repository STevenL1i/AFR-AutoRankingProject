from datetime import datetime
import json
import xlsxwriter
import connectserver
import deffunc as func

config = "server.json"

db = connectserver.connectserver(config, "league")
cursor = db.cursor()

today = datetime.today().strftime('%Y-%m-%d')
query = f'SELECT GP_CHN, raceDate FROM raceCalendar \
        WHERE raceStatus = "ON GOING" OR raceDate = {today} \
        ORDER BY raceDate ASC;'
cursor.execute(query)
result = cursor.fetchall()

if len(result) == 0:
    query = f'SELECT GP_CHN, raceDate FROM raceCalendar \
            WHERE raceStatus = "FINISHED" AND raceDate <= "{today}" \
            ORDER BY raceDate DESC;'
    cursor.execute(query)
    result = cursor.fetchall()


try:
    result = list(result[0])
    race_name = result[0]
    date_name = result[1].strftime('%m.%d')
except Exception:
    race_name = "Pre-Season"
    date_name = datetime.today().strftime('%m.%d')

if date_name[3] == '0':
    date_name = date_name[0:3] + date_name[-1]
if date_name[0] == '0':
    date_name = date_name[1:]

# get season name/number
with open(config, "r") as server:
    servercfg = json.load(server)
seasonname = servercfg["league"].split("_")[1].upper()

# create and open the excel file
workbook = xlsxwriter.Workbook(f'SVS {seasonname} 【{date_name}】 {race_name}.xlsx')


formatter = {}
with open("format/format.json") as format:
    formatter = json.load(format)
flagdict = {}
with open("format/flag.json") as flag:
    flagdict = json.load(flag)
gpdict = {}
with open("format/gp.json") as gp:
    gpdict = json.load(gp)
pointsdict = {}
with open("format/points.json") as points:
    pointsdict = json.load(points)


def get_driverlist():
    driverlist = workbook.add_worksheet("车手名单") 

    # Setting row height
    for i in range(0,100):
        driverlist.set_row(i, 16)
    
    # get group count number
    query = "SELECT DISTINCT(driverGroup) FROM driverList \
            ORDER BY CASE driverGroup \
                WHEN 'East' THEN 1 \
                WHEN 'West' THEN 2 \
                WHEN 'South' THEN 3 \
                WHEN 'North' THEN 4 \
                WHEN 'Middle' THEN 5 \
            END, driverGroup;"
    cursor.execute(query)
    grouplist = cursor.fetchall()
    groupcount = len(grouplist)

    # set column width and write group name for title
    for i in range(0, groupcount):
        driverlist.set_column(0+i*2, 0+i*2, 22)
        driverlist.set_column(1+i*2, 1+i*2, 3)
        driverlist.write(0, 0+i*2, grouplist[i][0], workbook.add_format(formatter["driverlist"]["header"]))

    for i in range(0, groupcount):
        query = f'SELECT driverName FROM driverList \
                WHERE driverGroup = "{grouplist[i][0]}" \
                  AND driverName != "Race Director" \
                ORDER BY driverName;'
        cursor.execute(query)
        result = cursor.fetchall()
        
        row = 1
        for driver in result:
            driverlist.write(row, 0+i*2, driver[0], workbook.add_format(formatter["driverlist"]["default"]))
            row += 1


def get_racecalendar():
    racecalendar = workbook.add_worksheet("赛程安排")

    # Setting row height
    for i in range(0,40):
        racecalendar.set_row(i, 31)
    
    # get group count number
    query = "SELECT DISTINCT(driverGroup) FROM driverList \
            ORDER BY CASE driverGroup \
                WHEN 'East' THEN 1 \
                WHEN 'West' THEN 2 \
                WHEN 'South' THEN 3 \
                WHEN 'North' THEN 4 \
                WHEN 'Middle' THEN 5 \
            END, driverGroup;"
    cursor.execute(query)
    grouplist = cursor.fetchall()
    groupcount = len(grouplist)

    # set column width and write group name for title
    for i in range(0, groupcount):
        racecalendar.set_column(0+i*4, 0+i*4, 17)
        racecalendar.set_column(1+i*4, 2+i*4, 15)
        racecalendar.set_column(3+i*4, 3+i*4, 9)
        racecalendar.merge_range(0, 0+i*4, 0, 2+i*4, grouplist[i][0], workbook.add_format(formatter["racecalendar"]["bigheader"]))
        racecalendar.write(1, 0+i*4, "日期", workbook.add_format(formatter["racecalendar"]["smallheader"]))
        racecalendar.write(1, 1+i*4, "分站", workbook.add_format(formatter["racecalendar"]["smallheader"]))
        racecalendar.write(1, 2+i*4, "天气", workbook.add_format(formatter["racecalendar"]["smallheader"]))

        query = f'SELECT raceDate, GP_CHN, raceStatus FROM raceCalendar \
                WHERE driverGroup = "{grouplist[i][0]}" ORDER BY Round ASC;'
        cursor.execute(query)
        result = cursor.fetchall()
        row = 2
        for race in result:
            racecalendar.write(row, 0+i*4, race[0], workbook.add_format(formatter["racecalendar"][race[2]]))
            racecalendar.write(row, 1+i*4, race[1], workbook.add_format(formatter["racecalendar"][race[2]]))
            racecalendar.write(row, 2+i*4, "晴朗", workbook.add_format(formatter["racecalendar"][race[2]]))
            row += 1


def get_leaderboard_short():
    # get group count number
    query = "SELECT DISTINCT(driverGroup) FROM driverList \
            ORDER BY CASE driverGroup \
                WHEN 'East' THEN 1 \
                WHEN 'West' THEN 2 \
                WHEN 'South' THEN 3 \
                WHEN 'North' THEN 4 \
                WHEN 'Middle' THEN 5 \
            END, driverGroup;"
    cursor.execute(query)
    grouplist = cursor.fetchall()
    groupcount = len(grouplist)

    leaderboard_list = []
    for group in grouplist:
        leaderboard_list.append(workbook.add_worksheet(f'{group[0]}积分榜'))

    for i in range(0, len(grouplist)):
        leaderboard = leaderboard_list[i]
        group = grouplist[i][0]

        # setting row width
        leaderboard.set_row(0, 31)
        query = f'SELECT COUNT(*) FROM driverLeaderBoard WHERE driverGroup = "{group}";'
        cursor.execute(query)
        result = cursor.fetchall()
        drivercount = result[0][0]
        for pos in range(1,drivercount+1):
            leaderboard.set_row(pos, 18)
        
        # setting column width
        leaderboard.set_column(0,0, 3)
        leaderboard.set_column(1,1, 21)
        leaderboard.set_column(2,3, 9)

        # creating header
        leaderboard.write(0,0, "Pos.", workbook.add_format(formatter["pointsformat"]["header"]))
        leaderboard.write(0,1, "Driver", workbook.add_format(formatter["pointsformat"]["header"]))
        leaderboard.write(0,3, "Points", workbook.add_format(formatter["pointsformat"]["header"]))
        for pos in range(1,drivercount+1):
            leaderboard.write(pos, 0, pos, workbook.add_format(formatter["pointsformat"]["header"]))

        query = f'SELECT driverName, totalPoints FROM driverLeaderBoard \
                WHERE driverGroup = "{group}" ORDER BY totalPoints DESC;'
        cursor.execute(query)
        result = cursor.fetchall()
        row = 1
        for driver in result:
            leaderboard.write(row, 1, driver[0], workbook.add_format(formatter["driverformat"]["default"]))
            leaderboard.write(row, 3, driver[1], workbook.add_format(formatter["pointsformat"]["default"]))
            row += 1


def get_leaderboard_full():
    # get group count number
    query = "SELECT DISTINCT(driverGroup) FROM driverList \
            ORDER BY CASE driverGroup \
                WHEN 'East' THEN 1 \
                WHEN 'West' THEN 2 \
                WHEN 'South' THEN 3 \
                WHEN 'North' THEN 4 \
                WHEN 'Middle' THEN 5 \
            END, driverGroup;"
    cursor.execute(query)
    grouplist = cursor.fetchall()
    groupcount = len(grouplist)

    leaderboard_list = []
    for group in grouplist:
        leaderboard_list.append(workbook.add_worksheet(f'{group[0]}全积分榜'))
    
    for i in range(0, len(grouplist)):
        leaderboard:xlsxwriter.Workbook.worksheet_class = leaderboard_list[i]
        group = grouplist[i][0]

        # setting row width
        leaderboard.set_row(0, 31)
        query = f'SELECT COUNT(*) FROM driverLeaderBoard WHERE driverGroup = "{group}";'
        cursor.execute(query)
        result = cursor.fetchall()
        drivercount = result[0][0]
        for pos in range(1, drivercount*2+1):
            leaderboard.set_row(pos, 18)
        
        # setting column width
        leaderboard.set_column(0,0, 3)
        leaderboard.set_column(1,1, 21)
        query = f'SELECT GP_ENG FROM raceCalendar \
                WHERE driverGroup = "{group}" AND Round is not null\
                ORDER BY Round ASC;'
        cursor.execute(query)
        racelist = cursor.fetchall()
        racecount = len(racelist)
        leaderboard.set_column(2, racecount+2, 9)

        # creating the header
        leaderboard.write(0,0, "Pos.", workbook.add_format(formatter["pointsformat"]["header"]))
        leaderboard.write(0,1, "Driver", workbook.add_format(formatter["pointsformat"]["header"]))
        rowcursor = 1
        for i in range(1, drivercount+1):
            leaderboard.merge_range(rowcursor, 0, rowcursor+1, 0, i, workbook.add_format(formatter["pointsformat"]["header"]))
            rowcursor += 2

        # flag of each race
        tempcursor = 2
        for race in racelist:
            race = race[0]
            leaderboard.insert_image(0, tempcursor, flagdict[race], {'x_scale':0.96, 'y_scale':0.98})
            tempcursor += 1
        leaderboard.write(0, tempcursor, "Points", workbook.add_format(formatter["pointsformat"]["header"]))
        
        # get the list of race done
        query = f'SELECT GP_ENG FROM raceCalendar \
                WHERE driverGroup = "{group}" AND raceStatus = "FINISHED" \
                AND Round is not null \
                ORDER BY Round ASC;'
        cursor.execute(query)
        doneracelist = cursor.fetchall()

        # retirve driver leaderboard from database and write into the table
        for i in range(0, len(doneracelist)):
            query = f'SELECT driverName, {func.get_key(gpdict, doneracelist[i][0])}, totalPoints \
                    FROM driverLeaderBoard \
                    WHERE driverGroup = "{group}" ORDER BY totalPoints DESC;'
            cursor.execute(query)
            result = cursor.fetchall()
            """ version 1.0: only showing the finished position in leaderboard
            for j in range(0, len(result)):
                leaderboard.write(1+j, 1, result[j][0], workbook.add_format(formatter["driverformat"]["default"]))
                pos = result[j][1]
                try:
                    if pos <= 3 and pos >= 1:
                        leaderboard.write(1+j, 2+i, pos, workbook.add_format(formatter["pointsformat"][str(pos)]))
                    elif pointsdict[str(pos)] > 0:
                        leaderboard.write(1+j, 2+i, pos, workbook.add_format(formatter["pointsformat"]["points"]))
                    elif pointsdict[str(pos)] == 0 and pos > 0:
                        leaderboard.write(1+j, 2+i, pos, workbook.add_format(formatter["pointsformat"]["outpoint"]))
                    elif pos == -1:
                        leaderboard.write(1+j, 2+i, "RET", workbook.add_format(formatter["pointsformat"]["retired"]))
                    elif pos == -2:
                        leaderboard.write(1+j, 2+i, "DNF", workbook.add_format(formatter["pointsformat"]["dnf"]))
                    elif pos == -3:
                        leaderboard.write(1+j, 2+i, "DSQ", workbook.add_format(formatter["pointsformat"]["dsq"]))
                    elif pos == -4:
                        leaderboard.write(1+j, 2+i, "DNS", workbook.add_format(formatter["pointsformat"]["dns"]))
                except TypeError:
                    leaderboard.write(1+j, 2+i, "DNA", workbook.add_format(formatter["pointsformat"]["dna"]))
                
                leaderboard.write(1+j, 2+racecount, result[j][2], workbook.add_format(formatter["pointsformat"]["header"]))
            """
            ### version 2.0: show finished position and points at the same time
            rowcursor = 1
            for j in range(0, len(result)):
                leaderboard.merge_range(rowcursor, 1, rowcursor+1, 1, result[j][0], workbook.add_format(formatter["driverformat"]["default"]))
                pos = result[j][1]
                try:
                    if pos <= 3 and pos >= 1:
                        leaderboard.write(rowcursor, 2+i, pos, workbook.add_format(formatter["pointsformat"][str(pos)]))
                        leaderboard.write(rowcursor+1, 2+i, pointsdict[str(pos)], workbook.add_format(formatter["pointsformat"]["default"]))
                    elif pointsdict[str(pos)] > 0:
                        leaderboard.write(rowcursor, 2+i, pos, workbook.add_format(formatter["pointsformat"]["points"]))
                        leaderboard.write(rowcursor+1, 2+i, pointsdict[str(pos)], workbook.add_format(formatter["pointsformat"]["default"]))
                    elif pointsdict[str(pos)] == 0 and pos > 0:
                        leaderboard.write(rowcursor, 2+i, pos, workbook.add_format(formatter["pointsformat"]["outpoint"]))
                        leaderboard.write(rowcursor+1, 2+i, pointsdict[str(pos)], workbook.add_format(formatter["pointsformat"]["default"]))
                    elif pos == -1:
                        leaderboard.write(rowcursor, 2+i, "RET", workbook.add_format(formatter["pointsformat"]["retired"]))
                        leaderboard.write(rowcursor+1, 2+i, pointsdict[str(pos)], workbook.add_format(formatter["pointsformat"]["default"]))
                    elif pos == -2:
                        leaderboard.write(rowcursor, 2+i, "DNF", workbook.add_format(formatter["pointsformat"]["dnf"]))
                        leaderboard.write(rowcursor+1, 2+i, pointsdict[str(pos)], workbook.add_format(formatter["pointsformat"]["default"]))
                    elif pos == -3:
                        leaderboard.write(rowcursor, 2+i, "DSQ", workbook.add_format(formatter["pointsformat"]["dsq"]))
                        leaderboard.write(rowcursor+1, 2+i, pointsdict[str(pos)], workbook.add_format(formatter["pointsformat"]["default"]))
                    elif pos == -4:
                        leaderboard.write(rowcursor, 2+i, "DNS", workbook.add_format(formatter["pointsformat"]["dns"]))
                        leaderboard.write(rowcursor+1, 2+i, pointsdict[str(pos)], workbook.add_format(formatter["pointsformat"]["default"]))
                except TypeError:
                    leaderboard.write(rowcursor, 2+i, "DNA", workbook.add_format(formatter["pointsformat"]["dna"]))
                    leaderboard.write(rowcursor+1, 2+i, pointsdict[str(pos)], workbook.add_format(formatter["pointsformat"]["default"]))
                
                leaderboard.merge_range(rowcursor, 2+racecount, rowcursor+1, 2+racecount, result[j][2], workbook.add_format(formatter["pointsformat"]["header"]))
                
                rowcursor += 2

                



# Race Director details
def get_racedirector():
    racedirector = workbook.add_worksheet("判罚记录")
    query = "SELECT * FROM raceDirector \
        WHERE CaseNumber != 'C000' \
        ORDER BY CaseNumber ASC;"
    cursor.execute(query)
    result = cursor.fetchall()

    # set row height
    for i in range(0, len(result)+1):
        racedirector.set_row(i, 16)

    # set column width
    racedirector.set_column(0,0, 9)
    racedirector.set_column(1,1, 14)
    racedirector.set_column(2,2, 20)
    racedirector.set_column(3,3, 8)
    racedirector.set_column(4,4, 12)
    racedirector.set_column(5,5, 12)
    racedirector.set_column(6,6, 70)

    # write the header
    racedirector.write(0,0, "案件编号", workbook.add_format(formatter["racedirector"]["header"]))
    racedirector.write(0,1, "日期", workbook.add_format(formatter["racedirector"]["header"]))
    racedirector.write(0,2, "车手", workbook.add_format(formatter["racedirector"]["header"]))
    racedirector.write(0,3, "组别", workbook.add_format(formatter["racedirector"]["header"]))
    racedirector.write(0,4, "比赛", workbook.add_format(formatter["racedirector"]["header"]))
    racedirector.write(0,5, "处罚", workbook.add_format(formatter["racedirector"]["header"]))
    racedirector.write(0,6, "大致描述", workbook.add_format(formatter["racedirector"]["header"]))


    
    row = 1
    for incidents in result:
        racedirector.write(row, 0, incidents[0], workbook.add_format(formatter["racedirector"]["default"]))
        racedirector.write(row, 1, incidents[1], workbook.add_format(formatter["racedirector"]["date"]))
        racedirector.write(row, 2, incidents[2], workbook.add_format(formatter["racedirector"]["default"]))
        racedirector.write(row, 3, incidents[3], workbook.add_format(formatter["racedirector"]["default"]))
        racedirector.write(row, 4, incidents[4], workbook.add_format(formatter["racedirector"]["default"]))
        racedirector.write(row, 5, incidents[5], workbook.add_format(formatter["racedirector"]["default"]))
        racedirector.write(row, 6, incidents[6], workbook.add_format(formatter["racedirector"]["default"]))
        row += 1


def main():
    get_driverlist()
    get_racecalendar()
    get_leaderboard_short()
    get_leaderboard_full()
    get_racedirector()
    workbook.close()

if __name__ == "__main__":
    main()