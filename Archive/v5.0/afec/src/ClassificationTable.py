from datetime import datetime
import xlsxwriter
import connectserver
import ref_dict
import ref_format

db = connectserver.connectserver("afec")
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
            ORDER BY raceDate DESC'
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


# create and open the excel file
workbook = xlsxwriter.Workbook(f'AFEC S1【{date_name}】{race_name}.xlsx')
driverlist = workbook.add_worksheet("车手名单")
racecalendar = workbook.add_worksheet("赛程安排")
##signup = workbook.add_worksheet("参赛名单")
leaderboard = workbook.add_worksheet("积分榜")
leaderboard_cons = workbook.add_worksheet("车队积分榜")
leaderboard_full = workbook.add_worksheet("总积分榜")
licensepoint = workbook.add_worksheet("车手安全分")
lanusernamelist = workbook.add_worksheet("LAN name")
seasonstats = workbook.add_worksheet("数据统计")
racedirector = workbook.add_worksheet("判罚详细")

formatter = ref_format.format(workbook)

# Driver list worksheet
def get_driverlist():
    # Setting column and row width
    for i in range(0,100):
        driverlist.set_row(i, 16)
    driverlist.set_column(0,0, 20)
    driverlist.set_column(1,1, 20)
    driverlist.set_column(2,2, 20)
    driverlist.set_column(3,3, 20)
    driverlist.set_column(4,4, 3)
    driverlist.set_column(5,5, 20)
    # write the title
    driverlist.merge_range("A1:D1", "AFEC", formatter.default["groupf"])
    driverlist.write("F1", "Reserve", formatter.default["Reserve"])


    # teamed driver
    query = 'SELECT * FROM teamList \
                WHERE driver_1 is not NULL OR driver_2 is not NULL \
                    OR driver_3 is not NULL OR driver_4 is not NULL \
                ORDER BY teamName ASC;'
    cursor.execute(query)
    result = cursor.fetchall()

    row = 1
    col = 0
    side = 0
    for team in result:
        if side == 0:
            pass
        elif side == 1:
            col += 2
        
        driverlist.write(row, col, team[0], formatter.driverformat[team[1]])
        driverlist.write(row+1, col, team[2], formatter.driverformat[team[1]])
        driverlist.write(row+2, col, "", formatter.driverformat[team[1]])
        driverlist.write(row+3, col, "", formatter.driverformat[team[1]])
        driverlist.write(row, col+1, team[3], formatter.driverformat[team[1]])
        driverlist.write(row+1, col+1, team[4], formatter.driverformat[team[1]])
        driverlist.write(row+2, col+1, team[5], formatter.driverformat[team[1]])
        driverlist.write(row+3, col+1, team[6], formatter.driverformat[team[1]])

        if side == 0:
            side = 1
        elif side == 1:
            side = 0
            col = 0
            row += 4

    """
    # reserve driver
    query = "SELECT * FROM driverList WHERE team = "

    row = 1
    col = 5
    """

# Race Calendar worksheet
def get_racecalendar():
    # Setting column and row width
    racecalendar.set_column(0,0, 17)
    racecalendar.set_column(1,2, 15)
    racecalendar.set_column(3,3, 9)
    racecalendar.set_column(4,4, 17)
    racecalendar.set_column(5,6, 15)
    racecalendar.set_column(7,7, 9)
    racecalendar.set_column(8,9, 17)
    racecalendar.set_column(10,10, 15)
    racecalendar.set_row(0, 30)
    for i in range(1,40):
        racecalendar.set_row(i, 31)

    # Creating the header
    racecalendar.merge_range("A1:C1", "AFEC - S1", formatter.racecalendar["RCHformat"])
    racecalendar.write("A2", "日期", formatter.racecalendar["RCdefaultf"])
    racecalendar.write("B2", "分站", formatter.racecalendar["RCdefaultf"])
    racecalendar.write("C2", "长度", formatter.racecalendar["RCdefaultf"])

    # retirve driverlist from database and write into the table
    query = "SELECT raceDate, GP_CHN, raceLength, raceStatus FROM raceCalendar;"
    cursor.execute(query)
    result = cursor.fetchall()

    row = 2
    col = 0
    for race in result:
        race = list(race)
        racedate = race[0]
        gp = race[1]
        length = race[2]
        status = race[3]
        
        if length == "HALF":
            length = "50%"
        elif length == "FULL":
            length = "100%"
        racecalendar.write(row, col, racedate, formatter.racecalendar[status])
        racecalendar.write(row, col+1, gp, formatter.racecalendar[status])
        racecalendar.write(row, col+2, length, formatter.racecalendar[status])

        row += 1


