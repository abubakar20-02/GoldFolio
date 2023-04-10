# create UserArchive function that can convert excel file to db.
import sqlite3
import subprocess
import uuid
from datetime import timedelta, datetime
import calendar

import pandas as pd
from fpdf import FPDF

from Database import DB_Code, DBFunctions, SetUpFile

dp = 1


class Log:
    def __init__(self):
        super().__init__()
        self.c = None
        self.conn = None
        self.Profile = None
        self.uid = None
        self.TransactionType = None

        self.UserLog = self.UserLog()
        self.InvestmentLog = self.InvestmentLog()
        self.MoneyLog = self.Money()
        self.createTable()

    def SelectProfile(self, User):
        self.Profile = User
        print(self.Profile)

    def saveState(self, FolderName):
        self.__SetUpConnection()
        sql = "SELECT * FROM Log WHERE User_ID=?"
        param = (self.Profile,)
        # Use pandas to read the data from the SQL database
        df = pd.read_sql(sql, self.conn, params=param)
        self.conn.close()
        df.to_excel(f"{FolderName}/Log.xlsx", index=False)

    def loadState(self, FolderName):
        # Use pandas to read the data from the SQL database
        df = pd.read_excel(f"{FolderName}/Log.xlsx")
        self.__SetUpConnection()
        df.to_sql(name='Log', con=self.conn, if_exists='append', index=False)
        self.conn.close()

    # need refactoring
    def generateTransactionID(self):
        self.uid = str(uuid.uuid4())

    # __ makes the method private
    def __SetUpConnection(self):
        self.conn = sqlite3.connect(SetUpFile.DBLog)
        self.c = self.conn.cursor()

    def deleteUser(self):
        self.MoneyLog.deleteUser(self.Profile)
        self.InvestmentLog.deleteUser(self.Profile)
        self.UserLog.deleteUser(self.Profile)
        self.__SetUpConnection()
        self.c.execute("DELETE FROM Log WHERE User_ID=?", (self.Profile,))
        self.conn.commit()
        self.conn.close()

    def createTable(self):
        self.__SetUpConnection()
        self.c.execute('''
              CREATE TABLE IF NOT EXISTS Log
              ([User_ID] VARCHAR, [TimeStamp] TIMESTAMP DEFAULT CURRENT_TIMESTAMP ,[Transaction_ID] VARCHAR PRIMARY KEY, [TransactionType] VARCHAR)
              ''')
        self.conn.commit()
        self.conn.close()

    def dropTable(self):
        self.__SetUpConnection()
        try:
            self.c.execute("DELETE FROM Log")
            self.c.execute("DELETE FROM InvestmentLog")
            self.c.execute("DELETE FROM UserLog")
            self.c.execute("DELETE FROM Money")
            self.conn.commit()
        except sqlite3.Error as error:
            print(error)
        finally:
            self.conn.close()

    def insert(self, Transaction_ID, TransactionType):
        self.__SetUpConnection()
        self.generateTransactionID()
        self.TransactionType = TransactionType
        self.c.execute('''
              INSERT INTO Log (User_ID,Transaction_ID,TransactionType)
                    VALUES 
                    (?,?,?)
              ''', (self.Profile, Transaction_ID, TransactionType,))
        self.conn.commit()
        self.conn.close()

    # use timestamp here
    def previousStage(self):
        self.__SetUpConnection()
        self.generateTransactionID()
        self.c.execute('''
            SELECT COUNT(*) FROM Log WHERE User_ID = ?
              ''', (self.Profile,))
        Records = self.c.fetchone()[0]
        if Records == 0:
            return
        print(f"Inside profile: {self.Profile}")
        self.c.execute('''
            SELECT * FROM Log WHERE User_ID = ?
              ''', (self.Profile,))
        Data = self.c.fetchone()
        print(f"everything {Data}")
        self.c.execute('''
            SELECT * FROM Log WHERE User_ID = ? ORDER BY TIMESTAMP DESC LIMIT 1
              ''', (self.Profile,))
        Data = self.c.fetchone()
        print(f"actual data: {Data}")
        # print(Data[1])
        self.c.execute('''
            DELETE FROM Log WHERE Transaction_ID = ?
              ''', (Data[2],))
        self.conn.commit()
        self.conn.close()
        self.UserLog.SearchByID(Data[2])
        self.InvestmentLog.SearchByID(Data[2])
        self.MoneyLog.SearchByID(Data[2])

    class UserLog:
        def __init__(self):
            self.c = None
            self.conn = None
            self.__createTable()

        def SetUpConnection(self):
            self.conn = sqlite3.connect(SetUpFile.DBLog)
            self.c = self.conn.cursor()

        def saveState(self, FolderName,Profile):
            self.SetUpConnection()
            sql = "SELECT * FROM UserLog WHERE User_ID=?"
            param = (Profile,)
            # Use pandas to read the data from the SQL database
            df = pd.read_sql(sql, self.conn, params=param)
            self.conn.close()
            df.to_excel(f"{FolderName}/UserLog.xlsx", index=False)

        def loadState(self, FolderName):
            # Use pandas to read the data from the SQL database
            df = pd.read_excel(f"{FolderName}/UserLog.xlsx")
            self.SetUpConnection()
            df.to_sql(name='UserLog', con=self.conn, if_exists='append', index=False)
            self.conn.close()

        def __createTable(self):
            self.SetUpConnection()
            self.c.execute('''
                  CREATE TABLE IF NOT EXISTS UserLog
                  ([TimeStamp] TIMESTAMP DEFAULT CURRENT_TIMESTAMP,[Transaction_ID] VARCHAR PRIMARY KEY, [Transaction_Type] TEXT DEFAULT "" , [NoOfRecordsAffected] INTEGER DEFAULT 0 , [User_ID] VARCHAR DEFAULT ""  ,[FirstName] TEXT DEFAULT "" , [LastName] TEXT DEFAULT "", [Money] REAL DEFAULT 0.0,
                  FOREIGN KEY(Transaction_ID) REFERENCES Log(Transaction_ID))
                  ''')
            self.conn.commit()
            self.conn.close()

        def deleteUser(self, UserID):
            self.SetUpConnection()
            self.c.execute("DELETE FROM UserLog WHERE User_ID=?", (UserID,))
            self.conn.commit()
            self.conn.close()

        def DeleteStatement(self, id, RecordsAffected, User_ID):
            self.SetUpConnection()
            self.c.execute('''
            INSERT INTO UserLog (Transaction_ID,Transaction_Type,NoOfRecordsAffected,User_ID)
                    VALUES 
                    (?,?,?,?)
                  ''', (id, DB_Code.UD, RecordsAffected, User_ID))
            self.conn.commit()
            self.conn.close()

        def InsertStatement(self, id, User_ID, FName, LName, Money):
            self.SetUpConnection()
            self.c.execute('''
            INSERT INTO UserLog (Transaction_ID,Transaction_Type,User_ID,FirstName, LastName, Money)
                    VALUES 
                    (?,?,?,?,?,?)
                  ''', (id, DB_Code.UI, User_ID, FName, LName, Money))
            self.conn.commit()
            self.conn.close()

        def UpdateStatement(self, id, User_ID, Money):
            self.SetUpConnection()
            self.c.execute('''
            INSERT INTO UserLog (Transaction_ID,Transaction_Type,User_ID, Money)
                    VALUES 
                    (?,?,?,?)
                  ''', (id, DB_Code.UU, User_ID, Money))
            self.conn.commit()
            self.conn.close()

        def dropTable(self):
            self.SetUpConnection()
            try:
                self.c.execute("DROP TABLE UserLog")
                self.conn.commit()
            except sqlite3.Error as error:
                print(error)
            finally:
                self.conn.close()

        # move this to user.py
        def SearchByID(self, Transaction_ID):
            self.SetUpConnection()
            self.c.execute("BEGIN TRANSACTION")
            self.c.execute('''
            SELECT * FROM UserLog WHERE Transaction_ID = ?
                  ''', (Transaction_ID,))
            Data = self.c.fetchone()

            self.c.execute('''
            SELECT COUNT(*) FROM UserLog WHERE Transaction_ID = ?
                  ''', (Transaction_ID,))
            Records = self.c.fetchone()[0]
            if Records > 0:
                try:
                    self.c.execute('''
                    DELETE FROM UserLog WHERE Transaction_ID = ?
                          ''', (Transaction_ID,))
                    self.conn.commit()
                except sqlite3.Error as Error:
                    print(Error)
                Transaction_Type = Data[2]
                NoOfRecordsAffected = Data[3]
                User_ID = Data[4]
                FirstName = Data[5]
                LastName = Data[6]
                Money = Data[7]
                print("User")
                from Database import User
                from Database import Archive
                self.user = User.User()
                self.UserArchive = Archive.UserArchive()
                if Transaction_Type == DB_Code.UD:
                    if User_ID is None:
                        print("Recover from User archive using No of records")
                        # none
                        # self.UserArchive.getData()
                        # reverse order
                        # while not NoOfRecordsAffected == 0:
                        #
                        #     # self.InsertStatement()
                        #     NoOfRecordsAffected = NoOfRecordsAffected-1
                    else:
                        from Database.Investment import Investment
                        from Database import Archive

                        RecoverdData = self.UserArchive.getData(User_ID)
                        print("------------------")
                        # print(RecoverdData)
                        print("------------------")
                        # FirstName, LastName,Money, False(Not Log)
                        # use same transaction id
                        if RecoverdData is not None:
                            self.user.insertIntoTable(RecoverdData[3], RecoverdData[4], RecoverdData[5],
                                                      LogChanges=False)
                        print("Recover using user id")
                        # problem here
                        print("Using count recover the most recent data from archive for that user")
                        while NoOfRecordsAffected > 0:
                            print("yo")
                            self.Investment = Investment()
                            self.InvestmentArchive = Archive.InvestmentArchive()
                            self.Investment.setProfile(User_ID)
                            RecoverdData = self.InvestmentArchive.getData(User_ID)
                            if RecoverdData is not None:
                                self.Investment.insertIntoTable(RecoverdData[2], RecoverdData[3], RecoverdData[4],
                                                                LogChanges=False)
                            NoOfRecordsAffected = NoOfRecordsAffected - 1

                elif Transaction_Type == DB_Code.UI:
                    print("Delete using User_ID")
                    self.user.deleteRecord(User_ID, LogChanges=False)

                elif Transaction_Type == DB_Code.UU:
                    print("Update using archive user data")
                    RecoverdData = self.UserArchive.getData(User_ID)
                    print("-------------")
                    # print(RecoverdData)
                    if RecoverdData is not None:
                        print(RecoverdData[2], RecoverdData[5])
                        self.user.updateRecord(RecoverdData[2], RecoverdData[5], LogChanges=False)
                    print("-------------")
                    # self.userArchive.getData()
                else:
                    print("Something else")
                print("")
            self.conn.commit()
            # print(User_ID)
            self.conn.close()

    class InvestmentLog:
        def __init__(self):
            self.c = None
            self.conn = None
            self.__createTable()

        def SetUpConnection(self):
            self.conn = sqlite3.connect(SetUpFile.DBLog)
            self.c = self.conn.cursor()

        def saveState(self, FolderName,Profile):
            self.SetUpConnection()
            sql = "SELECT * FROM InvestmentLog WHERE User_ID=?"
            param = (Profile,)
            # Use pandas to read the data from the SQL database
            df = pd.read_sql(sql, self.conn, params=param)
            self.conn.close()
            df.to_excel(f"{FolderName}/InvestmentLog.xlsx", index=False)

        def loadState(self, FolderName):
            # Use pandas to read the data from the SQL database
            df = pd.read_excel(f"{FolderName}/InvestmentLog.xlsx")
            self.SetUpConnection()
            df.to_sql(name='InvestmentLog', con=self.conn, if_exists='append', index=False)
            self.conn.close()

        def deleteUser(self, UserID):
            self.SetUpConnection()
            self.c.execute("DELETE FROM InvestmentLog WHERE User_ID=?", (UserID,))
            self.conn.commit()
            self.conn.close()

        def __createTable(self):
            self.SetUpConnection()
            self.c.execute('''
                  CREATE TABLE IF NOT EXISTS InvestmentLog
                  ([TimeStamp] TIMESTAMP DEFAULT CURRENT_TIMESTAMP,[Transaction_ID] VARCHAR PRIMARY KEY, [Transaction_Type] TEXT DEFAULT "" , [NoOfRecordsAffected] INTEGER DEFAULT 0 , [Investment_ID] VARCHAR DEFAULT "", [User_ID] VARCHAR DEFAULT "",[Gold] REAL DEFAULT 0.0,[Purity] REAL DEFAULT 0.0, [BoughtFor] REAL DEFAULT 0.0, [ProfitLoss] REAL DEFAULT 0.0,
                  FOREIGN KEY(Transaction_ID) REFERENCES Log(Transaction_ID))
                  ''')
            self.conn.commit()
            self.conn.close()

        # could be refactored
        def SellAllProfitStatement(self, id, RecordsAffected, User_ID):
            self.SetUpConnection()
            self.c.execute('''
            INSERT INTO InvestmentLog (Transaction_ID,Transaction_Type,NoOfRecordsAffected,User_ID)
                    VALUES 
                    (?,?,?,?)
                  ''', (id, DB_Code.ISP, RecordsAffected, User_ID))
            self.conn.commit()
            self.conn.close()

        # could be refactored
        def SellAllStatement(self, id, RecordsAffected, User_ID):
            self.SetUpConnection()
            self.c.execute('''
            INSERT INTO InvestmentLog (Transaction_ID,Transaction_Type,NoOfRecordsAffected,User_ID)
                    VALUES 
                    (?,?,?,?)
                  ''', (id, DB_Code.ISA, RecordsAffected, User_ID))
            self.conn.commit()
            self.conn.close()

        def DeleteStatement(self, id, RecordsAffected, User_ID):
            self.SetUpConnection()
            self.c.execute('''
            INSERT INTO InvestmentLog (Transaction_ID,Transaction_Type,NoOfRecordsAffected,User_ID)
                    VALUES 
                    (?,?,?,?)
                  ''', (id, DB_Code.ID, RecordsAffected, User_ID))
            self.conn.commit()
            self.conn.close()

        def InsertStatement(self, id, User_ID, Gold, Purity, BoughtFor, ProfitLoss):
            self.SetUpConnection()
            self.c.execute('''
            INSERT INTO InvestmentLog (Transaction_ID,Transaction_Type,User_ID,Gold, Purity, BoughtFor, ProfitLoss)
                    VALUES 
                    (?,?,?,?,?,?,?)
                  ''', (id, DB_Code.IB, User_ID, Gold, Purity, BoughtFor, ProfitLoss))
            self.conn.commit()
            self.conn.close()

        # def UpdateStatement(self, id, DB_Code, User_ID, Money):
        #     self.SetUpConnection()
        #     self.c.execute('''
        #     INSERT INTO UserLog (Transaction_ID,Transaction_Type,User_ID, Money)
        #             VALUES
        #             (?,?,?,?)
        #           ''', (id, DB_Code, User_ID, Money))
        #     self.conn.commit()
        #     self.conn.close()
        def dropTable(self):
            self.SetUpConnection()
            try:
                self.c.execute("DROP TABLE InvestmentLog")
                self.conn.commit()
            except sqlite3.Error as error:
                print(error)
            finally:
                self.conn.close()

        def SearchByID(self, Transaction_ID):
            self.SetUpConnection()
            self.c.execute("BEGIN TRANSACTION")
            self.c.execute('''
            SELECT * FROM InvestmentLog WHERE Transaction_ID = ?
                  ''', (Transaction_ID,))
            Data = self.c.fetchone()

            self.c.execute('''
            SELECT COUNT(*) FROM InvestmentLog WHERE Transaction_ID = ?
                  ''', (Transaction_ID,))
            Records = self.c.fetchone()[0]
            if Records > 0:
                try:
                    self.c.execute('''
                    DELETE FROM InvestmentLog WHERE Transaction_ID = ?
                          ''', (Transaction_ID,))
                    self.conn.commit()
                except sqlite3.Error as Error:
                    print(Error)
                Transaction_Type = Data[2]
                NoOfRecordsAffected = Data[3]
                Investment_ID = Data[4]
                User_ID = Data[5]
                Gold = Data[6]
                Purity = Data[7]
                BoughtFor = Data[8]
                ProfitLoss = Data[9]

                from Database.Investment import Investment
                from Database import Archive
                from Database import Statement
                self.Investment = Investment()
                self.InvestmentArchive = Archive.InvestmentArchive()
                self.Statement = Statement.Statement()

                print("Investment")
                print(Transaction_Type)
                if Transaction_Type == DB_Code.IB:
                    print("Use Investment ID to delete")
                    # RecoverdData = self.InvestmentArchive.getData(User_ID)
                    # print(RecoverdData)
                    # if RecoverdData is not None:
                    self.Investment.deleteRecord(User_ID, TransactionID=Data[1], LogChanges=False, Archive=False)
                elif Transaction_Type == DB_Code.IU:
                    print("Use archive data to update using Investment ID")
                elif Transaction_Type == DB_Code.ISP:
                    print("Use User_ID to find most recent deleted investment using count")
                    self.Investment.setProfile(User_ID)
                    # loop count till all values inserted
                    while NoOfRecordsAffected > 0:
                        RecoverdData = self.InvestmentArchive.getData(User_ID)
                        print("Date:" + str(RecoverdData[1]))
                        self.Investment.insertIntoTable(RecoverdData[3], RecoverdData[4], RecoverdData[5],
                                                        LogChanges=False, Transaction_ID=RecoverdData[0],
                                                        Date=RecoverdData[1], ProfitLoss=RecoverdData[6],
                                                        IgnoreMoney=True)
                        # code to remove record from statement.
                        self.Statement.getData(User_ID)
                        NoOfRecordsAffected = NoOfRecordsAffected - 1
                    # adding archived data to User investment
                elif Transaction_Type == DB_Code.ID:
                    # problem here
                    print("Using count recover the most recent data from archive for that user")
                    while NoOfRecordsAffected > 0:
                        print("yo")
                        self.Investment.setProfile(User_ID)
                        RecoverdData = self.InvestmentArchive.getData(User_ID)
                        if RecoverdData is not None:
                            self.Investment.insertIntoTable(RecoverdData[3], RecoverdData[4], RecoverdData[5],
                                                            LogChanges=False, Transaction_ID=RecoverdData[0],
                                                            Date=RecoverdData[1], ProfitLoss=RecoverdData[6],
                                                            IgnoreMoney=True)
                            # code to remove record from statement.
                        self.Statement.getData(User_ID)
                        NoOfRecordsAffected = NoOfRecordsAffected - 1
                elif Transaction_Type == DB_Code.ISA:
                    print("Use User_ID to find most recent statement using count")
                    self.Investment.setProfile(User_ID)
                    # loop count till all values inserted
                    while NoOfRecordsAffected > 0:
                        RecoverdData = self.InvestmentArchive.getData(User_ID)
                        self.Investment.insertIntoTable(RecoverdData[3], RecoverdData[4], RecoverdData[5],
                                                        LogChanges=False, Transaction_ID=RecoverdData[0],
                                                        Date=RecoverdData[1], ProfitLoss=RecoverdData[6],
                                                        IgnoreMoney=True)
                        # code to remove record from statement.
                        self.Statement.getData(User_ID)
                        NoOfRecordsAffected = NoOfRecordsAffected - 1
                else:
                    print("nothing")
                print("")
            self.conn.commit()
            self.conn.close()

    class Money:

        def __init__(self):
            self.c = None
            self.conn = None
            self.Profile = None
            self.createTable()

        def setProfile(self, Profile):
            self.Profile = Profile
            print(f"profile set to: {Profile}")

        def saveState(self, FolderName,Profile):
            self.__SetUpConnection()
            sql = "SELECT * FROM Money WHERE User_ID=?"
            param = (Profile,)
            # Use pandas to read the data from the SQL database
            df = pd.read_sql(sql, self.conn, params=param)
            self.conn.close()
            df.to_excel(f"{FolderName}/MoneyLog.xlsx", index=False)

        def loadState(self, FolderName):
            # Use pandas to read the data from the SQL database
            df = pd.read_excel(f"{FolderName}/MoneyLog.xlsx")
            self.__SetUpConnection()
            df.to_sql(name='Money', con=self.conn, if_exists='append', index=False)
            self.conn.close()

        def __SetUpConnection(self):
            self.conn = sqlite3.connect(SetUpFile.DBLog)
            self.c = self.conn.cursor()

        def deleteUser(self, UserID):
            self.__SetUpConnection()
            self.c.execute("DELETE FROM Money WHERE User_ID=?", (UserID,))
            self.conn.commit()
            self.conn.close()

        def createTable(self):
            self.__SetUpConnection()
            self.c.execute('''
                  CREATE TABLE IF NOT EXISTS Money
                  ([Transaction_ID]VARCHAR PRIMARY KEY,[Date_Added] DEFAULT CURRENT_DATE,[User_ID] VARCHAR, [ActionType]  TEXT NOT NULL , [Change] REAL NOT NULL,[TradeCost] REAL)
                  ''')
            self.conn.commit()
            self.conn.close()

        def deleteTable(self):
            self.__SetUpConnection()
            try:
                self.c.execute("DELETE FROM Money")
                self.conn.commit()
            except sqlite3.Error as error:
                print(error)
            finally:
                self.conn.close()

        def insertIntoTable(self, User_ID, ActionType, Change, Transaction_ID=None, TradeCost=None):
            self.__SetUpConnection()
            if TradeCost is None:
                TradeCost = 0
            if Transaction_ID is None:
                Transaction_ID = str(uuid.uuid4())
            self.c.execute('''
                  INSERT INTO Money (Transaction_ID,User_ID,ActionType,Change,TradeCost)
                        VALUES 
                        (?,?,?,?,?)
                  ''', (Transaction_ID, User_ID, ActionType, round(Change, dp), round(TradeCost, dp)))
            self.conn.commit()
            self.conn.close()

        def deletefromTable(self, Transaction_ID):
            self.__SetUpConnection()
            self.c.execute('''
                  DELETE FROM Money WHERE Transaction_ID = ?
                  ''', (Transaction_ID,))
            self.conn.commit()
            self.conn.close()

        # move this to user.py
        def SearchByID(self, Transaction_ID):
            self.__SetUpConnection()
            self.c.execute("BEGIN TRANSACTION")
            self.c.execute('''
            SELECT * FROM Money WHERE Transaction_ID = ?
                  ''', (Transaction_ID,))
            Data = self.c.fetchone()

            self.c.execute('''
            SELECT COUNT(*) FROM Money WHERE Transaction_ID = ?
                  ''', (Transaction_ID,))
            Records = self.c.fetchone()[0]
            if Records == 0:
                self.conn.close()
                return
            try:
                self.c.execute('''
                DELETE FROM Money WHERE Transaction_ID = ?
                      ''', (Transaction_ID,))
                self.conn.commit()
            except sqlite3.Error as Error:
                print(Error)
            ActionType = Data[3]
            print(ActionType)
            from Database import User
            from Database.Investment import Investment
            User = User.User()
            Investment = Investment()
            User.SelectProfile(Data[2])
            if ActionType == DB_Code.MoneyIn:
                User.addMoney(-Data[4], LogChanges=False)
            if ActionType == DB_Code.MoneyOut:
                User.addMoney(-Data[4], LogChanges=False)
            elif ActionType == DB_Code.ProfitLoss:
                # using investment get bought price too.
                User.addMoney((-Data[4] - Data[5]), LogChanges=False)
            elif ActionType == DB_Code.BuyInvestment:
                User.addMoney(-Data[4], LogChanges=False)
            self.conn.close()

        def __getSum(self, ActionType, ColumnName, StartDate=None, EndDate=None):
            # add date as parameter too.
            self.__SetUpConnection()
            sql = "SELECT SUM({0}) FROM Money WHERE ActionType = ? AND User_ID = ?".format(ColumnName)
            if StartDate:
                # idk why I have to do this.
                StartDate = StartDate - timedelta(days=1)
                sql += f" AND Date_Added >= '{StartDate}'"

            if EndDate:
                sql += f" AND Date_Added <= '{EndDate}'"
            self.c.execute(sql, (ActionType, self.Profile))
            Sum = self.c.fetchone()[0]
            self.conn.close()
            print(Sum)
            return Sum

        def dataforgraph(self, StartDate=None, EndDate=None):
            b = 0
            a = self.__getSum(DB_Code.MoneyIn, "Change", StartDate=StartDate, EndDate=EndDate)
            if self.__getSum(DB_Code.MoneyOut, "Change", StartDate=StartDate, EndDate=EndDate) is not None:
                b = (0 - self.__getSum(DB_Code.MoneyOut, "Change", StartDate=StartDate, EndDate=EndDate))
            c = self.__getSum(DB_Code.ProfitLoss, "Change", StartDate=StartDate, EndDate=EndDate)
            d = self.__getSum(DB_Code.ProfitLoss, "TradeCost", StartDate=StartDate, EndDate=EndDate)

            if a is None:
                a = 0
            if c is None:
                c = 0
            if d is None:
                d = 0

            dict1 = dict([(DB_Code.MoneyIn, a), (DB_Code.MoneyOut, b), (DB_Code.ProfitLoss, c), ("TradeCost", d)])
            print(dict1)
            return dict1

        def getTable(self, StartDate=None, EndDate=None):
            self.__SetUpConnection()
            try:
                sql = "SELECT * FROM Money WHERE User_ID = ?"
                if StartDate is not None:
                    sql += f" AND Date_Added >= '{StartDate.strftime('%Y-%m-%d')}'"
                if EndDate is not None:
                    sql += f" AND Date_Added <= '{EndDate.strftime('%Y-%m-%d')}'"
                values = (self.Profile,)
                df = pd.read_sql(sql, self.conn, params=values)
                df = df.drop('User_ID', axis=1)
                df = df.drop('Transaction_ID', axis=1)
            except sqlite3.Error as error:
                print(error)
            finally:
                self.conn.close()
                return df

        def getMinMaxDates(self):
            self.__SetUpConnection()
            self.c.execute("SELECT MIN(Date_Added),Max(Date_Added) FROM Money")
            results = self.c.fetchone()
            self.conn.close()
            return results

        def Overall(self, Column, StartDate=None, EndDate=None):
            if StartDate is None and EndDate is None:
                StartDate, EndDate = self.getMinMaxDates()
                StartDate = datetime.strptime(StartDate, '%Y-%m-%d').date()
                EndDate = datetime.strptime(EndDate, '%Y-%m-%d').date()

            self.__SetUpConnection()
            delta = abs(EndDate - StartDate)
            if delta >= timedelta(days=366):
                return self.Yearly(Column, Start=StartDate, End=EndDate)
                # generate yearly
                print("years")
            elif delta <= timedelta(days=31):
                return self.Daily(Column, Start=StartDate, End=EndDate)
                # generate single
                print("single")
            else:
                return self.Monthly(Column, Start=StartDate, End=EndDate)
                # generate monthly
                print("months")
            self.conn.close()

        def generate_monthly_dict(self, start_date, end_date):
            result = {}
            current_date = start_date.replace(day=1)
            while current_date <= end_date:
                result[current_date.strftime('%Y-%m')] = 0
                current_date += timedelta(days=32)
                current_date = current_date.replace(day=1)
            print(result)
            return result

        def generate_yearly_dict(self, start_date, end_date):
            result = {}
            for year in range(start_date.year, end_date.year + 1):
                result[year] = 0
            print(result)
            return result

        def generate_daily_dict(self, start_date, end_date):
            result = {}
            date = start_date
            while date <= end_date:
                result[date] = 0
                date += timedelta(days=1)
            return result

        def Yearly(self, ColumnName, Start=None, End=None):
            self.__SetUpConnection()
            sql = (
                "SELECT strftime('%Y', Date_Added) AS year, SUM({0} + TradeCost) AS total_value FROM Money WHERE User_ID=?").format(
                ColumnName)
            if Start:
                # idk why I have to do this.
                sql += f" AND Date_Added >= '{Start.strftime('%Y-%m-%d')}'"

            if End:
                sql += f" AND Date_Added <= '{End.strftime('%Y-%m-%d')}'"

            sql += f"GROUP BY year"

            if Start and End:
                yearlydict = self.generate_yearly_dict(Start, End)

            print(sql)

            self.c.execute(sql, (self.Profile,))

            total = 0
            for rows in self.c.fetchall():
                year, sum = rows
                total = total + sum
                print(type(year))
                yearlydict[datetime.strptime(year, '%Y').year] = total

            print("----")
            print(yearlydict)
            print("----")

            self.conn.close()
            return yearlydict

        def Monthly(self, ColumnName, Start=None, End=None):
            self.__SetUpConnection()
            # might need to include trade cost too
            sql = (
                "SELECT strftime('%Y-%m', Date_Added) AS month, SUM({0} + TradeCost) AS total_value FROM Money WHERE User_ID=?").format(
                ColumnName)
            if Start:
                # idk why I have to do this.
                sql += f" AND Date_Added >= '{Start.strftime('%Y-%m-%d')}'"

            if End:
                sql += f" AND Date_Added <= '{End.strftime('%Y-%m-%d')}'"

            sql += f"GROUP BY month"

            print(sql)

            if Start and End:
                monthlydict = self.generate_monthly_dict(Start, End)

            print(sql)

            self.c.execute(sql, (self.Profile,))
            total = 0
            for rows in self.c.fetchall():
                print("hmm")
                print(rows)
                month, sum = rows
                total = total + sum
                monthlydict[month] = total

            print("----")
            print(monthlydict)
            print("----")

            self.conn.close()
            return monthlydict

        def Daily(self, ColumnName, Start=None, End=None):
            sql = "SELECT SUM({0} + TradeCost) FROM Money WHERE Date_Added = ? AND User_ID=?".format(ColumnName)

            sql1 = "SELECT DISTINCT Date_Added FROM Money WHERE User_ID = ?"

            if Start:
                # idk why I have to do this.
                StartDate = Start - timedelta(days=1)
                sql1 += f" AND Date_Added >= '{StartDate}'"

            if End:
                sql1 += f" AND Date_Added <= '{End}'"

            sql1 += f" ORDER BY Date_Added ASC"

            # execute SQL query to get all dates
            # self.c.execute(sql1, (self.Profile,))

            dictionary = self.generate_daily_dict(Start, End)
            dates = []
            date = Start
            while date <= End:
                dates.append(date)
                date += timedelta(days=1)

            # loop through dates and print the sum of values for each date
            sum = 0
            for date in dates:
                # format_str = '%Y-%m-%d'
                # date = datetime.strptime(date, format_str)
                self.c.execute(sql, (date, self.Profile))
                sum_of_values = self.c.fetchone()[0]
                if sum_of_values is None:
                    sum_of_values = 0
                sum += sum_of_values
                dictionary[date] = sum
                # if Mode is None:
                # dictionary[date] = sum_of_values
                # else:
                #     dictionary[date] = sum

            # close database connection
            self.conn.close()
            print("----")
            print(dictionary)
            print("----")
            return dictionary

        def getMoneyAdded(self, StartDate=None, EndDate=None):
            self.__SetUpConnection()
            sql = "SELECT SUM(Change) From Money WHERE User_ID = ? AND ActionType = ?"
            if StartDate:
                # idk why I have to do this.
                sql += f" AND Date_Added >= '{StartDate}'"

            if EndDate:
                sql += f" AND Date_Added <= '{EndDate}'"
            print(sql)
            print(f"profile {self.Profile} , code {DB_Code.MoneyIn}")
            self.c.execute(sql,
                           (self.Profile, DB_Code.MoneyIn))
            value = self.c.fetchone()[0]
            if value is None:
                value = 0
            value = value
            self.conn.close()
            return value

        # def getMoneyAdded(self, StartDate=None, EndDate=None):
        #     self.__SetUpConnection()
        #     sql = "SELECT SUM(Change) From Money WHERE User_ID=? AND ActionType = ?"
        #     if StartDate:
        #         # idk why I have to do this.
        #         sql += f" AND Date_Added >= '{StartDate}'"
        #
        #     if EndDate:
        #         sql += f" AND Date_Added <= '{EndDate}'"
        #     self.c.execute(sql,
        #                    (self.Profile,DB_Code.MoneyIn))
        #     value = self.c.fetchone()[0]
        #     self.conn.close()
        #     return value

        def getMoneyOut(self, StartDate=None, EndDate=None):
            self.__SetUpConnection()
            sql = "SELECT SUM(Change) From Money WHERE User_ID=? AND ActionType=?"
            if StartDate:
                # idk why I have to do this.
                sql += f" AND Date_Added >= '{StartDate}'"

            if EndDate:
                sql += f" AND Date_Added <= '{EndDate}'"
            self.c.execute(sql,
                           (self.Profile, DB_Code.MoneyOut))
            value = self.c.fetchone()[0]
            if value is None:
                value = 0
            value = - value
            self.conn.close()
            return value

        def formatToWeek(self, number):
            ranges = []
            start = 1
            end = 7
            while end < number:
                ranges.append((start, end))
                start += 7
                end += 7
            ranges.append((start, number))
            return ranges

        def getDatesInWeekFormatForMonth(self, year, month):
            Add = {}
            Withdrawn = {}
            days_in_month = calendar.monthrange(year, month)[1]
            print(self.formatToWeek(days_in_month))
            for start, end in self.formatToWeek(days_in_month):
                start_date = datetime(year, month, start).date()
                end_date = datetime(year, month, end).date()
                Add[f"{start}-{end}"] = self.getMoneyAdded(StartDate=start_date, EndDate=end_date)
                Withdrawn[f"{start}-{end}"] = self.getMoneyOut(StartDate=start_date, EndDate=end_date)

            return Add, Withdrawn

        def getDatesInMonthFormatForMonth(self, year):
            Add = {}
            Withdrawn = {}
            for month in range(12):
                days_in_month = calendar.monthrange(year, month + 1)[1]
                start_date = datetime(year, month + 1, 1).date()
                end_date = datetime(year, month + 1, days_in_month).date()
                month_name = start_date.strftime("%b")
                Add[f"{month_name}"] = self.getMoneyAdded(StartDate=start_date, EndDate=end_date)
                Withdrawn[f"{month_name}"] = self.getMoneyOut(StartDate=start_date, EndDate=end_date)

            return Add, Withdrawn

        def getInvestmentMade(self, StartDate=None, EndDate=None):
            sql = "SELECT COUNT(User_ID) FROM Money WHERE User_ID=? AND ActionType=?"
            if StartDate:
                # idk why I have to do this.
                sql += f" AND Date_Added >= '{StartDate}'"

            if EndDate:
                sql += f" AND Date_Added <= '{EndDate}'"
            self.__SetUpConnection()
            self.c.execute(sql, (self.Profile, DB_Code.IB))
            count = self.c.fetchone()[0]
            self.conn.close()
            return count

        def getInvestmentSold(self, StartDate=None, EndDate=None):
            sql = "SELECT COUNT(User_ID) FROM Money WHERE User_ID=? AND ActionType=?"
            if StartDate:
                # idk why I have to do this.
                sql += f" AND Date_Added >= '{StartDate}'"

            if EndDate:
                sql += f" AND Date_Added <= '{EndDate}'"
            self.__SetUpConnection()
            self.c.execute(sql, (self.Profile, DB_Code.ProfitLoss))
            count = self.c.fetchone()[0]
            self.conn.close()
            return count

            # for i, r in enumerate(self.getMonthRange(days_in_month)):
            #     print(f"Range {i + 1}: {r[0]}-{r[1]}")
            # self.__SetUpConnection()
            # sql = "SELECT SUM(Change) From Money WHERE User_ID=? AND ActionType=?"
            # self.c.execute(sql,
            #                (self.Profile, DB_Code.MoneyOut))
            # value = self.c.fetchone()[0]
            # if value is None:
            #     value = 0
            # self.conn.close()
            # return value

        def convertToExcel(self, StartDate=None, EndDate=None, FilePath='output_file.xlsx'):
            self.__SetUpConnection()
            # Define the parameters for the query
            params = (self.Profile,)

            # Query the database and create a DataFrame
            sql = 'SELECT Date_Added,ActionType,Change,TradeCost FROM Money WHERE User_ID= ?'
            if StartDate is not None:
                sql += f" AND Date_Added >= '{StartDate.strftime('%Y-%m-%d')}'"
            if EndDate is not None:
                sql += f" AND Date_Added <= '{EndDate.strftime('%Y-%m-%d')}'"
            df = pd.read_sql(sql, con=self.conn, params=params)

            df.to_excel(FilePath, index=False)
            self.conn.close()
            subprocess.Popen(['start', 'excel.exe', FilePath], shell=True)

        def PDF(self, FilePath, StartDate=None, EndDate=None):
            self.__SetUpConnection()
            # Define the parameters for the query
            params = (self.Profile,)

            # Query the database and create a DataFrame
            sql = 'SELECT Date_Added,ActionType,Change,TradeCost FROM Money WHERE User_ID= ?'
            if StartDate is not None:
                sql += f" AND Date_Added >= '{StartDate.strftime('%Y-%m-%d')}'"
            if EndDate is not None:
                sql += f" AND Date_Added <= '{EndDate.strftime('%Y-%m-%d')}'"
            df = pd.read_sql(sql, con=self.conn, params=params)

            # Create a PDF document using the fpdf library
            pdf = MyPDF()
            pdf.add_page()
            pdf.alias_nb_pages()

            # Set the font and size of the text in the PDF document
            pdf.set_font("Arial", size=12)

            # Calculate the maximum width of the data in each column
            column_width = pdf.w / len(df.columns)

            # Create a list of equal column widths that fill the width of the page
            column_widths = [column_width] * len(df.columns)

            # Set the left margin to 0 to stretch the table to take the entire width of the page
            left_margin = 0

            # Add the DataFrame to the PDF document as a table
            pdf.set_x(left_margin)
            for i, column in enumerate(df.columns):
                pdf.cell(column_widths[i], 10, str(column), border=1)
            for index, row in df.iterrows():
                pdf.ln()
                pdf.set_x(left_margin)
                for i, column in enumerate(df.columns):
                    pdf.cell(column_widths[i], 10, str(row[column]), border=1)

            # Save the PDF document to a file
            pdf.output(FilePath)
            self.conn.close()


class MyPDF(FPDF):
    def footer(self):
        # Add a footer to the bottom center of each page
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
