import sqlite3
import SetUpFile


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
              ([TimeStamp] TIMESTAMP DEFAULT CURRENT_TIMESTAMP,[Transaction_ID] VARCHAR PRIMARY KEY, [Transaction_Type] TEXT DEFAULT "" , [NoOfRecordsAffected] INTEGER DEFAULT 1 , [Investment_ID] VARCHAR, [User_ID] VARCHAR,[Gold] REAL ,[Purity] REAL, [BoughtFor] REAL, [ProfitLoss] REAL,
              FOREIGN KEY(Transaction_ID) REFERENCES Log(Transaction_ID))
              ''')
        self.conn.commit()
        self.conn.close()

    def DeleteStatement(self, id, DB_Code, RecordsAffected, User_ID):
        self.SetUpConnection()
        self.c.execute('''
        INSERT INTO InvestmentLog (Transaction_ID,Transaction_Type,NoOfRecordsAffected,User_ID)
                VALUES 
                (?,?,?,?)
              ''', (id, DB_Code, RecordsAffected, User_ID))
        self.conn.commit()
        self.conn.close()

    def InsertStatement(self, id, DB_Code, User_ID, Gold, Purity, BoughtFor, ProfitLoss):
        self.SetUpConnection()
        self.c.execute('''
        INSERT INTO InvestmentLog (Transaction_ID,Transaction_Type,User_ID,Gold, Purity, BoughtFor, ProfitLoss)
                VALUES 
                (?,?,?,?,?,?,?)
              ''', (id, DB_Code, User_ID, Gold, Purity, BoughtFor, ProfitLoss))
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