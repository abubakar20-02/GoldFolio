import os
import sqlite3

from xlsxwriter import Workbook

import DB_Code
from UserArchive import UserArchive
from Log import Log

import SetUpFile
import pandas as pd


class User:
    def __init__(self):
        self.c = None
        self.conn = None
        self.a = UserArchive()
        self.b = Log()

    def __SetUpConnection(self):
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

    def createTable(self):
        self.__SetUpConnection()
        self.c.execute('''
              CREATE TABLE IF NOT EXISTS User
              ([User_ID] VARCHAR PRIMARY KEY, [FirstName] TEXT , [LastName] TEXT, [Money] REAL)
              ''')
        self.conn.commit()
        self.conn.close()

    def deleteTable(self):
        self.__SetUpConnection()
        try:
            self.c.execute("SELECT * FROM User")
            Values = self.c.fetchall()
            self.c.execute("DELETE FROM User")
            self.conn.commit()
            self.b.insert(DB_Code.UD)
            self.Archive(Values)
        except sqlite3.Error as error:
            print(error)
        finally:
            self.conn.close()

    def Archive(self, Values):
        self.a.SetUpConnection()
        try:

            self.a.c.executemany("INSERT INTO ArchiveUser(User_ID, FirstName, LastName, Money) VALUES(?,?,?,?)", Values)
            self.a.conn.commit()
        except sqlite3.Error as error:
            print(error)
        finally:
            self.a.conn.close()

    def deleteRecord(self, User_ID):
        self.__SetUpConnection()
        try:
            self.c.execute("SELECT * FROM User WHERE User_ID = ?", (User_ID,))
            Values = self.c.fetchall()
            self.c.execute('''DELETE FROM Investment WHERE User_ID = ?''', (User_ID,))
            self.c.execute('''
                  DELETE FROM User WHERE User_Id = ?
                  ''', (User_ID,))
            self.conn.commit()
            self.b.insert(DB_Code.UD)
            self.Archive(Values)
        except Exception as e:
            self.conn.rollback()
            print(f"Error: {e}")
        finally:
            self.conn.close()

    def insertIntoTable(self, FName, LName, Money):
        self.__SetUpConnection()
        self.c.execute('''
          INSERT INTO User (User_ID, FirstName,LastName,Money)

                VALUES
                (?,?,?,?)
          ''', (self.generate_unique_initials(FName, LName), FName, LName, Money))
        self.conn.commit()
        self.b.insert(DB_Code.UI)
        self.conn.close()

    def updateRecord(self, User_ID, Money):
        self.__SetUpConnection()
        self.c.execute('''
              UPDATE User SET Money = ? WHERE User_ID = ?
              ''', (Money, User_ID))
        self.conn.commit()
        self.b.insert(DB_Code.UU)
        self.conn.close()

    def showTable(self):
        self.__SetUpConnection()
        try:
            self.c.execute('''
                      SELECT * FROM User
                      ''')
            self.conn.commit()
            df = pd.DataFrame(self.c.fetchall(), columns=['User_ID', 'FirstName', 'LastName', 'Money'])
            print(df)
        except sqlite3.Error as error:
            print(error)
        finally:
            self.conn.close()
        # self.convertToExcel()

    def convertToExcel(self):
        self.__SetUpConnection()
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
