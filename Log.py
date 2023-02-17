# create a function that can convert excel file to db.
import sqlite3
import uuid

import SetUpFile


class Log:
    def __init__(self):
        super().__init__()
        self.c = None
        self.conn = None
        self.Profile = None
        # done temporarily to skip the pain of deleting table everytime I run.
        self.dropTable()
        self.createTable()

    def setProfile(self, user):
        self.Profile = user

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

    def insert(self, TransactionType):
        id = str(uuid.uuid4())
        # try:
        #     self.c.execute('''
        #           INSERT INTO Investment (Investment_ID, User_ID , Gold, Purity, BoughtFor, ProfitLoss)
        #
        #                 VALUES
        #                 (?,?,?,?,?,?)
        #           ''', (InvestmentId, UserID, Gold, Purity, BoughtFor, 0.00))
        self.__SetUpConnection()
        self.c.execute('''
              INSERT INTO Log (Transaction_ID,TransactionType)
                    VALUES 
                    (?,?)
              ''', (id, TransactionType,))
        self.conn.commit()
        self.conn.close()
