import os
import sqlite3
import uuid

from xlsxwriter import Workbook

import DB_Code
from Archive import UserArchive
from Log import Log
import SetUpFile
import pandas as pd
from Investment import Investment


def generateTransactionID():
    return str(uuid.uuid4())


class User:
    def __init__(self):
        self.c = None
        self.conn = None
        self.a = UserArchive()
        self.Log = Log()
        self.UserLog = Log.UserLog()
        self.Investment = Investment()

    def __SetUpConnection(self):
        self.conn = sqlite3.connect(SetUpFile.DBName)
        self.c = self.conn.cursor()

    def __generate_initials(self, first_name, last_name):
        initials = first_name[0].lower() + last_name[0].lower()
        return initials

    def generate_unique_initials(self, first_name, last_name):
        """Generate InvestmentArchive unique user ID using first name and last name."""
        initials = self.__generate_initials(first_name, last_name)
        i = 1
        while True:
            self.c.execute("SELECT COUNT(*) FROM User WHERE User_Id = ?", (initials,))
            count = self.c.fetchone()[0]
            if count == 0:
                return initials
            initials = self.__generate_initials(first_name, last_name) + str(i)
            i += 1

    def createTable(self):
        self.__SetUpConnection()
        self.c.execute('''
              CREATE TABLE IF NOT EXISTS User
              ([User_ID] VARCHAR PRIMARY KEY, [FirstName] TEXT , [LastName] TEXT, [Money] REAL)
              ''')
        self.conn.commit()
        self.conn.close()

    def deleteTable(self, *LogChanges):
        self.__SetUpConnection()
        try:
            self.c.execute("SELECT * FROM User")
            Values = self.c.fetchall()
            self.c.execute("SELECT COUNT(*) FROM User")
            RecordsAffected = self.c.fetchone()[0]
            self.c.execute("DELETE FROM User")
            self.conn.commit()
            if LogChanges == ():
                self.__LogForDelete(RecordsAffected, None, Values, generateTransactionID())
        except sqlite3.Error as error:
            print(error)
        finally:
            self.conn.close()

    def deleteRecord(self, User_ID, LogChanges=True):
        """Takes user id to delete record and if log change is not empty, then the code saves InvestmentArchive log."""
        Transaction_ID = generateTransactionID()
        self.__SetUpConnection()
        try:
            self.c.execute("SELECT * FROM User WHERE User_ID = ?", (User_ID,))
            Values = self.c.fetchall()
            self.c.execute("SELECT COUNT(*) FROM Investment WHERE User_ID = ?", (User_ID,))
            RecordsAffected = self.c.fetchone()[0]

            print("checked")

            if RecordsAffected > 0:
                # jnkasdjnasdkskhjansahjkndsansdjkajkasdkasdhjn
                self.Investment.deleteRecord(User_ID, LogChanges=False)
            self.conn.commit()
            self.c.execute('''
                  DELETE FROM User WHERE User_Id = ?
                  ''', (User_ID,))
            self.conn.commit()
            if LogChanges is True:
                self.Log.insert(Transaction_ID, DB_Code.UD)
                self.__LogForDelete(RecordsAffected, User_ID, Values, Transaction_ID)
        except Exception as e:
            self.conn.rollback()
            print(f"Error: {e}")
        finally:
            self.conn.close()

    def __LogForDelete(self, RecordsAffected, User_ID, Values, Transaction_ID):
        # sadklmasdjhnklaslkedsmaklsmlskasdkaln
        self.UserLog.DeleteStatement(Transaction_ID, RecordsAffected, User_ID)
        self.a.Archive(DB_Code.DELETECOMMAND, Values)

    def __LogForInsert(self, FName, LName, Money, User_ID, Transaction_ID):
        self.UserLog.InsertStatement(Transaction_ID, User_ID, FName, LName, Money)
        self.Log.insert(Transaction_ID, DB_Code.UI)

    def __LogForUpdate(self, Money, User_ID, Values, TransactionID):
        self.Log.insert(TransactionID, DB_Code.UU)
        self.UserLog.UpdateStatement(TransactionID, User_ID, Money)
        # mention this was updated
        self.a.Archive(DB_Code.UPDATECOMMAND, Values)

    def insertIntoTable(self, FName, LName, Money, LogChanges=True):
        """Takes record data to insert and if log change is not empty, then the code saves InvestmentArchive log."""
        self.__SetUpConnection()
        User_ID = self.generate_unique_initials(FName, LName)
        self.c.execute('''
          INSERT INTO User (User_ID, FirstName,LastName,Money)

                VALUES
                (?,?,?,?)
          ''', (User_ID, FName, LName, Money))
        self.conn.commit()
        if LogChanges is True:
            self.__LogForInsert(FName, LName, Money, User_ID, generateTransactionID())
        self.conn.close()

    def updateRecord(self, User_ID, Money, LogChanges=True):
        """Takes user id to locate the user, take money to change and if log change is not empty, then the code saves
        InvestmentArchive log. """
        self.__SetUpConnection()
        self.c.execute("SELECT * FROM User WHERE User_ID = ?", (User_ID,))
        Values = self.c.fetchall()
        self.c.execute('''
              UPDATE User SET Money = ? WHERE User_ID = ?
              ''', (Money, User_ID))
        self.conn.commit()
        if LogChanges is True:
            TransactionID = generateTransactionID()
            self.__LogForUpdate(Money, User_ID, Values, TransactionID)
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