# leaderboard (short)
def get_leaderboard_short():
    # Setting row width
    leaderboard.set_row(0, 31)
    query = f'SELECT count(*) FROM driverLeaderBoard;'
    cursor.execute(query)
    result = cursor.fetchall()
    drivercount = result[0]
    drivercount = list(drivercount)
    drivercount = drivercount[0]
    for pos in range(1,drivercount+1):
        leaderboard.set_row(pos, 18)

    # setting column width
    leaderboard.set_column(0,0, 3)
    leaderboard.set_column(1,1, 21)
    leaderboard.set_column(2,4, 9)
    leaderboard.set_column(5,5, 21)
    leaderboard.set_column(6,6, 9)
    leaderboard.set_column(7,7, 3)
    leaderboard.set_column(8,8, 21)
    leaderboard.set_column(9,10, 9)

    # Creating the header
    leaderboard.write(0,0, "Pos.", formatter.pointsformat["header"])
    leaderboard.write(0,1, "Driver", formatter.pointsformat["header"])
    leaderboard.write(0,3, "Points", formatter.pointsformat["header"])
    leaderboard.write(0,4, "L.P.", formatter.pointsformat["header"])
    for pos in range(1,drivercount+1):
        leaderboard.write(pos, 0, pos, formatter.pointsformat["header"])
    
    tempcursor = 0
    leaderboard.write(tempcursor, 7, "Pos.", formatter.pointsformat["header"])
    leaderboard.write(tempcursor, 8, "Team", formatter.pointsformat["header"])
    leaderboard.write(tempcursor, 10, "Points", formatter.pointsformat["header"])
    """
    for pos in range(1,11):
        leaderboard.write(tempcursor + pos, 7, pos, formatter.pointsformat["header"])
    """

    # retirve driverleaderboard from database and write into the table
    query = f'SELECT driverLeaderBoard.driverName, driverLeaderBoard.totalPoints, driverLeaderBoard.team, \
            licensePoint.warning, licensePoint.totalLicensePoint, licensePoint.raceBan, licensePoint.qualiBan, teamList.teamColor \
            FROM driverLeaderBoard JOIN licensePoint ON \
            driverLeaderBoard.driverName = licensePoint.driverName \
                                    JOIN teamList ON \
            teamList.teamName = driverLeaderBoard.team \
            ORDER BY totalPoints DESC;'
    cursor.execute(query)
    result = cursor.fetchall()

    row = 1
    col = 1
    for driver in result:
        driver = list(driver)
        drivername = driver[0]
        totalpoints = driver[1]
        team = driver[2]
        teamcolor = driver[-1]
        warning = driver[3]
        totallp = driver[4]
        raceban = driver[5]
        qualiban = driver[6]

        # writing driver's name
        if warning != 0:
            tag = warning % 4
            #△☆★
            if tag == 0.5:
                drivername = "△" + drivername
            elif tag == 1:
                drivername = "☆" + drivername
            elif tag == 1.5:
                drivername = "△☆" + drivername
            elif tag == 2:
                drivername = "★" + drivername
            elif tag == 2.5:
                drivername = "△★" + drivername
            elif tag == 3:
                drivername = "☆★" + drivername
            elif tag == 3.5:
                drivername = "△☆★" + drivername
            elif tag == 0:
                drivername = "★★" + drivername


        if driver[2] == "Retired":
            leaderboard.write(row, col, drivername, formatter.driverformat["Reserve"])
        else:
            leaderboard.write(row, col, drivername, formatter.driverformat[teamcolor])
        # championship points
        leaderboard.write(row, col+2, totalpoints, formatter.pointsformat["header"])
        # license points
        if totallp == 11 or totallp == 12:
            leaderboard.write(row, col+3, totallp, formatter.licensepointformat["excellent"])
        elif totallp >= 7 and totallp <= 10:
            leaderboard.write(row, col+3, totallp, formatter.licensepointformat["good"])
        elif totallp >= 4 and totallp <= 6:
            leaderboard.write(row, col+3, totallp, formatter.licensepointformat["poor"])
        elif totallp >= 1 and totallp <= 3:
            leaderboard.write(row, col+3, totallp, formatter.licensepointformat["danger"])
        elif totallp == 0:
            leaderboard.write(row, col+3, totallp, formatter.licensepointformat["trigger"])
        # any race or quali ban
        if qualiban != 0:
            banmsg = f'Qualiying to be DSQ x{qualiban}'
            leaderboard.write(row, col+4, banmsg, formatter.licensepointformat["trigger"])
        if raceban != 0:
            banmsg = f'Race to be DSQ x{raceban}'
            leaderboard.write(row, col+4, banmsg, formatter.licensepointformat["trigger"])

        row += 1

    # constructors leaderboard
    query = f'SELECT constructorsLeaderBoard.team, teamList.teamColor, constructorsLeaderBoard.totalPoints \
            FROM constructorsLeaderBoard JOIN teamList ON \
            constructorsLeaderBoard.team = teamList.teamName \
            ORDER BY totalPoints DESC;'
    cursor.execute(query)
    result = cursor.fetchall()

    row = 1
    col = 8
    for team in result:
        team = list(team)
        leaderboard.write(row, col-1, row, formatter.pointsformat["header"])
        leaderboard.write(row, col, team[0], formatter.driverformat[team[1]])
        leaderboard.write(row, col+2, team[2], formatter.pointsformat["header"])
        row += 1



