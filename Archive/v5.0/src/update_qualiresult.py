import connectserver
import upload_qualiresult


def update_qualiresult():
    db = connectserver.connectserver("afr")
    cursor = db.cursor()

    # first search and delete the original result
    while True:
        try:
            round = input("请输入比赛站数（比如输入12代表第12站）, 输入q回到主菜单：")
            if round == 'q' or round == 'Q':
                break
            round = int(round)
            print()
            print("1. A1")
            print("2. A2")
            print("3. A3")
            group = input("请选择组别, 输入q回到主菜单：")
            if group == '1':
                group = "A1"
            elif group == '2':
                group = "A2"
            elif group == '3':
                group = "A3"
            elif group == 'q' or group == 'Q':
                break
            else:
                raise ValueError("请输入正确的选项")

            query = f'SELECT DISTINCT(raceCalendar.Round), qualiResult.driverGroup, \
                    qualiResult.GP, raceCalendar.GP_CHN \
                    FROM qualiResult JOIN raceCalendar ON \
                    qualiResult.driverGroup = raceCalendar.driverGroup AND \
                    qualiResult.GP = raceCalendar.GP_ENG \
                    WHERE qualiResult.driverGroup = "{group}" AND raceCalendar.Round = {round}'
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result) == 0:
                raise AttributeError("没有找到相关比赛，请重新输入正确的数字和选项\n")
            result = list(result[0])
            racedesc = f'{group} {result[3]} {result[2]}'

            test = input(f'你选择了 “{racedesc}”，按Enter以继续，输入q回到上一级\n')
            if test == 'q' or test == 'Q':
                raise ValueError()

            query = f'DELETE FROM qualiResult WHERE driverGroup = "{group}" AND GP = "{result[2]}";'
            cursor.execute(query)
            db.commit()

            test = input("原比赛记录已清除，按Enter重新上传排位赛数据，输入q回到主菜单\n")
            if test == 'q' or test == 'Q':
                break

            upload_qualiresult.upload_quali()
            break


        
        except Exception as e:
            print(str(e))


if __name__ == "__main__":
    update_qualiresult()