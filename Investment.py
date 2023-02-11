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
              ([Investment_ID] VARCHAR PRIMARY KEY, [User_ID] VARCHAR,[Gold] REAL ,[Purity] REAL, [BoughtFor] REAL, [ProfitLoss] REAL,
              FOREIGN KEY(User_ID) REFERENCES User(User_ID))
              ''')
        self.conn.commit()
        self.conn.close()

    def deleteRecord(self, User_ID):
        """Takes in the user ID to delete investment for that ID."""
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
        """Takes in the investmentID , User ID, Gold in grams, Purity and the total price bought for"""
        self.__SetUpConnection()
        try:
            self.c.execute('''
                  INSERT INTO Investment (Investment_ID, User_ID , Gold, Purity, BoughtFor, ProfitLoss)

                        VALUES
                        (?,?,?,?,?,?)
                  ''', (InvestmentId, UserID, Gold, Purity, BoughtFor, 0.00))
            self.conn.commit()
        except sqlite3.Error as error:
            print(error)
        finally:
            self.conn.close()

    def updateRecord(self, User_ID, Money, Gold, Purity, GoldRate):
        """Takes in the user id to update the value of gold , weight of the gold and the purity of the gold."""
        self.__SetUpConnection()
        self.c.execute('''
              UPDATE User SET Money = ? , Gold = ?, Purity=?, ProfitLoss =(SELECT round(((?-(BoughtFor/Gold))/(BoughtFor/Gold))*100,2) WHERE User_ID = ?
              ''', (Money, Gold, Purity, User_ID, GoldRate))
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
                              columns=['Investment_ID', 'User_ID', 'Gold', 'Purity', 'BoughtFor', 'ProfitLoss'])
            print(df)
        except sqlite3.Error as error:
            print(error)
        finally:
            self.conn.close()

    def showInvestmentForUser(self, User_ID):
        """Show the investment of the given user id"""
        self.__SetUpConnection()
        self.c.execute('''
                  SELECT * FROM Investment WHERE User_ID =?
                  ''', (User_ID,))
        self.conn.commit()
        df = pd.DataFrame(self.c.fetchall(),
                          columns=['Investment_ID', 'User_ID', 'Gold', 'Purity', 'BoughtFor'])
        self.conn.close()
        print(df)

    def updateProfitLoss(self, GoldRate):
        """Run continuously to update profit/loss"""
        self.__SetUpConnection()
        self.c.execute('''
                  UPDATE Investment SET ProfitLoss =(SELECT round(((?-(BoughtFor/Gold))/(BoughtFor/Gold))*100,2))
                  ''', (GoldRate,))
        self.conn.commit()
        self.conn.close()
        self.showTable()

    def showProfit(self):
        self.__SetUpConnection()
        self.c.execute('''
                    SELECT * FROM Investment WHERE ProfitLoss>0
                  ''')
        self.conn.commit()
        df = pd.DataFrame(self.c.fetchall(),
                          columns=['Investment_ID', 'User_ID', 'Gold', 'Purity', 'BoughtFor', 'ProfitLoss'])
        print(df)
        self.conn.close()

    def showLoss(self):
        self.__SetUpConnection()
        self.c.execute('''
                    SELECT * FROM Investment WHERE ProfitLoss<0
                  ''')
        self.conn.commit()
        df = pd.DataFrame(self.c.fetchall(),
                          columns=['Investment_ID', 'User_ID', 'Gold', 'Purity', 'BoughtFor', 'ProfitLoss'])
        print(df)
        self.conn.close()
