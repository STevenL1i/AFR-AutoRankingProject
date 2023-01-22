import datetime, csv, json, tkinter, traceback
from tkinter import filedialog

import mysql.connector
import deffunc as func

settingsf = open("settings/settings.json", "r", encoding='utf-8')
settings:dict = json.load(settingsf)
settingsf.close()
logpath = settings["default"]["log"]

# upload new driver
def welcome_newdriver(db:mysql.connector.MySQLConnection):
    # db = connectserver.connectserver("server.json", "db")
    cursor = db.cursor()

    try:
        func.logging(logpath, func.delimiter_string("User uploading newdriver data", 60), end="\n\n\n")
        root = tkinter.Tk()
        root.withdraw()
        files = filedialog.askopenfilenames()

        report = {"success":0, "failed":0, "skip":0}
        for filepath in files:
            func.logging(logpath, f'file: {filepath}')
            print(f'file: {filepath}')

            newdriverf = open(filepath, "r")
            reader = csv.DictReader(newdriverf)
            
            record = 0
            for row in reader:
                drivername = row.get("driverName")
                team = row.get("team")
                group = row.get("driverGroup")
                status = row.get("driverStatus")
                jointime = row.get("joinTime")
                raceban = row.get("raceBan")
                qualiban = row.get("qualiBan")
                pwd = row.get("password")
                if drivername.replace(" ","") == "" and team.replace(" ","") == "" and group.replace(" ","") == "" \
                and status.replace(" ","") == "" and jointime.replace(" ","") == "" \
                and raceban.replace(" ","") == "" and qualiban.replace(" ","") == "" and pwd.replace(" ","") == "":
                    break

                if jointime == '':
                    jointime = datetime.datetime.today().strftime('%Y-%m-%d')
                
                try:
                    qualiban = int(qualiban)
                except ValueError:
                    qualiban = 0
                try:
                    raceban = int(raceban)
                except ValueError:
                    raceban = 0

                record += 1

                try:
                    # update the driverlist
                    query = "INSERT INTO driverList VALUES \
                            (%s, %s, %s, %s, %s, %s);"
                    val = (drivername, team, group, status, jointime, 1)
                    func.logging(logpath, f'UPLOAD: driver {record}-{drivername}.........')
                    print(f'UPLOAD: driver {record}-{drivername}.........')
                    cursor.execute(query, val)

                    # update the driverLeaderBoard
                    query = "INSERT INTO driverLeaderBoard \
                            (driverName, team, driverGroup, totalPoints) VALUES (%s, %s, %s, %s);"
                    val = (drivername, team, group, 0)
                    cursor.execute(query, val)

                    # update the driver license point
                    query = "INSERT INTO licensePoint (driverName, driverGroup, warning, totalLicensePoint, raceBan, qualiBan) \
                            VALUES (%s, %s, %s, %s, %s, %s);"
                    val = (drivername, group, 0, 12, raceban, qualiban)
                    cursor.execute(query, val)

                    # create LAN account for the new driver
                    # From Season 10 on, account create for driver will be permanent
                    # if driver already has an account, here will update the password
                    try:
                        # driver may choose not to create account
                        if pwd.replace(" ","") == "" or pwd == "null" or pwd == "none" or pwd == "no":
                            raise ValueError("User don't need a new LAN account")

                        # username will be driver id, but only retain alphabets and numbers
                        username = ""
                        for c in drivername:
                            if ord(c) >= 65 and ord(c) <= 90:
                                username += c
                            elif ord(c) >= 97 and ord(c) <= 122:
                                username += c
                            elif ord(c) >= 48 and ord(c) <= 57:
                                username += c
                        
                        # upload to LANusername table
                        query = "INSERT INTO afr_elo.LANusername VALUES (%s, %s, %s, %s);"
                        val = (drivername, username, pwd, "STANDBY")
                        func.logging(logpath, f'UPLOAD: LAN account for {drivername}-{username}......')
                        cursor.execute(query, val)
                    
                    except mysql.connector.errors.IntegrityError:
                        query = f'UPDATE afr_elo.LANusername SET password = "{pwd}" \
                                WHERE username = "{username}";'
                        func.logging(logpath, f'WARNING: User account exists, updating password......', end="\n\n")
                        cursor.execute(query)

                    except ValueError as e:
                        func.logging(logpath, str(e), end="\n\n")
                    
                    report["success"] += 1
                
                except mysql.connector.errors.IntegrityError:
                    report["skip"] += 1
                    func.logging(logpath, "WARNING: driver already existed............", end="\n\n")
                    print("WARNING: driver already existed............\n")

            db.commit()
            newdriverf.close()

        func.logging(logpath)
        func.logging(logpath, f'车手上传报告（共{record}条）:')
        func.logging(logpath, f'    {report["success"]:<3}位新增上传')
        func.logging(logpath, f'    {report["skip"]:<3}位已上传，更新其LAN账号信息')
        func.logging(logpath, f'    {report["failed"]:<3}位上传失败，请查看日志信息')
        func.logging(logpath, "新车手数据上传完成，稍后请记得将文件上传到赛会群备份", end="\n\n\n\n\n\n")

        print()
        print(f'车手上传报告（共{record}条）:')
        print(f'    {report["success"]:<3}位新增上传')
        print(f'    {report["skip"]:<3}位已上传，更新其LAN账号信息')
        print(f'    {report["failed"]:<3}位上传失败')
        print("新车手数据上传完成，稍后请记得将文件上传到赛会群备份")


    except Exception as e:
        func.logging(logpath, traceback.format_exc())
        func.logging(logpath, "Error: " + str(e), end="\n\n")
        print("错误提示：" + str(e))
        print("数据上传失败，请检查上传文件数据是否正确，或查看日志咨询管理员")