# full constructors leaderboard
def get_leaderboard_constructors():
    # setting row width
    leaderboard_cons.set_row(0, 31)
    for i in range(1,20):
        leaderboard_cons.set_row(i, 23)
    
    # setting column width
    leaderboard_cons.set_column(0,0, 3)
    leaderboard_cons.set_column(1,1, 21)
    query = "SELECT COUNT(DISTINCT(GP_ENG)) FROM raceCalendar WHERE Round != 0 OR Round != null;"
    cursor.execute(query)
    result = cursor.fetchall()
    result = list(result[0])
    race_count = result[0]
    leaderboard_cons.set_column(2, race_count*3+1, 2.4)
    leaderboard_cons.set_column(race_count*3+2, race_count*3+3, 9)

    # creating the header
    leaderboard_cons.write(0,0, "Pos.", formatter.pointsformat["header"])
    leaderboard_cons.write(0,1, "Team", formatter.pointsformat["header"])
    """
    for i in range(1,11):
        leaderboard_cons.write(i, 0, i, formatter.pointsformat["header"])
    """

    # flags of each race
    query = "SELECT DISTINCT(GP_ENG), Round FROM raceCalendar WHERE Round != 0 OR Round != null ORDER BY Round;"
    cursor.execute(query)
    result = cursor.fetchall()
    tempcursor = 2
    for race in result:
        race = list(race)
        race = race[0]
        leaderboard_cons.insert_image(0, tempcursor, ref_dict.flag_dict[race], {'x_scale':0.96, 'y_scale':0.98})
        tempcursor += 3
    leaderboard_cons.write(0, tempcursor, "Points", formatter.pointsformat["header"])


    # retirve constructors leaderboard from database and write into the table
    query = f'SELECT COUNT(DISTINCT(GP)) FROM raceResult;'
    cursor.execute(query)
    result = cursor.fetchall()
    result = list(result[0])
    race_done = result[0]

    query = f'SELECT constructorsLeaderBoard.*, teamList.teamColor \
            FROM constructorsLeaderBoard JOIN teamList ON \
            constructorsLeaderBoard.team = teamList.teamName \
            ORDER BY totalPoints DESC;'
    cursor.execute(query)
    result = cursor.fetchall()

    row = 1
    col = 0
    for team in result:
        team = list(team)
        teamname = team[0]
        teamcolor = team[-1]
        tempcursor = col
        # team name
        leaderboard_cons.write(row, tempcursor, row, formatter.pointsformat["header"])
        leaderboard_cons.write(row, tempcursor+1, teamname, formatter.teamformat[teamcolor])
        # finish position of each race
        for r in range(2, 2 + race_done*3):
            if team[r] != None:
                if team[r] == 1:
                    leaderboard_cons.write(row, tempcursor+r, team[r], formatter.pointsformat["p1"])
                elif team[r] == 2:
                    leaderboard_cons.write(row, tempcursor+r, team[r], formatter.pointsformat["p2"])
                elif team[r] == 3:
                    leaderboard_cons.write(row, tempcursor+r, team[r], formatter.pointsformat["p3"])
                elif team[r] >= 4 and team[r] <= 10:
                    leaderboard_cons.write(row, tempcursor+r, team[r], formatter.pointsformat["points"])
                elif team[r] >= 11:
                    leaderboard_cons.write(row, tempcursor+r, team[r], formatter.pointsformat["outpoint"])
                elif team[r] == -1:
                    leaderboard_cons.write(row, tempcursor+r, "RET", formatter.pointsformat["retired"])
                elif team[r] == -2:
                    leaderboard_cons.write(row, tempcursor+r, "DNS", formatter.pointsformat["dns"])
                elif team[r] == -4:
                    leaderboard_cons.write(row, tempcursor+r, "DSQ", formatter.pointsformat["dsq"])
            else:
                leaderboard_cons.write(row, tempcursor+r, "DNA", formatter.pointsformat["dna"])

        leaderboard_cons.write(row, 2 + race_count*3, team[-2], formatter.pointsformat["header"])
        row += 1


