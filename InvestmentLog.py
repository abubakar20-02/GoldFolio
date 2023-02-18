import sqlite3

import DB_Code
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
              ([TimeStamp] TIMESTAMP DEFAULT CURRENT_TIMESTAMP,[Transaction_ID] VARCHAR PRIMARY KEY, [Transaction_Type] TEXT DEFAULT "" , [NoOfRecordsAffected] INTEGER DEFAULT 1 , [Investment_ID] VARCHAR DEFAULT "", [User_ID] VARCHAR DEFAULT "",[Gold] REAL DEFAULT 0.0,[Purity] REAL DEFAULT 0.0, [BoughtFor] REAL DEFAULT 0.0, [ProfitLoss] REAL DEFAULT 0.0,
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

            print("Investment")
            if Transaction_Type == DB_Code.IB:
                print("Use Investment ID to delete")
            elif Transaction_Type == DB_Code.IU:
                print("Use archive data to update using Investment ID")
            elif Transaction_Type == DB_Code.ISP:
                print("Use User_ID to find most recent deleted investment using count")
            elif Transaction_Type == DB_Code.ISA:
                print("Use User_ID to find most recent deleted investment using count")
            else:
                print("nothing")
            print("")
        self.conn.commit()
        self.conn.close()
