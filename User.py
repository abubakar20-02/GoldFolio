import os
import sqlite3

from xlsxwriter import Workbook

import SetUpFile
import pandas as pd


class User:
    def __init__(self):
        self.c = None
        self.conn = None

    def SetUpConnection(self):
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
        self.SetUpConnection()
        try:
            self.c.execute("DROP TABLE User")
            self.conn.commit()
        except sqlite3.Error as error:
            print(error)
        finally:
            self.conn.close()

    def createTable(self):
        self.SetUpConnection()
        self.c.execute('''
              CREATE TABLE IF NOT EXISTS User
              ([User_ID] VARCHAR PRIMARY KEY, [FirstName] TEXT , [LastName] TEXT, [Money] REAL, [Gold] REAL)
              ''')
        self.conn.commit()
        self.conn.close()

    def deleteRecord(self, User_ID):
        self.SetUpConnection()
        try:
            self.c.execute('''DELETE FROM Investment WHERE User_ID = ?''', (User_ID,))
            self.c.execute('''
                  DELETE FROM User WHERE User_Id = ?
                  ''', (User_ID,))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"Error: {e}")
        finally:
            self.conn.close()

    def insertIntoTable(self, FName, LName, Money, Gold):
        self.SetUpConnection()
        self.c.execute('''
          INSERT INTO User (User_ID, FirstName,LastName,Money,Gold)

                VALUES
                (?,?,?,?,?)
          ''', (self.generate_unique_initials(FName, LName), FName, LName, Money, Gold))
        self.conn.commit()
        self.conn.close()

    def updateRecord(self, User_ID, Money, Gold):
        self.SetUpConnection()
        self.c.execute('''
              UPDATE User SET Money = ? , Gold = ? WHERE User_ID = ?
              ''', (Money, Gold, User_ID))
        self.conn.commit()
        self.conn.close()

    def showTable(self):
        self.SetUpConnection()
        try:
            self.c.execute('''
                      SELECT * FROM User
                      ''')
            self.conn.commit()
            df = pd.DataFrame(self.c.fetchall(), columns=['User_ID', 'FirstName', 'LastName', 'Money', 'Gold'])
            print(df)
        except sqlite3.Error as error:
            print(error)
        finally:
            self.conn.close()
        # self.convertToExcel()

    def convertToExcel(self):
        self.SetUpConnection()
        workbook = Workbook(SetUpFile.ExcelFileName)
        worksheet = workbook.add_worksheet()
        self.c.execute("select * from User")
        mysel = self.c.execute("select * from User")
        for i, row in enumerate(mysel):
            for j, value in enumerate(row):
                worksheet.write(i + 1, j, value)
        workbook.close()
        self.conn.commit()
        self.conn.close()
        os.system(SetUpFile.ExcelFileName)


