import sqlite3
import SetUpFile


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
              ([Transaction_ID] VARCHAR PRIMARY KEY, [Transaction_Type] TEXT DEFAULT "" , [NoOfRecordsAffected] INTEGER DEFAULT 1 , [User_ID] VARCHAR DEFAULT ""  ,[FirstName] TEXT DEFAULT "" , [LastName] TEXT DEFAULT "", [Money] REAL DEFAULT 0.0,
              FOREIGN KEY(Transaction_ID) REFERENCES Log(Transaction_ID))
              ''')
        self.conn.commit()
        self.conn.close()

    def DeleteStatement(self, id, DB_Code, RecordsAffected, User_ID):
        self.SetUpConnection()
        self.c.execute('''
        INSERT INTO UserLog (Transaction_ID,Transaction_Type,NoOfRecordsAffected,User_ID)
                VALUES 
                (?,?,?,?)
              ''', (id, DB_Code, RecordsAffected, User_ID))
        self.conn.commit()
        self.conn.close()

    def InsertStatement(self, id, DB_Code, User_ID, FName, LName, Money):
        self.SetUpConnection()
        self.c.execute('''
        INSERT INTO UserLog (Transaction_ID,Transaction_Type,User_ID,FirstName, LastName, Money)
                VALUES 
                (?,?,?,?,?,?)
              ''', (id, DB_Code, User_ID, FName, LName, Money))
        self.conn.commit()
        self.conn.close()

    def UpdateStatement(self, id, DB_Code, User_ID, Money):
        self.SetUpConnection()
        self.c.execute('''
        INSERT INTO UserLog (Transaction_ID,Transaction_Type,User_ID, Money)
                VALUES 
                (?,?,?,?)
              ''', (id, DB_Code, User_ID, Money))
        self.conn.commit()
        self.conn.close()
