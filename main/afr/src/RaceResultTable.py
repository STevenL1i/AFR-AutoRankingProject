import json, traceback, xlsxwriter
from datetime import datetime

import mysql.connector
import connectserver
import deffunc as func


# loading all the necessary json settings
# settings
settingsf = open("settings/settings.json", "r", encoding='utf-8')
settings:dict = json.load(settingsf)
settingsf.close()
# format
formatf = open("settings/format.json", "r", encoding='utf-8')
format:dict = json.load(formatf)
formatf.close()
# log
logpath = settings["default"]["log"]



def get_raceresulttable(workbook:xlsxwriter.Workbook, db:mysql.connector.MySQLConnection, race:tuple):
    cursor = db.cursor()

    # race = (GP_ENG, GP_CHN, Round)
    round = int(race[2]); gp = race[0]; gpchn = race[1]
    raceresult = workbook.add_worksheet(f'R{round:02} {gpchn}')

    query = f'SELECT MAX(position) FROM qualiResult \
            WHERE GP = "{gp}";'
    cursor.execute(query)
    result = cursor.fetchall()
    maxqualicount = result[0][0]

    colcursor = 0
    for i in range(0, len(settings["drivergroup"]["order"])):
        group = settings["drivergroup"]["order"][i]
        func.logging(logpath, func.delimiter_string(f'{group}-{gp}', 50), end="\n\n")
        print(func.delimiter_string(f'{group}-{gp}', 50), end="\n\n")

        # setting header row height and column width
        raceresult.set_row(0, 20)
        raceresult.set_row(1, 20)
        raceresult.set_row(2, 20)
        raceresult.set_column(colcursor, colcursor, 3)
        raceresult.set_column(colcursor+1, colcursor+1, 20)
        raceresult.set_column(colcursor+2, colcursor+2, 15)
        raceresult.set_column(colcursor+3, colcursor+4, 5)
        raceresult.set_column(colcursor+5, colcursor+5, 7)




        ##### quali result #####
        # writing header
        raceresult.merge_range(0, colcursor, 0, colcursor+5, settings["content"]["codename"][group], workbook.add_format(format["teamformat"][group]))
        raceresult.merge_range(1, colcursor, 1, colcursor+5, "Qualiying", workbook.add_format(format["default"]["header_11"]))
        raceresult.write(2, colcursor+1, "车手", workbook.add_format(format["default"]["header_11"]))
        raceresult.write(2, colcursor+2, "圈速", workbook.add_format(format["default"]["header_11"]))
        raceresult.write(2, colcursor+3, "轮胎", workbook.add_format(format["default"]["header_11"]))

        # get quali result
        query = f'SELECT qualiResult.*, teamList.teamColor \
                FROM qualiResult LEFT JOIN teamList \
                ON qualiResult.team = teamList.teamName \
                AND qualiResult.driverGroup = teamList.driverGroup \
                WHERE qualiResult.driverGroup = "{group}" AND GP = "{gp}" \
                ORDER BY position ASC;'
        func.logging(logpath, f'Fetching qualiying data {group}-{gp}......', end="\n\n")
        print(f'Fetching qualiying data {group}-{gp}......\n')
        cursor.execute(query)
        result = cursor.fetchall()

        print(f'Writing qualiying data {group}-{gp}......')
        rowcursor = 3
        for i in range(0, len(result)):
            driver = list(result[i])
            if settings["drivergroup"]["enable_team"][group] == False:
                driver[4] = driver[0]
            # setting row height
            raceresult.set_row(rowcursor, 20)

            # Pos. / status
            if driver[7] == "FINISHED":
                raceresult.write(rowcursor, colcursor, i+1, workbook.add_format(format["default"]["header_11"]))
            else:
                if driver[7] == "RETIRED":
                    driver[7] = "RET"
                raceresult.write(rowcursor, colcursor, driver[7], workbook.add_format(format["raceresultformat"][driver[7]]))

            func.logging(logpath, f'Writing qualiying record {i+1}-{driver[3]}......')
            # drivername
            try:
                raceresult.write(rowcursor, colcursor+1, driver[3], workbook.add_format(format["driverformat"][driver[-1]]))
            except KeyError:
                if driver[4] == "Reserve":
                    driver[4] = "Reserve_leaderboard"
                raceresult.write(rowcursor, colcursor+1, driver[3], workbook.add_format(format["driverformat"][driver[4]]))
            # lap time
            if driver[5] == None or driver[5] == "None":
                driver[5] = "--:--.---"
            raceresult.write(rowcursor, colcursor+2, driver[5], workbook.add_format(format["raceresultformat"]["laptimeformat"]))
            # tyre
            try:
                raceresult.write(rowcursor, colcursor+3, driver[6], workbook.add_format(format["raceresultformat"][driver[6]]))
            except KeyError:
                raceresult.write(rowcursor, colcursor+3, "-", workbook.add_format(format["default"]["header_12"]))

            rowcursor += 1

        func.logging(logpath)
        print()

        rowcursor = maxqualicount + 4




        ##### race result #####
        # setting row height and writing header
        raceresult.set_row(rowcursor-1, 20)
        raceresult.set_row(rowcursor, 20)
        raceresult.set_row(rowcursor+1, 20)
        raceresult.merge_range(rowcursor, colcursor, rowcursor, colcursor+5, "Race", workbook.add_format(format["default"]["header_11"]))
        rowcursor += 1
        raceresult.write(rowcursor, colcursor+1, "车手", workbook.add_format(format["default"]["header_11"]))
        raceresult.write(rowcursor, colcursor+2, "差距", workbook.add_format(format["default"]["header_11"]))
        raceresult.write(rowcursor, colcursor+3, "起跑", workbook.add_format(format["default"]["header_11"]))
        raceresult.write(rowcursor, colcursor+4, "P.C.", workbook.add_format(format["default"]["header_11"]))

        # get race result
        query = f'SELECT raceResult.*, teamList.teamColor \
                FROM raceResult LEFT JOIN teamList \
                ON raceResult.team = teamList.teamName \
                AND raceResult.driverGroup = teamList.driverGroup \
                WHERE raceResult.driverGroup = "{group}" AND GP = "{gp}" \
                ORDER BY finishPosition ASC;'
        func.logging(logpath, f'Fetching race data {group}-{gp}......', end="\n\n")
        print(f'Fetching race data {group}-{gp}......\n')
        cursor.execute(query)
        result = cursor.fetchall()

        print(f'Writing race data {group}-{gp}......')
        rowcursor += 1
        for i in range(0, len(result)):
            driver = list(result[i])
            if settings["drivergroup"]["enable_team"][group] == False:
                driver[4] = driver[0]
            # setting row height
            raceresult.set_row(rowcursor, 20)

            # Pos. / status
            if driver[8] == "FINISHED":
                raceresult.write(rowcursor, colcursor, i+1, workbook.add_format(format["default"]["header_11"]))
            else:
                if driver[8] == "RETIRED":
                    driver[8] = "RET"
                raceresult.write(rowcursor, colcursor, driver[8], workbook.add_format(format["raceresultformat"][driver[8]]))

            func.logging(logpath, f'Writing race record {i+1}-{driver[3]}......')
            # drivername
            try:
                raceresult.write(rowcursor, colcursor+1, driver[3], workbook.add_format(format["driverformat"][driver[-1]]))
            except KeyError:
                if driver[4] == "Reserve":
                    driver[4] = "Reserve_leaderboard"
                raceresult.write(rowcursor, colcursor+1, driver[3], workbook.add_format(format["driverformat"][driver[4]]))
            # gap / interval
            raceresult.write(rowcursor, colcursor+2, driver[7], workbook.add_format(format["raceresultformat"]["puredata"]))
            # starting grid
            raceresult.write(rowcursor, colcursor+3, driver[5], workbook.add_format(format["raceresultformat"]["puredata"]))
            poschange = driver[2] - driver[5]
            if poschange > 0:
                raceresult.write(rowcursor, colcursor+4, f'+{poschange}', workbook.add_format(format["raceresultformat"]["posup"]))
            elif poschange == 0:
                raceresult.write(rowcursor, colcursor+4, 0, workbook.add_format(format["raceresultformat"]["poshold"]))
            elif poschange < 0:
                raceresult.write(rowcursor, colcursor+4, poschange, workbook.add_format(format["raceresultformat"]["posdown"]))

            rowcursor += 1

        func.logging(logpath, end="\n")
        print()
        
        rowcursor += 1

        ##### fastest lap #####
        # setting row height
        raceresult.set_row(rowcursor-1, 20)
        raceresult.set_row(rowcursor, 20)
        raceresult.set_row(rowcursor+1, 20)
        raceresult.set_row(rowcursor+2, 20)

        # get fastest lap data
        query = f'SELECT qualiraceFL.GP, qualiraceFL.driverGroup, qualiraceFL.raceFLdriver, \
                         raceResult.fastestLap, qualiraceFL.raceFLteam, teamList.teamColor, qualiraceFL.raceFLvalidation \
                FROM qualiraceFL JOIN raceResult \
                  ON qualiraceFL.driverGroup = raceResult.driverGroup \
                 AND qualiraceFL.GP = raceResult.GP \
                 AND qualiraceFL.raceFLdriver = raceResult.driverName \
                                LEFT JOIN teamList \
                  ON qualiraceFL.driverGroup = teamList.driverGroup \
                 AND qualiraceFL.raceFLteam = teamList.teamName \
                WHERE qualiraceFL.driverGroup = "{group}" AND qualiraceFL.GP = "{gp}";' 
        func.logging(logpath, f'Fetching race FL data {group}-{gp}......')
        # print(f'Fetching race FL data {group}-{gp}......\n')
        cursor.execute(query)
        result = cursor.fetchall()
        try:
            func.logging(logpath, f'Writing race FL data {group}-{gp}......')
            print(f'Writing race FL data {group}-{gp}......')
            racefl = list(result[0])
            if settings["drivergroup"]["enable_team"][group] == False:
                racefl[5] = racefl[1]
            # drivername
            try:
                raceresult.write(rowcursor, colcursor+1, racefl[2], workbook.add_format(format["driverformat"][racefl[5]]))
            except KeyError:
                if racefl[4] == "Reserve":
                    racefl[4] = "Reserve_leaderboard"
                raceresult.write(rowcursor, colcursor+1, racefl[2], workbook.add_format(format["driverformat"][racefl[4]]))
            # laptime
            raceresult.write(rowcursor, colcursor+2, racefl[3], workbook.add_format(format["raceresultformat"]["laptimeformat"]))
            # fl label
            raceresult.merge_range(rowcursor, colcursor+3, rowcursor, colcursor+4, 
                                    "fastest lap", workbook.add_format(format["raceresultformat"]["flLabel"]))
            # fl validation
            if racefl[6] == 0:
                raceresult.merge_range(rowcursor+1, colcursor+1, rowcursor+1, colcursor+4, 
                                        "*points will not allocated", workbook.add_format(format["raceresultformat"]["validationLabel"]))

        except IndexError:
            pass

        finally:
            func.logging(logpath)
            print()
            colcursor += 6





    ##### whole weekend #####
    func.logging(logpath, func.delimiter_string(f'Whole-{gp}', 50), end="\n\n")
    print(func.delimiter_string(f'Whole-{gp}', 50), end="\n\n")

    # setting header row height and column width
    raceresult.set_row(0, 20)
    raceresult.set_row(1, 20)
    raceresult.set_row(2, 20)
    raceresult.set_column(colcursor, colcursor, 3)
    raceresult.set_column(colcursor+1, colcursor+1, 20)
    raceresult.set_column(colcursor+2, colcursor+2, 15)
    raceresult.set_column(colcursor+3, colcursor+4, 5)
    raceresult.set_column(colcursor+5, colcursor+5, 7)

    # writing header
    raceresult.merge_range(0, colcursor, 0, colcursor+5, "Whole League", workbook.add_format(format["teamformat"][group]))
    raceresult.merge_range(1, colcursor, 1, colcursor+5, "Qualiying", workbook.add_format(format["default"]["header_11"]))
    raceresult.write(2, colcursor+1, "车手", workbook.add_format(format["default"]["header_11"]))
    raceresult.write(2, colcursor+2, "圈速", workbook.add_format(format["default"]["header_11"]))
    raceresult.write(2, colcursor+3, "轮胎", workbook.add_format(format["default"]["header_11"]))

    # get quali result
    query = f'SELECT driverGroup, GP, position, driverName, \
            team, fastestLap, tyre, driverStatus \
            FROM qualiResult \
            WHERE GP = "{gp}" \
            ORDER BY fastestLap ASC;'
    func.logging(logpath, f'Fetching qualiying data Whole-{gp}......', end="\n\n")
    print(f'Fetching qualiying data Whole-{gp}......\n')
    cursor.execute(query)
    result = cursor.fetchall()

    print(f'Writing qualiying data whole-{gp}......')
    rowcursor = 3
    for i in range(0, len(result)):
        driver = list(result[i])
        
        # setting row height
        raceresult.set_row(rowcursor, 20)

        # Pos. / status
        if driver[7] == "FINISHED":
            raceresult.write(rowcursor, colcursor, i+1, workbook.add_format(format["default"]["header_11"]))
        else:
            if driver[7] == "RETIRED":
                driver[7] = "RET"
            raceresult.write(rowcursor, colcursor, driver[7], workbook.add_format(format["raceresultformat"][driver[7]]))

        func.logging(logpath, f'Writing qualiying record {i+1}-{driver[3]}......')
        # drivername
        raceresult.write(rowcursor, colcursor+1, driver[3], workbook.add_format(format["driverformat"][driver[0]]))
        # lap time
        if driver[5] == None or driver[5] == "None":
            driver[5] = "-:--.---"
        raceresult.write(rowcursor, colcursor+2, driver[5], workbook.add_format(format["raceresultformat"]["laptimeformat"]))
        # tyre
        try:
            raceresult.write(rowcursor, colcursor+3, driver[6], workbook.add_format(format["raceresultformat"][driver[6]]))
        except KeyError:
            raceresult.write(rowcursor, colcursor+3, "-", workbook.add_format(format["default"]["header_12"]))

        rowcursor += 1
    
    func.logging(logpath, end="\n\n")
    print("\n\n")


