import math, csv, json, datetime, traceback
import tkinter
from tkinter import filedialog
import mysql.connector
import dbconnect
import xlsxwriter






def standard_deviation(data:list) -> int:
    total = 0
    avgl = sum(data) / len(data)
    for i in range(0, len(data)):
        total += pow(data[i] - avgl, 2)
    sd = math.sqrt(total / len(data))

    return sd



def upload_tt(db:mysql.connector.MySQLConnection):
    cursor = db.cursor()

    root = tkinter.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename()

    with open(filepath) as tt_data:
        reader = csv.DictReader(tt_data)

        count = 0
        for row in reader:
            drivername = row.get("driverName")
            circuit = row.get("circuit")
            s1 = row.get("sector_1")
            s2 = row.get("sector_2")
            s3 = row.get("sector_3")
            lt_str = row.get("Laptime_str")

            if drivername.replace(" ","") == "" and circuit.replace(" ","") == "" \
            and s1.replace(" ","") == "" and s2.replace(" ","") == "" \
            and s3.replace(" ","") == "" and lt_str.replace(" ","") == "":
                continue

            count += 1
            print(f'uploading row {count}......')

            lt = datetime.datetime.strptime(lt_str, '%M:%S.%f')
            lt.microsecond
            lt = lt.minute * 60 + lt.second + lt.microsecond / 1000000

            try:
                query = "INSERT INTO tt VALUES (%s, %s, %s, %s, %s, %s, %s)"
                val = (drivername, circuit, s1, s2, s3, lt, lt_str)
                cursor.execute(query, val)
            except mysql.connector.errors.IntegrityError as e:
                if str(e).find("Duplicate entry") != -1 and str(e).find("tt.PRIMARY") != -1:
                    query = f'UPDATE tt \
                            SET driverName = "{drivername}", \
                                circuit = "{circuit}", \
                                sector_1 = "{s1}", \
                                sector_2 = "{s2}", \
                                sector_3 = "{s3}", \
                                Laptime = "{lt}", \
                                Laptime_str = "{lt_str}" \
                            WHERE driverName = "{drivername}" AND circuit = "{circuit}";'
                    cursor.execute(query)
                else:
                    raise mysql.connector.errors.IntegrityError(e)

        db.commit()



def upload_eval(db:mysql.connector.MySQLConnection):
    cursor = db.cursor()
    
    root = tkinter.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename()

    with open(filepath) as eval_data:
        reader = csv.DictReader(eval_data)

        count = 0
        for row in reader:
            drivername = row.get("driverName")
            lap = row.get("Lap")
            lt_str = row.get("Laptime_str")
            tyre = row.get("Tyre")
            status = row.get("Status")

            if drivername.replace(" ","") == "" and lap.replace(" ","") == "" \
            and lt_str.replace(" ","") == "" and tyre.replace(" ","") == "" \
            and status.replace(" ","") == "":
                continue
            
            count += 1
            print(f'uploading row {count}......')

            lt = datetime.datetime.strptime(lt_str, '%M:%S.%f')
            lt.microsecond
            lt = lt.minute * 60 + lt.second + lt.microsecond / 1000000

            try:
                query = "INSERT INTO evalrace VALUES (%s, %s, %s, %s, %s, %s)"
                val = (drivername, lap, lt, lt_str, tyre, status)
                cursor.execute(query, val)
            except mysql.connector.errors.IntegrityError as e:
                if str(e).find("Duplicate entry") != -1 and str(e).find("evalrace.PRIMARY") != -1:
                    query = f'UPDATE evalrace \
                            SET driverName = "{drivername}", \
                                Lap = "{lap}", \
                                Laptime = "{lt}", \
                                Laptime_str = "{lt_str}", \
                                tyre = "{tyre}", \
                                status = "{status}" \
                            WHERE driverName = "{drivername}" AND Lap = "{lap}";'
                    cursor.execute(query)
                else:
                    raise mysql.connector.errors.IntegrityError(e)

        db.commit()





