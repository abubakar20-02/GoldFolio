import math
import os
import sqlite3
import uuid

import pandas as pd
from xlsxwriter import Workbook

import DBFunctions
import DB_Code
import SetUpFile
from Archive import UserArchive
from Investment import Investment
from Log import Log


def generateTransactionID():
    return str(uuid.uuid4())


class User:
    def __init__(self):
        self.c = None
        self.conn = None
        self.Profile = None
        self.a = UserArchive()
        self.Log = Log()
        self.UserLog = Log.UserLog()
        self.Investment = Investment()
        self.MoneyLog = Log.Money()

    def __SetUpConnection(self):
        self.conn = sqlite3.connect(SetUpFile.DBName)
        self.c = self.conn.cursor()

    def SelectProfile(self, Profile):
        self.Profile = Profile

    def ImportFromExcel(self):
        source = 'UserTemplate.xlsx'
        target = 'User.xlsx'
        # shutil.copyfile(source,target)
        # os.system(target)

        sheet_name = 'Sheet1'

        path = target

        # Read the Excel file into a DataFrame
        df = pd.read_excel(path, sheet_name=sheet_name)

        # Define the SQL query to insert the data into the table
        table_name = "User"
        columns = ','.join(df.columns)
        placeholders = ','.join(['?' for _ in range(len(df.columns))])
        print(placeholders)
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        print(sql)

        # Loop through the rows in the DataFrame and insert them into the table
        for _, row in df.iterrows():
            values = tuple(row)

            # self.c.execute(sql, values)
            # dont update log again and again but add to user log
            try:
                # if not float would go to except.
                float(values[3])
                if not (values[1].isalpha() and values[2].isalpha()):
                    print('name contains invalid letters')
                    continue
                if str(values[0])[:2] == self.generate_unique_initials(values[1], values[2])[:2]:
                    # close function after we finish using generate unique initials.
                    self.conn.close()
                    self.insertIntoTable(values[1], values[2], values[3], UserID=values[0], LogChanges=False)
                if isinstance(values[0], (int, float)) and math.isnan(values[0]):
                    self.insertIntoTable(values[1], values[2], values[3], LogChanges=False)
                    # print("empty")
                print("fine")
            except:
                print("wrong")
        # send number of values added to user log

    def __generate_initials(self, first_name, last_name):
        initials = first_name[0].lower() + last_name[0].lower()
        return initials

    def generate_unique_initials(self, first_name, last_name):
        """Generate InvestmentArchive unique user ID using first name and last name."""
        self.__SetUpConnection()
        initials = self.__generate_initials(first_name, last_name)
        i = 1
        while True:
            self.c.execute("SELECT COUNT(*) FROM User WHERE User_Id = ?", (initials,))
            count = self.c.fetchone()[0]
            if count == 0:
                break
            initials = self.__generate_initials(first_name, last_name) + str(i)
            i += 1
        return initials

    def createTable(self):
        self.__SetUpConnection()
        self.c.execute('''
              CREATE TABLE IF NOT EXISTS User
              ([User_ID] VARCHAR PRIMARY KEY, [FirstName]  TEXT NOT NULL , [LastName] TEXT NOT NULL, [Money] REAL NOT NULL)
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
            a = RecordsAffected
            print("checked")
            while a > 0:
                # jnkasdjnasdkskhjansahjkndsansdjkajkasdkasdhjn
                self.Investment.deleteRecord(User_ID, LogChanges=False)
                a = a - 1
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
        print("wow")
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

    def insertIntoTable(self, FName, LName, Money, LogChanges=True, UserID=None):
        """Takes record data to insert and if log change is not empty, then the code saves InvestmentArchive log."""
        self.__SetUpConnection()
        if UserID is None:
            UserID = self.generate_unique_initials(FName, LName)
        self.c.execute('''
          INSERT INTO User (User_ID, FirstName,LastName,Money)

                VALUES
                (?,?,?,?)
          ''', (UserID, FName, LName, Money))
        self.conn.commit()
        if LogChanges is True:
            Transaction_ID = generateTransactionID()
            self.__LogForInsert(FName, LName, Money, UserID, Transaction_ID)
            self.MoneyLog.insertIntoTable(UserID, DB_Code.MoneyIn, Money, Transaction_ID=Transaction_ID)
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

    def isUserExist(self, User_ID):
        self.__SetUpConnection()
        self.c.execute('''
                  SELECT COUNT(*) FROM User WHERE User_ID = ?
                  ''', (User_ID,))
        Count = self.c.fetchone()[0]
        self.conn.close()
        if Count > 0:
            return True
        else:
            return False

    def getMoney(self):
        self.__SetUpConnection()
        self.c.execute('''
                  SELECT Money FROM User WHERE User_ID = ?
                  ''', (self.Profile,))
        Money = self.c.fetchone()[0]
        self.conn.close()
        return Money

    def updateMoney(self, Money):
        self.__SetUpConnection()
        self.c.execute('''
                  UPDATE User SET Money=? WHERE User_ID = ?
                  ''', (Money, self.Profile))
        self.conn.commit()
        self.conn.close()

    def addMoney(self, Money, LogChanges=None):
        print('add money')
        TotalMoney = self.getMoney() + Money
        self.updateMoney(TotalMoney)
        if LogChanges is None:
            Transaction_ID = generateTransactionID()
            self.Log.insert(Transaction_ID, DB_Code.MoneyIn)
            self.MoneyLog.insertIntoTable(self.Profile, DB_Code.MoneyIn, Money, Transaction_ID=Transaction_ID)

    def cashout(self, Money):
        TotalMoney = self.getMoney()
        if Money > TotalMoney:
            print("not enough cash")
            return
        else:
            self.updateMoney(self.getMoney() - Money)
            Transaction_ID = generateTransactionID()
            self.Log.insert(Transaction_ID, DB_Code.MoneyOut)
            self.MoneyLog.insertIntoTable(self.Profile, DB_Code.MoneyOut, -Money, Transaction_ID=Transaction_ID)

        # get current money then add money for that user.

    def convertToExcel(self):
        DBFunctions.convertToExcel("User", SetUpFile.DBName, RemoveFirstColumn=False)