def main(db:mysql.connector.MySQLConnection):
    cursor = db.cursor()

    # logging
    func.logging(logpath, func.delimiter_string("User downloading RaceResult Table", 60), end="\n\n")

    try:
        today = datetime.today().strftime('%Y-%m-%d')
        query = f'SELECT Round, driverGroup, GP_CHN FROM raceCalendar \
                WHERE raceStatus = "FINISHED" \
                ORDER BY raceDate DESC LIMIT 1;'
        cursor.execute(query)
        result = cursor.fetchall()
        try:
            round = int(result[0][0])
            group = result[0][1]
            gp = result[0][2]
        except IndexError:
            round = 0
            gp = "Pre-Season"
        
        # get season name/number
        leaguename = settings["default"]["leaguename"]
        seasonname = settings["default"]["seasonname"]
        

        filename = f'{leaguename} {seasonname} 成绩结算（R{round:02} {gp}）.xlsx'
        func.logging(logpath, f'Exporting Race result table to "{filename}"......', end="\n\n")
        print(f'Exporting Race result table to {filename}......\n')
        workbook = xlsxwriter.Workbook(filename)

        # get the race result list
        """
        query = 'SELECT * FROM raceCalendar \
                WHERE raceStatus = "FINISHED" \
                ORDER BY Round ASC, CASE driverGroup \
                    WHEN "A1" THEN 1 \
                    WHEN "A2" THEN 2 \
                    WHEN "A3" THEN 3 \
                    ELSE 4 \
                END, driverGroup;'
        """
        query = 'SELECT * FROM raceCalendar \
                WHERE raceStatus = "FINISHED" \
                ORDER BY Round ASC, CASE driverGroup \n'
        for i in range(0, len(settings["drivergroup"]["order"])):
            group = settings["drivergroup"]["order"][i]
            query += f'WHEN "{group}" THEN {i+1} \n'
        query += f'ELSE {len(settings["drivergroup"]["order"])+1}\n'
        query += "END, driverGroup;"

        query = 'SELECT DISTINCT(GP_ENG), GP_CHN, Round FROM raceCalendar \
                WHERE raceStatus = "FINISHED" \
                ORDER BY Round ASC;'
        print(f'Fetching race list......\n')
        cursor.execute(query)
        result = cursor.fetchall()

        for race in result:
            func.logging(logpath, func.delimiter_string(f'R{race[2]:02}-{race[0]}', 70), end="\n\n")
            print(func.delimiter_string(f'R{race[2]:02}-{race[0]}', 70), end="\n\n")
            get_raceresulttable(workbook, db, race)
        
        workbook.close()
        func.logging(logpath, f'Race result table save to file "{filename}" complete', end="\n\n\n\n\n\n")
        print(f'Race result table save to file "{filename}" complete')


    except Exception as e:
        func.logging(logpath, traceback.format_exc())
        func.logging(logpath, "Error: " + str(e), end="\n\n")
        print("错误提示：" + str(e))
        print("成绩表下载失败，推荐咨询管理员寻求解决......")



"""
if __name__ == "__main__":
    main(connectserver.connectserver("server.json", "db"))
"""
