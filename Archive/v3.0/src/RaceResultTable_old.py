from datetime import datetime
import xlsxwriter
import connectserver as connector

db = connector.connectserver()
cursor = db.cursor()

# create and open the excel file
today = datetime.today().strftime('%Y-%m-%d')
query = f'SELECT Round, GP_CHN FROM raceCalendar \
        WHERE raceDate <= "{today}" \
        ORDER BY raceDate DESC;'
cursor.execute(query)
result = cursor.fetchall()
result = list(result[0])
round = result[0]   
race_name = result[1]

workbook = xlsxwriter.Workbook(f'AFR S7 数据分析（R{round}{race_name}）.xlsx')


# create the worksheet for each race
cursor.execute("SELECT DISTINCT(GP_CHN)FROM raceCalendar;")
result = cursor.fetchall()
race = []
for r in result:
    r = list(r)
    race.append(r[0])

raceresult_list = []
for a in range(0,len(race)):
    sheetname = f'R{a+1} {race[a]}'
    raceresult_list.append(workbook.add_worksheet(sheetname))



# some useful stuff
gp_dict = {
    "澳大利亚": "Australia",
    "巴林": "Bahrain",
    "越南": "Vietnam",
    "中国": "China",
    "荷兰": "Netherlands",
    "西班牙": "Spain",
    "摩纳哥": "Monaco",
    "阿塞拜疆": "Azerbaijan",
    "加拿大": "Canada",
    "法国": "France",
    "奥地利": "Austria",
    "英国": "Britain",
    "匈牙利": "Hungary",
    "比利时": "Belgium",
    "意大利": "Italy",
    "新加坡": "Singapore",
    "俄罗斯": "Russia",
    "日本": "Japan",
    "美国": "USA",
    "墨西哥": "Mexico",
    "巴西": "Brazil",
    "阿布扎比": "Abu Dahbi"
}
def get_key(my_dict, val):
    for key, value in my_dict.items():
        if val == value:
            return key
    return "key doesn't exist"


