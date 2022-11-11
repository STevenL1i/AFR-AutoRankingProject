from datetime import datetime
import json
import xlsxwriter
import connectserver
import deffunc as func

config = "server.json"

db = connectserver.connectserver(config, "league")
cursor = db.cursor()

# loading format
formatter = {}
with open("format/format.json") as format:
    formatter = json.load(format)

def get_raceresulttable(race:str, racesheet:object, workbook:object):
    query = f'SELECT DISTINCT(driverGroup) FROM raceResult \
        WHERE GP = "{race}" \
        ORDER BY case driverGroup \
            WHEN "East" THEN 1 \
            WHEN "West" THEN 2 \
            WHEN "South" THEN 3 \
            WHEN "North" THEN 4 \
            WHEN "Middle" THEN 5 \
            ELSE 6 \
        END, driverGroup;'
    cursor.execute(query)
    result = cursor.fetchall()
    grouplist = []
    for r in result:
        grouplist.append(r[0])
    
    for i in range(0, 60):
        racesheet.set_row(i, 20)
    
    # writing race result table for each group
    for i in range(0, len(grouplist)):
        group = grouplist[i]

        # setting column width
        racesheet.set_column(0+i*6, 0+i*6, 3)
        racesheet.set_column(1+i*6, 1+i*6, 20)
        racesheet.set_column(2+i*6, 2+i*6, 15)
        racesheet.set_column(3+i*6, 4+i*6, 5)
        racesheet.set_column(5+i*6, 5+i*6, 7)

        # writing header
        # .merge_range(first_row, first_col, sec_~, sec_~)
        racesheet.merge_range(0, 0+i*6, 0, 5+i*6, group, workbook.add_format(formatter["raceresult"]["header"]))
        racesheet.merge_range(1, 0+i*6, 1, 5+i*6, "Qualiying", workbook.add_format(formatter["raceresult"]["header"]))
        racesheet.merge_range(24, 0+i*6, 24, 5+i*6, "Race", workbook.add_format(formatter["raceresult"]["header"]))

        racesheet.write(2, 1+i*6, "车手", workbook.add_format(formatter["raceresult"]["header"]))
        racesheet.write(2, 2+i*6, "圈速", workbook.add_format(formatter["raceresult"]["header"]))

        racesheet.write(25, 1+i*6, "车手", workbook.add_format(formatter["raceresult"]["header"]))
        racesheet.write(25, 2+i*6, "差距", workbook.add_format(formatter["raceresult"]["header"]))
        racesheet.write(25, 3+i*6, "起跑", workbook.add_format(formatter["raceresult"]["header"]))
        racesheet.write(25, 4+i*6, "P.C.", workbook.add_format(formatter["raceresult"]["header"]))


        # writing race result details
        ### qualiying ###
        query = f'SELECT * FROM qualiResult \
                WHERE driverGroup = "{group}" AND GP = "{race}" \
                ORDER BY fastestLap ASC;'
        cursor.execute(query)
        result = cursor.fetchall()

        for pos in range(0, len(result)):
            fl = result[pos][4]
            if fl == "0.000" or fl == "9:59.999":
                fl = "-:--.---"
            racesheet.write(3+pos, 0+i*6, pos+1, workbook.add_format(formatter["raceresult"]["header"]))
            racesheet.write(3+pos, 1+i*6, result[pos][2], workbook.add_format(formatter["raceresult"]["drivername"]))
            racesheet.write(3+pos, 2+i*6, fl, workbook.add_format(formatter["raceresult"]["laptime"]))

        ### race ###

        # these are the same steps as in "pointsrecalibration"
        # creating a temp table for arranging
        query = "SHOW CREATE TABLE raceResult;"
        cursor.execute(query)
        result = cursor.fetchall()

        # create temporary table
        try:
            createquery = result[0][1].replace("raceResult", "tempraceResult")
            cursor.execute(createquery)
        except:
            pass

        # firstly clear all the records at tempraceResult table
        query = "DELETE FROM tempraceResult;"
        cursor.execute(query)
        db.commit()

        # get the original result of the race (raw result)
        query = f'SELECT * FROM raceResult \
                WHERE GP = "{race}" AND driverGroup = "{group}";'
        cursor.execute(query)
        result = cursor.fetchall()

        # copy into temp table
        for r in result:
            totaltime_sec = r[8]
            penalty = r[9]
            # also adding in-game penalty to totaltime
            realtotaltime_sec = totaltime_sec + penalty
            realtotaltime = func.second_To_laptime(realtotaltime_sec)

            query = "INSERT INTO tempraceResult VALUES \
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            val = (r[0], r[1], r[2], r[3], r[4], r[5], r[6], realtotaltime, realtotaltime_sec, 0, r[10])
            cursor.execute(query, val)
        db.commit()

        # get possible post-game penalty and adding time to driver's result
        query = f'SELECT driverName, penalty FROM raceDirector \
                WHERE driverGroup = "{group}" AND GP = "{race}";'
        cursor.execute(query)
        result = cursor.fetchall()
        for penalty in result:
            penaltytime = int(penalty[1].replace("s", "").replace("S", ""))
            query = f'UPDATE tempraceResult \
                    SET totaltime_sec = totaltime_sec + {penaltytime} \
                    WHERE driverName = "{penalty[0]}";'
            cursor.execute(query)
            db.commit()
        
        # get the final result after both in-game and post-game penalty
        query = "SELECT * FROM tempraceResult \
                ORDER BY CASE driverStatus \
                    WHEN 'DNF' THEN 1 \
                    WHEN 'RETIRED' THEN 2 \
                    WHEN 'DSQ' THEN 3 \
                    WHEN 'DNS' THEN 4 \
                END, driverStatus, \
                laps DESC, totaltime_sec ASC;"
        cursor.execute(query)
        result = cursor.fetchall()

        # writing the final race result to table
        for j in range(0, len(result)):
            pos = j+1
            driver = result[j]
            # interval = driver[8] - result[0][8]
            
            if pos == 1:
                interval = driver[7]
            elif driver[6] - result[0][6] == -1:
                interval = f'+{result[0][6] - driver[6]} Lap'
            elif driver[6] - result[0][6] < -1:
                interval = f'+{result[0][6] - driver[6]} Laps'
            else:
                interval = f'+{driver[8] - result[0][8]}'
            
            if pos == -1:
                pos = "RET"
            elif pos == -2:
                pos = "DNF"
            elif pos == -3:
                pos = "DSQ"
            elif pos == -4:
                pos = "DNS"

            racesheet.write(26+j, 0+i*6, pos, workbook.add_format(formatter["raceresult"]["header"]))
            racesheet.write(26+j, 1+i*6, driver[2], workbook.add_format(formatter["raceresult"]["drivername"]))
            racesheet.write(26+j, 2+i*6, interval, workbook.add_format(formatter["raceresult"]["interval"]))
            racesheet.write(26+j, 3+i*6, driver[4], workbook.add_format(formatter["raceresult"]["default"]))
            if driver[4] - pos > 0:
                racesheet.write(26+j, 4+i*6, driver[4]-pos, workbook.add_format(formatter["raceresult"]["posup"]))
            elif driver[4] - pos < 0:
                racesheet.write(26+j, 4+i*6, driver[4]-pos, workbook.add_format(formatter["raceresult"]["posdown"]))
            elif driver[4] - pos == 0:
                racesheet.write(26+j, 4+i*6, driver[4]-pos, workbook.add_format(formatter["raceresult"]["poshold"]))

