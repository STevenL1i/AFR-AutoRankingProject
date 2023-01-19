import csv, json, tkinter, traceback
from datetime import datetime
from tkinter import filedialog

import deffunc as func
import mysql.connector

settingsf = open("settings/settings.json", "r", encoding='utf-8')
settings:dict = json.load(settingsf)
settingsf.close()
logpath = settings["default"]["log"]

# upload qualiying result
def upload_quali(db:mysql.connector.MySQLConnection):
    # db = connectserver.connectserver("server.json", "db")
    cursor = db.cursor()

    try:
        func.logging(logpath, func.delimiter_string("User uploading qualiying data", 60), end="\n\n\n")
        root = tkinter.Tk()
        root.withdraw()
        filepath = filedialog.askopenfilename()

        qualif = open(filepath, "r")
        reader = csv.DictReader(qualif)

        record = 0
        report = {"success":0, "failed":0, "update":0}
        for row in reader:
            drivergroup = row.get("driverGroup")
            gp = row.get("GP")
            position = row.get("position")
            drivername = row.get("driverName")
            team = row.get("team")
            fl = row.get("fastestLap")
            tyre = row.get("tyre")
            status = row.get("driverStatus")

            if drivergroup.replace(" ","") == "" and gp.replace(" ","") == "" and position.replace(" ","") == "" \
            and drivername.replace(" ","") == "" and team.replace(" ","") == "" and fl.replace(" ","") == "" \
            and tyre.replace(" ","") == "" and status.replace(" ","") == "":
                break

            if fl.replace(" ","") == '':
                fl = None
            if tyre.replace(" ","") == '':
                tyre = None
            
            record += 1

            try:
                query = "INSERT INTO qualiResult VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
                val = (drivergroup, gp, position, drivername, team, fl, tyre, status)
                func.logging(logpath, f'UPLOAD: qualiresult {drivergroup}-{gp}-{position}-{drivername}......')
                print(f'UPLOAD: qualiresult {drivergroup}-{gp}-{position}-{drivername}......')
                cursor.execute(query, val)

                report["success"] += 1

            except mysql.connector.errors.IntegrityError as e:
                # duplicate:
                # Duplicate entry 'A1-Bahrain-1' for key 'qualiResult.PRIMARY'
                if str(e).find("Duplicate entry") != -1 and str(e).find("qualiResult.PRIMARY") != -1:
                    func.logging(logpath, f'WARNING: Quali record {drivergroup}-{gp}-{position} already exist......')
                    if tyre != None:
                        tyre = "\"" + tyre + "\""
                    else:
                        tyre = "null"
                    query = f'UPDATE qualiResult \
                            SET driverName = "{drivername}", \
                                team = "{team}", \
                                fastestLap = "{fl}", \
                                tyre = {tyre}, \
                                driverStatus = "{status}" \
                            WHERE driverGroup = "{drivergroup}" AND GP = "{gp}" AND position = "{position}";'
                    func.logging(logpath, f'UPDATE: {drivergroup}-{gp}-{position}-{drivername}......', end="\n\n")
                    print(f'UPDATE: {drivergroup}-{gp}-{position}-{drivername}......\n')
                    cursor.execute(query)

                    report["update"] += 1
                
                # foreign key:
                # Cannot add or update a child row: a foreign key constraint fails 
                # (`afr_s10`.`qualiResult`, CONSTRAINT `qualiResult_FK1` FOREIGN KEY (`driverName`) 
                # REFERENCES `driverList` (`driverName`) ON DELETE CASCADE ON UPDATE CASCADE)
                elif str(e).find("foreign key constraint") != -1:
                    func.logging(logpath, f'ERROR: drivername {drivername} doesn\'t find/match in driverlist', end="\n\n")
                    print(f'ERROR: drivername {drivername} doesn\'t find/match in driverlist\n')
                    report["failed"] += 1


        db.commit()
        qualif.close()

        func.logging(logpath)
        func.logging(logpath, f'排位成绩上传报告（共{record}条）:')
        func.logging(logpath, f'    {report["success"]:<3}条成绩新增')
        func.logging(logpath, f'    {report["update"]:<3}条成绩更新')
        func.logging(logpath, f'    {report["failed"]:<3}条上传失败，请查看日志信息')
        func.logging(logpath, "排位成绩上传完成，稍后请记得将文件上传到赛会群备份", end="\n\n\n\n\n\n")
        
        print()
        print(f'排位成绩上传报告（共{record}条）:')
        print(f'    {report["success"]:<3}条成绩新增')
        print(f'    {report["update"]:<3}条成绩更新')
        print(f'    {report["failed"]:<3}条上传失败，请查看日志信息')
        print("排位成绩上传完成，稍后请记得将文件上传到赛会群备份")


    except Exception as e:
        func.logging(logpath, traceback.format_exc())
        func.logging(logpath, "Error: " + str(e), end="\n\n")
        print("错误提示：" + str(e))
        print("数据上传失败，请检查上传文件数据是否正确，或查看日志咨询管理员")