# full leaderboard
def get_leaderboard_full():
    # Setting row width
    leaderboard_full.set_row(0, 31)
    query = f'SELECT count(*) FROM driverLeaderBoard;'
    cursor.execute(query)
    result = cursor.fetchall()
    drivercount = result[0]
    drivercount = list(drivercount)
    drivercount = drivercount[0]
    for pos in range(1,drivercount+1):
        leaderboard_full.set_row(pos, 18)
        tempcursor = pos
    

    # setting column width
    leaderboard_full.set_column(0,0, 3)
    leaderboard_full.set_column(1,1, 21)
    query = "SELECT COUNT(DISTINCT(GP_ENG)) FROM raceCalendar WHERE Round != 0 OR Round != null;"
    cursor.execute(query)
    result = cursor.fetchall()
    result = list(result[0])
    race_count = result[0]
    leaderboard_full.set_column(2, race_count + 2, 9)
    
    # creating the header
    leaderboard_full.write(0,0, "Pos.", formatter.pointsformat["header"])
    leaderboard_full.write(0,1, "Team", formatter.pointsformat["header"])
    for i in range(1, drivercount+1):
        leaderboard_full.write(i, 0, i, formatter.pointsformat["header"])

    

    # flags of each race
    query = "SELECT DISTINCT(GP_ENG), Round FROM raceCalendar WHERE Round != 0 OR Round != null ORDER BY Round;"
    cursor.execute(query)
    result = cursor.fetchall()
    tempcursor = 2
    for race in result:
        race = list(race)
        race = race[0]
        leaderboard_full.insert_image(0, tempcursor, ref_dict.flag_dict[race], {'x_scale':0.96, 'y_scale':0.98})
        tempcursor += 1
    leaderboard_full.write(0, tempcursor, "Points", formatter.pointsformat["header"])
    
    
    # retirve driver leaderboard from database and write into the table
    query = f'SELECT COUNT(DISTINCT(GP)) FROM raceResult;'
    cursor.execute(query)
    result = cursor.fetchall()
    result = list(result[0])
    race_done = result[0]

    query = f'SELECT driverLeaderBoard.*, teamList.teamColor \
            FROM driverLeaderBoard JOIN teamList ON \
            driverLeaderBoard.team = teamList.teamName \
            ORDER BY totalPoints DESC;'
    cursor.execute(query)
    result = cursor.fetchall()

    row = 1
    col = 1
    for driver in result:
        driver = list(driver)
        drivername = driver[0]
        team = driver[1]
        teamcolor = driver[-1]
        tempcursor = col
        # driver's name
        if team == "Retired":
            leaderboard_full.write(row, tempcursor, drivername, formatter.driverformat["Reserve"])
        else:
            leaderboard_full.write(row, tempcursor, drivername, formatter.driverformat[teamcolor])
        tempcursor += 1

        for r in range(3, 3+race_done):
            position = driver[r]

            pointsformat = workbook.add_format({"font_size":11})
            pointsformat.set_font_name("Dengxian")
            pointsformat.set_align("center")
            pointsformat.set_align("vcenter")
            if position != None:
                if position == 1:
                    pointsformat.set_bg_color("#FFFF00")
                elif position == 2:
                    pointsformat.set_bg_color("#EEECE1")
                elif position == 3:
                    pointsformat.set_bg_color("#FFC000")
                elif position >= 4 and position <= 10:
                    pointsformat.set_bg_color("#00B050")
                elif position > 10:
                    pointsformat.set_bg_color("#538DD5")
                elif position == -1:
                    pointsformat.set_bg_color("#7030A0")
                    position = "RET"
                elif position == -2:
                    pointsformat.set_bg_color("#7030A0")
                    position = "DNF"
                elif position == -3:
                    pointsformat.set_bg_color("#A6A6A6")
                    position = "DNS"
                elif position == -4:
                    pointsformat.set_bg_color("#FF0000")
                    position = "DSQ"
            else:
                position = "DNA"

            leaderboard_full.write(row, tempcursor, position, pointsformat)
            del pointsformat

            tempcursor += 1

        leaderboard_full.write(row, race_count+2, driver[-2], formatter.pointsformat["header"])
        
        row += 1
            






