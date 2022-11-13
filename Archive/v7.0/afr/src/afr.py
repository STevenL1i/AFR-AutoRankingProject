import deffunc as func
import connectserver
serverconfig = "server.json"

import upload_driverdata
# welcome_newdriver(db):mysql.connector.MySQLConnection         # passed
# welcome_newteam(db:mysql.connector.MySQLConnection)           # passed
# transfer_driver(db:mysql.connector.MySQLConnection)           # passed, but possible unexpected special case

import upload_racedata
# upload_quali(db:mysql.connector.MySQLConnection)              # passed
# upload_race(db:mysql.connector.MySQLConnection)               # passed
# upload_rd(db:mysql.connector.MySQLConnection)                 # passed

import update_racedata
# update_racestatus(db:mysql.connector.MySQLConnection)         # passed
# update_eventresult(db:mysql.connector.MySQLConnection)        # passed
#          this including update quali/race/racedirector data

import pointsrecalibration
import ClassificationTable
import RaceResultTable

def main():
    try:
        db = connectserver.connectserver(serverconfig, "db")
    except Exception:
        input("\nDatabase connection unreachable, please try again......\n")
        exit(0)

    while True:
        print("\n欢迎来到AFR联赛积分管理系统 (v7.0)\n")
        menu = ["上传排位成绩", "上传正赛成绩", "上传判罚数据",
                "上传新车手", "上传新车队", "上传转会记录",
                "更新比赛状态", "更新比赛数据", "校准积分", 
                "下载最新积分统计表", "下载最新比赛结算表", "查看教程文档"]
        for i in range(0,len(menu)):
            print(f'{i+1}.{menu[i]}')
        print()
        print("0.退出")
        print()
        choice = input("请输入你所要选择的功能： ")
        while True:
            if choice == '1':
                print()
                print("你选择了“上传排位成绩”")
                test = input("请按Enter以上传文件（记住别选错文件了）输入q回到主菜单 ")
                if test == 'q' or test == 'Q':
                    break
                upload_racedata.upload_quali(db)
                print()
                input("请按Enter回到主菜单\n")
                break


            if choice == '2':
                print()
                print("你选择了“上传正赛成绩”")
                test = input("请按Enter以上传文件（记住别选错文件了）输入q回到主菜单 ")
                if test == 'q' or test == 'Q':
                    break
                upload_racedata.upload_race(db)
                print()
                input("请按Enter回到主菜单\n")
                break


            if choice == '3':
                print()
                print("你选择了“上传判罚数据”")
                test = input("请按Enter以上传文件（记住别选错文件了）输入q回到主菜单 ")
                if test == 'q' or test == 'Q':
                    break
                upload_racedata.upload_rd(db)
                print()
                input("请按Enter回到主菜单\n")
                break




            if choice == '4':
                print()
                print("你选择了“上传新车手”")
                test = input("请按Enter以上传文件（记住别选错文件了）输入q回到主菜单 ")
                if test == 'q' or test == 'Q':
                    break
                upload_driverdata.welcome_newdriver(db)
                print()
                input("请按Enter回到主菜单\n")
                break


            if choice == '5':
                print()
                print("你选择了“上传新车队”")
                test = input("请按Enter以上传文件（记住别选错文件了）输入q回到主菜单 ")
                if test == 'q' or test == 'Q':
                    break
                upload_driverdata.welcome_newteam(db)
                print()
                input("请按Enter回到主菜单\n")
                break
            

            if choice == '6':
                print()
                print("你选择了“上传转会记录”")
                test = input("请按Enter以上传文件（记住别选错文件了）输入q回到主菜单 ")
                if test == 'q' or test == 'Q':
                    break
                upload_driverdata.transfer_driver(db)
                print()
                input("请按Enter回到主菜单\n")
                break




            if choice == '7':
                print()
                print("你选择了“更新比赛状态”")
                update_racedata.update_racestatus(db)
                print()
                input("请按Enter回到主菜单\n")
                break
                
            
            if choice == '8':
                print()
                print("你选择了“更新比赛数据”")
                update_racedata.update_eventresult(db)
                print()
                input("请按Enter回到主菜单\n")
                break




            if choice == '9':
                print()
                print("你选择了“校准积分”")
                test = input("请按Enter以下载最新积分榜，输入q回到主菜单 ")
                if test == 'q' or test == 'Q':
                    break
                pointsrecalibration.main(db)
                print()
                input("请按Enter回到主菜单\n")
                break


            if choice == '10':
                print()
                print("你选择了“下载最新积分统计表”")
                test = input("请按Enter以下载最新积分榜，输入q回到主菜单 ")
                if test == 'q' or test == 'Q':
                    break
                ClassificationTable.main(db)
                print()
                input("请按Enter回到主菜单\n")
                break


            if choice == '11':
                print()
                print("你选择了“下载最新积分统计表”")
                test = input("请按Enter以下载最新积分榜，输入q回到主菜单 ")
                if test == 'q' or test == 'Q':
                    break
                RaceResultTable.main(db)
                print()
                input("请按Enter回到主菜单\n")
                break
            
                
            


            elif choice == '12':
                print("功能仍在开发中......请暂时手动打开文档阅读\n")
                input("请按Enter回到主菜单\n")
                break



            if choice == '0':
                print()
                input("请按Enter键以退出............")
                return 0

            else:
                break
            


if __name__ == "__main__":
    main()