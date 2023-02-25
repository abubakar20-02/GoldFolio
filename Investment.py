import math
import sqlite3
import uuid
from datetime import datetime

import pandas as pd

import DBFunctions
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
        self.MoneyLog = Log.Money()

    def ImportFromExcel(self):
        # source = 'UserTemplate.xlsx'
        target = 'Investment.xlsx'
        # shutil.copyfile(source,target)
        # os.system(target)

        sheet_name = 'Sheet1'

        path = target

        # Read the Excel file into a DataFrame
        df = pd.read_excel(path, sheet_name=sheet_name)

        from User import User
        User = User()

        # check if user id exists already then only add. use purity boughtfor gold to be sure its real number.
        # date_added to be a date.

        # Define the SQL query to insert the data into the table
        table_name = "Investment"
        columns = ','.join(df.columns)
        placeholders = ','.join(['?' for _ in range(len(df.columns))])
        print(placeholders)
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        print(sql)
        # Loop through the rows in the DataFrame and insert them into the table
        for _, row in df.iterrows():
            values = tuple(row)
            # check if user id exists in user db.
            if not User.isUserExist(values[1]):
                # if user doesnt exist in profile then dont add them.
                continue

            # check if the data is correct. Gold, Purity and Bought for have to be numbers and not empty whereas
            # profit loss only needs to be a number, but it can be None.
            if not (self.CorrectNumberFormat(values[2]) and self.CorrectNumberFormat(
                    values[3]) and self.CorrectNumberFormat(values[4]) and isinstance(values[5], (float, int))):
                continue

            # if it reaches here, then user is in the list, so we can set profile.
            self.setProfile(values[1])

            # checks if time is none or date is empty.
            if isinstance(values[0], datetime) and values[0] is pd.NaT or self.isEmpty(values[0]):
                self.insertIntoTable(values[2], values[3], values[4], ProfitLoss=values[5], LogChanges=False)
            else:
                if isinstance(values[0], datetime):
                    # if date is in the future then don't add it.
                    # if datetime.strptime(values[0].strftime("%Y-%m-%d"), '%Y-%m-%d').date() > datetime.now().date():
                    #     print("future")
                    #     continue
                    # convert date to Y-m-d format
                    self.insertIntoTable(values[2], values[3], values[4], Date=values[0].strftime("%Y-%m-%d"),
                                         ProfitLoss=values[5], LogChanges=False,IgnoreMoney=True)

    def isEmpty(self, value):
        # value is a number and it is not none.
        if isinstance(value, (float, int)) and (math.isnan(value)):
            return True
        else:
            return False

    def CorrectNumberFormat(self, value):
        # value is a number and it is not none.
        if isinstance(value, (float, int)) and not (math.isnan(value)):
            return True
        else:
            return False

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
              ([Investment_ID] VARCHAR PRIMARY KEY,[Date_Added] DATE, [User_ID] VARCHAR,[Gold] REAL ,[Purity] REAL, [BoughtFor] REAL, [ProfitLoss] REAL,
              FOREIGN KEY(User_ID) REFERENCES User(User_ID))
              ''')
        self.conn.commit()
        self.conn.close()

    def deleteTable(self):
        self.__SetUpConnection()
        try:
            self.c.execute("DELETE FROM Investment")
            self.conn.commit()
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

    # dsfjknnnsjhjjjhjhjhjhjhjhjhjhjhjhjhjhjhjhjahjkfsd
    # need to use investment id to delete
    def deleteRecord(self, User_ID, LogChanges=True, Archive=True, TransactionID=None):
        """Takes in the user ID to delete investment for that ID."""
        self.__SetUpConnection()
        if TransactionID is not None:
            print("yoooooooo")
            self.c.execute('''
                  SELECT * FROM Investment WHERE Investment_ID = ? LIMIT 1
                  ''', (TransactionID,))
            Values = self.c.fetchone()
            print(Values)
            if Archive:
                self.InvestmentArchive.Archive(Values)
            self.c.execute('''
                  DELETE FROM Investment WHERE Investment_ID = ? 
                  ''', (Values[0],))
            self.conn.commit()
            self.conn.close()
            return
        try:
            self.c.execute('''
                  SELECT COUNT(*) FROM Investment WHERE User_Id = ?
                  ''', (User_ID,))
            RecordsAffected = self.c.fetchone()[0]
            a = RecordsAffected
            # while a > 0:
            self.c.execute('''
                  SELECT * FROM Investment WHERE User_Id = ? LIMIT 1
                  ''', (User_ID,))
            Values = self.c.fetchall()
            if Archive:
                self.InvestmentArchive.Archive(Values)
            self.c.execute('''
                  DELETE FROM Investment WHERE Investment_ID = (SELECT Investment_ID FROM Investment WHERE User_Id = ?) 
                  ''', (User_ID,))
            print("---")
            print(User_ID)
            print("---")
            # a = a - 1
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

    def insertIntoTable(self, Gold, Purity, BoughtFor, LogChanges=True, Transaction_ID=None, Date=None,
                        ProfitLoss=None, IgnoreMoney=False):
        """Takes in the investmentID , User ID, Gold in grams, Purity and the total price bought for"""
        self.__SetUpConnection()
        if IgnoreMoney is False:
            from User import User
            User = User()
            User.SelectProfile(self.Profile)
            TotalMoney = User.getMoney()
            if TotalMoney < BoughtFor:
                print("not enough cash")
                return

        if Date is None:
            Date = datetime.now().date()
        else:
            if datetime.strptime(Date, '%Y-%m-%d').date() > datetime.now().date():
                print("date is in future")
                return
        Error = True
        # loop until there is no error.
        while Error:
            Error = False
            if Transaction_ID is None:
                Transaction_ID = generateTransactionID()
            try:
                self.c.execute('''
                      INSERT INTO Investment (Investment_ID,Date_Added, User_ID , Gold, Purity, BoughtFor, ProfitLoss)
    
                            VALUES
                            (?,?,?,?,?,?,?)
                      ''', (Transaction_ID, Date, self.Profile, Gold, Purity, BoughtFor, ProfitLoss))
                self.conn.commit()
                self.conn.close()
                if IgnoreMoney is False:
                    User.addMoney(-BoughtFor, LogChanges=False)
                if LogChanges is True:
                    self.__LogForInsert(BoughtFor, Gold, Purity, Transaction_ID)
            except sqlite3.Error as error:
                print(error)
                Error = True

    def __LogForInsert(self, BoughtFor, Gold, Purity, Transaction_ID):
        self.Log.insert(Transaction_ID, DB_Code.IB)
        self.MoneyLog.insertIntoTable(self.Profile, DB_Code.BuyInvestment, -BoughtFor, Transaction_ID=Transaction_ID)
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
                  UPDATE Investment SET ProfitLoss =(SELECT round(((?-(BoughtFor/Gold))/(BoughtFor/Gold))*100,2) WHERE User_ID =?)
                  ''', (GoldRate, self.Profile))
        self.conn.commit()
        self.conn.close()
        # self.showTable()

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
    def sellProfit(self, LogChanges=True, Rate=None):
        # only apply rate to what is going to be sold.
        if Rate is not None:
            # if connected to a thread this might not work all the time.
            self.updateProfitLoss(Rate)
        self.__SetUpConnection()
        self.c.execute('''SELECT * FROM Investment WHERE (ProfitLoss>0 AND User_ID=?)''', (self.Profile,))
        Values = self.c.fetchall()
        self.c.execute('''SELECT COUNT(*) FROM Investment WHERE (ProfitLoss>0 AND User_ID=?)''', (self.Profile,))
        RecordsAffected = self.c.fetchone()[0]
        print(RecordsAffected)
        # calculate total profit
        # profitloss/100 * bought for
        self.c.execute('''SELECT SUM((ProfitLoss/100)*BoughtFor) FROM Investment WHERE (ProfitLoss>0 AND User_ID=?)''',
                       (self.Profile,))
        TotalProfit = self.c.fetchone()[0]
        if TotalProfit is None:
            return
        self.c.execute('''SELECT SUM(BoughtFor) FROM Investment WHERE (ProfitLoss>0 AND User_ID=?)''',
                       (self.Profile,))
        TotalCost = self.c.fetchone()[0]
        from User import User
        User = User()
        User.SelectProfile(self.Profile)
        User.addMoney(TotalProfit + TotalCost, LogChanges=False)
        print("Total Profit:" + str(TotalProfit))
        self.c.execute('''
                    INSERT INTO Statement SELECT * FROM Investment WHERE (ProfitLoss>0 AND User_ID=?)
                  ''', (self.Profile,))
        self.c.execute('''
                    DELETE FROM Investment WHERE (ProfitLoss>0 AND User_ID=?)
                  ''', (self.Profile,))
        self.conn.commit()
        if LogChanges is True:
            Transaction_ID = generateTransactionID()
            self.__LogSellProfit(RecordsAffected, Values, Transaction_ID)
            print("hmmm")
            self.MoneyLog.insertIntoTable(self.Profile, DB_Code.ProfitLoss, TotalProfit, Transaction_ID=Transaction_ID,
                                          TradeCost=TotalCost)
        self.conn.close()

    def __LogSellProfit(self, RecordsAffected, Values, my_uuid):
        self.Log.insert(my_uuid, DB_Code.ISP)
        self.InvestmentLog.SellAllProfitStatement(my_uuid, RecordsAffected, self.Profile)
        self.InvestmentArchive.Archive(Values)

    # add user here
    def sellAll(self, LogChanges=True, Date=None, Rate=None):
        if Rate is not None:
            self.updateProfitLoss(Rate)
        self.__SetUpConnection()
        if Date is None:
            Date = datetime.now().date()
        self.c.execute('''SELECT MIN(Date_Added) FROM Investment WHERE User_ID= ?''', (self.Profile,))
        minimum_date = self.c.fetchone()[0]
        print(minimum_date)
        if minimum_date is not None and datetime.strptime(str(Date), '%Y-%m-%d').date() < datetime.strptime(
                minimum_date, '%Y-%m-%d').date():
            print("------------")
            print("invalid")
            print("------------")
            return

        #
        #     Values = self.c.fetchall()
        #     if  > datetime.now().date():
        #         print("date is in future")
        #         return

        self.c.execute('''SELECT * FROM Investment WHERE User_ID= ?''', (self.Profile,))
        Values = self.c.fetchall()
        self.c.execute('''SELECT COUNT(*) FROM Investment WHERE User_ID= ?''', (self.Profile,))
        RecordsAffected = self.c.fetchone()[0]

        # calculate total profit
        # profitloss/100 * bought for
        self.c.execute('''SELECT SUM((ProfitLoss/100)*BoughtFor) FROM Investment WHERE (User_ID=? AND ProfitLoss>=0)''',
                       (self.Profile,))
        TotalPositiveProfit = self.c.fetchone()[0]
        self.c.execute(
            '''SELECT SUM((ProfitLoss/100)*BoughtFor) FROM Investment WHERE (User_ID=? AND ProfitLoss<0)''',
            (self.Profile,))
        TotalNegativeProfit = self.c.fetchone()[0]
        print("-" + str(TotalNegativeProfit))
        print("+" + str(TotalPositiveProfit))

        self.c.execute('''SELECT SUM(BoughtFor) FROM Investment WHERE (User_ID=?)''',
                       (self.Profile,))
        TotalCost = self.c.fetchone()[0]
        if TotalCost is None:
            TotalCost = 0

        print(TotalCost)

        from User import User
        User = User()
        User.SelectProfile(self.Profile)
        if TotalPositiveProfit is None:
            TotalPositiveProfit = 0
        if TotalNegativeProfit is None:
            TotalNegativeProfit = 0
            print(TotalPositiveProfit + TotalNegativeProfit)
        User.addMoney((TotalPositiveProfit + TotalNegativeProfit + TotalCost), LogChanges=False)

        self.c.execute('''
                    INSERT INTO Statement(Investment_ID,User_ID,Gold,Purity,BoughtFor,ProfitLoss) SELECT Investment_ID,User_ID,Gold,Purity,BoughtFor,ProfitLoss FROM Investment WHERE User_ID= ?
                  ''', (self.Profile,))
        self.c.execute('''
                    DELETE FROM Investment WHERE User_ID=?
                  ''', (self.Profile,))
        self.conn.commit()
        self.conn.close()
        if RecordsAffected > 0 and LogChanges is True:
            Transaction_ID = generateTransactionID()
            self.__LogSellAll(RecordsAffected, Values, Transaction_ID)
            self.MoneyLog.insertIntoTable(self.Profile, DB_Code.ProfitLoss, (TotalPositiveProfit + TotalNegativeProfit),
                                          Transaction_ID=Transaction_ID, TradeCost=TotalCost)

    def __LogSellAll(self, RecordsAffected, Values, id):
        self.Log.insert(id, DB_Code.ISA)
        self.InvestmentLog.SellAllStatement(id, RecordsAffected, self.Profile)
        self.InvestmentArchive.Archive(Values)

    import sqlite3

    def traverse_all_dates(self, ColumnName):
        # connect to database
        dictionary = {}
        self.__SetUpConnection()

        sql = "SELECT SUM({0}) FROM Investment WHERE Date_Added = ?".format(ColumnName)

        # execute SQL query to get all dates
        self.c.execute("SELECT DISTINCT Date_Added FROM Investment ORDER BY Date_Added ASC")

        # loop through dates and print the sum of values for each date
        for row in self.c.fetchall():
            date = row[0]
            self.c.execute(sql, (date,))
            format_str = '%Y-%m-%d'
            date=datetime.strptime(date, format_str)
            print(type(date))
            sum_of_values = self.c.fetchone()[0]
            dictionary[date] = sum_of_values
            print(f"{date}: {sum_of_values}")
        print(dictionary)

        # close database connection
        self.conn.close()
        return dictionary

    def add_to_dict(self, dictionary, key, value):
        dictionary[key] = value
        return dictionary

    def convertToExcel(self):
        DBFunctions.convertToExcel("Investment", SetUpFile.DBName)
