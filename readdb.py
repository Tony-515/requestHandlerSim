import sqlite3

def getAllRows():
    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        print("Connected to SQLite")

        sqlite_select_query = """SELECT * from Requests ORDER BY id DESC"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchmany(100)
        print("Total rows are:  ", len(records))
        print("Printing each row")
        for row in records:
            print("Id: ", row[0])
            print("Num: ", row[1])
            print("Fact: ", row[2])
            print("Timestamp: ", row[3])
            print("\n")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from table", error)
    finally:
        if connection:
            connection.close()
            print("The Sqlite connection is closed")

getAllRows()