# upload new team
def welcome_newteam(db:mysql.connector.MySQLConnection):
    # db = connectserver.connectserver("server.json", "db")
    cursor = db.cursor()

    try:
        func.logging(logpath, func.delimiter_string("User uploading newteam data", 60), end="\n\n\n")
        root = tkinter.Tk()
        root.withdraw()
        files = filedialog.askopenfilenames()

        report = {"success":0, "failed":0, "update":0}
        for filepath in files:
            func.logging(logpath, f'file: {filepath}')
            print(f'file: {filepath}')

            newteamf = open(filepath, "r")
            reader = csv.DictReader(newteamf)

            record = 0
            for row in reader:
                teamname = row.get("teamName")
                teamcolor = row.get("teamColor")
                group = row.get("driverGroup")
                if teamname.replace(" ","") == "" and teamcolor.replace(" ","") == "" \
                and group.replace(" ","") == "":
                    break

                record += 1

                try:
                    query = "INSERT INTO teamList \
                            (teamName, teamColor, driverGroup) \
                            VALUES (%s, %s, %s);"
                    val = (teamname, teamcolor, group)
                    func.logging(logpath, f'UPLOAD: team {record}-{group}-{teamname}......')
                    print(f'UPLOAD: team {record}-{group}-{teamname}......')
                    cursor.execute(query, val)

                    query = "INSERT INTO constructorsLeaderBoard \
                            (team, driverGroup, totalPoints) VALUES (%s, %s, %s);"
                    val = (teamname, group, 0)
                    cursor.execute(query, val)

                    report["success"] += 1
                
                except mysql.connector.errors.IntegrityError:
                    query = f'UPDATE teamList \
                            SET teamColor ="{teamcolor}" \
                            WHERE teamName = "{teamname}" AND driverGroup = "{group}";'
                    func.logging(logpath, f'WARNING: Team {group}-{teamname} already exist\nUPDATE: teamcolor to {teamcolor}......', end="\n\n")
                    print(f'WARNING: Team {group}-{teamname} already exist\nUPDATE: teamcolor to {teamcolor}......\n')
                    cursor.execute(query)
                    
                    report["update"] += 1
            

            db.commit()
            newteamf.close()

        func.logging(logpath)
        func.logging(logpath, f'车队上传报告（共{record}条）:')
        func.logging(logpath, f'    {report["success"]:<3}支新增上传')
        func.logging(logpath, f'    {report["update"]:<3}支已上传，更新其车队信息')
        func.logging(logpath, f'    {report["failed"]:<3}支上传失败，请查看日志信息')
        func.logging(logpath, "新车队数据上传完成，稍后请记得将文件上传到赛会群备份", end="\n\n\n\n\n\n")

        print()
        print(f'车队上传报告（共{record}条）:')
        print(f'    {report["success"]:<3}支新增上传')
        print(f'    {report["update"]:<3}支已上传，更新其车队信息')
        print(f'    {report["failed"]:<3}支上传失败')
        print("新车队数据上传完成，稍后请记得将文件上传到赛会群备份")


    except Exception as e:
        func.logging(logpath, traceback.format_exc())
        func.logging(logpath, "Error: " + str(e), end="\n\n")
        print("错误提示：" + str(e))
        print("数据上传失败，请检查上传文件数据是否正确，或查看日志咨询管理员")



