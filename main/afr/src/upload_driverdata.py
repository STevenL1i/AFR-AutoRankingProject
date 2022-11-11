import datetime, csv, json, tkinter, traceback
from tkinter import filedialog

import mysql.connector

settingsf = open("settings/settings.json", "r", encoding='utf-8')
settings:dict = json.load(settingsf)
settingsf.close()

# upload new driver
def welcome_newdriver(db:mysql.connector.MySQLConnection):
    # db = connectserver.connectserver("server.json", "db")
    cursor = db.cursor()

    try:
        root = tkinter.Tk()
        root.withdraw()
        filepath = filedialog.askopenfilename()

        newdriverf = open(filepath, "r")
        reader = csv.DictReader(newdriverf)

        record = 0
        report = {"success":0, "failed":0, "skip":0}
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
            print(f'Uploading records {record}.........')

            try:
                # update the driverlist
                query = "INSERT INTO driverList VALUES \
                        (%s, %s, %s, %s, %s, %s);"
                val = (drivername, team, group, status, jointime, 1)
                print(f'Uploading driver {drivername}.........')
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
                        elif ord(c) >= 48 and ord(c) >= 57:
                            username += c
                    
                    # upload to LANusername table
                    query = "INSERT INTO afr_elo.LANusername VALUES (%s, %s, %s, %s);"
                    val = (drivername, username, pwd, "STANDBY")
                    print(f'Creating LAN account for {drivername}-{username}......')
                    cursor.execute(query, val)
                
                except mysql.connector.errors.IntegrityError:
                    query = f'UPDATE afr_elo.LANusername SET password = "{pwd}" \
                            WHERE username = "{username}";'
                    print(f'User account exists, updating password......')
                    cursor.execute(query)

                except ValueError as e:
                    print(str(e))
                
                report["success"] += 1
                print()
            
            except mysql.connector.errors.IntegrityError:
                report["skip"] += 1
                print("driver already existed, skipping to next driver............\n")


        db.commit()
        newdriverf.close()

        print()
        print(f'车手上传报告（共{record}条）:')
        print(f'    {report["success"]:<3}位新增上传')
        print(f'    {report["skip"]:<3}位已上传，更新其LAN账号信息')
        print(f'    {report["failed"]:<3}位上传失败')
        print("新车手数据上传成功，稍后请记得将文件上传到赛会群备份")


    except Exception as e:
        if settings["general"]["DEBUG_MODE"] == True:
            print()
            print(traceback.format_exc())
            print()
        print("错误提示：" + str(e))
        print("数据上传失败，请检查上传文件数据是否正确，或咨询管理员")



# upload new team
def welcome_newteam(db:mysql.connector.MySQLConnection):
    # db = connectserver.connectserver("server.json", "db")
    cursor = db.cursor()

    try:
        root = tkinter.Tk()
        root.withdraw()
        filepath = filedialog.askopenfilename()

        newteamf = open(filepath, "r")
        reader = csv.DictReader(newteamf)

        record = 0
        report = {"success":0, "failed":0, "update":0}
        for row in reader:
            teamname = row.get("teamName")
            teamcolor = row.get("teamColor")
            group = row.get("driverGroup")
            if teamname.replace(" ","") == "" and teamcolor.replace(" ","") == "" \
            and group.replace(" ","") == "":
                break

            record += 1
            print(f'Uploading records {record}......')

            try:
                query = "INSERT INTO teamList \
                        (teamName, teamColor, driverGroup) \
                        VALUES (%s, %s, %s);"
                val = (teamname, teamcolor, group)
                print(f'Uploading team {group}-{teamname}......')
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
                print(f'Team {group}-{teamname} already exist, updating teamcolor to {teamcolor}......')
                cursor.execute(query)
                
                report["update"] += 1
            
            print()

        db.commit()
        newteamf.close()

        print()
        print(f'车队上传报告（共{record}条）:')
        print(f'    {report["success"]:<3}支新增上传')
        print(f'    {report["update"]:<3}支已上传，更新其车队信息')
        print(f'    {report["failed"]:<3}支上传失败')
        print("新车队数据上传成功，稍后请记得将文件上传到赛会群备份")


    except Exception as e:
        if settings["general"]["DEBUG_MODE"] == True:
            print()
            print(traceback.format_exc())
            print()
        print("错误提示：" + str(e))
        print("数据上传失败，请检查上传文件数据是否正确，或咨询管理员")



