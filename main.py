import sqlite3
import pandas as pd
from xlsxwriter import Workbook
import os


def generate_initials(first_name, last_name):
    initials = first_name[0].lower() + last_name[0].lower()
    return initials


def generate_unique_initials(conn, first_name, last_name):
    initials = generate_initials(first_name, last_name)
    i = 1
    while True:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM User WHERE User_Id = ?", (initials,))
        count = cursor.fetchone()[0]
        if count == 0:
            return initials
        initials = generate_initials(first_name, last_name) + str(i)
        i += 1


conn = sqlite3.connect('test_database')
c = conn.cursor()


def deleteTable(c):
    c.execute("DROP TABLE User")


deleteTable(c)


def createTable(c):
    c.execute('''
          CREATE TABLE IF NOT EXISTS User
          ([User_ID] VARCHAR PRIMARY KEY, [FirstName] TEXT , [LastName] TEXT, [Money] REAL, [Gold] REAL)
          ''')
    conn.commit()


createTable(c)


def deleteRecord(c, User_ID):
    c.execute('''
          DELETE FROM User WHERE User_Id = ?
          ''', (User_ID,))
    conn.commit()


def insertIntoTable(c, FName, LName, Money, Gold):
    c.execute('''
          INSERT INTO User (User_ID, FirstName,LastName,Money,Gold)

                VALUES
                (?,?,?,?,?)
          ''', (generate_unique_initials(conn, FName, LName), FName, LName, Money, Gold))
    conn.commit()


def updateRecord(c, User_ID, Money, Gold):
    c.execute('''
          UPDATE User SET Money = ? , Gold = ? WHERE User_ID = ?
          ''', (Money, Gold, User_ID))
    conn.commit()


insertIntoTable(c, "Muhammad", "Abubakar", 123.1, 11)
insertIntoTable(c, "Muhammad", "Abubakar", 123.1, 11)
insertIntoTable(c, "Muhammad", "Abubakar", 123.1, 11)
deleteRecord(c, "ma1")
insertIntoTable(c, "Muhammad", "Abubakar", 123.1, 12)
updateRecord(c, "ma2", 10.1, 10)
insertIntoTable(c, "Hamza", "Rizwan", 10, 1)
updateRecord(c, "hr", 12.6, 1234)
insertIntoTable(c, "Hamza", "Rizwan", 10, 1)


def showTable(c):
    c.execute('''
              SELECT * FROM User
              ''')
    df = pd.DataFrame(c.fetchall(), columns=['User_ID', 'FirstName', 'LastName', 'Money', 'Gold'])
    print(df)
    convertToExcel(c)


def convertToExcel(c):
    workbook = Workbook('output.xlsx')
    worksheet = workbook.add_worksheet()
    c.execute("select * from User")
    mysel = c.execute("select * from User")
    for i, row in enumerate(mysel):
        for j, value in enumerate(row):
            worksheet.write(i+1, j, value)
    workbook.close()
    os.system('output.xlsx')

showTable(c)
