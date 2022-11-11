from datetime import datetime
import xlsxwriter
import connectserver as connector

db = connector.connectserver()
cursor = db.cursor()

gp_dict = {
    "AUS": "Australia",
    "BHR": "Bahrain",
    "VNM": "Vietnam",
    "CHN": "China",
    "NLD": "Netherlands",
    "ESP": "Spain",
    "MCO": "Monaco",
    "AZE": "Azerbaijan",
    "CAN": "Canada",
    "FRA": "France",
    "AUT": "Austria",
    "GBR": "Britain",
    "HUN": "Hungary",
    "BEL": "Belgium",
    "ITA": "Italy",
    "SGP": "Singapore",
    "RUS": "Russia",
    "JPN": "Japan",
    "USA": "USA",
    "MEX": "Mexico",
    "BRA": "Brazil",
    "UAE": "Abu Dahbi"
}
def get_key(my_dict, val):
    for key, value in my_dict.items():
        if val == value:
            return key
    return "key doesn't exist"

today = datetime.today().strftime('%Y-%m-%d')
query = f'SELECT GP_CHN, raceDate FROM raceCalendar \
        WHERE raceDate <= "{today}" \
        ORDER BY raceDate DESC;'
cursor.execute(query)
result = cursor.fetchall()
result = list(result[0])
race_name = result[0]
date_name = result[1].strftime('%m.%d')



# create and open the excel file
workbook = xlsxwriter.Workbook(f'AFR S7【{date_name}】{race_name}.xlsx')
driverlist = workbook.add_worksheet("车手名单")
racecalendar = workbook.add_worksheet("赛程安排")
signup = workbook.add_worksheet("参赛名单")
a1leaderboard = workbook.add_worksheet("A1积分榜")
a1leaderboard_cons = workbook.add_worksheet("A1车队积分榜")
a1leaderboard_full = workbook.add_worksheet("A1总积分榜")
a2leaderboard = workbook.add_worksheet("A2积分榜")
a2leaderboard_cons = workbook.add_worksheet("A2车队积分榜")
a2leaderboard_full = workbook.add_worksheet("A2总积分榜")
licensepoint = workbook.add_worksheet("车手安全分")
lanusernamelist = workbook.add_worksheet("LAN name")


# format use across whole table
driverformat = {}
mercedesf = workbook.add_format({"font_size":11})
mercedesf.set_bg_color("#33CCCC")
mercedesf.set_font_name("Dengxian")
mercedesf.set_align("vcenter")
driverformat["Mercedes AMG"] = mercedesf
ferrarif = workbook.add_format({"font_size":11})
ferrarif.set_bg_color("FF0000")
ferrarif.set_font_name("Dengxian")
ferrarif.set_align("vcenter")
driverformat["Ferrari"] = ferrarif
redbullf = workbook.add_format({"font_size":11})
redbullf.set_bg_color("#0070C0")
redbullf.set_font_name("Dengxian")
redbullf.set_align("vcenter")
driverformat["Red Bull Racing"] = redbullf
mclarenf = workbook.add_format({"font_size":11})
mclarenf.set_bg_color("#FFC000")
mclarenf.set_font_name("Dengxian")
mclarenf.set_align("vcenter")
driverformat["McLaren"] = mclarenf
racingpointf = workbook.add_format({"font_size":11})
racingpointf.set_bg_color("#006633")
racingpointf.set_font_name("Dengxian")
racingpointf.set_align("vcenter")
driverformat["Racing Point"] = racingpointf
renaultf = workbook.add_format({"font_size":11})
renaultf.set_bg_color("#FFFF00")
renaultf.set_font_name("Dengxian")
renaultf.set_align("vcenter")
driverformat["Renault"] = renaultf
alphataurif = workbook.add_format({"font_size":11})
alphataurif.set_bg_color("#00B0F0")
alphataurif.set_font_name("Dengxian")
alphataurif.set_align("vcenter")
driverformat["Alpha Tauri"] = alphataurif
alfaromeof = workbook.add_format({"font_size":11})
alfaromeof.set_bg_color("#800000")
alfaromeof.set_font_name("Dengxian")
alfaromeof.set_align("vcenter")
driverformat["Alfa Romeo"] = alfaromeof
williamsf = workbook.add_format({"font_size":11})
williamsf.set_bg_color("#666699")
williamsf.set_font_name("Dengxian")
williamsf.set_align("vcenter")
driverformat["Williams"] = williamsf
haasf = workbook.add_format({"font_size":11})
haasf.set_bg_color("BFBFBF")
haasf.set_font_name("Dengxian")
haasf.set_align("vcenter")
driverformat["Haas"] = haasf
reservef = workbook.add_format({"font_size":11})
reservef.set_font_name("Dengxian")
reservef.set_align("vcenter")
reservef.set_bg_color("#000000")
reservef.set_font_color("#FFFFFF")
driverformat["Reserve"] = reservef
teamafr2f = workbook.add_format({"font_size":11})
teamafr2f.set_font_name("Dengxian")
teamafr2f.set_align("vcenter")
teamafr2f.set_bg_color("#E26B0A")
driverformat["Team AFR2"] = teamafr2f
teamafr3f = workbook.add_format({"font_size":11})
teamafr3f.set_font_name("Dengxian")
teamafr3f.set_align("vcenter")
teamafr3f.set_bg_color("#00FF00")
driverformat["Team AFR3"] = teamafr3f

teamformat = {}
mercedesf = workbook.add_format({"font_size":11})
mercedesf.set_bg_color("#33CCCC")
mercedesf.set_font_name("Dengxian")
mercedesf.set_align("vcenter")
mercedesf.set_bold(True)
teamformat["Mercedes AMG"] = mercedesf
ferrarif = workbook.add_format({"font_size":11})
ferrarif.set_bg_color("FF0000")
ferrarif.set_font_name("Dengxian")
ferrarif.set_align("vcenter")
ferrarif.set_bold(True)
teamformat["Ferrari"] = ferrarif
redbullf = workbook.add_format({"font_size":11})
redbullf.set_bg_color("#0070C0")
redbullf.set_font_name("Dengxian")
redbullf.set_align("vcenter")
redbullf.set_bold(True)
teamformat["Red Bull Racing"] = redbullf
mclarenf = workbook.add_format({"font_size":11})
mclarenf.set_bg_color("#FFC000")
mclarenf.set_font_name("Dengxian")
mclarenf.set_align("vcenter")
mclarenf.set_bold(True)
teamformat["McLaren"] = mclarenf
racingpointf = workbook.add_format({"font_size":11})
racingpointf.set_bg_color("#006633")
racingpointf.set_font_name("Dengxian")
racingpointf.set_align("vcenter")
racingpointf.set_bold(True)
teamformat["Racing Point"] = racingpointf
renaultf = workbook.add_format({"font_size":11})
renaultf.set_bg_color("#FFFF00")
renaultf.set_font_name("Dengxian")
renaultf.set_align("vcenter")
renaultf.set_bold(True)
teamformat["Renault"] = renaultf
alphataurif = workbook.add_format({"font_size":11})
alphataurif.set_bg_color("#00B0F0")
alphataurif.set_font_name("Dengxian")
alphataurif.set_align("vcenter")
alphataurif.set_bold(True)
teamformat["Alpha Tauri"] = alphataurif
alfaromeof = workbook.add_format({"font_size":11})
alfaromeof.set_bg_color("#800000")
alfaromeof.set_font_name("Dengxian")
alfaromeof.set_align("vcenter")
alfaromeof.set_bold(True)
teamformat["Alfa Romeo"] = alfaromeof
williamsf = workbook.add_format({"font_size":11})
williamsf.set_bg_color("#666699")
williamsf.set_font_name("Dengxian")
williamsf.set_align("vcenter")
williamsf.set_bold(True)
teamformat["Williams"] = williamsf
haasf = workbook.add_format({"font_size":11})
haasf.set_bg_color("BFBFBF")
haasf.set_font_name("Dengxian")
haasf.set_align("vcenter")
haasf.set_bold(True)
teamformat["Haas"] = haasf
reservef = workbook.add_format({"font_size":11})
reservef.set_font_name("Dengxian")
reservef.set_align("vcenter")
reservef.set_bg_color("#000000")
reservef.set_font_color("#FFFFFF")
reservef.set_bold(True)
teamformat["Reserve"] = reservef
teamafr2f = workbook.add_format({"font_size":11})
teamafr2f.set_font_name("Dengxian")
teamafr2f.set_align("vcenter")
teamafr2f.set_bg_color("#E26B0A")
teamafr2f.set_bold(True)
teamformat["Team AFR2"] = teamafr2f
teamafr3f = workbook.add_format({"font_size":11})
teamafr3f.set_font_name("Dengxian")
teamafr3f.set_align("vcenter")
teamafr3f.set_bg_color("#00FF00")
teamafr3f.set_bold(True)
teamformat["Team AFR3"] = teamafr3f

