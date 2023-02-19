import sqlite3
import uuid

import pandas as pd

import DB_Code
import SetUpFile
from Archive import InvestmentArchive
from Log import Log


def generateTransactionID():
    return str(uuid.uuid4())


# give user the ability when selling to input manual gold rate too.

# create UserArchive function that can convert excel file to db.
class Investment:
    def __init__(self):
        super().__init__()
        self.c = None
        self.conn = None
        self.Profile = None
        self.InvestmentArchive = InvestmentArchive()
        self.Log = Log()
        self.InvestmentLog = Log.InvestmentLog()

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
            self.c.execute("DELETE FROM Investment")
            print("Delete Investment")
            # self.c.execute("SELECT * FROM Investment")
            # Values = self.c.fetchall()
            # self.c.execute("SELECT COUNT(*) FROM Investment")
            # RecordsAffected = self.c.fetchone()[0]
            # self.c.execute("DROP TABLE Investment")
            # self.conn.commit()
            # if RecordsAffected > 0:
            #     self.Log.insert(id, "DeleteInvestment")
            #     self.InvestmentLog.DeleteStatement(id, "DropInvestments", RecordsAffected, None)
            #     self.UserArchive.Archive(Values)
        except sqlite3.Error as error:
            print(error)
        finally:
            self.conn.close()
#dsfjknnnsjhjjjhjhjhjhjhjhjhjhjhjhjhjhjhjhjahjkfsd
    # need to use investment id to delete
    def deleteRecord(self, User_ID, LogChanges=True):
        """Takes in the user ID to delete investment for that ID."""

        self.__SetUpConnection()
        try:
            self.c.execute('''
                  SELECT COUNT(*) FROM Investment WHERE User_Id = ?
                  ''', (User_ID,))
            RecordsAffected = self.c.fetchone()[0]
            a = RecordsAffected
            while a > 0:
                self.c.execute('''
                      SELECT * FROM Investment WHERE User_Id = ? LIMIT 1
                      ''', (User_ID,))
                Values = self.c.fetchall()
                #dsfasjkoasdjklasdjnkasd
                if LogChanges is True:
                    print("Archived")
                    self.InvestmentArchive.Archive(Values)
                self.c.execute('''
                      DELETE FROM Investment WHERE Investment_ID IN(SELECT Investment_ID FROM Investment WHERE User_Id = ? LIMIT 1) 
                      ''', (User_ID,))
                a = a - 1
            self.conn.commit()
            if LogChanges is True:
                self.LogForDelete(generateTransactionID(), RecordsAffected, User_ID)
        except sqlite3.Error as error:
            print(error)
        finally:
            self.conn.close()

    def LogForDelete(self, id, RecordsAffected, User_ID):
        self.Log.insert(id, DB_Code.ID)
        self.InvestmentLog.DeleteStatement(id, RecordsAffected, User_ID)

    def insertIntoTable(self, Gold, Purity, BoughtFor, LogChanges=True, Transaction_ID=None):
        """Takes in the investmentID , User ID, Gold in grams, Purity and the total price bought for"""
        self.__SetUpConnection()
        Error = True
        # loop until there is no error.
        while Error:
            Error = False
            if Transaction_ID is None:
                Transaction_ID = generateTransactionID()
            try:
                self.c.execute('''
                      INSERT INTO Investment (Investment_ID, User_ID , Gold, Purity, BoughtFor, ProfitLoss)
    
                            VALUES
                            (?,?,?,?,?,?)
                      ''', (Transaction_ID, self.Profile, Gold, Purity, BoughtFor, 0.00))
                if LogChanges is True:
                    self.__LogForInsert(BoughtFor, Gold, Purity, Transaction_ID)
            except sqlite3.Error as error:
                print(error)
                Error = True
        self.conn.commit()
        self.conn.close()

    def __LogForInsert(self, BoughtFor, Gold, Purity, Transaction_ID):
        self.Log.insert(Transaction_ID, DB_Code.IB)
        self.InvestmentLog.InsertStatement(Transaction_ID, self.Profile, Gold, Purity, BoughtFor, 0.00)

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
        # self.Log.insert(my_uuid, DB_Code.IU)
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
    def sellProfit(self, LogChanges=True):
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
        if RecordsAffected > 0 and LogChanges is True:
            self.__LogSellProfit(RecordsAffected, Values, generateTransactionID())
        self.conn.close()

    def __LogSellProfit(self, RecordsAffected, Values, my_uuid):
        self.Log.insert(my_uuid, DB_Code.ISP)
        self.InvestmentLog.SellAllProfitStatement(my_uuid, RecordsAffected, self.Profile)
        self.InvestmentArchive.Archive(Values)

    # add user here
    def sellAll(self, LogChanges=True):
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
        self.conn.close()
        if RecordsAffected > 0 and LogChanges is True:
            self.__LogSellAll(RecordsAffected, Values, generateTransactionID())

    def __LogSellAll(self, RecordsAffected, Values, id):
        self.Log.insert(id, DB_Code.ISA)
        self.InvestmentLog.SellAllStatement(id, RecordsAffected, self.Profile)
        self.InvestmentArchive.Archive(Values)