def analyse_tt(db:mysql.connector.MySQLConnection, circuitlist:list,
               workbook:xlsxwriter.Workbook,
               tt1:xlsxwriter.workbook.Worksheet,
               tt2:xlsxwriter.workbook.Worksheet,
               tt3:xlsxwriter.workbook.Worksheet,
               quali:xlsxwriter.workbook.Worksheet):
    cursor = db.cursor()

    worksheet = [tt1, tt2, tt3, quali]
    for i in range(0, len(circuitlist)):
        query = f'SELECT * FROM tt WHERE circuit = "{circuitlist[i]}" ORDER BY Laptime ASC'
        # driverName, circuit, sector_1, sector_2, sector_3, totaltime, totaltime_str
        cursor.execute(query)
        result = cursor.fetchall()

        # set column and row width
        for r in range(0, 300):
            worksheet[i].set_row(r, 16)
        worksheet[i].set_column(0, 0, 4)
        worksheet[i].set_column(1, 1, 20)
        worksheet[i].set_column(2, 2, 10)
        worksheet[i].set_column(3, 3, 6)
        worksheet[i].set_column(4, 4, 10)
        worksheet[i].set_column(5, 5, 6)
        worksheet[i].set_column(6, 6, 10)
        worksheet[i].set_column(7, 7, 6)
        worksheet[i].set_column(8, 8, 13)

        name = []
        s1_list = []
        s2_list = []
        s3_list = []
        s1_list_asc = []
        s2_list_asc = []
        s3_list_asc = []
        tt = []
        for lap in result:
            lap = list(lap)
            name.append(lap[0])
            s1_list.append(float(lap[2]))
            s1_list_asc.append(float(lap[2]))
            s2_list.append(float(lap[3]))
            s2_list_asc.append(float(lap[3]))
            s3_list.append(float(lap[4]))
            s3_list_asc.append(float(lap[4]))
            tt.append(lap[-1])
        s1_list_asc.sort()
        s2_list_asc.sort()
        s3_list_asc.sort()

        format = workbook.add_format({"font_size": 11})
        format.set_font_name("Dengxian")
        format.set_align("vcenter")
        format.set_text_wrap(True)
        worksheet[i].write(0, 0, "", format)
        worksheet[i].write(0, 1, "车手id", format)
        worksheet[i].write(0, 2, "S1", format)
        worksheet[i].write(0, 3, "S1.no.", format)
        worksheet[i].write(0, 4, "S2", format)
        worksheet[i].write(0, 5, "S2.no.", format)
        worksheet[i].write(0, 6, "S3", format)
        worksheet[i].write(0, 7, "S3.no.", format)
        worksheet[i].write(0, 8, "圈速", format)

        col = 1
        row = 1
        for x in range(0, len(tt)):
            worksheet[i].write(row, 0, x+1, format)
            worksheet[i].write(row, col, name[x], format)
            worksheet[i].write(row, col + 1, s1_list[x], format)
            worksheet[i].write(row, col + 2, s1_list_asc.index(s1_list[x]) + 1, format)
            worksheet[i].write(row, col + 3, s2_list[x], format)
            worksheet[i].write(row, col + 4, s2_list_asc.index(s2_list[x]) + 1, format)
            worksheet[i].write(row, col + 5, s3_list[x], format)
            worksheet[i].write(row, col + 6, s3_list_asc.index(s3_list[x]) + 1, format)
            worksheet[i].write(row, col + 7, tt[x], format)
            row += 1


