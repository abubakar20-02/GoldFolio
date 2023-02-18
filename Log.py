# create a function that can convert excel file to db.
import sqlite3
import uuid

import DB_Code
from UserLog import UserLog
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
        self.UserLog = UserLog()
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
