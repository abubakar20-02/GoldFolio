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
        try:
            self.c.execute('''
                      SELECT * FROM User
                      ''')
            df = pd.DataFrame(self.c.fetchall(), columns=['User_ID', 'FirstName', 'LastName', 'Money', 'Gold'])
            print(df)
        except sqlite3.Error as error:
            print(error)

        # self.convertToExcel()

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


class Investment:
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect(SetUpFile.DBName)
        self.conn.execute("PRAGMA busy_timeout = 500")
        self.c = self.conn.cursor()

    def deleteTable(self):
        try:
            self.c.execute("DROP TABLE Investment")
        except sqlite3.Error as error:
            print("Failed to delete record from sqlite table", error)

    def createTable(self):
        self.c.execute('''
              CREATE TABLE IF NOT EXISTS Investment
              ([Investment_ID] VARCHAR PRIMARY KEY, [User_ID] VARCHAR,[Gold] REAL , [BoughtFor] REAL,
              FOREIGN KEY(User_ID) REFERENCES User(User_ID))
              ''')
        self.conn.commit()

    # def deleteRecord(self, User_ID):
    #     self.c.execute('''
    #           DELETE FROM User WHERE User_Id = ?
    #           ''', (User_ID,))
    #     self.conn.commit()
    #
    def insertIntoTable(self, InvestmentId, UserID, Gold, BoughtFor):
        try:
            self.c.execute('''
                  INSERT INTO Investment (Investment_ID, User_ID , Gold ,BoughtFor)

                        VALUES
                        (?,?,?,?)
                  ''', (InvestmentId, UserID, Gold, BoughtFor))
            self.conn.commit()
        except sqlite3.Error as error:
            print(error)

    #
    # def updateRecord(self, User_ID, Money, Gold):
    #     self.c.execute('''
    #           UPDATE User SET Money = ? , Gold = ? WHERE User_ID = ?
    #           ''', (Money, Gold, User_ID))
    #     self.conn.commit()
    #
    def showTable(self):
        try:
            self.c.execute('''
                      SELECT * FROM Investment
                      ''')
            df = pd.DataFrame(self.c.fetchall(),
                              columns=['Investment_ID', 'User_ID', 'Gold', 'BoughtFor'])
            print(df)
        except sqlite3.Error as error:
            print(error)

    def showInvestmentForUser(self, User_ID):
        self.c.execute('''
                  SELECT * FROM Investment WHERE User_ID =?
                  ''', (User_ID,))
        df = pd.DataFrame(self.c.fetchall(),
                          columns=['Investment_ID', 'User_ID', 'Gold', 'BoughtFor'])
        print(df)
    #     # self.convertToExcel()
    #
    # def convertToExcel(self):
    #     workbook = Workbook(SetUpFile.ExcelFileName)
    #     worksheet = workbook.add_worksheet()
    #     self.c.execute("select * from User")
    #     mysel = self.c.execute("select * from User")
    #     for i, row in enumerate(mysel):
    #         for j, value in enumerate(row):
    #             worksheet.write(i + 1, j, value)
    #     workbook.close()
    #     os.system(SetUpFile.ExcelFileName)


User = User()
Inv = Investment()
# User.createTable()
# Inv.createTable()
# User.insertIntoTable("Muhammad", "Abubakar", 12,1)
# User.insertIntoTable("Mo","Abu",11,1)
# Inv.insertIntoTable("1","ma", 40,12)
# User.deleteRecord("ma")

Inv.showTable()
Inv.insertIntoTable("2","ma1",12,12)
Inv.showTable()
# User.showTable()