def analyse_tt_all(db:mysql.connector.MySQLConnection, circuitlist:list,
                   workbook:xlsxwriter.Workbook,
                   tt_all:xlsxwriter.workbook.Worksheet):
    cursor = db.cursor()
    
    # set column and row width
    for r in range(0, 100):
        tt_all.set_row(r, 16)
    tt_all.set_column(0, 0, 4)
    tt_all.set_column(1, 1, 20)
    tt_all.set_column(2, 2, 10)
    tt_all.set_column(3, 3, 4)
    tt_all.set_column(4, 4, 10)
    tt_all.set_column(5, 5, 4)
    tt_all.set_column(6, 6, 10)
    tt_all.set_column(7, 7, 4)
    tt_all.set_column(8, 8, 13)

    # writing header
    format = workbook.add_format({"font_size": 11})
    format.set_font_name("Dengxian")
    format.set_align("vcenter")
    format.set_text_wrap()
    tt_all.write(0, 0, "", format)
    tt_all.write(0, 1, "车手id", format)
    tt_all.write(0, 2, circuitlist[0], format)
    tt_all.write(0, 3, "排名", format)
    tt_all.write(0, 4, circuitlist[1], format)
    tt_all.write(0, 5, "排名.", format)
    tt_all.write(0, 6, circuitlist[2], format)
    tt_all.write(0, 7, "排名", format)
    tt_all.write(0, 8, "总圈速", format)
    
    # get driverlist
    query = f'SELECT driverName, SUM(Laptime) FROM tt WHERE circuit != "{circuitlist[-1]}" \
            GROUP BY driverName ORDER BY SUM(Laptime);'
    cursor.execute(query)
    result = cursor.fetchall()
    driverlist = []
    for temp in result:
        driverlist.append(temp[0])

        
    # get ranking for each circuit
    query = f'SELECT driverName, Laptime FROM tt WHERE circuit = "{circuitlist[0]}" ORDER BY Laptime;'
    cursor.execute(query)
    france = cursor.fetchall()
    france_no = []
    for temp in france:
        france_no.append(temp[0])

    query = f'SELECT driverName, Laptime FROM tt WHERE circuit = "{circuitlist[1]}" ORDER BY Laptime;'
    cursor.execute(query)
    hungary = cursor.fetchall()
    hungary_no = []
    for temp in hungary:
        hungary_no.append(temp[0])

    query = f'SELECT driverName, Laptime FROM tt WHERE circuit = "{circuitlist[2]}" ORDER BY Laptime;'
    cursor.execute(query)
    russia = cursor.fetchall()
    russia_no = []
    for temp in russia:
        russia_no.append(temp[0])

    row = 1
    for driver in driverlist:
        query = f'SELECT driverName, circuit, Laptime, Laptime_str FROM tt \
                WHERE driverName = "{driver}" AND circuit != "France_quali" \
                ORDER BY CASE circuit \
                    WHEN "{circuitlist[0]}" THEN 1 \
                    WHEN "{circuitlist[1]}" THEN 2 \
                    WHEN "{circuitlist[2]}" THEN 3 \
                    ELSE 4 \
                    END, circuit;'
        cursor.execute(query)
        result = cursor.fetchall()

        totaltime = france[france_no.index(driver)][1] + \
                    hungary[hungary_no.index(driver)][1] + \
                    russia[russia_no.index(driver)][1]

        tt_all.write(row, 0, row, format)
        tt_all.write(row, 1, driver, format)
        tt_all.write(row, 2, result[0][3], format)
        tt_all.write(row, 3, france_no.index(driver)+1, format)
        tt_all.write(row, 4, result[1][3], format)
        tt_all.write(row, 5, hungary_no.index(driver)+1, format)
        tt_all.write(row, 6, result[2][3], format)
        tt_all.write(row, 7, russia_no.index(driver)+1, format)
        tt_all.write(row, 8, totaltime, format)

        row += 1