pointsformat = {}
headerf = workbook.add_format({"font_size":11})
headerf.set_font_name("Dengxian")
headerf.set_align("center")
headerf.set_align("vcenter")
pointsformat["header"] = headerf
p1 = workbook.add_format({"font_size":11})
p1.set_font_name("Dengxian")
p1.set_align("center")
p1.set_align("vcenter")
p1.set_bg_color("#FFFF00")
pointsformat["p1"] = p1
p2 = workbook.add_format({"font_size":11})
p2.set_font_name("Dengxian")
p2.set_align("center")
p2.set_align("vcenter")
p2.set_bg_color("#EEECE1")
pointsformat["p2"] = p2
p3 = workbook.add_format({"font_size":11})
p3.set_font_name("Dengxian")
p3.set_align("center")
p3.set_align("vcenter")
p3.set_bg_color("#FFC000")
pointsformat["p3"] = p3
points = workbook.add_format({"font_size":11})
points.set_font_name("Dengxian")
points.set_align("center")
points.set_align("vcenter")
points.set_bg_color("#00B050")
pointsformat["points"] = points
outpoint = workbook.add_format({"font_size":11})
outpoint.set_font_name("Dengxian")
outpoint.set_align("center")
outpoint.set_align("vcenter")
outpoint.set_bg_color("#538DD5")
pointsformat["outpoint"] = outpoint
retired = workbook.add_format({"font_size":11})
retired.set_font_name("Dengxian")
retired.set_align("center")
retired.set_align("vcenter")
retired.set_bg_color("#7030A0")
pointsformat["retired"] = retired
dns = workbook.add_format({"font_size":11})
dns.set_font_name("Dengxian")
dns.set_align("center")
dns.set_align("vcenter")
dns.set_bg_color("#A6A6A6")
pointsformat["dns"] = dns
dsq = workbook.add_format({"font_size":11})
dsq.set_font_name("Dengxian")
dsq.set_align("center")
dsq.set_align("vcenter")
dsq.set_bg_color("#FF0000")
pointsformat["dsq"] = dsq
dna = workbook.add_format({"font_size":11})
dna.set_font_name("Dengxian")
dna.set_align("center")
dna.set_align("vcenter")
pointsformat["dna"] = dna

licensepointformat = {}
# excellent 11-12
excellentf = workbook.add_format({"font_size":11})
excellentf.set_font_name("Dengxian")
excellentf.set_align("center")
excellentf.set_align("vcenter")
excellentf.set_bg_color("#00FF00")
licensepointformat["excellent"] = excellentf
# good 7-10
goodf = workbook.add_format({"font_size":11})
goodf.set_font_name("Dengxian")
goodf.set_align("center")
goodf.set_align("vcenter")
goodf.set_bg_color("#92D050")
licensepointformat["good"] = goodf
# poor 4-6
poorf = workbook.add_format({"font_size":11})
poorf.set_font_name("Dengxian")
poorf.set_align("center")
poorf.set_align("vcenter")
poorf.set_bg_color("#FFFF00")
licensepointformat["poor"] = poorf
# danger 1-3
dangerf = workbook.add_format({"font_size":11})
dangerf.set_font_name("Dengxian")
dangerf.set_align("center")
dangerf.set_align("vcenter")
dangerf.set_bg_color("#FF0000")
licensepointformat["danger"] = dangerf
# trigger 0
triggerf = workbook.add_format({"font_size":11})
triggerf.set_font_name("Dengxian")
triggerf.set_align("center")
triggerf.set_align("vcenter")
triggerf.set_bg_color("#000000")
triggerf.set_font_color("#FFFFFF")
licensepointformat["trigger"] = triggerf