# driver's license point
def get_licensepoint():
    # Setting row width
    licensepoint.set_row(0, 31)
    query = f'SELECT count(*) FROM licensePoint;'
    cursor.execute(query)
    result = cursor.fetchall()
    drivercount = result[0]
    drivercount = list(drivercount)
    drivercount = drivercount[0]
    for pos in range(1,drivercount+1):
        licensepoint.set_row(pos, 18)
        tempcursor = pos
    

    # setting column width
    licensepoint.set_column(0,0, 3)
    licensepoint.set_column(1,1, 21)
    query = "SELECT COUNT(DISTINCT(GP_ENG)) FROM raceCalendar WHERE Round != 0 OR Round != null;"
    cursor.execute(query)
    result = cursor.fetchall()
    result = list(result[0])
    race_count = result[0]
    licensepoint.set_column(2, race_count + 2, 9)

    # writing the header
    licensepoint.write(0,1, "Drvier", formatter.pointsformat["header"])

    # flags of each race
    query = "SELECT DISTINCT(GP_ENG), Round FROM raceCalendar WHERE Round != 0 OR Round != null ORDER BY Round;"
    cursor.execute(query)
    result = cursor.fetchall()
    tempcursor = 2
    for race in result:
        race = list(race)
        race = race[0]
        licensepoint.insert_image(0, tempcursor, ref_dict.flag_dict[race], {'x_scale':0.96, 'y_scale':0.98})
        tempcursor += 1
    licensepoint.write(0, tempcursor, "Points", formatter.pointsformat["header"])


    # retirve driverlist from database and write into the table
    query = "SELECT licensePoint.*, driverList.team, teamList.teamColor \
            FROM licensePoint JOIN driverList ON \
            licensePoint.driverName = driverList.driverName \
                                JOIN teamList ON \
            driverList.team = teamList.teamName \
            WHERE driverList.team != 'Retired' \
            ORDER BY driverList.team ASC, \
                CASE driverList.driverStatus \
                    WHEN '1st driver' THEN 1 \
                    WHEN '2ed driver' THEN 2 \
                    WHEN '3rd driver' THEN 3 \
                    WHEN '4th driver' THEN 4 \
                    ELSE 5 \
                    END, driverList.driverStatus;"
    cursor.execute(query)
    result = cursor.fetchall()

    row = 1
    col = 0
    for driver in result:
        driver = list(driver)
        drivername = driver[0]
        teamcolor = driver[-1]
        licensepoint.write(row, 1, drivername, formatter.driverformat[teamcolor])

        for i in range(2, 2 + race_count):
            licensepoint.write(row, i, driver[i], formatter.pointsformat["header"])
            
            if driver[3+race_count] >= 11:
                rank = "excellent"
            elif driver[3+race_count] >= 7 and driver[3+race_count] <= 10:
                rank = "good"
            elif driver[3+race_count] >= 4 and driver[3+race_count] <= 6:
                rank = "poor"
            elif driver[3+race_count] >= 1 and driver[3+race_count] <= 3:
                rank = "danger"
            else:
                rank = "trigger"
            licensepoint.write(row, 2 + race_count, driver[3+race_count], formatter.licensepointformat[rank])

        row += 1


# LAN username and password
def get_lanusername():
    # setting row width
    cursor.execute("SELECT COUNT(*) FROM afr_s8.LANusername;")
    result = cursor.fetchall()
    drivercount = result[0]
    drivercount = list(drivercount)
    drivercount = drivercount[0]
    for pos in range(1,drivercount+1):
        lanusernamelist.set_row(pos, 15)

    # setting column width
    lanusernamelist.set_column(0,2, 22)

    # write the header
    lanusernamelist.write(0,0, "游戏id", formatter.lanusernameformat["ACTIVE"])
    lanusernamelist.write(0,1, "LAN用户名", formatter.lanusernameformat["ACTIVE"])
    lanusernamelist.write(0,2, "密码", formatter.lanusernameformat["ACTIVE"])

    # retirve driverlist from database and write into the table
    query = "SELECT * FROM LANusername ORDER BY username ASC;"
    cursor.execute(query)
    result = cursor.fetchall()

    row = 1
    col = 0
    for account in result:
        account = list(account)
        status = account[-1]
        for i in range(0,3):
            lanusernamelist.write(row, col+i, account[i], formatter.lanusernameformat[status])
        row += 1


