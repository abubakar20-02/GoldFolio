import sqlite3
import pandas as pd
from xlsxwriter import Workbook
import os

import SetUpFile


class User:
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect(SetUpFile.DBName)
        self.c = self.conn.cursor()

    def generate_initials(self, first_name, last_name):
        initials = first_name[0].lower() + last_name[0].lower()
        return initials

    def generate_unique_initials(self, first_name, last_name):
        initials = self.generate_initials(first_name, last_name)
        i = 1
        while True:
            self.c.execute("SELECT COUNT(*) FROM User WHERE User_Id = ?", (initials,))
            count = self.c.fetchone()[0]
            if count == 0:
                return initials
            initials = self.generate_initials(first_name, last_name) + str(i)
            i += 1

    def deleteTable(self):
        try:
            self.c.execute("DROP TABLE User")
        except sqlite3.Error as error:
            print("Failed to delete record from sqlite table", error)

    def createTable(self):
        self.c.execute('''
              CREATE TABLE IF NOT EXISTS User
              ([User_ID] VARCHAR PRIMARY KEY, [FirstName] TEXT , [LastName] TEXT, [Money] REAL, [Gold] REAL)
              ''')
        self.conn.commit()

    def deleteRecord(self, User_ID):
        self.c.execute('''
              DELETE FROM User WHERE User_Id = ?
              ''', (User_ID,))
        self.conn.commit()

    def insertIntoTable(self, FName, LName, Money, Gold):
        self.c.execute('''
              INSERT INTO User (User_ID, FirstName,LastName,Money,Gold)

                    VALUES
                    (?,?,?,?,?)
              ''', (self.generate_unique_initials(FName, LName), FName, LName, Money, Gold))
        self.conn.commit()

    def updateRecord(self, User_ID, Money, Gold):
        self.c.execute('''
              UPDATE User SET Money = ? , Gold = ? WHERE User_ID = ?
              ''', (Money, Gold, User_ID))
        self.conn.commit()

    def showTable(self):
        self.c.execute('''
                  SELECT * FROM User
                  ''')
        df = pd.DataFrame(self.c.fetchall(), columns=['User_ID', 'FirstName', 'LastName', 'Money', 'Gold'])
        print(df)
        self.convertToExcel()

    def convertToExcel(self):
        workbook = Workbook(SetUpFile.ExcelFileName)
        worksheet = workbook.add_worksheet()
        self.c.execute("select * from User")
        mysel = self.c.execute("select * from User")
        for i, row in enumerate(mysel):
            for j, value in enumerate(row):
                worksheet.write(i + 1, j, value)
        workbook.close()
        os.system(SetUpFile.ExcelFileName)


User = User()

User.deleteTable()
User.deleteTable()

User.createTable()

User.insertIntoTable("Muhammad", "Abubakar", 123.1, 11)
User.insertIntoTable("Muhammad", "Abubakar", 123.1, 11)
User.insertIntoTable("Muhammad", "Abubakar", 123.1, 11)
User.deleteRecord("ma1")
User.insertIntoTable("Muhammad", "Abubakar", 123.1, 12)
User.updateRecord("ma2", 10.1, 10)
User.insertIntoTable("Hamza", "Rizwan", 10, 1)
User.updateRecord("hr", 12.6, 1234)
User.insertIntoTable("Hamza", "Rizwan", 10, 1)

User.showTable()