# Driver list worksheet
def get_driverlist():
    # Setting column and row width
    for i in range(0,100):
        driverlist.set_row(i, 16)
    driverlist.set_column(0,0, 15)
    driverlist.set_column(1,1, 20)
    driverlist.set_column(2,2, 3)
    driverlist.set_column(3,4, 20)
    driverlist.set_column(5,5, 3)
    driverlist.set_column(6,6, 15)
    driverlist.set_column(7,7, 20)
    driverlist.set_column(8,8, 3)
    driverlist.set_column(9,10, 20)
    driverlist.set_column(11,11, 3)
    driverlist.set_column(12,13, 20)

    # Setting format
    teamformat = []
    groupf = workbook.add_format({"font_size":12})
    groupf.set_font_name("Dengxian")
    groupf.set_align("center")
    groupf.set_align("vcenter")
    mercedesf = workbook.add_format({"font_size":11})
    mercedesf.set_bg_color("#33CCCC")
    mercedesf.set_font_name("Dengxian")
    mercedesf.set_align("vcenter")
    teamformat.append(mercedesf)
    ferrarif = workbook.add_format({"font_size":11})
    ferrarif.set_bg_color("FF0000")
    ferrarif.set_font_name("Dengxian")
    ferrarif.set_align("vcenter")
    teamformat.append(ferrarif)
    redbullf = workbook.add_format({"font_size":11})
    redbullf.set_bg_color("#0070C0")
    redbullf.set_font_name("Dengxian")
    redbullf.set_align("vcenter")
    teamformat.append(redbullf)
    mclarenf = workbook.add_format({"font_size":11})
    mclarenf.set_bg_color("#FFC000")
    mclarenf.set_font_name("Dengxian")
    mclarenf.set_align("vcenter")
    teamformat.append(mclarenf)
    racingpointf = workbook.add_format({"font_size":11})
    racingpointf.set_bg_color("#006633")
    racingpointf.set_font_name("Dengxian")
    racingpointf.set_align("vcenter")
    teamformat.append(racingpointf)
    renaultf = workbook.add_format({"font_size":11})
    renaultf.set_bg_color("#FFFF00")
    renaultf.set_font_name("Dengxian")
    renaultf.set_align("vcenter")
    teamformat.append(renaultf)
    alphataurif = workbook.add_format({"font_size":11})
    alphataurif.set_bg_color("#00B0F0")
    alphataurif.set_font_name("Dengxian")
    alphataurif.set_align("vcenter")
    teamformat.append(alphataurif)
    alfaromeof = workbook.add_format({"font_size":11})
    alfaromeof.set_bg_color("#800000")
    alfaromeof.set_font_name("Dengxian")
    alfaromeof.set_align("vcenter")
    teamformat.append(alfaromeof)
    williamsf = workbook.add_format({"font_size":11})
    williamsf.set_bg_color("#666699")
    williamsf.set_font_name("Dengxian")
    williamsf.set_align("vcenter")
    teamformat.append(williamsf)
    haasf = workbook.add_format({"font_size":11})
    haasf.set_bg_color("BFBFBF")
    haasf.set_font_name("Dengxian")
    haasf.set_align("vcenter")
    teamformat.append(haasf)
    reservef = workbook.add_format({"font_size":11})
    reservef.set_font_name("Dengxian")
    reservef.set_align("vcenter")
    teamformat.append(reservef)
    testingf = workbook.add_format({"font_size":11})
    testingf.set_font_name("Dengxian")
    testingf.set_bg_color("#00CC00")
    testingf.set_align("vcenter")
    teamformat.append(testingf)
    failtestingf = workbook.add_format({"font_size":11})
    failtestingf.set_font_name("Dengxian")
    failtestingf.set_bg_color("#974706")
    failtestingf.set_align("vcenter")
    teamformat.append(failtestingf)
    retiredf = workbook.add_format({"font_size":11})
    retiredf.set_font_name("Dengxian")
    retiredf.set_bg_color("#000000")
    retiredf.set_font_color("#FFFFFF")
    retiredf.set_align("vcenter")
    teamformat.append(retiredf)


    # write the title
    driverlist.merge_range("A1:B1", "A1", groupf)
    driverlist.merge_range("G1:H1", "A2", groupf)
    driverlist.write("D1", "Reserve", reservef)
    driverlist.write("J1", "Reserve", reservef)
    driverlist.write("M1", "A3", reservef)
    driverlist.write("N1", "Testing", reservef)
    
    # write pre-built table
    teamname_CHN = ["梅赛德斯AMG", "法拉利", "红牛", "迈凯伦", "赛点",
                    "雷诺", "阿尔法图里", "阿尔法罗密欧", "威廉姆斯", "哈斯",
                    "替补", "测试", "测试不及格"]
    teamname_ENG = ["Mercedes AMG", "Ferrari", "Red Bull Racing", "McLaren",
                    "Racing Point", "Renault", "Alpha Tauri", "Alfa Romeo",
                    "Williams", "Haas", "Reserve", "Testing", "Failed", "Retired"]
    a1row = 1
    a1col = 0
    a2row = 1
    a2col = 6
    for i in range(0, 10):
        driverlist.write(a1row, a1col, teamname_CHN[i], teamformat[i])
        driverlist.write(a1row+1, a1col, teamname_ENG[i], teamformat[i])
        driverlist.write(a1row+2, a1col, "", teamformat[i])
        driverlist.write(a1row, a1col+1, "", teamformat[i])
        driverlist.write(a1row+1, a1col+1, "", teamformat[i])
        driverlist.write(a1row+2, a1col+1, "", teamformat[i])
        driverlist.write(a2row, a2col, teamname_CHN[i], teamformat[i])
        driverlist.write(a2row+1, a2col, teamname_ENG[i], teamformat[i])
        driverlist.write(a2row+2, a2col, "", teamformat[i])
        driverlist.write(a2row, a2col+1, "", teamformat[i])
        driverlist.write(a2row+1, a2col+1, "", teamformat[i])
        driverlist.write(a2row+2, a2col+1, "", teamformat[i])
        a1row += 3
        a2row += 3

    # retirve driverlist from database and write into the table
    a1row = 1
    a1col = 1
    a2row = 1
    a2col = 7
    # formal driver
    for i in range(0,10):
        query = f'SELECT driverName, team, driverGroup \
                FROM afr_s7.driverList \
                WHERE driverGroup = "A1" and team = "{teamname_ENG[i]}" \
                ORDER BY driverStatus;'
        cursor.execute(query)
        result = cursor.fetchall()

        tempcursor = a1row
        for d in result:
            d = list(d)
            driverlist.write(tempcursor, a1col, d[0], teamformat[i])
            tempcursor += 1
        a1row +=3

        query = f'SELECT driverName, team, driverGroup \
                FROM afr_s7.driverList \
                WHERE driverGroup = "A2" and team = "{teamname_ENG[i]}" \
                ORDER BY driverStatus;'
        cursor.execute(query)
        result = cursor.fetchall()

        tempcursor = a2row
        for d in result:
            d = list(d)
            driverlist.write(tempcursor, a2col, d[0], teamformat[i])
            tempcursor += 1
        
        a2row += 3

    # reserve driver
    a1row = 1
    a1col = 3
    a2row = 1
    a2col = 9
    a3row = 1
    a3col = 12
    
    query = f'SELECT driverName, team, driverGroup \
            FROM afr_s7.driverList \
            WHERE driverGroup = "A1" and team = "{teamname_ENG[10]}" \
            ORDER BY joinTime;'
    cursor.execute(query)
    result = cursor.fetchall()

    tempcursor = a1row
    for d in result:
        d = list(d)
        driverlist.write(tempcursor, a1col, d[0], teamformat[10])
        if tempcursor == 31:
            tempcursor = a1row
            a1col += 1
        else:
            tempcursor += 1

    query = f'SELECT driverName, team, driverGroup \
            FROM afr_s7.driverList \
            WHERE driverGroup = "A1" and team = "{teamname_ENG[13]}" \
            ORDER BY joinTime;'
    cursor.execute(query)
    result = cursor.fetchall()

    for d in result:
        d = list(d)
        driverlist.write(tempcursor, a1col, d[0], teamformat[13])
        if tempcursor == 31:
            tempcursor = a1row
            a1col += 1
        else:
            tempcursor += 1


    query = f'SELECT driverName, team, driverGroup \
            FROM afr_s7.driverList \
            WHERE driverGroup = "A2" and team = "{teamname_ENG[10]}" \
            ORDER BY joinTime;'
    cursor.execute(query)
    result = cursor.fetchall()

    tempcursor = a2row
    for d in result:
        d = list(d)
        driverlist.write(tempcursor, a2col, d[0], teamformat[10])
        if tempcursor == 31:
            tempcursor = a2row
            a2col += 1
        else:
            tempcursor += 1
    
    query = f'SELECT driverName, team, driverGroup \
            FROM afr_s7.driverList \
            WHERE driverGroup = "A2" and team = "{teamname_ENG[13]}" \
            ORDER BY joinTime;'
    cursor.execute(query)
    result = cursor.fetchall()

    for d in result:
        d = list(d)
        driverlist.write(tempcursor, a2col, d[0], teamformat[13])
        if tempcursor == 21:
            tempcursor = a2row
            a2col += 1
        else:
            tempcursor += 1


    query = f'SELECT driverName, team, driverGroup \
            FROM afr_s7.driverList \
            WHERE driverGroup = "A3" and team = "{teamname_ENG[10]}" \
            ORDER BY joinTime;'
    cursor.execute(query)
    result = cursor.fetchall()

    tempcursor = a3row
    for d in result:
        d = list(d)
        driverlist.write(tempcursor, a3col, d[0], teamformat[10])
        tempcursor += 1


    # testing driver
    trow = 1
    tcol = 13

    query = f'SELECT driverName, team, driverGroup, driverStatus \
            FROM afr_s7.driverList \
            WHERE driverGroup = "A3" and \
            (team = "{teamname_ENG[11]}" or team = "{teamname_ENG[12]}") \
            ORDER BY joinTime, \
                CASE driverStatus \
                    WHEN "testing driver" THEN 1 \
                    WHEN "testing fail" THEN 2 \
                    ELSE 3 \
                    END, driverStatus;'
    cursor.execute(query)
    result = cursor.fetchall()

    tempcursor = trow
    for d in result:
        d = list(d)
        if d[3] == "testing driver":
            driverlist.write(tempcursor, tcol, d[0], teamformat[11])
        elif d[3] == "testing fail":
            driverlist.write(tempcursor, tcol, d[0], teamformat[12])
        tempcursor += 1
    
    query = f'SELECT driverName, team, driverGroup \
            FROM afr_s7.driverList \
            WHERE driverGroup = "A3" and team = "{teamname_ENG[13]}" \
            ORDER BY joinTime;'
    cursor.execute(query)
    result = cursor.fetchall()

    tempcursor = a3row
    for d in result:
        d = list(d)
        driverlist.write(tempcursor, a3col, d[0], teamformat[13])
        tempcursor += 1


    # write the sign up table btw 
    # (only one table, just for modelling, not for recording data)
    signup.set_column(0,1, 15)
    for i in range(0,22):
        signup.set_row(i, 15)
    
    signup.merge_range("A1:B1", "A1", pointsformat["header"])
    a1row = 1
    a1col = 0
    for i in range(0, 10):
        signup.write(a1row, a1col, teamname_CHN[i], teamformat[i])
        signup.write(a1row+1, a1col, teamname_ENG[i], teamformat[i])
        a1row += 2
    signup.write(21, 0, "OB", teamformat[10])
    

