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
              ([Time] TIMESTAMP DEFAULT CURRENT_TIMESTAMP ,[Transaction_ID] VARCHAR PRIMARY KEY, [TableName] VARCHAR)
              ''')
        self.conn.commit()
        self.conn.close()

    def insert(self, TableName):
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
              INSERT INTO Log (Transaction_ID,TableName)
                    VALUES 
                    (?,?)
              ''', (id, TableName,))
        self.conn.commit()
        self.conn.close()