def analyse_quali(db:mysql.connector.MySQLConnection, circuitlist:list,
                  workbook:xlsxwriter.Workbook,
                  compare:xlsxwriter.workbook.Worksheet):
    cursor = db.cursor()

    # setting column and row width
    for r in range(0, 100):
        compare.set_row(r, 16)
    compare.set_column(0, 0, 4)
    compare.set_column(1, 1, 20)
    compare.set_column(2, 3, 10)
    compare.set_column(4, 4, 8)
    compare.set_column(5, 6, 10)
    compare.set_column(7, 7, 8)
    compare.set_column(8, 9, 10)
    compare.set_column(10, 10, 8)
    compare.set_column(11, 12, 13)
    compare.set_column(13, 13, 10)


    # get the driver list
    query = f'SELECT driverName FROM tt WHERE circuit = "{circuitlist[-1]}"'
    cursor.execute(query)
    result = cursor.fetchall()
    driverlist = []
    for i in range(0, len(result)):
        driverlist.append(result[i][0])

    # write the header
    format = workbook.add_format({"font_size": 11})
    format.set_font_name("Dengxian")
    format.set_align("vcenter")
    format.set_text_wrap()

    compare.write(0, 1, "车手id", format)
    compare.write(0, 2, "S1_TT", format)
    compare.write(0, 3, "S1_quali", format)
    compare.write(0, 4, "S1_delta", format)
    compare.write(0, 5, "S2_TT", format)
    compare.write(0, 6, "S2_quali", format)
    compare.write(0, 7, "S2_delta", format)
    compare.write(0, 8, "S3_TT", format)
    compare.write(0, 9, "S3_quali", format)
    compare.write(0, 10, "S3_delta", format)
    compare.write(0, 11, "圈速_TT", format)
    compare.write(0, 12, "圈速_quali", format)
    compare.write(0, 13, "圈速_delta", format)

    for i in range(0, len(driverlist)):
        compare.write(i+1, 0, i+1, format)

    row = 1
    for driver in driverlist:

        query = f'SELECT * FROM tt WHERE driverName = "{driver}" and circuit = "{circuitlist[-1]}"'
        cursor.execute(query)
        result_quali = cursor.fetchall()
        drivername = result_quali[0][0]
        s1_quali = result_quali[0][2]
        s2_quali = result_quali[0][3]
        s3_quali = result_quali[0][4]
        laptime_quali = result_quali[0][-2]
        laptime_quali_str = result_quali[0][-1]

        compare.write(row, 1, drivername, format)
        compare.write(row, 3, s1_quali, format)
        compare.write(row, 6, s2_quali, format)
        compare.write(row, 9, s3_quali, format)
        compare.write(row, 12, laptime_quali_str, format)

        query = f'SELECT * FROM tt WHERE drivername = "{driver}" and circuit = "{circuitlist[-1].split("_")[0]}";'
        cursor.execute(query)
        result_tt = cursor.fetchall()
        if len(result_tt) == 0:
            row += 1
            continue
        s1_tt = result_tt[0][2]
        s2_tt = result_tt[0][3]
        s3_tt = result_tt[0][4]
        laptime_tt = result_tt[0][-2]
        laptime_tt_str = result_tt[0][-1]

        compare.write(row, 2, s1_tt, format)
        compare.write(row, 5, s2_tt, format)
        compare.write(row, 8, s3_tt, format)
        compare.write(row, 11, laptime_tt_str, format)

        s1_delta = float(s1_tt) - float(s1_quali)
        s2_delta = float(s2_tt) - float(s2_quali)
        s3_delta = float(s3_tt) - float(s3_quali)
        laptime_delta = float(laptime_tt) - float(laptime_quali)

        format_delta = workbook.add_format({"font_size": 11})
        format_delta.set_font_name("Dengxian")
        format_delta.set_align("vcenter")
        format_delta.set_text_wrap()

        if s1_delta > 0:
            s1_delta = "+" + f'{s1_delta:.3f}'
            format_delta.set_bg_color("#FF0000")
        else:
            s1_delta = f'{s1_delta:.3f}'
            format_delta.set_bg_color("#00FF00")
        if s2_delta > 0:
            s2_delta = "+" + f'{s2_delta:.3f}'
            format_delta.set_bg_color("#FF0000")
        else:
            s2_delta = f'{s2_delta:.3f}'
            format_delta.set_bg_color("#00FF00")
        if s3_delta > 0:
            s3_delta = "+" + f'{s3_delta:.3f}'
            format_delta.set_bg_color("#FF0000")
        else:
            s3_delta = f'{s3_delta:.3f}'
            format_delta.set_bg_color("#00FF00")
        if laptime_delta > 0:
            laptime_delta = "+" + f'{laptime_delta:.3f}'
            format_delta.set_bg_color("#FF0000")
        else:
            laptime_delta = f'{laptime_delta:.3f}'
            format_delta.set_bg_color("#00FF00")

        compare.write(row, 4, s1_delta, format_delta)
        compare.write(row, 7, s2_delta, format_delta)
        compare.write(row, 10, s3_delta, format_delta)
        compare.write(row, 13, laptime_delta, format_delta)

        del format_delta
        row += 1


