import upload_newdriver as newdriver
import upload_transferdriver as transdriver
import upload_qualiresult as qualiresult
import upload_raceresult as raceresult
import upload_racedirector as racedirector
import pointsrecalibration
import checkracestatus
import update_qualiresult
import update_raceresult
# import ClassificationTable
# import RaceResultTable

while True:
    print("欢迎来到AFR联赛积分管理系统 (v3.3)")
    print()
    print("1.上传排位赛成绩")   # checked
    print("2.上传正赛成绩")   # checked
    print("3.上传判罚数据")   # checked
    print("4.上传新加入车手")   # checked
    print("5.上传车手转会记录")   # checked
    print("6.更新比赛状态")   # checked
    print("7.下载最新积分统计表")   # checked
    print("8.下载最新比赛结算表")   # checked
    print("9.更新排位成绩")   # checked
    print("10.更新正赛成绩")   # checked
    print("11.校准积分")   # checked
    print("12.查看使用说明文档")
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

            elif choice == '2':
                print()
                print("你选择了“上传正赛成绩”")
                test = input("请按Enter以上传文件（记住别选错文件了）输入q回到主菜单 ")
                if test == 'q' or test == 'Q':
                    break
                raceresult.upload_race()
                print()
                input("请按Enter回到主菜单\n")
                break

            elif choice == '3':
                print()
                print("你选择了“上传判罚数据”")
                test = input("请按Enter以上传文件（记住别选错文件了）输入q回到主菜单 ")
                if test == 'q' or test == 'Q':
                    break
                racedirector.upload_racedirector()
                print()
                input("请按Enter回到主菜单\n")
                break

            elif choice == '4':
                print()
                print("你选择了“上传新车手数据”")
                test = input("请按Enter以上传文件（记住别选错文件了）输入q回到主菜单 ")
                if test == 'q' or test == 'Q':
                    break
                newdriver.welcome_newdriver()
                print()
                input("请按Enter回到主菜单\n")
                break

            elif choice == '5':
                print()
                print("你选择了“上传车手转会记录”")
                test = input("请按Enter以继续, 输入q回到主菜单 ")
                if test == 'q' or test == 'Q':
                    break
                transdriver.transferdriver()
                print()
                input("请按Enter回到主菜单\n")
                break

            elif choice == '6':
                print()
                print("你选择了“更新比赛状态”")
                checkracestatus.checkracestatus()
                print()
                break

            elif choice == '7':
                print()
                print("你选择了“下载最新积分统计表”")
                test = input("请按Enter以下载最新积分榜，输入q回到主菜单 ")
                if test == 'q' or test == 'Q':
                    break
                import ClassificationTable
                print()
                print("最新积分统计表下载成功，现在可以在总表中找到最新的积分情况")
                input("请按Enter回到主菜单\n")
                del ClassificationTable
                break
                
            elif choice == '8':
                print()
                print("你选择了“下载最新比赛结算表”")
                test = input("请按Enter以下载最新积分榜，输入q回到主菜单 ")
                if test == 'q' or test == 'Q':
                    break
                import RaceResultTable
                print()
                print("最新比赛结算表下载成功，现在可以在结算表中找到直至目前所有比赛的结算结果")
                input("请按Enter回到主菜单\n")
                del RaceResultTable
                break

            elif choice == '9':
                print()
                print("你选择了“更新排位成绩”")
                test = input("请按Enter以继续，输入q回到主菜单 ")
                if test == 'q' or test == 'Q':
                    break
                update_qualiresult.update_qualiresult()
                print()
                input("请按Enter回到主菜单\n")
                break

            elif choice == '10':
                print()
                print("你选择了“更新正赛成绩”")
                test = input("请按Enter以继续，输入q回到主菜单 ")
                if test == 'q' or test == 'Q':
                    break
                update_raceresult.update_raceresult()
                print()
                input("请按Enter回到主菜单\n")
                break

            elif choice == '11':
                print("你选择了“校准积分”")
                test = input("请按Enter以继续，输入q回到主菜单 ")
                if test == 'q' or test == 'Q':
                    break
                pointsrecalibration.menu()
                print()
                print("积分校准已完成")
                input("请按Enter回到主菜单\n")
                break

            elif choice == '12':
                print("功能仍在开发中......请暂时手动打开文档阅读\n")
                input("请按Enter回到主菜单\n")
                break

            else:
                raise ValueError("请输入正确的选项!!!")

        except ValueError as e:
            print()
            print(str(e))
            print()
            input("请按Enter键以继续............")
            break
