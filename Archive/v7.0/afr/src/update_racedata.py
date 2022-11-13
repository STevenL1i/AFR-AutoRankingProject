import json, traceback
import mysql.connector

import upload_racedata

settingsf = open("settings/settings.json", "r", encoding='utf-8')
settings:dict = json.load(settingsf)
settingsf.close()


def askuser_race() -> tuple[str, str]:
    round = input("请输入比赛站数（比如输入12代表第12站）, 输入q回到主菜单：")
    if round == "q" or round == "Q":
        return None, None
    group = input("请输入组别, 输入q回到主菜单：")
    if group == 'q' or group == 'Q':
        return None, None
    
    return round, group


def askuser_event_type() -> tuple[str, str] or bool:
    print("1.排位")
    print("2.正赛")
    print("3.判罚")
    choice = input("请选择数据类别，输入q回到上一级：")
    if choice == "1":
        return "quali", "排位"
    elif choice == "2":
        return "race", "正赛"
    elif choice == "3":
        return "raceDirector", "判罚"
    elif choice == 'q' or choice == 'Q':
        return None, None
    else:
        return False, False


def askuser_status() -> str or bool:
    print("1. 比赛还未进行")
    print("2. 比赛正赛进行中")
    print("3. 比赛已完成")
    print("4. 比赛已取消")
    choice = input("请输入你的选择，输入q回到上一级：")
    if choice == '1':
        return "TO BE GO"
    elif choice == '2':
        return "ON GOING"
    elif choice == '3':
        return "FINISHED"
    elif choice == '4':
        return "CANCELLED"
    elif choice == 'q':
        return "Q"
    else:
        return False


def checkexist_race(db, round, group) -> tuple[str, str, str]:
    cursor = db.cursor()

    query = f'SELECT GP_CHN, GP_ENG FROM raceCalendar \
            WHERE Round = {round} AND driverGroup = "{group}";'
    cursor.execute(query)
    result = cursor.fetchall()
    
    if len(result) == 0:
        return None, None, None
    else:
        return group, result[0][0], result[0][1]


def checkstatus_race(db, status, round, group):
    try:
        cursor = db.cursor()
        query = f'UPDATE raceCalendar \
                SET raceStatus = "{status}" \
                WHERE Round = {round} AND driverGroup = "{group}";'
        cursor.execute(query)
        db.commit()
        print(f'race status updating complete...')
    except Exception as e:
        if settings["general"]["DEBUG_MODE"] == True:
            print()
            print(traceback.format_exc())
            print()
        print("错误提示：" + str(e))
        print("比赛状态更新失败，请检查步骤是否操作正确，此功能问题推荐咨询管理员")


def checkexist_result(db, round, group, event_type):
    cursor = db.cursor()

    query = f'SELECT DISTINCT(raceCalendar.Round), {event_type}Result.driverGroup, \
            {event_type}Result.GP, raceCalendar.GP_CHN \
            FROM {event_type}Result JOIN raceCalendar ON \
            {event_type}Result.driverGroup = raceCalendar.driverGroup AND \
            {event_type}Result.GP = raceCalendar.GP_ENG \
            WHERE {event_type}Result.driverGroup = "{group}" AND raceCalendar.Round = {round}'
    if event_type == "raceDirector":
        query = query.replace("Result", "")
    cursor.execute(query)
    result = cursor.fetchall()

    if len(result) == 0:
        return None, None, None
    else:
        return group, result[0][3], result[0][2]


def cleardata_event(db, gp, group, event_type):
    cursor = db.cursor()

    query = f'DELETE FROM {event_type}Result WHERE driverGroup = "{group}" AND GP = "{gp}";'
    print(f'Clearing {event_type} data of {group}-{gp}......')
    if event_type == "raceDirector":
        query = query.replace("Result", "")
    cursor.execute(query)
    db.commit()



# update race calendar (race status)
def update_racestatus(db:mysql.connector.MySQLConnection):
    cursor = db.cursor()
    while True:
        print()
        round, group = askuser_race()
        if round == None and group == None:
            break
        print()
        group, gpchn, gpeng = checkexist_race(db, round, group)
        if group == None and gpchn == None and gpeng == None:
            input("没有找到相关比赛，请重新输入正确数据\n")
            continue
        else:
            racedesc = f'{group}-{gpchn}-{gpeng}'
            test = input(f'你选择了 “{racedesc}”，按Enter以继续，输入q回到上一级\n')
            if test == 'q' or test == 'Q':
                continue
        
        status = askuser_status()
        if status == "Q":
            continue
        elif status == False:
            input("请选择正确的选项......")
            continue
        
        
        print(f'Updating race status {racedesc}-{status}......')
        checkstatus_race(db, status, round, group)
        break



# update quali/race/racedirector result (based on event_type parameter)
def update_eventresult(db:mysql.connector.MySQLConnection):
    cursor = db.cursor()
    while True:
        print()
        round, group = askuser_race()
        if round == None and group == None:
            break
        print()

        event_type, hint = askuser_event_type()
        if event_type == None and hint == None:
            continue
        elif event_type == False and hint == False:
            print("请输入正确的选项......")
            continue
        print()

        group, gpchn, gpeng = checkexist_result(db, round, group, event_type)
        if group == None and gpchn == None and gpeng == None:
            input("没有找到相关比赛结果，请重新输入正确数据\n")
            continue
        else:
            racedesc = f'{group}-{gpchn}-{gpeng}-{hint}'
        
        test = input(f'你选择了“{racedesc}”\n按Enter以清除成绩，输入q回到上一级\n')
        if test == 'q' or test == 'Q':
            continue
        
        cleardata_event(db, gpeng, group, event_type)
        test = input(f'\n原比赛记录已清除，按Enter重新上传{hint}数据，输入q回到主菜单\n')
        if test == 'q' or test == 'Q':
            break

        if event_type == "quali":
            upload_racedata.upload_quali(db)
        elif event_type == "race":
            upload_racedata.upload_race(db)
        elif event_type == "raceDirector":
            upload_racedata.upload_rd(db)
        else:
            raise ValueError("event_type error......")

        break





# update quali result
def update_qualiresult(db:mysql.connector.MySQLConnection):
    cursor = db.cursor()

# update race result
def update_raceresult(db:mysql.connector.MySQLConnection):
    cursor = db.cursor()

# update race director record
def update_racedirector(db:mysql.connector.MySQLConnection):
    cursor = db.cursor()