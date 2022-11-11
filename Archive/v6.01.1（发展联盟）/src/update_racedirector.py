from calendar import c
import connectserver
import upload_racedirector

def update_racedirector():
    db = connectserver.connectserver("server.json", "league")
    cursor = db.cursor()

    # first search and delete the original result
    while True:
        try:
            race = input("请输入比赛站名（同时支持中英文）, 输入q回到主菜单：")
            if race == "q" or race == "Q":
                break
            group = input("请选择组别, 输入q回到主菜单：")
            if group == 'q' or group == 'Q':
                break

            query = f'SELECT CaseNumber, CaseDate, raceDirector.driverGroup, GP, raceCalendar.GP_CHN \
                    FROM raceDirector JOIN raceCalendar \
                        ON raceDirector.GP = raceCalendar.GP_ENG \
                        AND raceDirector.driverGroup = raceCalendar.driverGroup \
                    WHERE driverName != "Race Director" AND \
                        raceDirector.driverGroup = "{group}" AND \
                        (raceCalendar.GP_CHN = "{race}" OR raceCalendar.GP_ENG = "{race}");'
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result) == 0:
                raise AttributeError("没有当场比赛的判罚记录，请重新输入正确的选项\n")
            
            racedesc = f'{group} {result[0][4]} {result[0][3]}'
            test = input(f'你选择了 “{racedesc}”，一共找到{len(result)}条判罚记录\n按Enter以继续，输入q回到上一级\n')
            if test == 'q' or test == 'Q':
                raise ValueError()
            
            query = f'DELETE FROM raceDirector WHERE driverName != "Race Director" \
                    AND driverGroup = "{group}" AND GP = "{result[0][3]}";'
            cursor.execute(query)
            db.commit()

            test = input("原比赛判罚记录已清除，按Enter重新上传排位赛数据，输入q回到主菜单\n")
            if test == 'q' or test == 'Q':
                break

            upload_racedirector.upload_racedirector()
            break

        except Exception as e:
            print(str(e))
