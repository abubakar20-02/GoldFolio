import sqlite3
import pandas as pd
from xlsxwriter import Workbook
import os

import SetUpFile


class Investment:
    def __init__(self):
        super().__init__()
        self.c = None
        self.conn = None

    # __ makes the method private
    def __SetUpConnection(self):
        self.conn = sqlite3.connect(SetUpFile.DBName)
        self.c = self.conn.cursor()

    def deleteTable(self):
        self.__SetUpConnection()
        try:
            self.c.execute("DROP TABLE Investment")
            self.conn.commit()
        except sqlite3.Error as error:
            print(error)
        finally:
            self.conn.close()

    def createTable(self):
        # date, gold rate, weight
        self.__SetUpConnection()
        self.c.execute('''
              CREATE TABLE IF NOT EXISTS Investment
              ([Investment_ID] VARCHAR PRIMARY KEY, [User_ID] VARCHAR,[Gold] REAL ,[Purity] REAL, [BoughtFor] REAL,
              FOREIGN KEY(User_ID) REFERENCES User(User_ID))
              ''')
        self.conn.commit()
        self.conn.close()

    def deleteRecord(self, User_ID):
        self.__SetUpConnection()
        try:
            self.c.execute('''
                  DELETE FROM Investment WHERE User_Id = ?
                  ''', (User_ID,))
            self.conn.commit()
        except sqlite3.Error as error:
            print(error)
        finally:
            self.conn.close()

    def insertIntoTable(self, InvestmentId, UserID, Gold, Purity, BoughtFor):
        self.__SetUpConnection()
        try:
            self.c.execute('''
                  INSERT INTO Investment (Investment_ID, User_ID , Gold, Purity, BoughtFor)

                        VALUES
                        (?,?,?,?,?)
                  ''', (InvestmentId, UserID, Gold, Purity, BoughtFor))
            self.conn.commit()
        except sqlite3.Error as error:
            print(error)
        finally:
            self.conn.close()

    def updateRecord(self, User_ID, Money, Gold, Purity):
        self.__SetUpConnection()
        self.c.execute('''
              UPDATE User SET Money = ? , Gold = ?, Purity=? WHERE User_ID = ?
              ''', (Money, Gold, Purity, User_ID))
        self.conn.commit()
        self.conn.close()

    def showTable(self):
        self.__SetUpConnection()
        try:
            self.c.execute('''
                      SELECT * FROM Investment
                      ''')
            self.conn.commit()
            df = pd.DataFrame(self.c.fetchall(),
                              columns=['Investment_ID', 'User_ID', 'Gold', 'Purity', 'BoughtFor'])
            print(df)
        except sqlite3.Error as error:
            print(error)
        finally:
            self.conn.close()

    def showInvestmentForUser(self, User_ID):
        self.__SetUpConnection()
        self.c.execute('''
                  SELECT * FROM Investment WHERE User_ID =?
                  ''', (User_ID,))
        self.conn.commit()
        df = pd.DataFrame(self.c.fetchall(),
                          columns=['Investment_ID', 'User_ID', 'Gold', 'Purity', 'BoughtFor'])
        self.conn.close()
        print(df)

    def showProfitLoss(self, GoldRate):
        self.__SetUpConnection()
        self.c.execute('''
                  SELECT User_ID ,Gold,BoughtFor, round(((?-(BoughtFor/Gold))/(BoughtFor/Gold))*100,2) AS result FROM Investment 
                  ''', (GoldRate,))
        self.conn.commit()
        df = pd.DataFrame(self.c.fetchall(),
                          columns=['User_ID','Gold(g)', 'BoughtFor', 'Change (%)'])
        self.conn.close()
        print("---------------")
        print(df)
        print("---------------")
