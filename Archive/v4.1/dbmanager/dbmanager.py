import traceback
import connectserver
import dbload as dbl

db = connectserver.connectserver()
cursor = db.cursor()

def dbcreate():
    fd = open("dbcreate.sql", "r")
    query = fd.read()
    fd.close()
    query = query.split(";")

    for q in query:
        cursor.execute(q)
    db.commit()

    dbl.dbload_basic()


def dbload():
    dbl.dbload()


def dbclear():
    fd = open("dbclear.sql", "r")
    query = fd.read()
    fd.close()
    query = query.split(";")

    for q in query:
        cursor.execute(q)
    db.commit()

def dbdrop():
    fd = open("dbdrop.sql", "r")
    query = fd.read()
    fd.close()
    query = query.split(";")

    for q in query:
        cursor.execute(q)
    db.commit()



def main():
    while True:
        print("AFR Automation Table manager")
        print()
        print("1.create database")
        print("2.load database")
        print("3.clear database")
        print("4.drop database")
        print()
        print("0.退出")
        choice = input("choose function： ")
        if choice == '1':
            try:
                dbcreate()
            except Exception as e:
                print(traceback.format_exc())
                print(str(e))
            finally:
                input("press enter back to main menu")
        elif choice == '2':
            try:
                dbload()
            except Exception as e:
                print(str(e))
            finally:
                input("press enter back to main menu")
        elif choice == '3':
            try:
                dbclear()
            except Exception as e:
                print(str(e))
            finally:
                input("press enter back to main menu")
        elif choice == '4':
            try:
                dbdrop()
            except Exception as e:
                print(str(e))
            finally:
                input("press enter back to main menu")
        elif choice == '0':
            break
        

if __name__ == "__main__":
    main()