# Race Calender worksheet
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
    for i in range(1,24):
        racecalendar.set_row(i, 31)

    # define some useful formatter
    racefinishdatef = workbook.add_format({"num_format": "yyyy/m/dd"})
    racefinishdatef.set_font_size("16")
    racefinishdatef.set_align("center")
    racefinishdatef.set_align("vcenter")
    racefinishdatef.set_font_name("黑体")
    racefinishdatef.set_bg_color("#00FF00")
    racecanceldatef = workbook.add_format({"num_format": "yyyy/m/dd"})
    racecanceldatef.set_font_size("16")
    racecanceldatef.set_align("center")
    racecanceldatef.set_align("vcenter")
    racecanceldatef.set_font_name("黑体")
    racecanceldatef.set_bg_color("#000000")
    racecanceldatef.set_font_color("#FFFFFF")
    raceongoingdatef = workbook.add_format({"num_format": "yyyy/m/dd"})
    raceongoingdatef.set_font_size("16")
    raceongoingdatef.set_align("center")
    raceongoingdatef.set_align("vcenter")
    raceongoingdatef.set_font_name("黑体")
    raceongoingdatef.set_bg_color("#538DD5")
    RCdatef = workbook.add_format({"num_format": "yyyy/m/dd"})
    RCdatef.set_font_size("16")
    RCdatef.set_align("center")
    RCdatef.set_align("vcenter")
    RCdatef.set_font_name("黑体")
    RCHformat = workbook.add_format({"font_size":26})
    RCHformat.set_font_name("Dengxian")
    RCHformat.set_bold()
    RCHformat.set_align("center")
    RCHformat.set_align("vcenter")
    RCformat16 = workbook.add_format({"font_size":16})
    RCformat16.set_align("center")
    RCformat16.set_align("vcenter")
    RCformat16.set_font_name("黑体")
    racefinishedf = workbook.add_format({"font_size":16})
    racefinishedf.set_align("center")
    racefinishedf.set_align("vcenter")
    racefinishedf.set_font_name("黑体")
    racefinishedf.set_bg_color("#00FF00")
    racecancelf = workbook.add_format({"font_size":16})
    racecancelf.set_align("center")
    racecancelf.set_align("vcenter")
    racecancelf.set_font_name("黑体")
    racecancelf.set_bg_color("#000000")
    racecancelf.set_font_color("#FFFFFF")
    raceongoingf = workbook.add_format({"font_size":16})
    raceongoingf.set_align("center")
    raceongoingf.set_align("vcenter")
    raceongoingf.set_font_name("黑体")
    raceongoingf.set_font_color("#3399FF")

    # Creating the header
    racecalendar.merge_range("A1:C1", "S7 - A1", RCHformat)
    racecalendar.merge_range("E1:G1", "S7 - A2", RCHformat)
    racecalendar.merge_range("I1:K1", "S7 - A3", RCHformat)
    racecalendar.write("A2", "日期", RCformat16)
    racecalendar.write("B2", "分站", RCformat16)
    racecalendar.write("C2", "天气", RCformat16)
    racecalendar.write("E2", "日期", RCformat16)
    racecalendar.write("F2", "分站", RCformat16)
    racecalendar.write("G2", "天气", RCformat16)
    racecalendar.write("I2", "日期", RCformat16)
    racecalendar.write("J2", "分站", RCformat16)
    racecalendar.write("K2", "天气", RCformat16)

    
    # retirve driverlist from database and write into the table
    query = "SELECT raceDate, GP_CHN, driverGroup, raceStatus \
            FROM raceCalendar;"
    cursor.execute(query)
    result = cursor.fetchall()

    a1row = 2
    a1col = 0
    a2row = 2
    a2col = 4
    a3row = 2
    a3col = 8
    for row in result:
        r = list(row)
        racedate = r[0]
        gp = r[1]
        weather = "动态"
        group = r[2]
        status = r[3]
        if group == "A1":
            if status == "FINISHED":
                racecalendar.write(a1row, a1col, racedate, racefinishdatef)
                racecalendar.write(a1row, a1col+1, gp, racefinishedf)
                racecalendar.write(a1row, a1col+2, weather, racefinishedf)                
            elif status == "CANCELLED":
                racecalendar.write(a1row, a1col, racedate, racecanceldatef)
                racecalendar.write(a1row, a1col+1, gp, racecancelf)
                racecalendar.write(a1row, a1col+2, weather, racecancelf)
            elif status == "ON GOING":
                racecalendar.write(a1row, a1col, racedate, raceongoingdatef)
                racecalendar.write(a1row, a1col+1, gp, raceongoingdatef)
                racecalendar.write(a1row, a1col+2, weather, raceongoingdatef)
            else:
                racecalendar.write(a1row, a1col, racedate, RCdatef)
                racecalendar.write(a1row, a1col+1, gp, RCformat16)
                racecalendar.write(a1row, a1col+2, weather, RCformat16)
            a1row += 1
        elif group == "A2":
            if status == "FINISHED":
                racecalendar.write(a2row, a2col, racedate, racefinishdatef)
                racecalendar.write(a2row, a2col+1, gp, racefinishedf)
                racecalendar.write(a2row, a2col+2, weather, racefinishedf)
            elif status == "CANCELLED":
                racecalendar.write(a2row, a2col, racedate, racecanceldatef)
                racecalendar.write(a2row, a2col+1, gp, racecancelf)
                racecalendar.write(a2row, a2col+2, weather, racecancelf)
            elif status == "ON GOING":
                racecalendar.write(a2row, a2col, racedate, raceongoingdatef)
                racecalendar.write(a2row, a2col+1, gp, raceongoingdatef)
                racecalendar.write(a2row, a2col+2, weather, raceongoingdatef)
            else:
                racecalendar.write(a2row, a2col, racedate, RCdatef)
                racecalendar.write(a2row, a2col+1, gp, RCformat16)
                racecalendar.write(a2row, a2col+2, weather, RCformat16)
            a2row += 1
        elif group == "A3":
            if status == "FINISHED":
                racecalendar.write(a3row, a3col, racedate, racefinishdatef)
                racecalendar.write(a3row, a3col+1, gp, racefinishedf)
                racecalendar.write(a3row, a3col+2, weather, racefinishedf)
            elif status == "CANCELLED":
                racecalendar.write(a3row, a3col, racedate, racecanceldatef)
                racecalendar.write(a3row, a3col+1, gp, racecancelf)
                racecalendar.write(a3row, a3col+2, weather, racecancelf)
            elif status == "ON GOING":
                racecalendar.write(a3row, a3col, racedate, raceongoingdatef)
                racecalendar.write(a3row, a3col+1, gp, raceongoingdatef)
                racecalendar.write(a3row, a3col+2, weather, raceongoingdatef)
            else:
                racecalendar.write(a3row, a3col, racedate, RCdatef)
                racecalendar.write(a3row, a3col+1, gp, RCformat16)
                racecalendar.write(a3row, a3col+2, weather, RCformat16)
            a3row += 1


