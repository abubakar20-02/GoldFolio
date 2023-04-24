import ast
import math
import sqlite3
import uuid
import bcrypt

import pandas as pd

from Database import DB_Code, DBFunctions, SetUpFile, Archive, Investment, Log, Statement


def generateTransactionID():
    """ Return a new transactionID. """
    return str(uuid.uuid4())


def hash_password(password):
    """ Return hashed password. """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password


class User:
    def __init__(self):
        self.c = None
        self.conn = None
        self.Profile = None
        self.a = Archive.UserArchive()
        self.b = Archive.InvestmentArchive()
        self.Log = Log.Log()
        self.UserLog = Log.Log.UserLog()
        self.Investment = Investment.Investment()
        self.Statement = Statement.Statement()
        self.MoneyLog = Log.Log.Money()

    def __SetUpConnection(self):
        self.conn = sqlite3.connect(SetUpFile.DBName)
        self.c = self.conn.cursor()

    def SelectProfile(self, Profile):
        """ Select user profile. """
        self.Profile = Profile
        self.Log.SelectProfile(self.Profile)
        self.Investment.setProfile(self.Profile)
        self.Statement.setProfile(self.Profile)

    def deleteArchiveLog(self):
        """ Remove all support database files. """
        self.Log.deleteUser()
        self.a.deleteUser(self.Profile)
        self.b.deleteUser(self.Profile)

    def deleteUser(self):
        """ Delete everything belonging to the user in every table. """
        self.Statement.deleteUser()
        self.Investment.deleteUser()
        self.__SetUpConnection()
        self.c.execute("DELETE FROM User WHERE User_ID=?", (self.Profile,))
        self.conn.commit()
        self.conn.close()
        self.deleteArchiveLog()

    def searchLikeUserID(self, UserID):
        """ Returns similar user ID """
        self.__SetUpConnection()
        sql = "SELECT User_ID,FirstName,LastName,Currency FROM User WHERE User_ID LIKE '%{}%'".format(UserID)
        df = pd.read_sql(sql, self.conn)
        self.conn.close()
        return df

    def ImportFromExcel(self):
        """ Import users from excel. """
        target = 'User.xlsx'
        sheet_name = 'Sheet1'
        path = target
        df = pd.read_excel(path, sheet_name=sheet_name)
        table_name = "User"
        columns = ','.join(df.columns)
        placeholders = ','.join(['?' for _ in range(len(df.columns))])
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        # load data from file.
        for _, row in df.iterrows():
            values = tuple(row)
            try:
                float(values[3])
                if not (values[1].isalpha() and values[2].isalpha()):
                    # name contain invalid letters.
                    continue
                if str(values[0])[:2] == self.generate_unique_initials(values[1], values[2])[:2]:
                    # close function after we finish using generate unique initials.
                    self.conn.close()
                    self.insertIntoTable(values[1], values[2], values[3], UserID=values[0], LogChanges=False)
                if isinstance(values[0], (int, float)) and math.isnan(values[0]):
                    self.insertIntoTable(values[1], values[2], values[3], LogChanges=False)
            except:
                None
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
        """ Create user table """
        self.__SetUpConnection()
        self.c.execute('''
              CREATE TABLE IF NOT EXISTS User
              ([User_ID] VARCHAR PRIMARY KEY, [FirstName]  TEXT NOT NULL , [LastName] TEXT NOT NULL, [Money] REAL NOT NULL, [Password] BINARY(60) NOT NULL,[Currency] VARCHAR NOT NULL ,[MinimumProfitMargin] REAL NOT NULL DEFAULT 0,[DecimalPoint] INTEGER NOT NULL DEFAULT 2, [UpdateFrequency] INTEGER NOT NULL DEFAULT 30,[GoldUnit] VARCHAR NOT NULL DEFAULT "g")
              ''')
        self.conn.commit()
        self.conn.close()

    def deleteTable(self):
        """Delete everything from the user table."""
        self.__SetUpConnection()
        try:
            self.c.execute("DELETE FROM User")
            self.conn.commit()
        except sqlite3.Error as error:
            print(error)
        finally:
            self.conn.close()

    def deleteRecord(self, User_ID, LogChanges=True):
        """Takes user id to delete record and if log change is not False, then the code saves InvestmentArchive log."""
        Transaction_ID = generateTransactionID()
        self.__SetUpConnection()
        try:
            self.c.execute("SELECT * FROM User WHERE User_ID = ?", (User_ID,))
            Values = self.c.fetchall()
            self.c.execute("SELECT COUNT(*) FROM Investment WHERE User_ID = ?", (User_ID,))
            RecordsAffected = self.c.fetchone()[0]
            a = RecordsAffected
            while a > 0:
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
        self.UserLog.DeleteStatement(Transaction_ID, RecordsAffected, User_ID)
        self.a.Archive(DB_Code.DELETECOMMAND, Values)

    def __LogForInsert(self, FName, LName, Money, User_ID, Transaction_ID):
        self.UserLog.InsertStatement(Transaction_ID, User_ID, FName, LName, Money)
        self.Log.insert(Transaction_ID, DB_Code.UI)

    # def __LogForUpdate(self, Money, User_ID, Values, TransactionID):
    #     self.Log.insert(TransactionID, DB_Code.UU)
    #     self.UserLog.UpdateStatement(TransactionID, User_ID, Money)
    #     # mention this was updated
    #     self.a.Archive(DB_Code.UPDATECOMMAND, Values)

    def insertIntoTable(self, FName, LName, Money, Password, Currency, LogChanges=True, UserID=None):
        """Takes record data to insert and if log change is not false, then the code saves InvestmentArchive log."""
        self.__SetUpConnection()
        if UserID is None:
            UserID = self.generate_unique_initials(FName, LName)
        self.c.execute('''
          INSERT INTO User (User_ID, FirstName,LastName,Money,Password,Currency)

                VALUES
                (?,?,?,?,?,?)
          ''', (UserID, FName, LName, Money, hash_password(Password), Currency))
        self.conn.commit()
        if LogChanges is True:
            self.Log.SelectProfile(UserID)
            Transaction_ID = generateTransactionID()
            self.__LogForInsert(FName, LName, Money, UserID, Transaction_ID)
            self.MoneyLog.insertIntoTable(UserID, DB_Code.MoneyIn, Money, Transaction_ID=Transaction_ID)
        self.conn.close()

    def updateRecord(self, User_ID, Money, LogChanges=True):
        """Takes user id to locate the user, take money to change and if log change is not false, then the code saves
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

    # def showTable(self):
    #     self.__SetUpConnection()
    #     try:
    #         self.c.execute('''
    #                   SELECT * FROM User
    #                   ''')
    #         self.conn.commit()
    #         df = pd.DataFrame(self.c.fetchall(), columns=['User_ID', 'FirstName', 'LastName', 'Money'])
    #         print(df)
    #     except sqlite3.Error as error:
    #         print(error)
    #     finally:
    #         self.conn.close()
    # self.convertToExcel()

    def isUserExist(self, User_ID):
        """Takes user id to check if user exists in the database, and if they do then return True. """
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
        """ Returns the money of the user."""
        self.__SetUpConnection()
        self.c.execute('''
                  SELECT Money FROM User WHERE User_ID = ?
                  ''', (self.Profile,))
        result = self.c.fetchone()
        if result is not None:
            Money = result[0]
        else:
            Money = 0
        self.conn.close()
        return round(Money, 1)

    def getName(self):
        """ Returns the full name of the user."""
        self.__SetUpConnection()
        self.c.execute('''
        SELECT FirstName,LastName FROM User WHERE User_ID=?
        ''', (self.Profile,))
        FirstName, LastName = self.c.fetchone()
        if FirstName is not None and LastName is not None:
            Name = FirstName + " " + LastName + " (" + self.Profile + ")"
        else:
            Name = "-"
        self.conn.close()
        return Name

    def updateMoney(self, Money):
        """ Update the money for the user."""
        self.__SetUpConnection()
        self.c.execute('''
                  UPDATE User SET Money=? WHERE User_ID = ?
                  ''', (Money, self.Profile))
        self.conn.commit()
        self.conn.close()

    def addMoney(self, Money, LogChanges=True):
        """ Takes money to add to the users total money and if the log change is not false, then the code saves
        to the money log."""
        TotalMoney = self.getMoney() + Money
        self.updateMoney(TotalMoney)
        if LogChanges:
            Transaction_ID = generateTransactionID()
            self.Log.insert(Transaction_ID, DB_Code.MoneyIn)
            self.MoneyLog.insertIntoTable(self.Profile, DB_Code.MoneyIn, Money, Transaction_ID=Transaction_ID)

    def cashout(self, Money, LogChanges=True):
        """ Takes money to remove from the users total money and if the log change is not false, then the code saves
        to the money log."""
        self.updateMoney(self.getMoney() - Money)
        if LogChanges:
            Transaction_ID = generateTransactionID()
            self.Log.insert(Transaction_ID, DB_Code.MoneyOut)
            self.MoneyLog.insertIntoTable(self.Profile, DB_Code.MoneyOut, -Money, Transaction_ID=Transaction_ID)

    def getDataForGraph(self):
        """ Returns format for graph input."""
        a = ("RawCash", self.getMoney())
        self.Investment.setProfile(self.Profile)
        b = ("GoldMoney", self.Investment.getSUM("BoughtFor"))
        dict1 = dict([a, b])
        return dict1

    def convertToExcel(self):
        """ convert database to excel file. """
        DBFunctions.convertToExcel("User", SetUpFile.DBName, RemoveFirstColumn=False)

    def getHashedPassword(self, UserID):
        """ Returns hashed password for the given user. """
        self.__SetUpConnection()
        self.c.execute("SELECT Password FROM USER WHERE User_ID=?", (UserID,))
        hashpass = self.c.fetchone()[0]
        self.conn.close()
        if not isinstance(hashpass, bytes):
            hashpass = ast.literal_eval(hashpass)
        return hashpass

    def UpdatePassword(self, User_ID, Password):
        """ Update password for given user. """
        self.__SetUpConnection()
        self.c.execute('''
        UPDATE User SET Password = ? WHERE User_ID = ?'''
                       , (hash_password(Password), User_ID))
        self.conn.commit()
        self.conn.close()

    def ChangeSettings(self, MinimumProfitMargin, DecimalPoint, UpdateFrequency, GoldUnit):
        """ Change setting for the user. """
        self.__SetUpConnection()
        self.c.execute('''
        UPDATE User SET MinimumProfitMargin = ?, DecimalPoint=?,UpdateFrequency=?, GoldUnit=?  WHERE User_ID = ?'''
                       , (MinimumProfitMargin, DecimalPoint, UpdateFrequency, GoldUnit, self.Profile))
        self.conn.commit()
        self.conn.close()

    def GetSettings(self):
        """ Return settings of the user. """
        self.__SetUpConnection()
        self.c.execute('''
        SELECT MinimumProfitMargin, DecimalPoint,UpdateFrequency,GoldUnit,Currency FROM User  WHERE User_ID = ?''',
                       (self.Profile,))
        values = self.c.fetchone()
        self.conn.close()
        return values

    def getTable(self):
        self.__SetUpConnection()
        try:
            sql = "SELECT User_ID,FirstName,LastName,Currency FROM User"
            df = pd.read_sql(sql, self.conn)
        except sqlite3.Error as error:
            print(error)
        finally:
            self.conn.close()
            # print(df)
            return df

    def saveState(self, FolderName):
        """ Save state for the given user """
        self.__SetUpConnection()
        sql = "SELECT * FROM User WHERE User_ID=?"
        param = (self.Profile,)
        df = pd.read_sql(sql, self.conn, params=param)
        self.conn.close()
        df.to_excel(f"{FolderName}/User.xlsx", index=False)

    def loadState(self, FolderName):
        """ Load state for the given user """
        df = pd.read_excel(f"{FolderName}/User.xlsx")
        self.__SetUpConnection()
        df.to_sql(name='User', con=self.conn, if_exists='append', index=False)
        self.conn.close()
