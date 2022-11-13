import traceback
import connectserver
import mysql.connector
import dbload as dbl

try:
    db = connectserver.connectserver("server.json", "db")
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

    for i in range(0, len(query)-1):
        token = query[i].split(" ")
        print(f'creating table {token[2]}......')
        cursor.execute(query[i])
    
    print()

    dbl.dbload_basic()
    db.commit()



def dbload():
    dbl.dbload()



def dbclear():
    fd = open("dbclear.sql", "r")
    query = fd.read()
    fd.close()
    query = query.split(";")

    for i in range(0, len(query)-1):
        token = query[i].split(" ")
        print(f'clearing table {token[-1].replace(";","")}......')
        cursor.execute(query[i])
    db.commit()



def dbdrop():
    fd = open("dbdrop.sql", "r")
    query = fd.read()
    fd.close()
    query = query.split(";")

    for i in range(0, len(query)-1):
        token = query[i].split(" ")
        print(f'deleting table {token[-1].replace(";","")}......')
        cursor.execute(query[i])
    db.commit()



def main():
    while True:
        print("AFR Automation Table manager (AFR Version v7.0)")
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
                print(str(e))
                print("database initialize failed, please check your input data and settings to try again")
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