# A1 leaderboard (short)
def get_a1leaderboard_short():
    # Setting row width
    a1leaderboard.set_row(0, 31)
    query = "SELECT count(*) FROM afr_s7.driverLeaderBoard WHERE driverGroup = \"A1\";"
    cursor.execute(query)
    result = cursor.fetchall()
    drivercount = result[0]
    drivercount = list(drivercount)
    drivercount = drivercount[0]
    for pos in range(1,drivercount+1):
        a1leaderboard.set_row(pos, 18)

    # setting column width
    a1leaderboard.set_column(0,0, 3)
    a1leaderboard.set_column(1,1, 21)
    a1leaderboard.set_column(2,4, 9)
    a1leaderboard.set_column(5,5, 3)
    a1leaderboard.set_column(6,6, 21)
    a1leaderboard.set_column(7,8, 9)


    # Creating the header
    a1leaderboard.write(0,0, "Pos.", pointsformat["header"])
    a1leaderboard.write(0,1, "Driver", pointsformat["header"])
    a1leaderboard.write(0,3, "Points", pointsformat["header"])
    for pos in range(1,drivercount+1):
        a1leaderboard.write(pos, 0, pos, pointsformat["header"])
    
    tempcursor = 0
    a1leaderboard.write(tempcursor, 5, "Pos.", pointsformat["header"])
    a1leaderboard.write(tempcursor, 6, "Team", pointsformat["header"])
    a1leaderboard.write(tempcursor, 8, "Points", pointsformat["header"])
    for pos in range(1,13):
        a1leaderboard.write(tempcursor + pos, 5, pos, pointsformat["header"])

    
    # retirve driverlist from database and write into the table
    query = "SELECT driverName, totalPoints, team FROM driverLeaderBoard \
            WHERE driverGroup = 'A1' \
            ORDER BY totalPoints DESC;"
    cursor.execute(query)
    result = cursor.fetchall()

    a1row = 1
    a1col = 1
    for driver in result:
        d = list(driver)
        if d[2] == "Retired":
            a1leaderboard.write(a1row, a1col, d[0], driverformat["Reserve"])
        else:
            a1leaderboard.write(a1row, a1col, d[0], driverformat[d[2]])
        a1leaderboard.write(a1row, a1col+2, d[1], pointsformat["header"])
        a1row += 1

    query = "SELECT team, totalPoints \
            FROM constructorsLeaderBoard \
            WHERE driverGroup = 'A1' \
            ORDER BY totalPoints DESC;"
    cursor.execute(query)
    result = cursor.fetchall()

    a1row = 1
    a1col = 6
    for team in result:
        t = list(team)
        a1leaderboard.write(a1row, a1col, t[0], driverformat[t[0]])
        a1leaderboard.write(a1row, a1col+2, t[1], pointsformat["header"])
        a1row += 1


# A1 full constructors leaderboard
def get_a1leaderboard_constructors():
    # setting row width
    a1leaderboard_cons.set_row(0, 31)
    for i in range(1,11):
        a1leaderboard_cons.set_row(i, 23)
    
    # setting column width
    a1leaderboard_cons.set_column(0,0, 3)
    a1leaderboard_cons.set_column(1,1, 21)
    a1leaderboard_cons.set_column(2,45, 4)
    a1leaderboard_cons.set_column(46,46, 9)

    # Creating the header
    picture = ["Australia.png", "Bahrain.png", "Vietnam.png", "China.png", "Netherlands.png",
            "Spain.png", "Monaco.png", "Azerbaijan.png", "Canada.png", "France.png",
            "Austria.png", "Britain.png", "Hungary.png", "Belgium.png", "Italy.png",
            "Singapore.png", "Russia.png", "Japan.png", "USA.png", "Mexico.png",
            "Brazil.png", "Abu Dhabi.png"]
    a1leaderboard_cons.write(0,0, "Pos.", pointsformat["header"])
    a1leaderboard_cons.write(0,1, "Team", pointsformat["header"])
    for i in range(1,11):
        a1leaderboard_cons.write(i, 0, i, pointsformat["header"])
    for i in range(0,22):
        thepicture = f'flags/{picture[i]}'
        a1leaderboard_cons.insert_image(0, i*2+2, thepicture, {'x_scale':0.96, 'y_scale':0.98})
    a1leaderboard_cons.write(0,46, "Points", pointsformat["header"])

    # retirve driverlist from database and write into the table
    cursor.execute("SELECT DISTINCT (GP) FROM afr_s7.raceResult;")
    result = cursor.fetchall()
    race_done = []
    for r in result:
        r = list(r)
        race_done.append(get_key(gp_dict, r[0]))
    racenum = len(race_done)

    query = "SELECT * FROM constructorsLeaderBoard \
            WHERE driverGroup = 'A1' \
            ORDER BY totalPoints DESC;"
    cursor.execute(query)
    result = cursor.fetchall()

    a1row = 1
    a1col = 0
    for team in result:
        t = list(team)
        tempcursor = a1col
        a1leaderboard_cons.write(a1row, tempcursor+1, t[0], teamformat[t[0]])
        for r in range(2, 2 + racenum*2):
            if t[r] != None:
                if t[r] == 1:
                    a1leaderboard_cons.write(a1row, tempcursor+r, t[r], pointsformat["p1"])
                elif t[r] == 2:
                    a1leaderboard_cons.write(a1row, tempcursor+r, t[r], pointsformat["p2"])
                elif t[r] == 3:
                    a1leaderboard_cons.write(a1row, tempcursor+r, t[r], pointsformat["p3"])
                elif t[r] >= 4 and t[r] <= 10:
                    a1leaderboard_cons.write(a1row, tempcursor+r, t[r], pointsformat["points"])
                elif t[r] >= 11:
                    a1leaderboard_cons.write(a1row, tempcursor+r, t[r], pointsformat["outpoint"])
                elif t[r] == -1:
                    a1leaderboard_cons.write(a1row, tempcursor+r, "RET", pointsformat["retired"])
                elif t[r] == -2:
                    a1leaderboard_cons.write(a1row, tempcursor+r, "DNS", pointsformat["dns"])
                elif t[r] == -4:
                    a1leaderboard_cons.write(a1row, tempcursor+r, "DSQ", pointsformat["dsq"])
            else:
                a1leaderboard_cons.write(a1row, tempcursor+r, "DNA", pointsformat["dna"])
            a1leaderboard_cons.write(a1row, 46, t[-1], pointsformat["header"])
        a1row += 1