# upload transfer driver
def transfer_driver(db:mysql.connector.MySQLConnection):
    # db = connectserver.connectserver("server.json", "db")
    cursor = db.cursor()

    try:
        root = tkinter.Tk()
        root.withdraw()
        filepath = filedialog.askopenfilename()

        transferdriverf = open(filepath, "r")
        reader = csv.DictReader(transferdriverf)

        record = 0
        report = {"success":0, "failed":0, "skip":0}
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
            print(f'Uploading records {record}......')

            try:
                # inserting transfer record to driverTransfer table
                query = "INSERT INTO driverTransfer VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
                val = (drivername, team_from, drivergroup_from, team_to, drivergroup_to,
                    description, transfertime, tokenused)
                cursor.execute(query, val)

                # update driverList table
                query = f'UPDATE driverList \
                        SET team = "{team_to}", \
                            driverGroup = "{drivergroup_to}", \
                            driverStatus = "{status}", \
                            transferToken = transferToken - {tokenused} \
                        WHERE driverName = "{drivername}" AND driverGroup = "{drivergroup_from}";'
                print(f'Transfering driver {drivername} to {drivergroup_to}-{team_to}.........')
                cursor.execute(query)

                # update licensePoint table
                query = f'UPDATE licensePoint \
                        SET driverGroup = "{drivergroup_to}" \
                        WHERE driverName = "{drivername}";'
                print(f'Updating {drivername}\'s license point profile.........')
                cursor.execute(query)

                # create/update profile in driverLeaderBoard
                try:
                    query = "INSERT INTO driverLeaderBoard \
                            (driverName, team, driverGroup, totalPoints) \
                            VALUES (%s, %s, %s, %s);"
                    val = (drivername, team_to, drivergroup_to, 0)
                    print(f'Creating/Updating {drivername}\'s driver leaderboard profile.........')
                    cursor.execute(query, val)
                
                except mysql.connector.errors.IntegrityError as e:
                    # Duplicate entry '333-Testing-A3' for key 'driverLeaderBoard.PRIMARY'
                    if str(e).find("Duplicate entry") != -1 \
                    and str(e).find("driverLeaderBoard.PRIMARY") != -1:
                        query = f'UPDATE driverLeaderBoard \
                                SET team = "{team_to}" \
                                WHERE driverName = "{drivername}" AND driverGroup = "{drivergroup_to}";'
                        print(f'{drivergroup_to}-{drivername} driver leaderboard profile already exist, updating profile......')
                        cursor.execute(query)
                        db.commit()

                    else:
                        raise mysql.connector.errors.IntegrityError(str(e))
                
                query = f'UPDATE driverLeaderBoard \
                        SET team = "{drivergroup_to}" \
                        WHERE driverName = "{drivername}" AND driverGroup != "{drivergroup_to}";'
                cursor.execute(query)
                db.commit()

                report["success"] += 1
                print()

            except mysql.connector.errors.IntegrityError as e:
                if str(e).find("Duplicate entry") != -1 and str(e).find("driverTransfer.PRIMARY") != -1:
                    report["skip"] += 1
                    print(f'{drivername} transfer from {drivergroup_from}-{team_from} to {drivergroup_to}-{team_to} already exist, skipping to next transfer............\n')
                else:
                    raise mysql.connector.errors.IntegrityError(str(e))
        
        db.commit()
        transferdriverf.close()

        print()
        print(f'转会上传报告（共{record}条）:')
        print(f'    {report["success"]:<3}条新增转会')
        print(f'    {report["skip"]:<3}条已上传转会（跳过）')
        print(f'    {report["failed"]:<3}条上传失败')
        print("车手转会记录上传成功，稍后请记得将文件上传到赛会群备份")


    except Exception as e:
        if settings["general"]["DEBUG_MODE"] == True:
            print()
            print(traceback.format_exc())
            print()
        print("错误提示：" + str(e))
        print("数据上传失败，请检查上传文件数据是否正确，或咨询管理员")