def main():
    today = datetime.today().strftime('%Y-%m-%d')
    query = f'SELECT Round, driverGroup, GP_CHN FROM raceCalendar \
            WHERE raceStatus = "FINISHED" \
            ORDER BY raceDate DESC LIMIT 1;'
    cursor.execute(query)
    result = cursor.fetchall()
    try:
        result = result[0]
        round = int(result[0])
        race_group = result[1]
        race_name = result[2]
        round = f'{round:02}'
    except IndexError:
        round = "00"
        race_name = "Pre-Season"

    # get season name/number
    with open(config, "r") as server:
        servercfg = json.load(server)

    seasonname = servercfg["league"].split("_")[1].upper()

    workbook = xlsxwriter.Workbook(f'SVS {seasonname} 数据分析（R{round} {race_group}_{race_name}）.xlsx')
    # create the worksheet for each race
    query = "SELECT DISTINCT(GP_ENG) FROM raceCalendar WHERE raceStatus != 'SEASON BREAK';"
    cursor.execute(query)
    result = cursor.fetchall()
    race = []
    for r in result:
        race.append(r[0])
    raceresult_sheet = []
    for r in race:
        raceresult_sheet.append(workbook.add_worksheet(r))

    for i in range(0, len(race)):
        get_raceresulttable(race[i], raceresult_sheet[i], workbook)
    
    workbook.close()
