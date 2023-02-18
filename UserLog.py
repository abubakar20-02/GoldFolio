import sqlite3

import DB_Code
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
              ([TimeStamp] TIMESTAMP DEFAULT CURRENT_TIMESTAMP,[Transaction_ID] VARCHAR PRIMARY KEY, [Transaction_Type] TEXT DEFAULT "" , [NoOfRecordsAffected] INTEGER DEFAULT 1 , [User_ID] VARCHAR DEFAULT ""  ,[FirstName] TEXT DEFAULT "" , [LastName] TEXT DEFAULT "", [Money] REAL DEFAULT 0.0,
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
                    #reverse order
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
