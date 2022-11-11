import upload_qualiresult as qualiresult
import upload_raceresult as raceresult
import upload_racedirector as racedirector

import update_qualiresult as updatequali
import update_raceresult as updaterace
import update_racedirector as updaterd

import upload_newdriver as newdriver
import upload_transferdriver as transferdriver
import update_racestatus as racestatus

import pointsrecalibration

while True:
    print("欢迎来到SVS联赛积分管理系统（2022/10/08）")
    print()
    print("1.上传排位赛成绩")           # passed
    print("2.上传正赛成绩")             # passed
    print("3.上传判罚数据")             # passed
    print("4.更新排位成绩")             # passed
    print("5.更新正赛成绩")             # passed
    print("6.更新判罚数据")             # passed
    print("7.上传新加入车手")           # passed
    print("8.上传车手转会记录")         # passed
    print("9.更新比赛状态")             # passed
    print("10.校准积分")                # passed
    print("11.下载最新积分统计表")      # half done (driver leaderboard final output)
    print("12.下载最新比赛结算表")      # half done (race result final output)
    print()
    print("0.退出")
    print()
    choice = input("请输入你所要选择的功能： ")
    if choice == '0':
        print()
        input("请按Enter键以退出............")
        break

    while True:
        try:
            if choice == '1':
                print()
                print("你选择了“上传排位赛成绩”")
                test = input("请按Enter以上传文件（记住别选错文件了）输入q回到主菜单 ")
                if test == 'q' or test == 'Q':
                    break
                qualiresult.upload_quali()
                print()
                input("请按Enter回到主菜单\n")
                break

            if choice == '2':
                print()
                print("你选择了“上传正赛成绩”")
                test = input("请按Enter以上传文件（记住别选错文件了）输入q回到主菜单 ")
                if test == 'q' or test == 'Q':
                    break
                raceresult.upload_race()
                print()
                input("请按Enter回到主菜单\n")
                break

            if choice == '3':
                print()
                print("你选择了“上传判罚数据”")
                test = input("请按Enter以上传文件（记住别选错文件了）输入q回到主菜单 ")
                if test == 'q' or test == 'Q':
                    break
                racedirector.upload_racedirector()
                print()
                input("请按Enter回到主菜单\n")
                break

            if choice == '4':
                print()
                print("你选择了“更新排位成绩”")
                test = input("请按Enter以继续，跟随系统提示进行操作，输入q回到主菜单 ")
                if test == 'q' or test == 'Q':
                    break
                updatequali.update_qualiresult()
                print()
                input("请按Enter回到主菜单\n")
                break

            if choice == '5':
                print()
                print("你选择了“更新正赛成绩”")
                test = input("请按Enter以继续，跟随系统提示进行操作，输入q回到主菜单 ")
                if test == 'q' or test == 'Q':
                    break
                updaterace.update_raceresult()
                print()
                input("请按Enter回到主菜单\n")
                break

            if choice == '6':
                print()
                print("你选择了“更新判罚数据”")
                test = input("请按Enter以继续，跟随系统提示进行操作，输入q回到主菜单 ")
                if test == 'q' or test == 'Q':
                    break
                updaterd.update_racedirector()
                print()
                input("请按Enter回到主菜单\n")
                break


            if choice == '7':
                print()
                print("你选择了“上传新车手数据”")
                test = input("请按Enter以上传文件（记住别选错文件了）输入q回到主菜单 ")
                if test == 'q' or test == 'Q':
                    break
                newdriver.welcome_newdriver()
                print()
                input("请按Enter回到主菜单\n")
                break

            if choice == '8':
                print()
                print("你选择了“上传车手转会记录”")
                test = input("请按Enter以上传文件（记住别选错文件了）输入q回到主菜单 ")
                if test == 'q' or test == 'Q':
                    break
                transferdriver.transferdriver()
                print()
                input("请按Enter回到主菜单\n")
                break
            
            if choice == '9':
                print()
                print("你选择了“更新比赛状态”")
                racestatus.askuserrace()
                print()
                input("比赛状态已更新，按Enter以回到主菜单")
                break

            if choice == '10':
                print()
                print("你选择了“校准积分”")
                test = input("请按Enter以继续，输入q回到主菜单 ")
                if test == 'q' or test == 'Q':
                    break
                pointsrecalibration.main()
                print()
                input("积分已校准完成，按Enter以回到主菜单")
                break

            if choice == '11':
                print()
                print("你选择了“下载最新积分统计表”")
                test = input("请按Enter以继续，输入q回到主菜单 ")
                if test == 'q' or test == 'Q':
                    break
                try:
                    import ClassificationTable
                    ClassificationTable.main()
                    print()
                    input("请按Enter回到主菜单\n")
                    del ClassificationTable
                    break
                except Exception as e:
                    print(str(e))
                    break

            if choice == '12':
                print()
                print("你选择了“下载最新比赛结算表”")
                test = input("请按Enter以继续，输入q回到主菜单 ")
                if test == 'q' or test == 'Q':
                    break
                try:
                    import RaceResultTable
                    RaceResultTable.main()
                    print()
                    input("请按Enter回到主菜单\n")
                    del RaceResultTable
                    break
                except Exception as e:
                    print(str(e))
                    break
            
            else:
                raise ValueError("请输入正确的选项!!!")
        


        
        except ValueError as e:
            print()
            print(str(e))
            print()
            input("请按Enter键以继续............")
            break