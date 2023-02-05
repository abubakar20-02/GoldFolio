import sqlite3
import pandas as pd


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


def deleteTable():
    c.execute("DROP TABLE User")


deleteTable()


def createTable():
    conn = sqlite3.connect('test_database')
    c = conn.cursor()
    c.execute('''
          CREATE TABLE IF NOT EXISTS User
          ([User_ID] VARCHAR PRIMARY KEY, [FirstName] TEXT , [LastName] TEXT, [Money] REAL, [Gold] REAL)
          ''')
    conn.commit()


createTable()


def insertIntoTable(FName, LName, Money, Gold):
    c.execute('''
          INSERT INTO User (User_ID, FirstName,LastName,Money,Gold)

                VALUES
                (?,?,?,?,?)
          ''', (generate_unique_initials(conn, FName, LName), FName, LName, Money, Gold))
    conn.commit()


insertIntoTable("Muhammad", "Abubakar", 123.1, 11)
insertIntoTable("Muhammad", "Abubakar", 123.1, 11)
insertIntoTable("Muhammad", "Abubakar", 123.1, 11)

c.execute('''
          SELECT * FROM User
          ''')

df = pd.DataFrame(c.fetchall(), columns=['User_ID', 'FirstName', 'LastName', 'Money', 'Gold'])
print(df)