# A1 full leaderboard
def get_a1leaderboard_full():
    # Setting row width
    a1leaderboard_full.set_row(0, 31)
    query = "SELECT count(*) FROM afr_s7.driverLeaderBoard WHERE driverGroup = \"A1\";"
    cursor.execute(query)
    result = cursor.fetchall()
    drivercount = result[0]
    drivercount = list(drivercount)
    drivercount = drivercount[0]
    for pos in range(1,drivercount+1):
        a1leaderboard_full.set_row(pos, 18)
        tempcursor = pos
    
    tempcursor += 2
    a1leaderboard_full.set_row(tempcursor, 32)
    for pos in range(1,13):
        a1leaderboard_full.set_row(tempcursor + pos, 23)

    # setting column width
    a1leaderboard_full.set_column(0,0, 3)
    a1leaderboard_full.set_column(1,1, 21)
    a1leaderboard_full.set_column(2,24, 9)

    # Creating the header
    picture = ["Australia.png", "Bahrain.png", "Vietnam.png", "China.png", "Netherlands.png",
            "Spain.png", "Monaco.png", "Azerbaijan.png", "Canada.png", "France.png",
            "Austria.png", "Britain.png", "Hungary.png", "Belgium.png", "Italy.png",
            "Singapore.png", "Russia.png", "Japan.png", "USA.png", "Mexico.png",
            "Brazil.png", "Abu Dhabi.png"]
    a1leaderboard_full.write(0,0, "Pos.", pointsformat["header"])
    a1leaderboard_full.write(0,1, "Driver", pointsformat["header"])
    for i in range(0,22):
        thepicture = f'flags/{picture[i]}'
        a1leaderboard_full.insert_image(0, i+2, thepicture, {'x_scale':0.96, 'y_scale':0.98})
    a1leaderboard_full.write(0,24, "Points", pointsformat["header"])
    for pos in range(1,drivercount+1):
        a1leaderboard_full.write(pos, 0, pos, pointsformat["header"])
        tempcursor = pos
    tempcursor += 2
    a1leaderboard_full.write(tempcursor, 0, "Pos.", pointsformat["header"])
    a1leaderboard_full.write(tempcursor, 1, "Team", pointsformat["header"])
    a1leaderboard_full.write(tempcursor, 3, "Points", pointsformat["header"])
    for pos in range(1,13):
        a1leaderboard_full.write(tempcursor + pos, 0, pos, pointsformat["header"])

    
    # retirve driverlist from database and write into the table
    cursor.execute("SELECT DISTINCT (GP) FROM afr_s7.raceResult;")
    result = cursor.fetchall()
    race_done = []
    for r in result:
        r = list(r)
        race_done.append(get_key(gp_dict, r[0]))
    racenum = len(race_done)

    query = "SELECT * FROM driverLeaderBoard \
            WHERE driverGroup = 'A1' \
            ORDER BY totalPoints DESC;"
    cursor.execute(query)
    result = cursor.fetchall()

    a1row = 1
    a1col = 1
    for driver in result:
        d = list(driver)
        tempcursor = a1col
        if d[1] == "Retired":
            a1leaderboard_full.write(a1row, tempcursor, d[0], driverformat["Reserve"])
        else:
            a1leaderboard_full.write(a1row, tempcursor, d[0], driverformat[d[1]])
        for r in range(1, 1 + racenum):
            if d[r*3] is not None:
                if d[r*3] == 1:
                    p1 = workbook.add_format({"font_size":11})
                    p1.set_font_name("Dengxian")
                    p1.set_align("center")
                    p1.set_align("vcenter")
                    p1.set_bg_color("#FFFF00")
                    if d[r*3+1] == 1:
                        p1.set_bold(True)
                    if d[r*3+2] is not None:
                        p1.set_italic(True)
                    a1leaderboard_full.write(a1row, tempcursor+r, d[r*3], p1)
                elif d[r*3] == 2:
                    p2 = workbook.add_format({"font_size":11})
                    p2.set_font_name("Dengxian")
                    p2.set_align("center")
                    p2.set_align("vcenter")
                    p2.set_bg_color("#EEECE1")
                    if d[r*3+1] == 1:
                        p2.set_bold(True)
                    if d[r*3+2] is not None:
                        p2.set_italic(True)
                    a1leaderboard_full.write(a1row, tempcursor+r, d[r*3], p2)
                elif d[r*3] == 3:
                    p3 = workbook.add_format({"font_size":11})
                    p3.set_font_name("Dengxian")
                    p3.set_align("center")
                    p3.set_align("vcenter")
                    p3.set_bg_color("#FFC000")
                    if d[r*3+1] == 1:
                        p3.set_bold(True)
                    if d[r*3+2] is not None:
                        p3.set_italic(True)
                    a1leaderboard_full.write(a1row, tempcursor+r, d[r*3], p3)
                elif d[r*3] >= 4 and d[r*3] <= 10:
                    points = workbook.add_format({"font_size":11})
                    points.set_font_name("Dengxian")
                    points.set_align("center")
                    points.set_align("vcenter")
                    points.set_bg_color("#00B050")
                    if d[r*3+1] == 1:
                        points.set_bold(True)
                    if d[r*3+2] is not None:
                        points.set_italic(True)
                    a1leaderboard_full.write(a1row, tempcursor+r, d[r*3], points)
                elif d[r*3] >= 11:
                    outpoint = workbook.add_format({"font_size":11})
                    outpoint.set_font_name("Dengxian")
                    outpoint.set_align("center")
                    outpoint.set_align("vcenter")
                    outpoint.set_bg_color("#538DD5")
                    if d[r*3+1] == 1:
                        outpoint.set_bold(True)
                    if d[r*3+2] is not None:
                        outpoint.set_italic(True)
                    a1leaderboard_full.write(a1row, tempcursor+r, d[r*3], outpoint)
                elif d[r*3] == -1:
                    retired = workbook.add_format({"font_size":11})
                    retired.set_font_name("Dengxian")
                    retired.set_align("center")
                    retired.set_align("vcenter")
                    retired.set_bg_color("#7030A0")
                    a1leaderboard_full.write(a1row, tempcursor+r, "RET", retired)
                elif d[r*3] == -2:
                    a1leaderboard_full.write(a1row, tempcursor+r, "DNS", pointsformat["dns"])
                elif d[r*3] == -4:
                    a1leaderboard_full.write(a1row, tempcursor+r, "DSQ", pointsformat["dsq"])
            else:
                a1leaderboard_full.write(a1row, tempcursor+r, "DNA", pointsformat["dna"])
            
        a1leaderboard_full.write(a1row, 24, d[69], pointsformat["header"])
        a1row += 1

    query = "SELECT team, totalPoints \
            FROM constructorsLeaderBoard \
            WHERE driverGroup = 'A1' \
            ORDER BY totalPoints DESC;"
    cursor.execute(query)
    result = cursor.fetchall()

    a1row += 2
    a1col = 1
    for team in result:
        t = list(team)
        a1leaderboard_full.write(a1row, a1col, t[0], teamformat[t[0]])
        a1leaderboard_full.write(a1row, a1col+2, t[1], pointsformat["header"])
        a1row += 1


# A2 leaderboard (short)
def get_a2leaderboard_short():
    # Setting row width
    a2leaderboard.set_row(0, 31)
    query = "SELECT count(*) FROM afr_s7.driverLeaderBoard WHERE driverGroup = \"A2\";"
    cursor.execute(query)
    result = cursor.fetchall()
    drivercount = result[0]
    drivercount = list(drivercount)
    drivercount = drivercount[0]
    for pos in range(1,drivercount+1):
        a2leaderboard.set_row(pos, 18)

    # setting column width
    a2leaderboard.set_column(0,0, 3)
    a2leaderboard.set_column(1,1, 21)
    a2leaderboard.set_column(2,4, 9)
    a2leaderboard.set_column(5,5, 3)
    a2leaderboard.set_column(6,6, 21)
    a2leaderboard.set_column(7,8, 9)


    # Creating the header
    
    a2leaderboard.write(0,0, "Pos.", pointsformat["header"])
    a2leaderboard.write(0,1, "Driver", pointsformat["header"])
    a2leaderboard.write(0,3, "Points", pointsformat["header"])
    for pos in range(1,drivercount+1):
        a2leaderboard.write(pos, 0, pos, pointsformat["header"])
    
    tempcursor = 0
    a2leaderboard.write(tempcursor, 5, "Pos.", pointsformat["header"])
    a2leaderboard.write(tempcursor, 6, "Team", pointsformat["header"])
    a2leaderboard.write(tempcursor, 8, "Points", pointsformat["header"])
    for pos in range(1,13):
        a2leaderboard.write(tempcursor + pos, 5, pos, pointsformat["header"])

    
    # retirve driverlist from database and write into the table
    query = "SELECT driverName, totalPoints, team FROM driverLeaderBoard \
            WHERE driverGroup = 'A2' \
            ORDER BY totalPoints DESC;"
    cursor.execute(query)
    result = cursor.fetchall()

    a2row = 1
    a2col = 1
    for driver in result:
        d = list(driver)
        if d[2] == "Retired":
            a2leaderboard.write(a2row, a2col, d[0], driverformat["Reserve"])
        else:
            a2leaderboard.write(a2row, a2col, d[0], driverformat[d[2]])
        a2leaderboard.write(a2row, a2col+2, d[1], pointsformat["header"])
        a2row += 1

    query = "SELECT team, totalPoints \
            FROM constructorsLeaderBoard \
            WHERE driverGroup = 'A2' \
            ORDER BY totalPoints DESC;"
    cursor.execute(query)
    result = cursor.fetchall()

    a2row = 1
    a2col = 6
    for team in result:
        t = list(team)
        a2leaderboard.write(a2row, a2col, t[0], driverformat[t[0]])
        a2leaderboard.write(a2row, a2col+2, t[1], pointsformat["header"])
        a2row += 1