def analyse_eval(db:mysql.connector.MySQLConnection,
                 workbook:xlsxwriter.Workbook,
                 eval:xlsxwriter.workbook.Worksheet):
    cursor = db.cursor()

    # setting column and row width
    for r in range(0, 100):
        eval.set_row(r, 16)
    eval.set_column(0, 0, 4)
    eval.set_column(1, 1, 20)
    eval.set_column(2, 5, 13)
    eval.set_column(6, 6, 12)
    eval.set_column(7, 7, 6)
    eval.set_column(8, 10, 8)

    # write the header
    format = workbook.add_format({"font_size": 11})
    format.set_font_name("Dengxian")
    format.set_align("vcenter")
    format.set_text_wrap()

    eval.write(0, 0, "Stint", format)
    eval.write(0, 1, "车手id", format)
    eval.write(0, 2, "最快圈速", format)
    eval.write(0, 3, "最慢圈速", format)
    eval.write(0, 4, "delta", format)
    eval.write(0, 5, "平均圈速", format)
    eval.write(0, 6, "stint标准差", format)
    eval.write(0, 7, "轮胎", format)
    eval.write(0, 8, "总圈数", format)
    eval.write(0, 9, "有效圈数", format)
    eval.write(0, 10, "spin圈数", format)


    # get the driver list
    query = "SELECT DISTINCT(driverName) FROM evalrace"
    cursor.execute(query)
    result = cursor.fetchall()
    driverlist = []
    for i in range(0, len(result)):
        driverlist.append(result[i][0])

    row = 1
    for driver in driverlist:
        eval.write(row, 1, driver, format)

        inlap = []; outlap = [1]
        query = f'SELECT Lap FROM evalrace WHERE Status = "IN LAP" AND driverName = "{driver}"'
        cursor.execute(query)
        result = cursor.fetchall()
        for i in range(0, len(result)):
            inlap.append(result[i][0])
        
        query = f'SELECT MAX(Lap) FROM evalrace'
        cursor.execute(query)
        result = cursor.fetchall()
        inlap.append(result[0][0]+1)

        query = f'SELECT Lap FROM evalrace WHERE Status = "OUT LAP" AND driverName = "{driver}"'
        cursor.execute(query)
        result = cursor.fetchall()
        for i in range(0, len(result)):
            outlap.append(result[i][0])

        for stint in range(1, len(inlap)+1):
            eval.write(row, 1, driver, format)

            query = f'SELECT Laptime, Laptime_str, Tyre FROM evalrace WHERE driverName = "{driver}" \
            AND Status = "ON TRACK" AND Lap > {outlap[stint-1]} AND Lap < {inlap[stint-1]}'
            cursor.execute(query)
            result = cursor.fetchall()

            laptime = []
            laptime_str = []
            tyre = ""
            for r in result:
                r = list(r)
                laptime.append(float(r[0]))
                laptime_str.append(r[1])
                tyre = r[2]

            if len(laptime) == 0:
                continue

            laptime_sorted = sorted(laptime)
            fl_str = laptime_str[laptime.index(laptime_sorted[0])]
            sl_str = laptime_str[laptime.index(laptime_sorted[-1])]
            delta = laptime_sorted[0] - laptime_sorted[-1]
            avgl = sum(laptime) / len(laptime)
            avgl_str = str(datetime.timedelta(seconds = avgl))[3:-3]
            sd = standard_deviation(laptime)

            format_sd = workbook.add_format({"font_size": 11})
            format_sd.set_font_name("Dengxian")
            format_sd.set_align("vcenter")
            format_sd.set_text_wrap()
            if sd <= 0.25:
                format_sd.set_bg_color("#FFFF00")
            elif sd > 0.25 and sd <= 0.5:
                format_sd.set_bg_color("#00FF00")
            elif sd > 0.8:
                format_sd.set_bg_color("#FF0000")

            eval.write(row, 0, stint, format)
            eval.write(row, 2, fl_str, format)
            eval.write(row, 3, sl_str, format)
            eval.write(row, 4, delta, format)
            eval.write(row, 5, avgl_str, format)
            eval.write(row, 6, sd, format_sd)
            eval.write(row, 7, tyre, format)
            eval.write(row, 9, len(laptime), format)

            del format_sd

            """
            query = f'SELECT Lap FROM evalrace WHERE driverName = "{driver}" \
                    AND Lap > {outlap[stint - 1]} AND Lap < {inlap[stint - 1]}'
            cursor.execute(query)
            result = cursor.fetchall()
            """
            eval.write(row, 8, (int(inlap[stint-1]) - int(outlap[stint-1]) - 1), format)

            query = f'SELECT Lap FROM evalrace WHERE driverName = "{driver}" \
                    AND Status = "SPIN" AND Lap > {outlap[stint - 1]} AND Lap < {inlap[stint - 1]}'
            cursor.execute(query)
            result = cursor.fetchall()
            eval.write(row, 10, len(result), format)
            row += 1


