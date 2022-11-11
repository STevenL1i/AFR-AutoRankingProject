import traceback
import connectserver
import mysql.connector
import dbload as dbl

try:
    db = connectserver.connectserver("server.json", "league")
except Exception:
    db = connectserver.connectserver("server.json")
cursor = db.cursor()

def dbcreate():
    dbname = input("please enter a database name: ")
    if dbname == "q" or dbname == "Q" or dbname == "quit" or dbname == "exit":
        return 0
    
    try:
        query = f'CREATE DATABASE {dbname};'
        cursor.execute(query)
        db.commit()

        print(f'new database "{dbname}" created successfully')
        print("please remember to change \"server.json\" file before further action \n")

    except mysql.connector.errors.DatabaseError:
        print(f'Database "{dbname}" already exist......')
        print("please change \"server.json\" file for further action \n")


def dbdelete():
    dbname = input("please enter the database name: ")
    if dbname == "q" or dbname == "Q" or dbname == "quit" or dbname == "exit":
        return 0
    
    try:
        query = f'DROP DATABASE {dbname};'
        cursor.execute(query)
        db.commit()

        print(f'database "{dbname}" deleted......')

    except mysql.connector.errors.DatabaseError:
        print(f'database "{dbname}" not exist\nit may already deleted in previous action......')



def dbinitialize():
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
        try:
            cursor.execute(q)
        except:
            pass
    db.commit()



def main():
    while True:
        print("AFR Automation Table manager (AFR Version)")
        print()
        print("1.initialize database")
        print("2.load database")
        print("3.clear database")
        print("4.drop database")
        print("5.create new database")
        print("6.delete database")
        print()
        print("0.退出")
        choice = input("choose function： ")
        if choice == '1':
            try:
                dbinitialize()
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
        
        elif choice == "5":
            try:
                dbcreate()
            except Exception as e:
                print(str(e))
            finally:
                input("press enter back to main menu")
        
        elif choice == "6":
            try:
                dbdelete()
            except Exception as e:
                print(str(e))
            finally:
                input("press enter back to main menu")
        
        elif choice == '0':
            break
        

if __name__ == "__main__":
    main()