# some useful format
defaultformat = {}
timef = workbook.add_format({"num_format":"m:ss.000"})
timef.set_font_size("12")
timef.set_font_name("Dengxian")
timef.set_align("center")
timef.set_align("vcenter")
defaultformat["header"] = timef
headerf = workbook.add_format({"font_size":12})
headerf.set_font_name("Dengxian")
headerf.set_align("center")
headerf.set_align("vcenter")
defaultformat["header"] = headerf
a1headerf = workbook.add_format({"font_size":12})
a1headerf.set_font_name("Dengxian")
a1headerf.set_align("center")
a1headerf.set_align("vcenter")
a1headerf.set_bg_color("#FFFF00")
defaultformat["a1header"] = a1headerf
a2headerf = workbook.add_format({"font_size":12})
a2headerf.set_font_name("Dengxian")
a2headerf.set_align("center")
a2headerf.set_align("vcenter")
a2headerf.set_bg_color("#E26B0A")
defaultformat["a2header"] = a2headerf
a3headerf = workbook.add_format({"font_size":12})
a3headerf.set_font_name("Dengxian")
a3headerf.set_align("center")
a3headerf.set_align("vcenter")
a3headerf.set_bg_color("#00B050")
defaultformat["a3header"] = a3headerf
laptimef = workbook.add_format({"font_size":12})
laptimef.set_font_name("Dengxian")
laptimef.set_align("center")
laptimef.set_align("vcenter")
defaultformat["laptime"] = laptimef
qualibanf = workbook.add_format({"font_size":12})
qualibanf.set_font_name("Dengxian")
qualibanf.set_align("center")
qualibanf.set_align("vcenter")
qualibanf.set_bg_color("#000000")
qualibanf.set_font_color("#FFFFFF")
defaultformat["qualiban"] = qualibanf
dnsf = workbook.add_format({"font_size":12})
dnsf.set_font_name("Dengxian")
dnsf.set_align("center")
dnsf.set_align("vcenter")
dnsf.set_bg_color("#808080")
defaultformat["dns"] = dnsf
retiredf = workbook.add_format({"font_size":12})
retiredf.set_font_name("Dengxian")
retiredf.set_align("center")
retiredf.set_align("vcenter")
retiredf.set_bg_color("#7030A0")
defaultformat["retired"] = retiredf
dnff = workbook.add_format({"font_size":12})
dnff.set_font_name("Dengxian")
dnff.set_align("center")
dnff.set_align("vcenter")
defaultformat["dnf"] = dnff
dsqf = workbook.add_format({"font_size":12})
dsqf.set_font_name("Dengxian")
dsqf.set_align("center")
dsqf.set_align("vcenter")
dsqf.set_bg_color("#FF0000")
defaultformat["dsq"] = dsqf
softtyref = workbook.add_format({"font_size":12})
softtyref.set_font_name("Dengxian")
softtyref.set_align("center")
softtyref.set_align("vcenter")
softtyref.set_bg_color("#FF0000")
softtyref.set_bold(True)
defaultformat["S"] = softtyref
mediumtyref = workbook.add_format({"font_size":12})
mediumtyref.set_font_name("Dengxian")
mediumtyref.set_align("center")
mediumtyref.set_align("vcenter")
mediumtyref.set_bg_color("#FFFF00")
mediumtyref.set_bold(True)
defaultformat["M"] = mediumtyref
hardtyref = workbook.add_format({"font_size":12})
hardtyref.set_font_name("Dengxian")
hardtyref.set_align("center")
hardtyref.set_align("vcenter")
hardtyref.set_bold(True)
defaultformat["H"] = hardtyref
intertyref = workbook.add_format({"font_size":12})
intertyref.set_font_name("Dengxian")
intertyref.set_align("center")
intertyref.set_align("vcenter")
intertyref.set_bg_color("#00B050")
intertyref.set_bold(True)
defaultformat["I"] = intertyref
wettyref = workbook.add_format({"font_size":12})
wettyref.set_font_name("Dengxian")
wettyref.set_align("center")
wettyref.set_align("vcenter")
wettyref.set_bg_color("#0070C0")
wettyref.set_bold(True)
defaultformat["W"] = wettyref
positionupf = workbook.add_format({"font_size":12})
positionupf.set_font_name("Dengxian")
positionupf.set_align("center")
positionupf.set_align("vcenter")
positionupf.set_bg_color("#00FF00")
positionupf.set_text_wrap()
defaultformat["positionup"] = positionupf
positiondownf = workbook.add_format({"font_size":12})
positiondownf.set_font_name("Dengxian")
positiondownf.set_align("center")
positiondownf.set_align("vcenter")
positiondownf.set_bg_color("#FF0000")
positiondownf.set_text_wrap()
defaultformat["positiondown"] = positiondownf
positionholdf = workbook.add_format({"font_size":12})
positionholdf.set_font_name("Dengxian")
positionholdf.set_align("center")
positionholdf.set_align("vcenter")
positionholdf.set_text_wrap()
defaultformat["positiondown"] = positionholdf
fastestlapf = workbook.add_format({"font_size":12})
fastestlapf.set_font_name("Dengxian")
fastestlapf.set_align("center")
fastestlapf.set_align("vcenter")
fastestlapf.set_bg_color("#7030A0")
defaultformat["fastestlap"] = fastestlapf
fakefastestlapf = workbook.add_format({"font_size":12})
fakefastestlapf.set_font_name("Dengxian")
fakefastestlapf.set_align("center")
fakefastestlapf.set_align("vcenter")
fakefastestlapf.set_bg_color("#000000")
fakefastestlapf.set_font_color("#FFFFFF")
defaultformat["fakefastestlap"] = fakefastestlapf
deniedheaderf = workbook.add_format({"font_size":12})
deniedheaderf.set_font_name("Dengxian")
deniedheaderf.set_align("center")
deniedheaderf.set_align("vcenter")
deniedheaderf.set_bg_color("#000000")
deniedheaderf.set_font_color("#FFFFFF")
defaultformat["deniedheader"] = deniedheaderf



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
testingf = workbook.add_format({"font_size":11})
testingf.set_font_name("Dengxian")
testingf.set_align("vcenter")
testingf.set_bg_color("#00FF00")
driverformat["Testing"] = testingf
failedf = workbook.add_format({"font_size":11})
failedf.set_font_name("Dengxian")
failedf.set_align("vcenter")
failedf.set_bg_color("#E26B0A")
driverformat["Failed"] = failedf
teamafr1f = workbook.add_format({"font_size":11})
teamafr1f.set_font_name("Dengxian")
teamafr1f.set_align("vcenter")
teamafr1f.set_bg_color("#FFFF00")
driverformat["Team AFR1"] = teamafr1f
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


