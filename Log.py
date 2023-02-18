# create a function that can convert excel file to db.
import sqlite3
import uuid

import DB_Code
from InvestmentLog import InvestmentLog
import SetUpFile


class Log:
    def __init__(self):
        super().__init__()
        self.c = None
        self.conn = None
        self.Profile = None
        self.uid = None
        self.TransactionType = None
        self.InvestmentLog = InvestmentLog()
        self.createTable()

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
            self.c.execute("DROP TABLE Log")
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

    def previousStage(self):
        self.__SetUpConnection()
        self.generateTransactionID()
        self.c.execute('''
            SELECT COUNT(*) FROM Log 
              ''')
        Records = self.c.fetchone()[0]
        self.c.execute('''
            SELECT * FROM Log LIMIT 1 OFFSET ?
              ''', (Records - 1,))
        Data = self.c.fetchone()
        print(Data[1])
        self.c.execute('''
            DELETE FROM Log WHERE Transaction_ID = ?
              ''', (Data[1],))
        self.conn.commit()
        self.conn.close()
        self.UserLog.SearchByID(Data[1])
        self.InvestmentLog.SearchByID(Data[1])

    def UserLogInsertStatement(self, id, User_ID, FName, LName, Money):
        self.UserLog.InsertStatement(id, DB_Code.UI, User_ID, FName, LName, Money)

    def UserLogDeleteStatement(self, id, RecordsAffected, User_ID):
        self.UserLog.DeleteStatement(id, DB_Code.UD, RecordsAffected, User_ID)

    def UserLogUpdateStatement(self, id, User_ID, Money):
        self.UserLog.DeleteStatement(id, DB_Code.UU, User_ID, Money)

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
                  ([TimeStamp] TIMESTAMP DEFAULT CURRENT_TIMESTAMP,[Transaction_ID] VARCHAR PRIMARY KEY, [Transaction_Type] TEXT DEFAULT "" , [NoOfRecordsAffected] INTEGER DEFAULT 1 , [User_ID] VARCHAR DEFAULT ""  ,[FirstName] TEXT DEFAULT "" , [LastName] TEXT DEFAULT "", [Money] REAL DEFAULT 0.0,
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
                if Transaction_Type == DB_Code.UD:
                    if User_ID is None:
                        print("Recover from User archive using No of records")
                        # reverse order
                    else:
                        print("Recover using user id")

                elif Transaction_Type == DB_Code.UI:
                    print("Delete using User_ID")
                    # self.user.deleteRecord(User_ID)

                elif Transaction_Type == DB_Code.UU:
                    print("Update using archive user data")
                    # self.userArchive.getData()
                else:
                    print("Something else")
                print("")
            self.conn.commit()
            # print(User_ID)
            self.conn.close()