# A2 full constructors leaderboard
def get_a2leaderboard_constructors():
    # setting row width
    a2leaderboard_cons.set_row(0, 31)
    for i in range(1,11):
        a2leaderboard_cons.set_row(i, 23)
    
    # setting column width
    a2leaderboard_cons.set_column(0,0, 3)
    a2leaderboard_cons.set_column(1,1, 21)
    a2leaderboard_cons.set_column(2,45, 4)
    a2leaderboard_cons.set_column(46,46, 9)

    # Creating the header
    picture = ["Australia.png", "Bahrain.png", "Vietnam.png", "China.png", "Netherlands.png",
            "Spain.png", "Monaco.png", "Azerbaijan.png", "Canada.png", "France.png",
            "Austria.png", "Britain.png", "Hungary.png", "Belgium.png", "Italy.png",
            "Singapore.png", "Russia.png", "Japan.png", "USA.png", "Mexico.png",
            "Brazil.png", "Abu Dhabi.png"]
    a2leaderboard_cons.write(0,0, "Pos.", pointsformat["header"])
    a2leaderboard_cons.write(0,1, "Team", pointsformat["header"])
    for i in range(1,11):
        a2leaderboard_cons.write(i, 0, i, pointsformat["header"])
    for i in range(0,22):
        thepicture = f'flags/{picture[i]}'
        a2leaderboard_cons.insert_image(0, i*2+2, thepicture, {'x_scale':0.96, 'y_scale':0.98})
    a2leaderboard_cons.write(0,46, "Points", pointsformat["header"])

    # retirve driverlist from database and write into the table
    cursor.execute("SELECT DISTINCT (GP) FROM afr_s7.raceResult;")
    result = cursor.fetchall()
    race_done = []
    for r in result:
        r = list(r)
        race_done.append(get_key(gp_dict, r[0]))
    racenum = len(race_done)

    query = "SELECT * FROM constructorsLeaderBoard \
            WHERE driverGroup = 'A2' \
            ORDER BY totalPoints DESC;"
    cursor.execute(query)
    result = cursor.fetchall()

    a2row = 1
    a2col = 0
    for team in result:
        t = list(team)
        tempcursor = a2col
        a2leaderboard_cons.write(a2row, tempcursor+1, t[0], teamformat[t[0]])
        for r in range(2, 2 + racenum*2):
            if t[r] != None:
                if t[r] == 1:
                    a2leaderboard_cons.write(a2row, tempcursor+r, t[r], pointsformat["p1"])
                elif t[r] == 2:
                    a2leaderboard_cons.write(a2row, tempcursor+r, t[r], pointsformat["p2"])
                elif t[r] == 3:
                    a2leaderboard_cons.write(a2row, tempcursor+r, t[r], pointsformat["p3"])
                elif t[r] >= 4 and t[r] <= 10:
                    a2leaderboard_cons.write(a2row, tempcursor+r, t[r], pointsformat["points"])
                elif t[r] >= 11:
                    a2leaderboard_cons.write(a2row, tempcursor+r, t[r], pointsformat["outpoint"])
                elif t[r] == -1:
                    a2leaderboard_cons.write(a2row, tempcursor+r, "RET", pointsformat["retired"])
                elif t[r] == -2:
                    a2leaderboard_cons.write(a2row, tempcursor+r, "DNS", pointsformat["dns"])
                elif t[r] == -4:
                    a2leaderboard_cons.write(a2row, tempcursor+r, "DSQ", pointsformat["dsq"])
            else:
                a2leaderboard_cons.write(a2row, tempcursor+r, "DNA", pointsformat["dna"])
            a2leaderboard_cons.write(a2row, 46, t[-1], pointsformat["header"])
        a2row += 1


# A2 full leaderboard
def get_a2leaderboard_full():
    # Setting row width
    a2leaderboard_full.set_row(0, 31)
    query = "SELECT count(*) FROM afr_s7.driverLeaderBoard WHERE driverGroup = \"A2\";"
    cursor.execute(query)
    result = cursor.fetchall()
    drivercount = result[0]
    drivercount = list(drivercount)
    drivercount = drivercount[0]
    for pos in range(1,drivercount+1):
        a2leaderboard_full.set_row(pos, 18)
        tempcursor = pos
    
    tempcursor += 2
    a2leaderboard_full.set_row(tempcursor, 32)
    for pos in range(1,13):
        a2leaderboard_full.set_row(tempcursor + pos, 23)

    # setting column width
    a2leaderboard_full.set_column(0,0, 3)
    a2leaderboard_full.set_column(1,1, 21)
    a2leaderboard_full.set_column(2,24, 9)


    # Creating the header
    picture = ["Australia.png", "Bahrain.png", "Vietnam.png", "China.png", "Netherlands.png",
            "Spain.png", "Monaco.png", "Azerbaijan.png", "Canada.png", "France.png",
            "Austria.png", "Britain.png", "Hungary.png", "Belgium.png", "Italy.png",
            "Singapore.png", "Russia.png", "Japan.png", "USA.png", "Mexico.png",
            "Brazil.png", "Abu Dhabi.png"]
    a2leaderboard_full.write(0,0, "Pos.", pointsformat["header"])
    a2leaderboard_full.write(0,1, "Driver", pointsformat["header"])
    for i in range(0,22):
        thepicture = f'flags/{picture[i]}'
        a2leaderboard_full.insert_image(0, i+2, thepicture, {'x_scale':0.96, 'y_scale':0.98})
    a2leaderboard_full.write(0,24, "Points", pointsformat["header"])
    for pos in range(1,drivercount+1):
        a2leaderboard_full.write(pos, 0, pos, pointsformat["header"])
        tempcursor = pos
    tempcursor += 2
    a2leaderboard_full.write(tempcursor, 0, "Pos.", pointsformat["header"])
    a2leaderboard_full.write(tempcursor, 1, "Team", pointsformat["header"])
    a2leaderboard_full.write(tempcursor, 3, "Points", pointsformat["header"])
    for pos in range(1,13):
        a2leaderboard_full.write(tempcursor + pos, 0, pos, pointsformat["header"])

    
    # retirve driverlist from database and write into the table
    cursor.execute("SELECT DISTINCT (GP) FROM afr_s7.raceResult;")
    result = cursor.fetchall()
    race_done = []
    for r in result:
        r = list(r)
        race_done.append(get_key(gp_dict, r[0]))
    racenum = len(race_done)

    query = "SELECT * FROM driverLeaderBoard \
            WHERE driverGroup = 'A2' \
            ORDER BY totalPoints DESC;"
    cursor.execute(query)
    result = cursor.fetchall()

    a2row = 1
    a2col = 1
    for driver in result:
        d = list(driver)
        tempcursor = a2col
        if d[1] == "Retired":
            a2leaderboard_full.write(a2row, tempcursor, d[0], driverformat["Reserve"])
        else:
            a2leaderboard_full.write(a2row, tempcursor, d[0], driverformat[d[1]])
        for r in range(1, 1 + racenum):
            if d[r*3] is not None:

                if d[r*3] == 1:
                    p1 = workbook.add_format({"font_size":11})
                    p1.set_font_name("Dengxian")
                    p1.set_align("center")
                    p1.set_align("vcenter")
                    p1.set_bg_color("#FFFF00")
                    if d[r*3+1] == 1:
                        p1.set_bold(True)
                    if d[r*3+2] is not None:
                        p1.set_italic(True)
                    a2leaderboard_full.write(a2row, tempcursor+r, d[r*3], p1)
                elif d[r*3] == 2:
                    p2 = workbook.add_format({"font_size":11})
                    p2.set_font_name("Dengxian")
                    p2.set_align("center")
                    p2.set_align("vcenter")
                    p2.set_bg_color("#EEECE1")
                    if d[r*3+1] == 1:
                        p2.set_bold(True)
                    if d[r*3+2] is not None:
                        p2.set_italic(True)
                    a2leaderboard_full.write(a2row, tempcursor+r, d[r*3], p2)
                elif d[r*3] == 3:
                    p3 = workbook.add_format({"font_size":11})
                    p3.set_font_name("Dengxian")
                    p3.set_align("center")
                    p3.set_align("vcenter")
                    p3.set_bg_color("#FFC000")
                    if d[r*3+1] == 1:
                        p3.set_bold(True)
                    if d[r*3+2] is not None:
                        p3.set_italic(True)
                    a2leaderboard_full.write(a2row, tempcursor+r, d[r*3], p3)
                elif d[r*3] >= 4 and d[r*3] <= 10:
                    points = workbook.add_format({"font_size":11})
                    points.set_font_name("Dengxian")
                    points.set_align("center")
                    points.set_align("vcenter")
                    points.set_bg_color("#00B050")
                    if d[r*3+1] == 1:
                        points.set_bold(True)
                    if d[r*3+2] is not None:
                        points.set_italic(True)
                    a2leaderboard_full.write(a2row, tempcursor+r, d[r*3], points)
                elif d[r*3] >= 11:
                    outpoint = workbook.add_format({"font_size":11})
                    outpoint.set_font_name("Dengxian")
                    outpoint.set_align("center")
                    outpoint.set_align("vcenter")
                    outpoint.set_bg_color("#538DD5")
                    if d[r*3+1] == 1:
                        outpoint.set_bold(True)
                    if d[r*3+2] is not None:
                        outpoint.set_italic(True)
                    a2leaderboard_full.write(a2row, tempcursor+r, d[r*3], outpoint)
                elif d[r*3] == -1:
                    retired = workbook.add_format({"font_size":11})
                    retired.set_font_name("Dengxian")
                    retired.set_align("center")
                    retired.set_align("vcenter")
                    retired.set_bg_color("#7030A0")
                    a2leaderboard_full.write(a2row, tempcursor+r, "RET", retired)
                elif d[r*3] == -2:
                    a2leaderboard_full.write(a2row, tempcursor+r, "DNS", pointsformat["dns"])
                elif d[r*3] == -4:
                    a2leaderboard_full.write(a2row, tempcursor+r, "DSQ", pointsformat["dsq"])
            else:
                a2leaderboard_full.write(a2row, tempcursor+r, "DNA", pointsformat["dna"])
            
        a2leaderboard_full.write(a2row, 24, d[69], pointsformat["header"])
        a2row += 1

    query = "SELECT team, totalPoints \
            FROM constructorsLeaderBoard \
            WHERE driverGroup = 'A2' \
            ORDER BY totalPoints DESC;"
    cursor.execute(query)
    result = cursor.fetchall()

    a2row += 2
    a2col = 1
    for team in result:
        t = list(team)
        a2leaderboard_full.write(a2row, a2col, t[0], teamformat[t[0]])
        a2leaderboard_full.write(a2row, a2col+2, t[1], pointsformat["header"])
        a2row += 1


