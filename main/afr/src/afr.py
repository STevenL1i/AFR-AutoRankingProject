import os, json, datetime, traceback
import deffunc as func
import dbconnect
serverconfig = "server.json"
VERSION = "AFR v8.0 (beta v7.4)"

settingsf = open("settings/settings.json", "r", encoding='utf-8')
settings:dict = json.load(settingsf)
settingsf.close()
logpath = settings["default"]["log"]
# generating log file
today = datetime.datetime.today()
try:
    os.mkdir("log")
except FileExistsError:
    pass
logf = open(logpath, "w")
logf.write(func.delimiter_string("Program launching", 50) + "\n")
logf.write(func.delimiter_string("Generating log", 50) + "\n")
logf.write(f'Time: {today.strftime("%Y-%m-%d %H:%M:%S")}\n')
logf.write(f'Program Version: {VERSION}\n')
logf.write(func.get_sysinfo() + "\n")
logf.close()

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
        db = dbconnect.connect_with_conf(serverconfig, "db")
    except Exception as e:
        errmsg = "Database connection unreachable, please try again......"
        func.logging(logpath, traceback.format_exc(), end="\n")
        func.logging(logpath, str(e), end="\n")
        func.logging(logpath, errmsg, end="\n\n")
        input("\n" + errmsg + "\n")
        func.logging(logpath, "Program exiting with code 0......\n")
        exit(0)

    while True:
        print(f'\n欢迎来到AFR联赛积分管理系统 ({VERSION})\n')
        menu = ["上传排位成绩", "上传正赛成绩", "上传判罚数据",
                "上传新车手", "上传新车队", "上传转会记录",
                "更新比赛状态", "更新比赛数据", "校准积分", 
                "下载最新积分统计表", "下载最新比赛结算表",
                "下载报名统计表", "下载LAN账号列表", "查看教程文档"]
        for i in range(0,len(menu)):
            print(f'{i+1}.{menu[i]}')
        print()
        print("0.退出")
        print()
        choices = input("请输入你所要选择的功能： ")
        choices_list = choices.split(" ")
        for choice in choices_list:
        # while True:
            if choice == '1':
                print()
                print("你选择了“上传排位成绩”")
                test = input("请按Enter以上传文件（记住别选错文件了）输入q回到上一级，输入Q回到主菜单 ")
                if test == 'q':
                    continue
                elif test == 'Q':
                    break
                upload_racedata.upload_quali(db)
                print()
                input("请按Enter回到主菜单\n")
                continue


            if choice == '2':
                print()
                print("你选择了“上传正赛成绩”")
                test = input("请按Enter以上传文件（记住别选错文件了）输入q回到上一级，输入Q回到主菜单 ")
                if test == 'q':
                    continue
                elif test == 'Q':
                    break
                upload_racedata.upload_race(db)
                print()
                input("请按Enter回到主菜单\n")
                continue


            if choice == '3':
                print()
                print("你选择了“上传判罚数据”")
                test = input("请按Enter以上传文件（记住别选错文件了）输入q回到上一级，输入Q回到主菜单 ")
                if test == 'q':
                    continue
                elif test == 'Q':
                    break
                upload_racedata.upload_rd(db)
                print()
                input("请按Enter回到主菜单\n")
                continue




            if choice == '4':
                print()
                print("你选择了“上传新车手”")
                test = input("请按Enter以上传文件（记住别选错文件了）输入q回到上一级，输入Q回到主菜单 ")
                if test == 'q':
                    continue
                elif test == 'Q':
                    break
                upload_driverdata.welcome_newdriver(db)
                print()
                input("请按Enter回到主菜单\n")
                continue


            if choice == '5':
                print()
                print("你选择了“上传新车队”")
                test = input("请按Enter以上传文件（记住别选错文件了）输入q回到上一级，输入Q回到主菜单 ")
                if test == 'q':
                    continue
                elif test == 'Q':
                    break
                upload_driverdata.welcome_newteam(db)
                print()
                input("请按Enter回到主菜单\n")
                continue
            

            if choice == '6':
                print()
                print("你选择了“上传转会记录”")
                test = input("请按Enter以上传文件（记住别选错文件了）输入q回到上一级，输入Q回到主菜单 ")
                if test == 'q':
                    continue
                elif test == 'Q':
                    break
                upload_driverdata.transfer_driver(db)
                print()
                input("请按Enter回到主菜单\n")
                continue




            if choice == '7':
                print()
                print("你选择了“更新比赛状态”")
                update_racedata.update_racestatus(db)
                print()
                input("请按Enter回到主菜单\n")
                continue
                
            
            if choice == '8':
                print()
                print("你选择了“更新比赛数据”")
                update_racedata.update_eventresult(db)
                print()
                input("请按Enter回到主菜单\n")
                continue




            if choice == '9':
                print()
                print("你选择了“校准积分”")
                test = input("请按Enter以下载最新积分榜，输入q回到上一级，输入Q回到主菜单 ")
                if test == 'q':
                    continue
                elif test == 'Q':
                    break
                pointsrecalibration.main(db)
                print()
                test = input("按Enter继续下载积分和结算表，输入q回到上一级，输入Q回到主菜单")
                if test == 'q':
                    continue
                elif test == 'Q':
                    break
                ClassificationTable.main(db)
                print()
                RaceResultTable.main(db)
                print()
                input("请按Enter回到主菜单\n")
                continue


            if choice == '10':
                print()
                print("你选择了“下载最新积分统计表”")
                test = input("请按Enter以下载最新积分榜，输入q回到上一级，输入Q回到主菜单 ")
                if test == 'q':
                    continue
                elif test == 'Q':
                    break
                ClassificationTable.main(db)
                print()
                input("请按Enter回到主菜单\n")
                continue


            if choice == '11':
                print()
                print("你选择了“下载最新积分统计表”")
                test = input("请按Enter以下载最新积分榜，输入q回到上一级，输入Q回到主菜单 ")
                if test == 'q':
                    continue
                elif test == 'Q':
                    break
                RaceResultTable.main(db)
                print()
                input("请按Enter回到主菜单\n")
                continue


            if choice == '12':
                print()
                print("你选择了“下载报名统计表”")
                test = input("请按Enter以下载今日比赛报名统计表，输入q回到上一级，输入Q回到主菜单 ")
                if test == 'q':
                    continue
                elif test == 'Q':
                    break
                print()
                ClassificationTable.registlist(db)
                print()
                input("请按Enter回到主菜单\n")
                continue


            if choice == '13':
                print()
                print("你选择了“下载LAN账号列表”")
                test = input("请按Enter以下载LAN账号列表，输入q回到上一级，输入Q回到主菜单 ")
                if test == 'q':
                    continue
                elif test == 'Q':
                    break
                print()
                ClassificationTable.lanuserlist(db)
                print()
                input("请按Enter回到主菜单\n")
                continue
            


            elif choice == '14':
                print("功能仍在开发中......请暂时手动打开文档阅读\n")
                input("请按Enter回到主菜单\n")
                continue



            if choice == '0':
                print()
                input("请按Enter键以退出............")
                func.logging(logpath, "\n\n\n\n\n\nProgram exiting with code 0......", end="\n\n")
                return 0

            else:
                continue
            


if __name__ == "__main__":
    main()