import os, datetime, traceback
import deffunc as func
import dbconnect
import mysql.connector
import dbload as dbl

VERSION = "AFR v8.2 DBmanager"
logpath = "log/log.log"
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

try:
    db = dbconnect.connect_with_conf("server.json", "db")
except Exception:
    db = dbconnect.connect_with_conf("server.json")
cursor = db.cursor()

def dbcreate():
    dbname = input("please enter a database name: ")
    if dbname == "q" or dbname == "Q" or dbname == "quit" or dbname == "exit":
        return 0
    
    try:
        query = f'CREATE DATABASE {dbname};'
        cursor.execute(query)
        db.commit()

        func.logging(logpath, f'new database "{dbname}" created successfully\n\n', "\n\n")
        print(f'new database "{dbname}" created successfully')
        print("please remember to change \"server.json\" file before further action \n")

    except mysql.connector.errors.DatabaseError as e:
        errmsg = f'Database "{dbname}" already exist......'
        func.logging(logpath, traceback.format_exc())
        func.logging(logpath, str(e) + "\n" + errmsg + "\n")
        print(errmsg)
        print("please change \"server.json\" file for further action \n")


def dbdelete():
    dbname = input("please enter the database name: ")
    if dbname == "q" or dbname == "Q" or dbname == "quit" or dbname == "exit":
        return 0
    
    try:
        query = f'DROP DATABASE {dbname};'
        cursor.execute(query)
        db.commit()

        func.logging(logpath, f'database "{dbname}" deleted......\n\n')
        print(f'database "{dbname}" deleted......')

    except mysql.connector.errors.DatabaseError as e:
        errmsg = f'database "{dbname}" not exist\nit may already deleted in previous action......'
        func.logging(traceback.format_exc() + "\n")
        func.logging(str(e) + "\n" + errmsg + "\n")
        print(errmsg)



def dbinitialize():
    fd = open("dbinit/dbcreate.sql", "r")
    query = fd.read()
    fd.close()
    query = query.split(";")

    for i in range(0, len(query)-1):
        token = query[i].split(" ")
        func.logging(logpath, f'creating table {token[2]}......')
        print(f'creating table {token[2]}......')
        cursor.execute(query[i])
        db.commit()

    func.logging(logpath)
    print()

    dbl.dbload_basic()
    db.commit()



def dbload():
    dbl.dbload()



def dbclear():
    fd = open("dbinit/dbclear.sql", "r")
    query = fd.read()
    fd.close()
    query = query.split(";")

    for i in range(0, len(query)-1):
        token = query[i].split(" ")
        print(f'clearing table {token[-1].replace(";","")}......')
        cursor.execute(query[i])
    db.commit()



def dbdrop():
    fd = open("dbinit/dbdrop.sql", "r")
    query = fd.read()
    fd.close()
    query = query.split(";")

    for i in range(0, len(query)-1):
        token = query[i].split(" ")
        func.logging(logpath, f'deleting table {token[-1].replace(";","")}......')
        print(f'deleting table {token[-1].replace(";","")}......')
        cursor.execute(query[i])
    
    func.logging(logpath)
    print()

    db.commit()



def main():
    while True:
        print(f'AFR Automation Table manager ({VERSION})')
        print()
        print("1.initialize database")
        print("2.load database (undeveloped, don't use)")
        print("3.clear database (also don't use, use 4.drop db instead and start over)")
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
                errmsg = "database initialize failed, please check your input data and settings to try again"
                func.logging(logpath, traceback.format_exc() + "\n")
                func.logging(logpath, str(e) + "\n" + errmsg + "\n")
                print(str(e))
                print(errmsg)
            finally:
                input("press enter back to main menu")
        




        elif choice == '2':
            try:
                # dbload()
                pass
            except Exception as e:
                print(str(e))
            finally:
                input("press enter back to main menu")
        
        elif choice == '3':
            try:
                # dbclear()
                pass
            except Exception as e:
                print(str(e))
            finally:
                input("press enter back to main menu")
        



        elif choice == '4':
            try:
                dbdrop()
            except Exception as e:
                func.logging(logpath, traceback.format_exc() + "\n")
                func.logging(logpath, str(e) + "\n" + errmsg + "\n\n")
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
            logf = open(logpath, "a")
            func.logging(logpath, "Program exiting with code 0......", end="\n\n\n\n\n\n")
            logf.close()
            break
        

if __name__ == "__main__":
    main()