# create UserArchive function that can convert excel file to db.
import sqlite3
import uuid
from datetime import timedelta

import pandas as pd

from Database import DB_Code, DBFunctions, SetUpFile


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

    # need refactoring
    def generateTransactionID(self):
        self.uid = str(uuid.uuid4())

    # __ makes the method private
    def __SetUpConnection(self):
        self.conn = sqlite3.connect(SetUpFile.DBLog)
        self.c = self.conn.cursor()

    def createTable(self):
        self.__SetUpConnection()
        self.c.execute('''
              CREATE TABLE IF NOT EXISTS Log
              ([TimeStamp] TIMESTAMP DEFAULT CURRENT_TIMESTAMP ,[Transaction_ID] VARCHAR PRIMARY KEY, [TransactionType] VARCHAR)
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
              INSERT INTO Log (Transaction_ID,TransactionType)
                    VALUES 
                    (?,?)
              ''', (Transaction_ID, TransactionType,))
        self.conn.commit()
        self.conn.close()

    # use timestamp here
    def previousStage(self):
        self.__SetUpConnection()
        self.generateTransactionID()
        self.c.execute('''
            SELECT COUNT(*) FROM Log 
              ''')
        Records = self.c.fetchone()[0]
        if Records == 0:
            return
        self.c.execute('''
            SELECT * FROM Log LIMIT 1 OFFSET ?
              ''', (Records - 1,))
        Data = self.c.fetchone()
        # print(Data[1])
        self.c.execute('''
            DELETE FROM Log WHERE Transaction_ID = ?
              ''', (Data[1],))
        self.conn.commit()
        self.conn.close()
        self.UserLog.SearchByID(Data[1])
        self.InvestmentLog.SearchByID(Data[1])
        self.MoneyLog.SearchByID(Data[1])

    class UserLog:
        def __init__(self):
            self.c = None
            self.conn = None
            self.__createTable()

        def SetUpConnection(self):
            self.conn = sqlite3.connect(SetUpFile.DBLog)
            self.c = self.conn.cursor()

        def __createTable(self):
            self.SetUpConnection()
            self.c.execute('''
                  CREATE TABLE IF NOT EXISTS UserLog
                  ([TimeStamp] TIMESTAMP DEFAULT CURRENT_TIMESTAMP,[Transaction_ID] VARCHAR PRIMARY KEY, [Transaction_Type] TEXT DEFAULT "" , [NoOfRecordsAffected] INTEGER DEFAULT 0 , [User_ID] VARCHAR DEFAULT ""  ,[FirstName] TEXT DEFAULT "" , [LastName] TEXT DEFAULT "", [Money] REAL DEFAULT 0.0,
                  FOREIGN KEY(Transaction_ID) REFERENCES Log(Transaction_ID))
                  ''')
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
            self.createTable()
            self.Profile = None

        def setProfile(self, Profile):
            self.Profile = Profile

        def __SetUpConnection(self):
            self.conn = sqlite3.connect(SetUpFile.DBLog)
            self.c = self.conn.cursor()

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
            if Transaction_ID is None:
                Transaction_ID = str(uuid.uuid4())
            self.c.execute('''
                  INSERT INTO Money (Transaction_ID,User_ID,ActionType,Change,TradeCost)
                        VALUES 
                        (?,?,?,?,?)
                  ''', (Transaction_ID, User_ID, ActionType, Change, TradeCost))
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
            if ActionType == DB_Code.MoneyOut:
                User.addMoney(-Data[4], LogChanges=False)
            elif ActionType == DB_Code.ProfitLoss:
                # using investment get bought price too.
                User.addMoney((-Data[4]), LogChanges=False)
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
            self.c.execute(sql, (ActionType, self.Profile,))
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

        def convertToExcel(self):
            DBFunctions.convertToExcel("Money", SetUpFile.DBLog)