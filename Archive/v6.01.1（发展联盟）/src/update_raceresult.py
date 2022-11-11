import connectserver
import upload_raceresult

def update_raceresult():
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

            query = f'SELECT DISTINCT(raceCalendar.Round), raceResult.driverGroup, \
                    raceResult.GP, raceCalendar.GP_CHN \
                    FROM raceResult JOIN raceCalendar ON \
                    raceResult.driverGroup = raceCalendar.driverGroup AND \
                    raceResult.GP = raceCalendar.GP_ENG \
                    WHERE raceResult.driverGroup = "{group}" AND \
                        (raceCalendar.GP_ENG = "{race}" OR raceCalendar.GP_CHN = "{race}");'
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result) == 0:
                raise AttributeError("没有找到相关比赛，请重新输入正确的选项\n")
            result = list(result[0])
            racedesc = f'{group} {result[3]} {result[2]}'

            test = input(f'你选择了 “{racedesc}”，按Enter以继续，输入q回到上一级\n')
            if test == 'q' or test == 'Q':
                raise ValueError()

            query = f'DELETE FROM raceResult WHERE driverGroup = "{group}" AND GP = "{result[2]}";'
            cursor.execute(query)
            db.commit()

            test = input("原比赛记录已清除，按Enter重新上传正赛数据，输入q回到主菜单\n")
            if test == 'q' or test == 'Q':
                break

            upload_raceresult.upload_race()
            break
        
        except Exception as e:
            print(str(e))