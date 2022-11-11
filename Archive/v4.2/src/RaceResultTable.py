from datetime import datetime
import xlsxwriter
import connectserver
import ref_dict
import ref_format

db = connectserver.connectserver()
cursor = db.cursor()

today = datetime.today().strftime('%Y-%m-%d')
query = f'SELECT Round, GP_CHN FROM raceCalendar \
        WHERE raceDate <= "{today}" AND raceStatus != "SEASON BREAK"\
        ORDER BY raceDate DESC;'
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


workbook = xlsxwriter.Workbook(f'AFR S9 数据分析（R{round} {race_name}）.xlsx')
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
        raceresult.set_column(6,6, 3)
        raceresult.set_column(12,12, 3)
        raceresult.set_column(18,18, 3)

        raceresult.set_column(1,1, 20)
        raceresult.set_column(7,7, 20)
        raceresult.set_column(13,13, 20)
        raceresult.set_column(19,19, 20)

        raceresult.set_column(2,2, 15)
        raceresult.set_column(8,8, 15)
        raceresult.set_column(14,14, 15)
        raceresult.set_column(20,20, 15)

        raceresult.set_column(3,4, 5)
        raceresult.set_column(9,10, 5)
        raceresult.set_column(15,16, 5)
        raceresult.set_column(21,22, 5)

        raceresult.set_column(5,5, 7)
        raceresult.set_column(11,11, 7)
        raceresult.set_column(17,17, 7)
        raceresult.set_column(23,23, 7)


        # retirve event result from database and write into the table
        # retirve driverlist from database and write into the table
        # retirve order : by (qualiying, race) - (A1, A2, A3)

        # qualiying result
        raceresult.merge_range("A1:F1", "Qualifying", formatter.raceresultformat["headerf"])      # the big header
        raceresult.merge_range("G1:L1", "Qualifying", formatter.raceresultformat["headerf"])
        raceresult.merge_range("M1:R1", "Qualifying", formatter.raceresultformat["headerf"])
        raceresult.merge_range("S1:W1", "Qualifying", formatter.raceresultformat["headerf"])
        maxdrivercount = 0

        # A1 group
        raceresult.merge_range("A2:F2", "A1", formatter.raceresultformat["a1headerf"])
        raceresult.write(2, 1, "车手", formatter.raceresultformat["headerf"])
        raceresult.write(2, 2, "圈速", formatter.raceresultformat["headerf"])
        raceresult.write(2, 3, "轮胎", formatter.raceresultformat["headerf"])
        round += 1
        query = f'SELECT DISTINCT(GP_ENG) FROM raceCalendar WHERE Round = {round};'
        cursor.execute(query)
        result = cursor.fetchall()
        try:
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
                        raceresult.write(tempcursor, a1col, lap[0], formatter.raceresultformat["headerf"])
                    else:
                        raceresult.write(tempcursor, a1col, lap[5], formatter.raceresultformat[lap[5]])

                    raceresult.write(tempcursor, a1col+1, lap[1], formatter.driverformat[lap[2]])

                    if  lap[3] != '' and lap[3] is not None:
                        raceresult.write(tempcursor, a1col+2, lap[3], formatter.raceresultformat["timef"])
                    else:
                        raceresult.write(tempcursor, a1col+2, "--:--.---", formatter.raceresultformat["timef"])

                    if lap[4] != '' and lap[4] is not None:
                        raceresult.write(tempcursor, a1col+3, lap[4], formatter.raceresultformat[lap[4]])
                    else:
                        raceresult.write(tempcursor, a1col+3, "-", formatter.raceresultformat["headerf"])
                    tempcursor += 1

                    drivercount = lap[0]
                except ValueError:
                    pass

            maxdrivercount = drivercount

        except Exception:
            pass


        # A2 group
        raceresult.merge_range("G2:L2", "A2", formatter.raceresultformat["a2headerf"])
        raceresult.write(2, 7, "车手", formatter.raceresultformat["headerf"])
        raceresult.write(2, 8, "圈速", formatter.raceresultformat["headerf"])
        raceresult.write(2, 9, "轮胎", formatter.raceresultformat["headerf"])

        query = f'SELECT position, driverName, team, fastestLap, tyre, driverStatus \
                FROM qualiResult WHERE GP = "{therace}" and driverGroup = "A2";'
        cursor.execute(query)
        result = cursor.fetchall()

        a2row = 3
        a2col = 6
        tempcursor = a2row
        for lap in result:
            try:
                if lap is None:
                    raise ValueError
                
                lap = list(lap)
                if lap[5] == "FINISHED" or lap[5] == "RETIRED":
                    raceresult.write(tempcursor, a2col, lap[0], formatter.raceresultformat["headerf"])
                else:
                    raceresult.write(tempcursor, a2col, lap[5], formatter.raceresultformat[lap[5]])

                raceresult.write(tempcursor, a2col+1, lap[1], formatter.driverformat[lap[2]])

                if lap[3] is not None:
                    raceresult.write(tempcursor, a2col+2, lap[3], formatter.raceresultformat["timef"])
                else:
                    raceresult.write(tempcursor, a2col+2, "--:--.---", formatter.raceresultformat["timef"])
                
                if lap[4] != '' and lap[4] is not None:
                    raceresult.write(tempcursor, a2col+3, lap[4], formatter.raceresultformat[lap[4]])
                else:
                    raceresult.write(tempcursor, a2col+3, "-", formatter.raceresultformat["headerf"])
                tempcursor += 1

                drivercount = lap[0]
            except ValueError:
                pass

        if drivercount > maxdrivercount:
            maxdrivercount = drivercount


        #"""
        # A3 group
        raceresult.merge_range("M2:R2", "A3", formatter.raceresultformat["a3headerf"])
        raceresult.write(2, 13, "车手", formatter.raceresultformat["headerf"])
        raceresult.write(2, 14, "圈速", formatter.raceresultformat["headerf"])
        raceresult.write(2, 15, "轮胎", formatter.raceresultformat["headerf"])

        """
        query = f'SELECT qualiResult.position, qualiResult.driverName, qualiResult.team, qualiResult.fastestLap, \
                qualiResult.tyre, qualiResult.driverStatus, driverList.driverGroup \
                FROM qualiResult JOIN driverList ON driverList.driverName = qualiResult.driverName \
                WHERE GP = "{therace}" AND qualiResult.driverGroup = "A3" \
                AND driverList.team != "Team AFR2" AND driverList.team != "Team AFR3";'
        """
        query = f'SELECT position, driverName, team, fastestLap, tyre, driverStatus \
                FROM qualiResult WHERE GP = "{therace}" and driverGroup = "A3";'
        cursor.execute(query)
        result = cursor.fetchall()

        a3row = 3
        a3col = 12
        tempcursor = a3row
        for lap in result:
            try:
                if lap is None:
                    raise ValueError
                
                lap = list(lap)
                if lap[5] == "FINISHED" or lap[5] == "RETIRED":
                    raceresult.write(tempcursor, a3col, lap[0], formatter.raceresultformat["headerf"])
                else:
                    raceresult.write(tempcursor, a3col, lap[5], formatter.raceresultformat[lap[5]])

                raceresult.write(tempcursor, a3col+1, lap[1], formatter.driverformat[lap[2]])

                if lap[3] != '' and lap[3] != None:
                    raceresult.write(tempcursor, a3col+2, lap[3], formatter.raceresultformat["timef"])
                else:
                    raceresult.write(tempcursor, a3col+2, "--:--.---", formatter.raceresultformat["timef"])

                if lap[4] != '' and lap[4] is not None:
                    raceresult.write(tempcursor, a3col+3, lap[4], formatter.raceresultformat[lap[4]])
                else:
                    raceresult.write(tempcursor, a3col+3, "-", formatter.raceresultformat["headerf"])
                tempcursor += 1
            
                drivercount = lap[0]
            except ValueError:
                pass

        if drivercount > maxdrivercount:
            maxdrivercount = drivercount
        #"""



        # race result
        # big header = maxdrivercount + 4
        # group header = maxdrivercount + 5
        # small header = maxdrivercount + 6
        # data = maxdrivercount + 7
        raceresult.merge_range(maxdrivercount+4, 0, maxdrivercount+4, 5, "Race", formatter.raceresultformat["headerf"])
        raceresult.merge_range(maxdrivercount+4, 6, maxdrivercount+4, 11, "Race", formatter.raceresultformat["headerf"])
        raceresult.merge_range(maxdrivercount+4, 12, maxdrivercount+4, 17, "Race", formatter.raceresultformat["headerf"])

        # A1 group
        a1row = maxdrivercount +5
        a1col = 0
        raceresult.merge_range(a1row, a1col, a1row, a1col+5, "A1", formatter.raceresultformat["a1headerf"])
        a1row += 1
        raceresult.write(a1row, a1col+1, "车手", formatter.raceresultformat["headerf"])
        raceresult.write(a1row, a1col+2, "差距", formatter.raceresultformat["headerf"])
        raceresult.write(a1row, a1col+3, "起跑", formatter.raceresultformat["headerf"])
        raceresult.write(a1row, a1col+4, "P.C.", formatter.raceresultformat["headerf"])
        a1row += 1

        query = f'SELECT * FROM raceResult WHERE GP = "{therace}" and driverGroup = "A1";'
        cursor.execute(query)
        result = cursor.fetchall()

        try:
            if result == []:
                raise ValueError

            tempcursor = a1row
            for position in result:
                p = list(position)
                if p[-1] == "FINISHED":
                    raceresult.write(tempcursor, a1col, p[2], formatter.raceresultformat["headerf"])
                elif p[-1] == "RETIRED":
                    raceresult.write(tempcursor, a1col, "RET", formatter.raceresultformat[p[-1]])
                else:
                    raceresult.write(tempcursor, a1col, p[-1], formatter.raceresultformat[p[-1]])

                raceresult.write(tempcursor, a1col+1, p[3], formatter.driverformat[p[4]])
                raceresult.write(tempcursor, a1col+2, p[7], formatter.raceresultformat["positionhold"])
                raceresult.write(tempcursor, a1col+3, p[5], formatter.raceresultformat["headerf"])


                positionchange = p[5] - p[2]
                if positionchange > 0:
                    positionchange = '+' + str(positionchange)
                    raceresult.write(tempcursor, a1col+4, positionchange, formatter.raceresultformat["positionup"])
                elif positionchange < 0:
                    positionchange = str(positionchange)
                    raceresult.write(tempcursor, a1col+4, positionchange, formatter.raceresultformat["positiondown"])
                else:
                    positionchange = str(positionchange)
                    raceresult.write(tempcursor, a1col+4, positionchange, formatter.raceresultformat["positionhold"])
                
                tempcursor += 1
            
            tempcursor += 1
            query = f'SELECT qualiraceFL.raceFLdriver, qualiraceFL.raceFLteam, \
                    qualiraceFL.raceFLvalidation, raceResult.fastestLap \
                    FROM qualiraceFL JOIN raceResult \
                    ON qualiraceFL.raceFLdriver = raceResult.driverName \
                        AND qualiraceFL.gp = raceResult.GP \
                        AND qualiraceFL.driverGroup = raceResult.driverGroup \
                    WHERE qualiraceFL.GP = "{therace}" and qualiraceFL.driverGroup = "A1";'
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result) != 0:
                result = result[0]
                result = list(result)
                fldriver = result[0]
                flteam = result[1]
                flvld = result[2]
                fl = result[3]
                raceresult.write(tempcursor, a1col+1, fldriver, formatter.driverformat[flteam])
                raceresult.write(tempcursor, a1col+2, fl, formatter.raceresultformat["timef"])
                raceresult.merge_range(tempcursor, a1col+3, tempcursor, a1col+5, "fastest lap", formatter.raceresultformat["fastestlap"])
                if flvld == 0:
                    raceresult.merge_range(tempcursor+1, a1col+1, tempcursor+1, a1col+4, "*points will not allocated", formatter.raceresultformat["deniedheader"])

        except ValueError:
            pass


        # A2 group
        a2row = maxdrivercount + 5
        a2col = 6
        raceresult.merge_range(a2row, a2col, a2row, a2col+5, "A2", formatter.raceresultformat["a2headerf"])
        a2row += 1
        raceresult.write(a2row, a2col+1, "车手", formatter.raceresultformat["headerf"])
        raceresult.write(a2row, a2col+2, "差距", formatter.raceresultformat["headerf"])
        raceresult.write(a2row, a2col+3, "起跑", formatter.raceresultformat["headerf"])
        raceresult.write(a2row, a2col+4, "P.C.", formatter.raceresultformat["headerf"])
        a2row += 1

        query = f'SELECT * FROM raceResult WHERE GP = "{therace}" and driverGroup = "A2";'
        cursor.execute(query)
        result = cursor.fetchall()

        try:
            if result == []:
                raise ValueError

            tempcursor = a2row
            for position in result:
                p = list(position)
                if p[-1] == "FINISHED":
                    raceresult.write(tempcursor, a2col, p[2], formatter.raceresultformat["headerf"])
                elif p[-1] == "RETIRED":
                    raceresult.write(tempcursor, a2col, "RET", formatter.raceresultformat[p[-1]])
                else:
                    raceresult.write(tempcursor, a2col, p[-1], formatter.raceresultformat[p[-1]])

                if p[4] == "Failed":
                    raceresult.write(tempcursor, a2col+1, p[3], formatter.driverformat["Testing"])
                else:
                    raceresult.write(tempcursor, a2col+1, p[3], formatter.driverformat[p[4]])

                raceresult.write(tempcursor, a2col+1, p[3], formatter.driverformat[p[4]])
                raceresult.write(tempcursor, a2col+2, p[7], formatter.raceresultformat["positionhold"])
                raceresult.write(tempcursor, a2col+3, p[5], formatter.raceresultformat["headerf"])

                positionchange = p[5] - p[2]
                if positionchange > 0:
                    positionchange = '+' + str(positionchange)
                    raceresult.write(tempcursor, a2col+4, positionchange, formatter.raceresultformat["positionup"])
                elif positionchange < 0:
                    positionchange = str(positionchange)
                    raceresult.write(tempcursor, a2col+4, positionchange, formatter.raceresultformat["positiondown"])
                else:
                    positionchange = str(positionchange)
                    raceresult.write(tempcursor, a2col+4, positionchange, formatter.raceresultformat["positionhold"])
                
                tempcursor += 1

            tempcursor += 1
            query = f'SELECT qualiraceFL.raceFLdriver, qualiraceFL.raceFLteam, \
                    qualiraceFL.raceFLvalidation, raceResult.fastestLap \
                    FROM qualiraceFL JOIN raceResult \
                    ON qualiraceFL.raceFLdriver = raceResult.driverName \
                        AND qualiraceFL.gp = raceResult.GP \
                        AND qualiraceFL.driverGroup = raceResult.driverGroup \
                    WHERE qualiraceFL.GP = "{therace}" and qualiraceFL.driverGroup = "A2";'
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result) != 0:
                result = result[0]
                result = list(result)
                fldriver = result[0]
                flteam = result[1]
                flvld = result[2]
                fl = result[3]
                raceresult.write(tempcursor, a2col+1, fldriver, formatter.driverformat[flteam])
                raceresult.write(tempcursor, a2col+2, fl, formatter.raceresultformat["timef"])
                raceresult.merge_range(tempcursor, a2col+3, tempcursor, a2col+5, "fastest lap", formatter.raceresultformat["fastestlap"])
                if flvld == 0:
                    raceresult.merge_range(tempcursor+1, a2col+1, tempcursor+1, a2col+4, "*points will not allocated", formatter.raceresultformat["deniedheader"])

        except ValueError:
            pass


        #"""
        # A3 group
        a3row = maxdrivercount + 5
        a3col = 12
        raceresult.merge_range(a3row, a3col, a3row, a3col+5, "A3", formatter.raceresultformat["a3headerf"])
        a3row += 1
        raceresult.write(a3row, a3col+1, "车手", formatter.raceresultformat["headerf"])
        raceresult.write(a3row, a3col+2, "差距", formatter.raceresultformat["headerf"])
        raceresult.write(a3row, a3col+3, "起跑", formatter.raceresultformat["headerf"])
        raceresult.write(a3row, a3col+4, "P.C.", formatter.raceresultformat["headerf"])
        a3row += 1

        query = f'SELECT * FROM raceResult WHERE GP = "{therace}" and driverGroup = "A3";'
        cursor.execute(query)
        result = cursor.fetchall()

        try:
            if result == []:
                raise ValueError
            
            tempcursor = a3row
            for position in result:
                p = list(position)
                if p[-1] == "FINISHED":
                    raceresult.write(tempcursor, a3col, p[2], formatter.raceresultformat["headerf"])
                elif p[-1] == "RETIRED":
                    raceresult.write(tempcursor, a3col, "RET", formatter.raceresultformat[p[-1]])
                elif p[-1] == "DNF":
                    raceresult.write(tempcursor, a3col, p[-1], formatter.raceresultformat[p[-1]])

                raceresult.write(tempcursor, a3col+1, p[3], formatter.driverformat[p[4]])
                raceresult.write(tempcursor, a3col+2, p[7], formatter.raceresultformat["positionhold"])
                raceresult.write(tempcursor, a3col+3, p[5], formatter.raceresultformat["headerf"])

                positionchange = p[5] - p[2]
                if positionchange > 0:
                    positionchange = '+' + str(positionchange)
                    raceresult.write(tempcursor, a3col+4, positionchange, formatter.raceresultformat["positionup"])
                elif positionchange < 0:
                    positionchange = str(positionchange)
                    raceresult.write(tempcursor, a3col+4, positionchange, formatter.raceresultformat["positiondown"])
                else:
                    positionchange = str(positionchange)
                    raceresult.write(tempcursor, a3col+4, positionchange, formatter.raceresultformat["positionhold"])
                
                tempcursor += 1

            tempcursor += 1
            query = f'SELECT qualiraceFL.raceFLdriver, qualiraceFL.raceFLteam, \
                    qualiraceFL.raceFLvalidation, raceResult.fastestLap \
                    FROM qualiraceFL JOIN raceResult \
                    ON qualiraceFL.raceFLdriver = raceResult.driverName \
                        AND qualiraceFL.gp = raceResult.GP \
                        AND qualiraceFL.driverGroup = raceResult.driverGroup \
                    WHERE qualiraceFL.GP = "{therace}" and qualiraceFL.driverGroup = "A3";'
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result) != 0:
                result = result[0]
                result = list(result)
                fldriver = result[0]
                flteam = result[1]
                flvld = result[2]
                fl = result[3]
                raceresult.write(tempcursor, a3col+1, fldriver, formatter.driverformat[flteam])
                raceresult.write(tempcursor, a3col+2, fl, formatter.raceresultformat["timef"])
                raceresult.merge_range(tempcursor, a3col+3, tempcursor, a3col+5, "fastest lap", formatter.raceresultformat["fastestlap"])
                if flvld == 0:
                    raceresult.merge_range(tempcursor+1, a3col+1, tempcursor+1, a3col+4, "*points will not allocated", formatter.raceresultformat["deniedheader"])
                
        except ValueError:
            pass
        #"""



        # weekend qualiying comparision
        raceresult.merge_range("S2:W2", "Wholeweekend", formatter.raceresultformat["a3headerf"])
        raceresult.write(2, 13, "车手", formatter.raceresultformat["headerf"])
        raceresult.write(2, 14, "圈速", formatter.raceresultformat["headerf"])
        raceresult.write(2, 15, "轮胎", formatter.raceresultformat["headerf"])
        srow = 3
        scol = 18

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
                raceresult.write(srow, scol, i+1, formatter.raceresultformat["headerf"])
            elif lap[7] == "QB":
                raceresult.write(srow, scol, lap[7], formatter.raceresultformat[lap[7]])

            if lap[0] == "A1":
                raceresult.write(srow, scol+1, lap[3], formatter.driverformat["Team AFR1"])
            elif lap[0] == "A2":
                raceresult.write(srow, scol+1, lap[3], formatter.driverformat["Team AFR2"])
            elif lap[0] == "A3":
                raceresult.write(srow, scol+1, lap[3], formatter.driverformat["Team AFR3"])
            
            if lap[5] == None:
                raceresult.write(srow, scol+2, "--:--.---", formatter.raceresultformat["headerf"])
            else:
                raceresult.write(srow, scol+2, lap[5], formatter.raceresultformat["headerf"])

            if lap[6] == None or lap[6] == '':
                raceresult.write(srow, scol+3, "-", formatter.raceresultformat["headerf"])
            else:
                raceresult.write(srow, scol+3, lap[6], formatter.raceresultformat[lap[6]])

            srow += 1




def menu():
    get_raceresulttable()
    workbook.close()

menu()