def analyse_eval2(db:mysql.connector.MySQLConnection,
                  workbook:xlsxwriter.Workbook,
                  eval2:xlsxwriter.workbook.Worksheet):
    cursor = db.cursor()
    # setting column and row width
    for r in range(0, 100):
        eval2.set_row(r, 16)
    eval2.set_column(0, 0, 4)
    eval2.set_column(1, 1, 20)
    eval2.set_column(2, 6, 13)
    eval2.set_column(7, 7, 7)
    eval2.set_column(8, 9, 8)
    
    # write the header
    format = workbook.add_format({"font_size": 11})
    format.set_font_name("Dengxian")
    format.set_align("vcenter")
    format.set_text_wrap()
    
    eval2.write(0, 0, "No.", format)
    eval2.write(0, 1, "车手id", format)
    eval2.write(0, 2, "最快圈速", format)
    eval2.write(0, 3, "最慢圈速", format)
    eval2.write(0, 4, "delta", format)
    eval2.write(0, 5, "平均圈速", format)
    eval2.write(0, 6, "总用时", format)
    eval2.write(0, 7, "轮胎", format)
    eval2.write(0, 8, "有效圈数", format)
    eval2.write(0, 9, "spin圈数", format)


    # get the driver list
    query = "SELECT DISTINCT(driverName) FROM evalrace;"
    cursor.execute(query)
    driverlist = cursor.fetchall()

    row = 1
    for driver in driverlist:
        driver = driver[0]
        
        query = f'SELECT * FROM evalrace WHERE driverName = "{driver}" \
                AND status != "OUT LAP" AND status != "IN LAP" \
                ORDER BY Lap ASC;'
        cursor.execute(query)
        result = cursor.fetchall()

        fl = float(result[0][2])
        sl = float(result[0][2])
        tyre = result[0][4]
        alltyre = result[0][4]
        totaltime = 0
        validlap = 0
        spinlap = 0
        for i in range(0, len(result)):
            # result[i] = (drivername, lap, lt:str, ltstr, tyre, status)
            lt = float(result[i][2])
            if result[i][5] != "SPIN":
                if lt <= fl:
                    fl = float(result[i][2])
                if lt >= sl:
                    sl = float(result[i][2])
                totaltime += float(result[i][2])
                validlap += 1
            
            if result[i][5] == "SPIN":
                
                spinlap += 1

            if tyre != result[i][4]:
                tyre = result[i][4]
                alltyre += tyre
        
        fl_str = f'{int(fl/60)}:{fl - int(fl/60)*60:06.3f}'
        sl_str = f'{int(sl/60)}:{sl - int(sl/60)*60:06.3f}'
        tt_str = f'{int(totaltime/60)}:{totaltime - int(totaltime/60)*60:06.3f}'
        delta = fl - sl
        delta_str = f'{delta:.3f}'
        avglap = totaltime / validlap
        avglap_str = f'{int(avglap/60)}:{avglap - int(avglap/60)*60:06.3f}'

        eval2.write(row, 1, driver, format)
        eval2.write(row, 2, fl_str, format)
        eval2.write(row, 3, sl_str, format)
        eval2.write(row, 4, delta_str, format) # delta
        eval2.write(row, 5, avglap_str, format) # avg
        eval2.write(row, 6, tt_str, format)
        eval2.write(row, 7, alltyre, format)
        eval2.write(row, 8, validlap, format) # valid lap
        eval2.write(row, 9, spinlap, format) # spin lap

        row += 1



