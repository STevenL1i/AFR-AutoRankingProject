import connectserver

def checkracestatus(db, cursor, status, race, group):
    query = f'UPDATE raceCalendar \
                    SET raceStatus = "{status}" \
                    WHERE driverGroup = "{group}" AND \
                        (GP_ENG = "{race}" OR GP_CHN = "{race}");'
    cursor.execute(query)
    db.commit()
    return True


def askuserrace():
    db = connectserver.connectserver("server.json", "league")
    cursor = db.cursor()

    while True:
        try:
            race = input("请输入比赛站名（同时支持中英文）, 输入q回到主菜单：")
            if race == "q" or race == "Q":
                break
            print()
            group = input("请选择组别, 输入q回到主菜单：")
            if group == 'q' or group == 'Q':
                break
            
            query = f'SELECT GP_CHN, GP_ENG FROM raceCalendar \
            WHERE driverGroup = "{group}" AND \
                (GP_ENG = "{race}" OR GP_CHN = "{race}");'
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result) == 0:
                raise AttributeError("没有找到相关比赛，请重新输入正确选项\n")
            result = list(result[0])
            racedesc = f'{group} {result[0]} {result[1]}'

            test = input(f'你选择了 “{racedesc}”，按Enter以继续，输入q回到上一级\n')
            if test == 'q' or test == 'Q':
                raise ValueError()
            
            print("1. 比赛还未进行")
            print("2. 比赛正赛进行中")
            print("3. 比赛已完成")
            print("4. 比赛已取消")
            choice = input("请输入你的选择，输入q回到上一级：")
            if choice == '1':
                status = "TO BE GO"
            elif choice == '2':
                status = "ON GOING"
            elif choice == '3':
                status = "FINISHED"
            elif choice == '4':
                status = "CANCELLED"
            elif choice == 'q':
                raise ValueError("")
            else:
                raise ValueError("请输入正确的选项")
            
            checkracestatus(db, cursor, status, race, group)
            break
        
        except Exception as e:
            print(str(e))