# Season stats
def get_seasonstats():
    # drivername, group, race start, attendance, pole, race win, podium, 
    # points finishing, race finished, race retired, race DNF
    # avg & best start and finishes, total position changed, ......
    # total LP penalty, total quali & race ban, total warning
   

    # get whole driver list
    #  WHERE team != "Retired"
    query = 'SELECT * FROM driverList \
            ORDER BY CASE driverGroup \
                        WHEN "A1" THEN 1 \
                        WHEN "A2" THEN 2 \
                        WHEN "A3" THEN 3 \
                        ELSE 4 END, \
                    CASE team \
                        WHEN "Mercedes AMG" THEN 1 \
                        WHEN "Red Bull Racing" THEN 2 \
                        WHEN "McLaren" THEN 3 \
                        WHEN "Aston Martin" THEN 4 \
                        WHEN "Alpine" THEN 5 \
                        WHEN "Ferrari" THEN 6 \
                        WHEN "Alpha Tauri" THEN 7 \
                        WHEN "Alfa Romeo" THEN 8 \
                        WHEN "Haas" THEN 9 \
                        WHEN "Williams" THEN 10 \
                        WHEN "Reserve" THEN 11 \
                        WHEN "Testing" THEN 12 \
                        WHEN "Team AFR2" THEN 13 \
                        WHEN "Retired" THEN 14 \
                        ELSE 15 END, \
                    CASE driverStatus \
                        WHEN "1st driver" THEN 1 \
                        WHEN "2ed driver" THEN 2 \
                        WHEN "3rd driver" THEN 3 \
                        WHEN "reserved driver" THEN 4 \
                        WHEN "A2 driver" THEN 5 \
                        ELSE 7 END, \
                    joinTime ASC;'
    cursor.execute(query)
    result = cursor.fetchall()


    # writing the header
    for i in range(0,len(result)):
        seasonstats.set_row(i, 16)

    col = 0
    seasonstats.set_column(0, col, 20)
    seasonstats.write(0, 0, "车手", formatter.pointsformat["header"])
    col += 1
    seasonstats.set_column(col, col, 9)
    seasonstats.write(0, col, "组别", formatter.pointsformat["header"])
    col += 1
    seasonstats.set_column(col, col, 9)
    seasonstats.write(0, col, "参赛场次", formatter.pointsformat["header"])
    col += 1
    seasonstats.set_column(col, col, 9)
    seasonstats.write(0, col, "参赛率", formatter.pointsformat["header"])
    col += 1
    seasonstats.set_column(col, col, 9)
    seasonstats.write(0, col, "杆位", formatter.pointsformat["header"])
    col += 1
    seasonstats.set_column(col, col, 9)
    seasonstats.write(0, col, "胜场数", formatter.pointsformat["header"])
    col += 1
    seasonstats.set_column(col, col, 9)
    seasonstats.write(0, col, "领奖台", formatter.pointsformat["header"])
    col += 1
    seasonstats.set_column(col, col, 9)
    seasonstats.write(0, col, "最速圈", formatter.pointsformat["header"])
    col += 1
    seasonstats.set_column(col, col, 9)
    seasonstats.write(0, col, "积分完赛", formatter.pointsformat["header"])
    col += 1
    seasonstats.set_column(col, col, 9)
    seasonstats.write(0, col, "完赛次数", formatter.pointsformat["header"])
    col += 1
    seasonstats.set_column(col, col, 9)
    seasonstats.write(0, col, "退赛次数", formatter.pointsformat["header"])
    col += 1
    seasonstats.set_column(col, col, 11)
    seasonstats.write(0, col, "未完赛次数", formatter.pointsformat["header"])
    col += 1
    seasonstats.set_column(col, col, 9)
    seasonstats.write(0, col, "平均起跑", formatter.pointsformat["header"])
    col += 1
    seasonstats.set_column(col, col, 9)
    seasonstats.write(0, col, "平均完赛", formatter.pointsformat["header"])
    col += 1
    seasonstats.set_column(col, col, 9)
    seasonstats.write(0, col, "最佳起跑", formatter.pointsformat["header"])
    col += 1
    seasonstats.set_column(col, col, 9)
    seasonstats.write(0, col, "最佳完赛", formatter.pointsformat["header"])
    col += 1
    seasonstats.set_column(col, col, 9)
    seasonstats.write(0, col, "位置变化", formatter.pointsformat["header"])
    col += 1
    seasonstats.set_column(col, col, 11)
    seasonstats.write(0, col, "驾照分扣分", formatter.pointsformat["header"])
    col += 1
    seasonstats.set_column(col, col, 11)
    seasonstats.write(0, col, "禁排位数", formatter.pointsformat["header"])
    col += 1
    seasonstats.set_column(col, col, 9)
    seasonstats.write(0, col, "禁赛数", formatter.pointsformat["header"])
    col += 1
    seasonstats.set_column(col, col, 9)
    seasonstats.write(0, col, "警告数", formatter.pointsformat["header"])
    col += 1
    seasonstats.set_column(col, col, 9)
    seasonstats.write(0, col, "", formatter.pointsformat["header"])

    # analyse stats
    row = 1
    for driver in result:
        col = 0
        drivername = driver[0]
        driverteam = driver[1]
        drivergroup = driver[2]

        if drivername == "Race Director":
            continue


        # driver name and driver group
        if driverteam == "Reserve":
            seasonstats.write(row, col, drivername, formatter.default["Reserve"])
        elif driverteam == "Testing":
            seasonstats.write(row, col, drivername, formatter.default["Testing"])
        elif driverteam == "Failed":
            seasonstats.write(row, col, drivername, formatter.default["Failed"])
        elif driverteam == "Retired":
            seasonstats.write(row, col, drivername, formatter.default["Retired"])
        else:
            seasonstats.write(row, col, drivername, formatter.driverformat[driverteam])
        col += 1

        seasonstats.write(row, col, drivergroup, formatter.pointsformat["header"])
        col += 1
        

        # race finished until now
        query = f'SELECT COUNT(*) FROM raceCalendar WHERE driverGroup = "{drivergroup}" AND raceStatus = "FINISHED";'
        cursor.execute(query)
        result = cursor.fetchall()

        racecount = result[0][0]

        # race start and attendance
        query = f'SELECT COUNT(*) FROM raceResult WHERE driverName = "{drivername}" and driverGroup = "{drivergroup}";'
        cursor.execute(query)
        result = cursor.fetchall()

        raceattend = result[0][0]
        attendace = f'{raceattend / racecount * 100 :.2f}%'

        seasonstats.write(row, col, raceattend, formatter.pointsformat["header"])
        col += 1
        seasonstats.write(row, col, attendace, formatter.pointsformat["header"])
        col += 1

        
        # pole position
        query = f'SELECT COUNT(*) FROM raceResult WHERE startposition = 1 AND driverName = "{drivername}" AND driverGroup = "{drivergroup}";'
        cursor.execute(query)
        result = cursor.fetchall()

        polecount = result[0][0]

        seasonstats.write(row, col, polecount, formatter.pointsformat["header"])
        col += 1


        # race win
        query = f'SELECT COUNT(*) FROM raceResult WHERE finishPosition = 1 AND driverName = "{drivername}" AND driverGroup = "{drivergroup}";'
        cursor.execute(query)
        result = cursor.fetchall()

        racewincount = result[0][0]

        seasonstats.write(row, col, racewincount, formatter.pointsformat["header"])
        col += 1


        # podium
        query = f'SELECT COUNT(*) FROM raceResult WHERE finishPosition <= 3 AND driverName = "{drivername}" AND driverGroup = "{drivergroup}";'
        cursor.execute(query)
        result = cursor.fetchall()

        podiumcount = result[0][0]

        seasonstats.write(row, col, podiumcount, formatter.pointsformat["header"])
        col += 1


        # fastest lap
        query = f'SELECT COUNT(*) FROM qualiraceFL WHERE driverGroup = "{drivergroup}" AND raceFLdriver = "{drivername}";'
        cursor.execute(query)
        result = cursor.fetchall()

        flcount = result[0][0]

        seasonstats.write(row, col, flcount, formatter.pointsformat["header"])
        col += 1


        # points finishing
        query = f'SELECT COUNT(*) FROM raceResult WHERE finishPosition <= 10 AND driverName = "{drivername}" AND driverGroup = "{drivergroup}";'
        cursor.execute(query)
        result = cursor.fetchall()

        ptsfinishingcount = result[0][0]

        seasonstats.write(row, col, ptsfinishingcount, formatter.pointsformat["header"])
        col += 1


        # race finished
        query = f'SELECT COUNT(*) FROM raceResult WHERE driverStatus = "FINISHED" AND driverName = "{drivername}" AND driverGroup = "{drivergroup}";'
        cursor.execute(query)
        result = cursor.fetchall()

        racefinishedcount = result[0][0]

        seasonstats.write(row, col, racefinishedcount, formatter.pointsformat["header"])
        col += 1


        # race retired
        query = f'SELECT COUNT(*) FROM raceResult WHERE driverStatus = "RETIRED" AND driverName = "{drivername}" AND driverGroup = "{drivergroup}";'
        cursor.execute(query)
        result = cursor.fetchall()

        raceretcount = result[0][0]

        seasonstats.write(row, col, raceretcount, formatter.pointsformat["header"])
        col += 1


        # race DNF
        query = f'SELECT COUNT(*) FROM raceResult WHERE driverStatus != "FINISHED" AND driverName = "{drivername}" AND driverGroup = "{drivergroup}";'
        cursor.execute(query)
        result = cursor.fetchall()

        racednfcount = result[0][0]

        seasonstats.write(row, col, racednfcount, formatter.pointsformat["header"])
        col += 1


        # average start and finished position 
        # best start and finished position
        # and total position changed
        query = f'SELECT startPosition, finishPosition FROM raceResult WHERE driverName = "{drivername}" AND driverGroup = "{drivergroup}";'
        cursor.execute(query)
        result = cursor.fetchall()

        startpos = []
        finishpos = []
        totalpc = 0
        for race in result:
            startpos.append(race[0])
            finishpos.append(race[1])
            totalpc += race[1] - race[0]

        try:
            avgstartpos = f'{sum(startpos) / len(startpos):.2f}'
        except ZeroDivisionError:
            avgstartpos = "null"

        try:
            avgfinishpos = f'{sum(finishpos) / len(finishpos):.2f}'
        except ZeroDivisionError:
            avgfinishpos = "null"

        try:
            beststart = min(startpos)
        except:
            beststart = "null"

        try:
            bestfinish = min(finishpos)
        except:
            bestfinish = "null"

        seasonstats.write(row, col, avgstartpos, formatter.pointsformat["header"])
        col += 1
        seasonstats.write(row, col, avgfinishpos, formatter.pointsformat["header"])
        col += 1
        seasonstats.write(row, col, beststart, formatter.pointsformat["header"])
        col += 1
        seasonstats.write(row, col, bestfinish, formatter.pointsformat["header"])
        col += 1
        seasonstats.write(row, col, totalpc, formatter.pointsformat["header"])
        col += 1


        # total LP penalty, total quali & race ban, total warning
        query = f'SELECT penaltyLP, penaltyWarning, qualiBan, raceBan FROM raceDirector \
                WHERE driverName = "{drivername}" AND driverGroup = "{drivergroup}";'
        cursor.execute(query)
        result = cursor.fetchall()

        penaltyLP = 0
        penaltywarning = 0
        qualiban = 0
        raceban = 0
        for record in result:
            # record[0] = penaltyLP
            if record[0] < 0:
                penaltyLP += record[0]
            
            # record[1] = penaltyWarning
            if record[1] > 0:
                penaltywarning += record[1]

            # record[2] = qualiban
            if record[2] > 0:
                qualiban += record[2]
            
            # record[3] = raceban
            if record[3] > 0:
                raceban += record[3]

        penaltyLP = abs(penaltyLP)

        seasonstats.write(row, col, penaltyLP, formatter.pointsformat["header"])
        col += 1
        seasonstats.write(row, col, qualiban, formatter.pointsformat["header"])
        col += 1
        seasonstats.write(row, col, raceban, formatter.pointsformat["header"])
        col += 1
        seasonstats.write(row, col, penaltywarning, formatter.pointsformat["header"])
        col += 1

        row += 1


