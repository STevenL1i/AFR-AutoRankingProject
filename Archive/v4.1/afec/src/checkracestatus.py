import connectserver


def checkracestatus():
    db = connectserver.connectserver()
    cursor = db.cursor()

    while True:
        try:
            round = input("请输入比赛站数（比如输入12代表第12站）, 输入q回到主菜单：")
            if round == 'q' or round == 'Q':
                break
            round = int(round)
            
            query = f'SELECT GP_CHN, GP_ENG FROM raceCalendar \
            WHERE Round = {round};'
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result) == 0:
                raise AttributeError("没有找到相关比赛，请重新输入正确的数字和选项\n")
            result = list(result[0])
            racedesc = f'{result[0]} {result[1]}'

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
                break
            else:
                raise ValueError("请输入正确的选项")
            
            query = f'UPDATE raceCalendar \
                    SET raceStatus = "{status}" \
                    WHERE Round = {round};'
            cursor.execute(query)
            db.commit()

            input("比赛状态已更新，按Enter以回到主菜单")
            break
                
        except Exception as e:
            print(str(e))


if __name__ == "__main__":
    checkracestatus()