# upload race result
def upload_race(db:mysql.connector.MySQLConnection):
    # db = connectserver.connectserver("server.json", "db")
    cursor = db.cursor()

    try:
        func.logging(logpath, func.delimiter_string("User uploading race data", 60), end="\n\n\n")
        root = tkinter.Tk()
        root.withdraw()
        filepath = filedialog.askopenfilename()

        racef = open(filepath, "r")
        reader = csv.DictReader(racef)

        record = 0
        report = {"success":0, "failed":0, "update":0}
        uploadracelist = []
        for row in reader:
            drivergroup = row.get("driverGroup")
            gp = row.get("GP")
            finishposition = row.get("finishPosition")
            drivername = row.get("driverName")
            team = row.get("team")
            startposition = row.get("startPosition")
            fl = row.get("fastestLap")
            gap = row.get("gap")
            status = row.get("driverStatus")

            if drivergroup.replace(" ","") == "" and gp.replace(" ","") == "" and finishposition.replace(" ","") == "" \
            and drivername.replace(" ","") == "" and team.replace(" ","") == "" and startposition.replace(" ","") == "" \
            and gap.replace(" ","") == "" and status.replace(" ","") == "" and fl.replace(" ","") == "":
                break

            if fl.replace(" ","") == '':
                fl = None
            
            record += 1

            try:
                query = "INSERT INTO raceResult VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
                val = (drivergroup, gp, finishposition, drivername, team, startposition, fl, gap, status)
                func.logging(logpath, f'UPLOAD: raceresult {drivergroup}-{gp}-{finishposition}-{drivername}......')
                print(f'UPLOAD: raceresult {drivergroup}-{gp}-{finishposition}-{drivername}......')
                cursor.execute(query, val)

                report["success"] += 1
            
            except mysql.connector.errors.IntegrityError as e:
                # duplicate:
                # Duplicate entry 'A1-Bahrain-1' for key 'raceResult.PRIMARY'
                if str(e).find("Duplicate entry") != -1 and str(e).find("raceResult.PRIMARY") != -1:
                    func.logging(logpath, f'WARNING: Race record {drivergroup}-{gp}-{finishposition} already exist......')
                    query = f'UPDATE raceResult \
                            SET driverName = "{drivername}", \
                                team = "{team}", \
                                startPosition = "{startposition}", \
                                fastestLap = "{fl}", \
                                gap = "{gap}", \
                                driverStatus = "{status}" \
                            WHERE driverGroup = "{drivergroup}" AND GP = "{gp}" AND finishPosition = "{finishposition}";'
                    func.logging(logpath, f'UPDATE: {drivergroup}-{gp}-{finishposition}-{drivername}......', end="\n\n")
                    print(f'UPDATE: {drivergroup}-{gp}-{finishposition}-{drivername}......\n')
                    cursor.execute(query)

                    report["update"] += 1
                
                # foreign key:
                # Cannot add or update a child row: a foreign key constraint fails 
                # (`afr_s10`.`raceResult`, CONSTRAINT `raceResult_FK1` FOREIGN KEY (`driverName`) 
                # REFERENCES `driverList` (`driverName`) ON DELETE CASCADE ON UPDATE CASCADE)
                elif str(e).find("foreign key constraint") != -1:
                    func.logging(logpath, f'ERROR: drivername {drivername} doesn\'t find/match in driverlist', end="\n\n")
                    print(f'ERROR: drivername {drivername} doesn\'t find/match in driverlist\n')
                    report["failed"] += 1
            
            
            therace = [drivergroup, gp]
            if (therace in uploadracelist) == False:
                uploadracelist.append(therace)

        
        # update race status
        for race in uploadracelist:
            drivergroup = race[0]
            gp = race[1]
            query = f'UPDATE raceCalendar \
                    SET raceStatus = "FINISHED" \
                    WHERE GP_ENG = "{gp}" AND driverGroup = "{drivergroup}";'
            func.logging(logpath, f'UPDATE: race status of {drivergroup}-{gp}......')
            print(f'UPDATE: race status of {drivergroup}-{gp}......')
            cursor.execute(query)
        db.commit()
        
        racef.close()

        func.logging(logpath)
        func.logging(logpath, f'正赛成绩上传报告（共{record}条）:')
        func.logging(logpath, f'    {report["success"]:<3}条成绩新增')
        func.logging(logpath, f'    {report["update"]:<3}条成绩更新')
        func.logging(logpath, f'    {report["failed"]:<3}条上传失败，请查看日志信息')
        func.logging(logpath, "正赛成绩上传完成，稍后请记得将文件上传到赛会群备份", end="\n\n\n\n\n\n")
        
        print()
        print(f'正赛成绩上传报告（共{record}条）:')
        print(f'    {report["success"]:<3}条成绩新增')
        print(f'    {report["update"]:<3}条成绩更新')
        print(f'    {report["failed"]:<3}条上传失败，请查看日志信息')
        print("正赛成绩上传完成，稍后请记得将文件上传到赛会群备份")

    
    except Exception as e:
        func.logging(logpath, traceback.format_exc())
        func.logging(logpath, "Error: " + str(e), end="\n\n")
        print("错误提示：" + str(e))
        print("数据上传失败，请检查上传文件数据是否正确，或查看日志咨询管理员")