# Race Director details
def get_racedirector():
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
    racedirector.set_column(3,3, 5)
    racedirector.set_column(4,4, 12)
    racedirector.set_column(5,5, 40)
    racedirector.set_column(6,6, 7)
    racedirector.set_column(7,7, 5)
    racedirector.set_column(8,8, 7)
    racedirector.set_column(9,9, 5)
    racedirector.set_column(10,10, 70)

    # write the header
    racedirector.write(0,0, "案件编号", formatter.racedirector["header"])
    racedirector.write(0,1, "日期", formatter.racedirector["header"])
    racedirector.write(0,2, "车手", formatter.racedirector["header"])
    racedirector.write(0,3, "组别", formatter.racedirector["header"])
    racedirector.write(0,4, "比赛", formatter.racedirector["header"])
    racedirector.write(0,5, "处罚", formatter.racedirector["header"])
    racedirector.write(0,6, "驾照分", formatter.racedirector["header"])
    racedirector.write(0,7, "警告", formatter.racedirector["header"])
    racedirector.write(0,8, "禁排位", formatter.racedirector["header"])
    racedirector.write(0,9, "禁赛", formatter.racedirector["header"])
    racedirector.write(0,10, "大致描述", formatter.racedirector["header"])


    
    row = 1
    for incidents in result:
        racedirector.write(row, 0, incidents[0], formatter.racedirector["default"])
        racedirector.write(row, 1, incidents[1], formatter.racedirector["date"])
        racedirector.write(row, 2, incidents[2], formatter.racedirector["default"])
        racedirector.write(row, 3, incidents[3], formatter.racedirector["default"])
        racedirector.write(row, 4, incidents[4], formatter.racedirector["default"])
        racedirector.write(row, 5, incidents[5], formatter.racedirector["default"])
        racedirector.write(row, 6, incidents[6], formatter.racedirector["default"])
        racedirector.write(row, 7, incidents[7], formatter.racedirector["default"])
        racedirector.write(row, 8, incidents[8], formatter.racedirector["default"])
        racedirector.write(row, 9, incidents[9], formatter.racedirector["default"])
        racedirector.write(row, 10, incidents[10], formatter.racedirector["default"])
        row += 1


def main():
    get_driverlist()
    get_racecalendar()
    get_leaderboard_short()
    get_leaderboard_constructors()
    get_leaderboard_full()
    get_licensepoint()
    # get_seasonstats()
    get_racedirector()
    workbook.close()

main()