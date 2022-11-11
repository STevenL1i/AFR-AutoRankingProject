import connectserver
import upload_raceresult


def update_raceresult():
    db = connectserver.connectserver()
    cursor = db.cursor()

    # first search and delete the original result
    while True:
        try:
            round = input("请输入比赛站数（比如输入12代表第12站）, 输入q回到主菜单：")
            if round == 'q' or round == 'Q':
                break
            round = int(round)

            query = f'SELECT DISTINCT(raceCalendar.Round),\
                    raceResult.GP, raceCalendar.GP_CHN \
                    FROM raceResult JOIN raceCalendar ON \
                    raceResult.GP = raceCalendar.GP_ENG \
                    WHERE raceCalendar.Round = {round}'
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result) == 0:
                raise AttributeError("没有找到相关比赛，请重新输入正确的数字和选项\n")
            result = list(result[0])
            racedesc = f'{result[2]} {result[1]}'

            test = input(f'你选择了 “{racedesc}”，按Enter以继续，输入q回到上一级\n')
            if test == 'q' or test == 'Q':
                raise ValueError()

            query = f'DELETE FROM raceResult WHERE GP = "{result[1]}";'
            cursor.execute(query)
            db.commit()

            test = input("原比赛记录已清除，按Enter重新上传正赛数据，输入q回到主菜单\n")
            if test == 'q' or test == 'Q':
                break

            upload_raceresult.upload_race()
            break
        
        except Exception as e:
            print(str(e))


if __name__ == "__main__":
    update_raceresult()