# drivers license point
def get_licensepoint():
    # setting row width
    licensepoint.set_row(0, 31)
    cursor.execute("SELECT count(*) FROM licensePoint;")
    result = cursor.fetchall()
    drivercount = result[0]
    drivercount = list(drivercount)
    drivercount = drivercount[0]
    for pos in range(1,drivercount+1):
        licensepoint.set_row(pos, 18)
    
    # setting column width
    licensepoint.set_column(0,0, 3)
    licensepoint.set_column(1,1, 21)
    licensepoint.set_column(2,25, 9)

    # write the header
    licensepoint.write(0,1, "Drvier", pointsformat["header"])
    picture = ["Australia.png", "Bahrain.png", "Vietnam.png", "China.png", "Netherlands.png",
            "Spain.png", "Monaco.png", "Azerbaijan.png", "Canada.png", "France.png",
            "Austria.png", "Britain.png", "Hungary.png", "Belgium.png", "Italy.png",
            "Singapore.png", "Russia.png", "Japan.png", "USA.png", "Mexico.png",
            "Brazil.png", "Abu Dhabi.png"]
    for i in range(0,22):
        thepicture = f'flags/{picture[i]}'
        licensepoint.insert_image(0, i+2, thepicture, {'x_scale':0.96, 'y_scale':0.98})
    licensepoint.write(0,23, "Warning", pointsformat["header"])
    licensepoint.write(0,24, "Points", pointsformat["header"])

    # retirve driverlist from database and write into the table
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

    row = 1
    col = 0
    for driver in result:
        d = list(driver)
        if d[1] == "A1":
            a1f = workbook.add_format({"font_size":11})
            a1f.set_bg_color("#FFFF00")
            a1f.set_font_name("Dengxian")
            a1f.set_align("vcenter")
            licensepoint.write(row, 1, d[0], a1f)
        elif d[1] == "A2":
            a2f = workbook.add_format({"font_size":11})
            a2f.set_bg_color("#E26B0A")
            a2f.set_font_name("Dengxian")
            a2f.set_align("vcenter")
            licensepoint.write(row, 1, d[0], a2f)
        elif d[1] == "A3":
            a3f = workbook.add_format({"font_size":11})
            a3f.set_bg_color("#00B050")
            a3f.set_font_name("Dengxian")
            a3f.set_align("vcenter")
            licensepoint.write(row, 1, d[0], a3f)

        for i in range(2,25):
            licensepoint.write(row, i, d[i], pointsformat["header"])
            if d[-1] >= 11:
                rank = "excellent"
            elif d[-1] >= 7 and d[-1] <= 10:
                rank = "good"
            elif d[-1] >= 4 and d[-1] <= 6:
                rank = "poor"
            elif d[-1] >= 1 and d[-1] <= 3:
                rank = "danger"
            else:
                rank = "danger"
            licensepoint.write(row, 25, d[25], licensepointformat[rank])

        row += 1
    

# LAN username and password
def get_lanusername():
    # setting row width
    cursor.execute("SELECT COUNT(*) FROM LANusername;")
    result = cursor.fetchall()
    drivercount = result[0]
    drivercount = list(drivercount)
    drivercount = drivercount[0]
    for pos in range(1,drivercount+1):
        lanusernamelist.set_row(pos, 15)

    # setting column width
    lanusernamelist.set_column(0,2, 22)

    # format across the LAN username list table
    lanf = workbook.add_format({"font_size":11})
    lanf.set_font_name("Dengxian")
    lanf.set_align("vcenter")
    lanf.set_text_wrap()
    RCf = workbook.add_format({"font_size":11})
    RCf.set_font_name("Dengxian")
    RCf.set_align("vcenter")
    RCf.set_bg_color("#00FF00")
    RCf.set_text_wrap()
    standbyf = workbook.add_format({"font_size":11})
    standbyf.set_font_name("Dengxian")
    standbyf.set_align("vcenter")
    standbyf.set_bg_color("#FFFF00")
    standbyf.set_text_wrap()


    # write the header
    lanusernamelist.write(0,0, "游戏id", lanf)
    lanusernamelist.write(0,1, "LAN用户名", lanf)
    lanusernamelist.write(0,2, "密码", lanf)

    # retirve driverlist from database and write into the table
    query = "SELECT * FROM afr_s7.LANusername ORDER BY username ASC;"
    cursor.execute(query)
    result = cursor.fetchall()

    row = 1
    col = 0
    for account in result:
        a = list(account)
        for i in range(0,3):
            if a[-1] == "Race Coordinator":
                lanusernamelist.write(row, col+i, a[i], RCf)
            elif a[-1] == "STANDBY":
                lanusernamelist.write(row, col+i, a[i], standbyf)
            else:
                lanusernamelist.write(row, col+i, a[i], lanf)
        row += 1


def close_doc():
    workbook.close()