# upload transfer driver
def transfer_driver(db:mysql.connector.MySQLConnection):
    # db = connectserver.connectserver("server.json", "db")
    cursor = db.cursor()

    try:
        func.logging(logpath, func.delimiter_string("User uploading transferdriver data", 60), end="\n\n\n")
        root = tkinter.Tk()
        root.withdraw()
        files = filedialog.askopenfilenames()
        
        report = {"success":0, "failed":0, "skip":0}
        for filepath in files:
            func.logging(logpath, f'file: {filepath}')
            print(f'file: {filepath}')

            transferdriverf = open(filepath, "r")
            reader = csv.DictReader(transferdriverf)

            record = 0
            for row in reader:
                drivername = row.get("driverName")
                team_from = row.get("team_from")
                team_to = row.get("team_to")
                drivergroup_from = row.get("driverGroup_from")
                drivergroup_to = row.get("driverGroup_to")
                status = row.get("driverStatus")
                description = row.get("description")
                transfertime = row.get("transferTime")
                tokenused = row.get("tokenUsed")
                
                if drivername.replace(" ","") == "" and team_from.replace(" ","") == "" and team_to.replace(" ","") == "" \
                and drivergroup_from.replace(" ","") == "" and drivergroup_to.replace(" ","") == "" \
                and status.replace(" ","") == "" and description.replace(" ","") == "" \
                and transfertime.replace(" ","") == "" and tokenused.replace(" ","") == "":
                    break

                if transfertime == '':
                    transfertime = datetime.datetime.today().strftime('%Y-%m-%d')
                
                record += 1

                try:
                    # inserting transfer record to driverTransfer table
                    query = "INSERT INTO driverTransfer VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
                    val = (drivername, team_from, drivergroup_from, team_to, drivergroup_to,
                        description, transfertime, tokenused)
                    func.logging(logpath, f'UPLOAD: Transfering driver {drivername} to {drivergroup_to}-{team_to}.........')
                    print(f'UPLOAD: Transfering driver {drivername} to {drivergroup_to}-{team_to}.........')
                    cursor.execute(query, val)

                    # update driverList table
                    query = f'UPDATE driverList \
                            SET team = "{team_to}", \
                                driverGroup = "{drivergroup_to}", \
                                driverStatus = "{status}", \
                                transferToken = transferToken - {tokenused} \
                            WHERE driverName = "{drivername}" AND driverGroup = "{drivergroup_from}";'
                    cursor.execute(query)

                    # update licensePoint table
                    query = f'UPDATE licensePoint \
                            SET driverGroup = "{drivergroup_to}" \
                            WHERE driverName = "{drivername}";'
                    func.logging(logpath, f'UPDATE: {drivername}\'s license point profile.........')
                    cursor.execute(query)

                    # create/update profile in driverLeaderBoard
                    try:
                        query = "INSERT INTO driverLeaderBoard \
                                (driverName, team, driverGroup, totalPoints) \
                                VALUES (%s, %s, %s, %s);"
                        val = (drivername, team_to, drivergroup_to, 0)
                        func.logging(logpath, f'UPDATE: {drivername}\'s driver leaderboard profile.........')
                        cursor.execute(query, val)
                    
                    except mysql.connector.errors.IntegrityError as e:
                        # Duplicate entry '333-Testing-A3' for key 'driverLeaderBoard.PRIMARY'
                        if str(e).find("Duplicate entry") != -1 \
                        and str(e).find("driverLeaderBoard.PRIMARY") != -1:
                            query = f'UPDATE driverLeaderBoard \
                                    SET team = "{team_to}" \
                                    WHERE driverName = "{drivername}" AND driverGroup = "{drivergroup_to}";'
                            cursor.execute(query)
                            db.commit()

                        else:
                            raise mysql.connector.errors.IntegrityError(str(e))
                    
                    query = f'UPDATE driverLeaderBoard \
                            SET team = "{drivergroup_to}" \
                            WHERE driverName = "{drivername}" AND driverGroup != "{drivergroup_to}";'
                    cursor.execute(query)
                    db.commit()

                    func.logging(logpath)
                    report["success"] += 1

                except mysql.connector.errors.IntegrityError as e:
                    if str(e).find("Duplicate entry") != -1 and str(e).find("driverTransfer.PRIMARY") != -1:
                        report["skip"] += 1
                        func.logging(logpath, f'WARNING: transfer record already exist, skipping to next transfer............', end="\n\n")
                        print(f'WARNING: transfer record already exist, skipping to next transfer............\n')
                    else:
                        raise mysql.connector.errors.IntegrityError(str(e))
            
            db.commit()
            transferdriverf.close()

        func.logging(logpath)
        func.logging(logpath, f'转会上传报告（共{record}条）:')
        func.logging(logpath, f'    {report["success"]:<3}条新增转会')
        func.logging(logpath, f'    {report["skip"]:<3}条已上传转会（跳过）')
        func.logging(logpath, f'    {report["failed"]:<3}条上传失败，请查看日志信息')
        func.logging(logpath, "车手转会记录上传完成，稍后请记得将文件上传到赛会群备份", end="\n\n\n\n\n\n")

        print()
        print(f'转会上传报告（共{record}条）:')
        print(f'    {report["success"]:<3}条新增转会')
        print(f'    {report["skip"]:<3}条已上传转会（跳过）')
        print(f'    {report["failed"]:<3}条上传失败')
        print("车手转会记录上传完成，稍后请记得将文件上传到赛会群备份")


    except Exception as e:
        func.logging(logpath, traceback.format_exc())
        func.logging(logpath, "Error: " + str(e), end="\n\n")
        print("错误提示：" + str(e))
        print("数据上传失败，请检查上传文件数据是否正确，或查看日志咨询管理员")