def analysis(db:mysql.connector.MySQLConnection):
    cursor = db.cursor()

    with open("server.json") as server:
        servercfg = json.load(server)

    dbname = servercfg["db"]
    season = dbname.split("_")[1].upper()

    query = "SELECT DISTINCT(circuit) FROM tt;"
    cursor.execute(query)
    result = cursor.fetchall()


    for circuit in result:
        if len(circuit[0].split("_")) > 1:
            result.append(circuit)
            result.remove(circuit)
            break

    circuitlist = []
    for circuit in result:
        circuitlist.append(circuit[0])

    # create excel file
    workbook = xlsxwriter.Workbook(f'AFR {season} Pre-Season tesing analysis.xlsx')
    tt1 = workbook.add_worksheet(circuitlist[0])
    tt2 = workbook.add_worksheet(circuitlist[1])
    tt3 = workbook.add_worksheet(circuitlist[2])
    tt_all = workbook.add_worksheet("TT_all")
    quali = workbook.add_worksheet(circuitlist[3])
    compare = workbook.add_worksheet("compare")
    eval = workbook.add_worksheet("race")
    eval2 = workbook.add_worksheet("race v2.0")

    analyse_tt(db, circuitlist, workbook, tt1,tt2,tt3,quali)
    analyse_quali(db, circuitlist, workbook, compare)
    analyse_tt_all(db, circuitlist, workbook, tt_all)
    analyse_eval(db, workbook, eval)
    analyse_eval2(db, workbook, eval2)
    workbook.close()






def main():
    db = dbconnect.connect_with_conf("server.json", "db")

    while True:
        print("Welcome to AFR evaluation analysier")
        print()
        print("1.Upload TT")
        print("2.Upload Eval. race")
        print("3.Download Analysis")
        print("4.Create new database")
        print()
        print("0.exit")
        print()
        choices = input("Your choice： ")
        choices_list = choices.split(" ")
        for choice in choices_list:
            if choice == "1":
                try:
                    upload_tt(db)
                except Exception as e:
                    print(traceback.format_exc() + "\n" + str(e) + "\n")
                finally:
                    input("press enter back to main menu")
            
            elif choice == "2":
                try:
                    upload_eval(db)
                except Exception as e:
                    print(traceback.format_exc() + "\n" + str(e) + "\n")
                finally:
                    input("press enter back to main menu")
            
            elif choice == "3":
                try:
                    analysis(db)
                except Exception as e:
                    print(traceback.format_exc() + "\n" + str(e) + "\n")
                finally:
                    input("press enter back to main menu")

            elif choice == "0":
                input("press enter to exit")
                exit(0)




if __name__ == "__main__":
    main()