for indexidx in range(0,len(raceresult_list)):
    raceresult = raceresult_list[indexidx]

    # setting row width
    for i in range(0,60):
        raceresult.set_row(i, 20)

    # setting column width
    raceresult.set_column(0,0, 3)
    raceresult.set_column(5,5, 3)
    raceresult.set_column(10,10, 3)
    raceresult.set_column(15,15, 3)
    raceresult.set_column(1,1, 20)
    raceresult.set_column(6,6, 20)
    raceresult.set_column(11,11, 20)
    raceresult.set_column(16,16, 20)
    raceresult.set_column(2,2, 15)
    raceresult.set_column(7,7, 15)
    raceresult.set_column(12,12, 15)
    raceresult.set_column(17,17, 15)
    raceresult.set_column(3,3, 5)
    raceresult.set_column(8,8, 5)
    raceresult.set_column(13,13, 5)
    raceresult.set_column(18,18, 5)
    raceresult.set_column(4,4, 10)
    raceresult.set_column(9,9, 10)
    raceresult.set_column(14,14, 10)
    raceresult.set_column(19,19, 10)


    # retirve driverlist from database and write into the table
    # retirve order : by (qualiying, race) - (A1, A2, A3)

    # qualiying result
    raceresult.merge_range("A1:T1", "Qualifying", headerf)      # the big header
    maxdrivercount = 0

    # A1 group
    raceresult.merge_range("A2:E2", "A1", a1headerf)
    raceresult.write(2, 1, "车手", headerf)
    raceresult.write(2, 2, "圈速", headerf)
    raceresult.write(2, 3, "轮胎", headerf)
    round = indexidx + 1
    query = f'SELECT DISTINCT(GP_ENG) FROM raceCalendar WHERE Round = {round};'
    cursor.execute(query)
    result = cursor.fetchall()
    result = list(result[0])
    therace = result[0]

    query = f'SELECT position, driverName, team, fastestLap, tyre, driverStatus \
            FROM qualiResult WHERE GP = "{therace}" and driverGroup = "A1";'
    cursor.execute(query)
    result = cursor.fetchall()

    a1row = 3
    a1col = 0
    tempcursor = a1row
    drivercount = 0
    for lap in result:
        try:
            if lap is None:
                raise ValueError
            
            lap = list(lap)
            if lap[5] == "FINISHED" or lap[5] == "RETIRED":
                raceresult.write(tempcursor, a1col, lap[0], headerf)
            elif lap[5] == "DSQ":
                raceresult.write(tempcursor, a1col, "DSQ", dsqf)
            elif lap[5] == "DNS":
                raceresult.write(tempcursor, a1col, "DNS", dnsf)
            elif lap[5] == "QB":
                raceresult.write(tempcursor, a1col, "QB", dnsf)

            raceresult.write(tempcursor, a1col+1, lap[1], driverformat[lap[2]])

            if  lap[3] != '' and lap[3] is not None:
                raceresult.write(tempcursor, a1col+2, lap[3], timef)
            else:
                raceresult.write(tempcursor, a1col+2, "--:--.---", timef)

            if lap[4] != '' and lap[4] is not None:
                raceresult.write(tempcursor, a1col+3, lap[4], defaultformat[lap[4]])
            else:
                raceresult.write(tempcursor, a1col+3, "-", headerf)
            tempcursor += 1

            drivercount = lap[0]
        except ValueError:
            pass

    maxdrivercount = drivercount


    # A2 group
    raceresult.merge_range("F2:J2", "A2", a2headerf)
    raceresult.write(2, 6, "车手", headerf)
    raceresult.write(2, 7, "圈速", headerf)
    raceresult.write(2, 8, "轮胎", headerf)

    query = f'SELECT position, driverName, team, fastestLap, tyre, driverStatus \
            FROM qualiResult WHERE GP = "{therace}" and driverGroup = "A2";'
    cursor.execute(query)
    result = cursor.fetchall()

    a2row = 3
    a2col = 5
    tempcursor = a2row
    for lap in result:
        try:
            if lap is None:
                raise ValueError
            
            lap = list(lap)
            if lap[5] == "FINISHED" or lap[5] == "RETIRED":
                raceresult.write(tempcursor, a2col, lap[0], headerf)
            elif lap[5] == "DSQ":
                raceresult.write(tempcursor, a2col, "DSQ", dsqf)
            elif lap[5] == "DNS":
                raceresult.write(tempcursor, a2col, "DNS", dnsf)
            elif lap[5] == "QB":
                raceresult.write(tempcursor, a2col, "QB", dnsf)

            raceresult.write(tempcursor, a2col+1, lap[1], driverformat[lap[2]])

            if lap[3] is not None:
                raceresult.write(tempcursor, a2col+2, lap[3], timef)
            else:
                raceresult.write(tempcursor, a2col+2, "--:--.---", timef)
            
            if lap[4] != '' and lap[4] is not None:
                raceresult.write(tempcursor, a2col+3, lap[4], defaultformat[lap[4]])
            else:
                raceresult.write(tempcursor, a2col+3, "-", headerf)
            tempcursor += 1

            drivercount = lap[0]
        except ValueError:
            pass

    if drivercount > maxdrivercount:
        maxdrivercount = drivercount


    # A3 group
    raceresult.merge_range("K2:O2", "A3", a3headerf)
    raceresult.write(2, 11, "车手", headerf)
    raceresult.write(2, 12, "圈速", headerf)
    raceresult.write(2, 13, "轮胎", headerf)

    query = f'SELECT qualiResult.position, qualiResult.driverName, qualiResult.team, qualiResult.fastestLap, \
            qualiResult.tyre, qualiResult.driverStatus, driverList.driverGroup \
            FROM qualiResult JOIN driverList ON driverList.driverName = qualiResult.driverName \
            WHERE GP = "{therace}" and qualiResult.driverGroup = "A3";'
    cursor.execute(query)
    result = cursor.fetchall()

    a3row = 3
    a3col = 10
    tempcursor = a3row
    for lap in result:
        try:
            if lap is None:
                raise ValueError
            
            lap = list(lap)
            if lap[5] == "FINISHED" or lap[5] == "RETIRED":
                raceresult.write(tempcursor, a3col, lap[0], headerf)
            elif lap[5] == "DSQ":
                raceresult.write(tempcursor, a3col, "DSQ", dsqf)
            elif lap[5] == "DNS":
                raceresult.write(tempcursor, a3col, "DNS", dnsf)
            elif lap[5] == "QB":
                raceresult.write(tempcursor, a3col, "QB", dnsf)

            if lap[-1] == "A1":
                raceresult.write(tempcursor, a3col+1, lap[1], driverformat["Team AFR1"])
            elif lap[-1] == "A2":
                raceresult.write(tempcursor, a3col+1, lap[1], driverformat["Team AFR2"])
            elif lap[-1] == "A3":
                raceresult.write(tempcursor, a3col+1, lap[1], driverformat["Team AFR3"])

            if lap[3] != '' and lap[3] != None:
                raceresult.write(tempcursor, a3col+2, lap[3], timef)
            else:
                raceresult.write(tempcursor, a3col+2, "--:--.---", timef)

            if lap[4] != '' and lap[4] is not None:
                raceresult.write(tempcursor, a3col+3, lap[4], defaultformat[lap[4]])
            else:
                raceresult.write(tempcursor, a3col+3, "-", headerf)
            tempcursor += 1
        
            drivercount = lap[0]
        except ValueError:
            pass

    if drivercount > maxdrivercount:
        maxdrivercount = drivercount


    # race result
    # big header = maxdrivercount + 4
    # group header = maxdrivercount + 5
    # small header = maxdrivercount + 6
    # data = maxdrivercount + 7
    raceresult.merge_range(maxdrivercount+4, 0, maxdrivercount+4, 14, "Race", headerf)

    # A1 group
    a1row = maxdrivercount +5
    a1col = 0
    raceresult.merge_range(a1row, a1col, a1row, a1col+4, "A1", a1headerf)
    a1row += 1
    raceresult.write(a1row, a1col+1, "车手", headerf)
    raceresult.write(a1row, a1col+2, "起跑", headerf)
    raceresult.write(a1row, a1col+3, "P.C.", headerf)
    a1row += 1

    query = f'SELECT * FROM raceResult WHERE GP = "{therace}" and driverGroup = "A1";'
    cursor.execute(query)
    result = cursor.fetchall()

    try:
        if result == []:
            raise ValueError

        fl_list = []
        fl_driver = []
        fl_team = []
        tempcursor = a1row
        for position in result:
            p = list(position)
            if p[7] == "FINISHED":
                raceresult.write(tempcursor, a1col, p[2], headerf)
            elif p[7] == "RETIRED":
                raceresult.write(tempcursor, a1col, "RET", defaultformat["retired"])
            elif p[7] == "DNF":
                raceresult.write(tempcursor, a1col, "DNF", defaultformat["dnf"])
            elif p[7] == "DSQ":
                raceresult.write(tempcursor, a1col, "DSQ", defaultformat["dsq"])

            raceresult.write(tempcursor, a1col+1, p[3], driverformat[p[4]])

            raceresult.write(tempcursor, a1col+2, p[5], headerf)

            positionchange = p[5] - p[2]
            if positionchange > 0:
                positionchange = '+' + str(positionchange)
                raceresult.write(tempcursor, a1col+3, positionchange, positionupf)
            elif positionchange < 0:
                positionchange = str(positionchange)
                raceresult.write(tempcursor, a1col+3, positionchange, positiondownf)
            else:
                positionchange = str(positionchange)
                raceresult.write(tempcursor, a1col+3, positionchange, positionholdf)
            
            if p[6] is None or p[7] != "FINISHED":
                fl = "9:59.999"
                fl_list.append(fl)
                fl_driver.append(p[3])
                fl_team.append(p[4])
            else:
                fl_list.append(p[6])
                fl_driver.append(p[3])
                fl_team.append(p[4])

            tempcursor += 1

        tempcursor += 1

        count_driver = len(fl_list)
        fl = "9:59.999"
        flvalidation = 0
        temp = 0

        for index in range(0, len(fl_list)):
            if fl_list[index] < fl and fl_list[index] != None:
                fl = fl_list[index]
                driver = fl_driver[index]
                team = fl_team[index]
                if (index + 1) < count_driver/2 + 1:
                    flvalidation = 1
                else:
                    flvalidation = 0
                temp = index + 1

        try:
            if fl == "9:59.999":
                raise ValueError

            if temp > count_driver/4*3 + 1:
                raceresult.write(tempcursor+1, a1col+1, driver, driverformat[team])
                raceresult.write(tempcursor+1, a1col+2, fl, headerf)
                raceresult.merge_range(tempcursor+1, a1col+3, tempcursor+1, a1col+4, "fastest lap", fakefastestlapf)

                fl_list = fl_list[:int(count_driver/4*3 + 1)]
                fl = "9:59.999"
                for index in range(0, len(fl_list)):
                    if fl_list[index] < fl and fl_list[index] != None:
                        fl = fl_list[index]
                        driver = fl_driver[index]
                        team = fl_team[index]
                        if (index + 1) < count_driver/2 + 1:
                            flvalidation = 1
                        else:
                            flvalidation = 0
                
                if flvalidation == 0:
                    raceresult.write(tempcursor, a1col+1, driver, driverformat[team])
                    raceresult.write(tempcursor, a1col+2, fl, headerf)
                    raceresult.merge_range(tempcursor, a1col+3, tempcursor, a1col+4, "fastest lap", fastestlapf)
                    raceresult.merge_range(tempcursor+2, a1col+1, tempcursor+2, a1col+4, "*points will not allocated", deniedheaderf)
                elif flvalidation == 1:
                    raceresult.write(tempcursor, a1col+1, driver, driverformat[team])
                    raceresult.write(tempcursor, a1col+2, fl, headerf)
                    raceresult.merge_range(tempcursor, a1col+3, tempcursor, a1col+4, "fastest lap", fastestlapf)

            else:
                if flvalidation == 0:
                    raceresult.write(tempcursor, a1col+1, driver, driverformat[team])
                    raceresult.write(tempcursor, a1col+2, fl, headerf)
                    raceresult.merge_range(tempcursor, a1col+3, tempcursor, a1col+4, "fastest lap", fastestlapf)
                    raceresult.merge_range(tempcursor+1, a1col+1, tempcursor+1, a1col+4, "*points will not allocated", deniedheaderf)
                elif flvalidation == 1:
                    raceresult.write(tempcursor, a1col+1, driver, driverformat[team])
                    raceresult.write(tempcursor, a1col+2, fl, headerf)
                    raceresult.merge_range(tempcursor, a1col+3, tempcursor, a1col+4, "fastest lap", fastestlapf)
        except ValueError:
            raceresult.merge_range(tempcursor, a1col+1, tempcursor, a1col+4, "*fastest lap record lost", deniedheaderf)
            raceresult.merge_range(tempcursor+1, a1col+1, tempcursor+1, a1col+4, "*points will not allocated", deniedheaderf)

    except ValueError:
        pass


    # A2 group
    a2row = maxdrivercount +5
    a2col = 5
    raceresult.merge_range(a2row, a2col, a2row, a2col+4, "A2", a2headerf)
    a2row += 1
    raceresult.write(a2row, a2col+1, "车手", headerf)
    raceresult.write(a2row, a2col+2, "起跑", headerf)
    raceresult.write(a2row, a2col+3, "P.C.", headerf)
    a2row += 1

    query = f'SELECT * FROM raceResult WHERE GP = "{therace}" and driverGroup = "A2";'
    cursor.execute(query)
    result = cursor.fetchall()

    try:
        if result == []:
            raise ValueError

        fl_list = []
        fl_driver = []
        fl_team = []
        tempcursor = a2row
        for position in result:
            p = list(position)
            if p[7] == "FINISHED":
                raceresult.write(tempcursor, a2col, p[2], headerf)
            elif p[7] == "RETIRED":
                raceresult.write(tempcursor, a2col, "RET", defaultformat["retired"])
            elif p[7] == "DNF":
                raceresult.write(tempcursor, a2col, "DNF", defaultformat["dnf"])
            elif p[7] == "DSQ":
                raceresult.write(tempcursor, a2col, "DSQ", defaultformat["dsq"])

            if p[4] == "Failed":
                raceresult.write(tempcursor, a2col+1, p[3], driverformat["Testing"])
            else:
                raceresult.write(tempcursor, a2col+1, p[3], driverformat[p[4]])

            raceresult.write(tempcursor, a2col+2, p[5], headerf)

            positionchange = p[5] - p[2]
            if positionchange > 0:
                positionchange = '+' + str(positionchange)
                raceresult.write(tempcursor, a2col+3, positionchange, positionupf)
            elif positionchange < 0:
                positionchange = str(positionchange)
                raceresult.write(tempcursor, a2col+3, positionchange, positiondownf)
            else:
                positionchange = str(positionchange)
                raceresult.write(tempcursor, a2col+3, positionchange, positionholdf)
            
            if p[6] is None or p[7] != "FINISHED":
                fl = "9:59.999"
                fl_list.append(fl)
                fl_driver.append(p[3])
                fl_team.append(p[4])
            else:
                fl_list.append(p[6])
                fl_driver.append(p[3])
                fl_team.append(p[4])

            tempcursor += 1

        tempcursor += 1

        count_driver = len(fl_list)
        fl = "9:59.999"
        flvalidation = 0
        temp = 0

        for index in range(0, len(fl_list)):
            if fl_list[index] < fl and fl_list[index] != None:
                fl = fl_list[index]
                driver = fl_driver[index]
                team = fl_team[index]
                if (index + 1) < count_driver/2 + 1:
                    flvalidation = 1
                else:
                    flvalidation = 0
                temp = index + 1


        try:
            if fl == "9:59.999":
                raise ValueError
            if temp > count_driver/4*3 + 1:
                raceresult.write(tempcursor+1, a2col+1, driver, driverformat[team])
                raceresult.write(tempcursor+1, a2col+2, fl, headerf)
                raceresult.merge_range(tempcursor+1, a2col+3, tempcursor+1, a2col+4, "fastest lap", fakefastestlapf)

                fl_list = fl_list[:int(count_driver/4*3 + 1)]
                fl = "9:59.999"
                for index in range(0, len(fl_list)):
                    if fl_list[index] < fl and fl_list[index] != None:
                        fl = fl_list[index]
                        driver = fl_driver[index]
                        team = fl_team[index]
                        if (index + 1) < count_driver/2 + 1:
                            flvalidation = 1
                        else:
                            flvalidation = 0
                if flvalidation == 0:
                    raceresult.write(tempcursor, a2col+1, driver, driverformat[team])
                    raceresult.write(tempcursor, a2col+2, fl, headerf)
                    raceresult.merge_range(tempcursor, a2col+3, tempcursor, a2col+4, "fastest lap", fastestlapf)
                    raceresult.merge_range(tempcursor+2, a2col+1, tempcursor+2, a2col+4, "*points will not allocated", deniedheaderf)
                elif flvalidation == 1:
                    raceresult.write(tempcursor, a2col+1, driver, driverformat[team])
                    raceresult.write(tempcursor, a2col+2, fl, headerf)
                    raceresult.merge_range(tempcursor, a2col+3, tempcursor, a2col+4, "fastest lap", fastestlapf)

            else:
                if flvalidation == 0:
                    raceresult.write(tempcursor, a2col+1, driver, driverformat[team])
                    raceresult.write(tempcursor, a2col+2, fl, headerf)
                    raceresult.merge_range(tempcursor, a2col+3, tempcursor, a2col+4, "fastest lap", fastestlapf)
                    raceresult.merge_range(tempcursor+1, a2col+1, tempcursor+1, a2col+4, "*points will not allocated", deniedheaderf)
                elif flvalidation == 1:
                    raceresult.write(tempcursor, a2col+1, driver, driverformat[team])
                    raceresult.write(tempcursor, a2col+2, fl, headerf)
                    raceresult.merge_range(tempcursor, a2col+3, tempcursor, a2col+4, "fastest lap", fastestlapf)
        except ValueError:
            raceresult.merge_range(tempcursor, a1col+1, tempcursor, a1col+4, "*fastest lap record lost", deniedheaderf)
            raceresult.merge_range(tempcursor+1, a1col+1, tempcursor+1, a1col+4, "*points will not allocated", deniedheaderf)


    except ValueError:
        pass

    # A3 group
    a3row = maxdrivercount + 5
    a3col = 10
    raceresult.merge_range(a3row, a3col, a3row, a3col+4, "A3", a3headerf)
    a3row += 1
    raceresult.write(a3row, a3col+1, "车手", headerf)
    raceresult.write(a3row, a3col+2, "起跑", headerf)
    raceresult.write(a3row, a3col+3, "P.C.", headerf)
    a3row += 1

    query = f'SELECT * FROM raceResult WHERE GP = "{therace}" and driverGroup = "A3";'
    cursor.execute(query)
    result = cursor.fetchall()

    try:
        if result == []:
            raise ValueError

        fl_list = []
        fl_driver = []
        fl_team = []
        tempcursor = a3row
        for position in result:
            p = list(position)
            if p[7] == "FINISHED":
                raceresult.write(tempcursor, a3col, p[2], headerf)
            elif p[7] == "RETIRED":
                raceresult.write(tempcursor, a3col, "RET", defaultformat["retired"])
            elif p[7] == "DNF":
                raceresult.write(tempcursor, a3col, "DNF", defaultformat["dnf"])
            elif p[7] == "DSQ":
                raceresult.write(tempcursor, a3col, "DSQ", defaultformat["dsq"])

            raceresult.write(tempcursor, a3col+1, p[3], driverformat[p[4]])

            raceresult.write(tempcursor, a3col+2, p[5], headerf)

            positionchange = p[5] - p[2]
            if positionchange > 0:
                positionchange = '+' + str(positionchange)
                raceresult.write(tempcursor, a3col+3, positionchange, positionupf)
            elif positionchange < 0:
                positionchange = str(positionchange)
                raceresult.write(tempcursor, a3col+3, positionchange, positiondownf)
            else:
                positionchange = str(positionchange)
                raceresult.write(tempcursor, a3col+3, positionchange, positionholdf)
            
            if p[6] is None or p[7] != "FINISHED":
                fl = "9:59.999"
                fl_list.append(fl)
                fl_driver.append(p[3])
                fl_team.append(p[4])
            else:
                fl_list.append(p[6])
                fl_driver.append(p[3])
                fl_team.append(p[4])

            tempcursor += 1

        tempcursor += 1

        count_driver = len(fl_list)
        fl = "9:59.999"
        flvalidation = 0
        temp = 0

        for index in range(0, len(fl_list)):
            if fl_list[index] < fl and fl_list[index] != None:
                fl = fl_list[index]
                driver = fl_driver[index]
                team = fl_team[index]
                if (index + 1) < count_driver/2 + 1:
                    flvalidation = 1
                else:
                    flvalidation = 0
                temp = index + 1

        try:
            if fl == "9:59.999":
                raise ValueError

            if temp > count_driver/4*3 + 1:
                raceresult.write(tempcursor+1, a3col+1, driver, driverformat[team])
                raceresult.write(tempcursor+1, a3col+2, fl, headerf)
                raceresult.merge_range(tempcursor+1, a3col+3, tempcursor+1, a3col+4, "fastest lap", fakefastestlapf)

                fl_list = fl_list[:int(count_driver/4*3 + 1)]
                fl = "9:59.999"
                for index in range(0, len(fl_list)):
                    if fl_list[index] < fl and fl_list[index] != None:
                        fl = fl_list[index]
                        driver = fl_driver[index]
                        team = fl_team[index]
                        if (index + 1) < count_driver/2 + 1:
                            flvalidation = 1
                        else:
                            flvalidation = 0
                if flvalidation == 0:
                    raceresult.write(tempcursor, a3col+1, driver, driverformat[team])
                    raceresult.write(tempcursor, a3col+2, fl, headerf)
                    raceresult.merge_range(tempcursor, a3col+3, tempcursor, a3col+4, "fastest lap", fastestlapf)
                    raceresult.merge_range(tempcursor+2, a3col+1, tempcursor+2, a3col+4, "*points will not allocated", deniedheaderf)
                elif flvalidation == 1:
                    raceresult.write(tempcursor, a3col+1, driver, driverformat[team])
                    raceresult.write(tempcursor, a3col+2, fl, headerf)
                    raceresult.merge_range(tempcursor, a3col+3, tempcursor, a3col+4, "fastest lap", fastestlapf)

            else:
                if flvalidation == 0:
                    raceresult.write(tempcursor, a3col+1, driver, driverformat[team])
                    raceresult.write(tempcursor, a3col+2, fl, headerf)
                    raceresult.merge_range(tempcursor, a3col+3, tempcursor, a3col+4, "fastest lap", fastestlapf)
                    raceresult.merge_range(tempcursor+1, a3col+1, tempcursor+1, a3col+4, "*points will not allocated", deniedheaderf)
                elif flvalidation == 1:
                    raceresult.write(tempcursor, a3col+1, driver, driverformat[team])
                    raceresult.write(tempcursor, a3col+2, fl, headerf)
                    raceresult.merge_range(tempcursor, a3col+3, tempcursor, a3col+4, "fastest lap", fastestlapf)
        
        except ValueError:
            raceresult.merge_range(tempcursor, a1col+1, tempcursor, a1col+4, "*fastest lap record lost", deniedheaderf)
            raceresult.merge_range(tempcursor+1, a1col+1, tempcursor+1, a1col+4, "*points will not allocated", deniedheaderf)

    except ValueError:
        pass


    # weekend qualiying comparision
    raceresult.merge_range("P2:T2", "Wholeweekend", a3headerf)
    raceresult.write(2, 16, "车手", headerf)
    raceresult.write(2, 17, "圈速", headerf)
    raceresult.write(2, 18, "轮胎", headerf)
    srow = 3
    scol = 15

    query = f'SELECT * FROM qualiResult \
            WHERE GP = "{therace}" \
            ORDER BY -fastestLap DESC, fastestLap ASC, \
            CASE driverStatus \
                WHEN "Retired" THEN 1 \
                WHEN "QB" THEN 2 \
                WHEN "DSQ" THEN 3 \
                WHEN "DNS" THEN 4 \
            END, driverStatus;'
    cursor.execute(query)
    result = cursor.fetchall()

    for i in range(0,len(result)):
        lap = list(result[i])

        if lap[7] == "FINISHED" or lap[7] == "RETIRED":
            raceresult.write(srow, scol, i+1, headerf)
        elif lap[7] == "QB":
            raceresult.write(srow, scol, "QB", defaultformat["qualiban"])
        elif lap[7] == "DSQ":
            raceresult.write(srow, scol, "DSQ", defaultformat["dsq"])
        elif lap[7] == "DNS":
            raceresult.write(srow, scol, "DNS", defaultformat["dns"])

        if lap[0] == "A1":
            raceresult.write(srow, scol+1, lap[3], driverformat["Team AFR1"])
        elif lap[0] == "A2":
            raceresult.write(srow, scol+1, lap[3], driverformat["Team AFR2"])
        elif lap[0] == "A3":
            raceresult.write(srow, scol+1, lap[3], driverformat["Team AFR3"])
        
        if lap[5] == None:
            raceresult.write(srow, scol+2, "--:--.---", headerf)
        else:
            raceresult.write(srow, scol+2, lap[5], headerf)

        if lap[6] == None or lap[6] == '':
            raceresult.write(srow, scol+3, "-", headerf)
        else:
            raceresult.write(srow, scol+3, lap[6], defaultformat[lap[6]])

        srow += 1
    


workbook.close()