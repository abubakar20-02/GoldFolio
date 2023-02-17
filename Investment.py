import sqlite3
import pandas as pd
import uuid

import DB_Code
from InvestmentArchive import InvestmentArchive
from Log import Log
from InvestmentLog import InvestmentLog
from xlsxwriter import Workbook
import os

import SetUpFile


# give user the ability when selling to input manual gold rate too.

# create a function that can convert excel file to db.
class Investment:
    def __init__(self):
        super().__init__()
        self.c = None
        self.conn = None
        self.Profile = None
        self.a = InvestmentArchive()
        self.b = Log()
        self.InvestmentLog = InvestmentLog()

    def setProfile(self, profile):
        self.Profile = profile

    # __ makes the method private
    def __SetUpConnection(self):
        self.conn = sqlite3.connect(SetUpFile.DBName)
        self.c = self.conn.cursor()

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

    def deleteTable(self):
        id = str(uuid.uuid4())
        self.__SetUpConnection()
        try:
            self.c.execute("SELECT * FROM Investment")
            Values = self.c.fetchall()
            self.c.execute("SELECT COUNT(*) FROM Investment")
            RecordsAffected = self.c.fetchone()[0]
            self.c.execute("DROP TABLE Investment")
            self.conn.commit()
            if RecordsAffected > 0:
                self.b.insert(id, "DeleteInvestment")
                self.InvestmentLog.DeleteStatement(id, DB_Code.ISA, RecordsAffected, None)
                self.a.Archive(Values)
        except sqlite3.Error as error:
            print(error)
        finally:
            self.conn.close()

    # need to use investment id to delete
    def deleteRecord(self, User_ID):
        """Takes in the user ID to delete investment for that ID."""
        self.__SetUpConnection()
        try:
            self.c.execute('''
                  DELETE FROM Investment WHERE User_Id = ?
                  ''', (User_ID,))
            self.conn.commit()
            self.b.insert("DeleteInvestment")
        except sqlite3.Error as error:
            print(error)
        finally:
            self.conn.close()

    def insertIntoTable(self, Gold, Purity, BoughtFor):
        """Takes in the investmentID , User ID, Gold in grams, Purity and the total price bought for"""
        self.__SetUpConnection()
        Error = True
        # loop until there is no error.
        while Error:
            Error = False
            my_uuid = str(uuid.uuid4())
            try:
                self.c.execute('''
                      INSERT INTO Investment (Investment_ID, User_ID , Gold, Purity, BoughtFor, ProfitLoss)
    
                            VALUES
                            (?,?,?,?,?,?)
                      ''', (my_uuid, self.Profile, Gold, Purity, BoughtFor, 0.00))
                self.b.insert(my_uuid, DB_Code.IB)
                self.InvestmentLog.InsertStatement(my_uuid, DB_Code.IB, self.Profile, Gold, Purity, BoughtFor, 0.00)
            except sqlite3.Error as error:
                print(error)
                Error = True
        self.conn.commit()
        self.conn.close()

    # need investment id to update.
    def updateRecord(self, Money, Gold, Purity, GoldRate):
        """Takes in the user id to update the value of gold , weight of the gold and the purity of the gold."""
        self.__SetUpConnection()
        my_uuid = str(uuid.uuid4())
        self.c.execute('''
              UPDATE User SET Money = ? , Gold = ?, Purity=?, ProfitLoss =(SELECT round(((?-(BoughtFor/Gold))/(BoughtFor/Gold))*100,2) WHERE User_ID = ?
              ''', (Money, Gold, Purity, self.Profile, GoldRate))
        self.conn.commit()
        # _________________________________________________
        # self.b.insert(my_uuid, DB_Code.IU)
        # self.InvestmentLog.UpdateStatement(my_uuid,DB_Code.IU, User_ID,)
        # _________________________________________________
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

    def showInvestmentForUser(self):
        """Show the investment of the given user id"""
        self.__SetUpConnection()
        self.c.execute('''
                  SELECT * FROM Investment WHERE User_ID =?
                  ''', (self.Profile,))
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

    # add user here
    def sellProfit(self):
        my_uuid = str(uuid.uuid4())
        self.__SetUpConnection()
        self.c.execute('''SELECT * FROM Investment WHERE (ProfitLoss>0 AND User_ID=?)''', (self.Profile,))
        Values = self.c.fetchall()
        self.c.execute('''SELECT COUNT(*) FROM Investment WHERE (ProfitLoss>0 AND User_ID=?)''', (self.Profile,))
        RecordsAffected = self.c.fetchone()[0]
        self.c.execute('''
                    INSERT INTO Statement SELECT * FROM Investment WHERE (ProfitLoss>0 AND User_ID=?)
                  ''', (self.Profile,))
        self.c.execute('''
                    DELETE FROM Investment WHERE (ProfitLoss>0 AND User_ID=?)
                  ''', (self.Profile,))
        self.conn.commit()
        if RecordsAffected > 0:
            self.b.insert(my_uuid, DB_Code.ISP)
            self.InvestmentLog.DeleteStatement(my_uuid, DB_Code.ISP, RecordsAffected, self.Profile)
            self.a.Archive(Values)
        self.conn.close()

    # add user here
    def sellAll(self):
        id = str(uuid.uuid4())
        self.__SetUpConnection()
        self.c.execute('''SELECT * FROM Investment WHERE User_ID= ?''', (self.Profile,))
        Values = self.c.fetchall()
        self.c.execute('''SELECT COUNT(*) FROM Investment WHERE User_ID= ?''', (self.Profile,))
        RecordsAffected = self.c.fetchone()[0]
        self.c.execute('''
                    INSERT INTO Statement SELECT * FROM Investment WHERE User_ID= ?
                  ''', (self.Profile,))
        self.c.execute('''
                    DELETE FROM Investment WHERE User_ID=?
                  ''', (self.Profile,))
        self.conn.commit()
        if RecordsAffected > 0:
            self.b.insert(id, DB_Code.ISA)
            self.InvestmentLog.DeleteStatement(id, DB_Code.ISA, RecordsAffected, self.Profile)
            self.a.Archive(Values)
        self.conn.close()