# upload qualiying result
def upload_rd(db:mysql.connector.MySQLConnection):
    # db = connectserver.connectserver("server.json", "db")
    cursor = db.cursor()

    try:
        func.logging(logpath, func.delimiter_string("User uploading race director data", 60), end="\n\n\n")
        root = tkinter.Tk()
        root.withdraw()
        filepath = filedialog.askopenfilename()

        rdf = open(filepath, "r")
        reader = csv.DictReader(rdf)

        record = 0
        report = {"success":0, "failed":0, "update":0}
        datetemp = 0
        num = 0
        for row in reader:
            date = row.get("casedate")    
            drivername = row.get("driverName")
            drivergroup = row.get("driverGroup")
            gp = row.get("GP")
            penalty = row.get("penalty")
            penaltyLP = row.get("penaltyLP")
            penaltywarning = row.get("penaltyWarning")
            qualiban = row.get("qualiBan")
            raceban = row.get("raceBan")
            description = row.get("PenaltyDescription")

            if date.replace(" ","") == "" and drivername.replace(" ","") == "" and drivergroup.replace(" ","") == "" \
            and gp.replace(" ","") == "" and penalty.replace(" ","") == "" and penaltyLP.replace(" ","") == "" \
            and penaltywarning.replace(" ","") == "" and qualiban.replace(" ","") == "" and raceban.replace(" ","") == "" \
            and description.replace(" ","") == "":
                break

            if date == "" or date == None:
                date = datetime.today().strftime('%Y-%m-%d')
            if qualiban == None or qualiban == '':
                    qualiban = 0
            if raceban == None or raceban == '':
                raceban = 0

            record += 1

            if date != datetemp:
                datetemp = date
                num = 1
            else:
                num += 1
            try:
                # formating case number
                # "{drivergroup}-{gpkey}-C{recordNum}"
                gpkey = func.get_key(settings["content"]["gp"], gp)
                casenum = f'{drivergroup}-{gpkey}-C{num:02}'

                query = "INSERT INTO raceDirector VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                val = (casenum, date, drivername, drivergroup, gp, penalty, penaltyLP, penaltywarning, qualiban, raceban, description)
                func.logging(logpath, f'UPLOAD: race director {casenum}-{drivergroup}-{gp}-{drivername}......')
                print(f'UPLOAD: race director {casenum}-{drivergroup}-{gp}-{drivername}......')
                cursor.execute(query, val)

                report["success"] += 1
            
            except mysql.connector.errors.IntegrityError as e:
                # duplicate:
                # Duplicate entry 'CaseNumber-CaseDate for key 'raceDirector.PRIMARY'
                if str(e).find("Duplicate entry") != -1 and str(e).find("raceDirector.PRIMARY") != -1:
                    func.logging(logpath, f'WARNING: Record {casenum}-{drivergroup}-{gp}-{drivername} already exist......')
                    print(f'Record {casenum}-{drivergroup}-{gp}-{drivername} already exist......')
                    query = f'UPDATE raceDirector \
                            SET driverName = "{drivername}", \
                                driverGroup = "{drivergroup}", \
                                GP = "{gp}", \
                                penalty = "{penalty}", \
                                penaltyLP = "{penaltyLP}", \
                                penaltyWarning = "{penaltywarning}", \
                                qualiBan = "{qualiban}", \
                                raceBan = "{raceban}", \
                                PenaltyDescription = "{description}" \
                            WHERE CaseNumber = "{casenum}" AND CaseDate = "{date}";'
                    func.logging(logpath, f'UPDATE: {casenum}-{drivergroup}-{gp}-{drivername}......', end="\n\n")
                    print(f'UPDATE: {casenum}-{drivergroup}-{gp}-{drivername}......\n')
                    cursor.execute(query)

                    report["update"] += 1

                # foreign key:
                # Cannot add or update a child row: a foreign key constraint fails 
                # (`afr_s10`.`raceDirector`, CONSTRAINT `raceDirector_FK1` FOREIGN KEY (`driverName`) 
                # REFERENCES `driverList` (`driverName`) ON DELETE CASCADE ON UPDATE CASCADE)
                elif str(e).find("foreign key constraint") != -1:
                    func.logging(logpath, f'ERROR: drivername {drivername} doesn\'t find/match in driverlist', end="\n\n")
                    print(f'ERROR: drivername {drivername} doesn\'t find/match in driverlist\n')
                    report["failed"] += 1
        
        db.commit()
        rdf.close()
        
        func.logging(logpath)
        func.logging(logpath, f'判罚数据上传报告（共{record}条）:')
        func.logging(logpath, f'    {report["success"]:<3}条判罚新增')
        func.logging(logpath, f'    {report["update"]:<3}条判罚更新')
        func.logging(logpath, f'    {report["failed"]:<3}条上传失败，请查看日志信息')
        func.logging(logpath, "判罚数据上传完成，稍后请记得将文件上传到赛会群备份", end="\n\n\n\n\n\n")

        print()
        print(f'判罚数据上传报告（共{record}条）:')
        print(f'    {report["success"]:<3}条判罚新增')
        print(f'    {report["update"]:<3}条判罚更新')
        print(f'    {report["failed"]:<3}条上传失败，请查看日志信息')
        print("判罚数据上传完成，稍后请记得将文件上传到赛会群备份")


    except Exception as e:
        func.logging(logpath, traceback.format_exc())
        func.logging(logpath, "Error: " + str(e), end="\n\n")
        print("错误提示：" + str(e))
        print("数据上传失败，请检查上传文件数据是否正确，或查看日志咨询管理员")
