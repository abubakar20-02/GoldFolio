import math
import sqlite3
import uuid
from datetime import datetime

import pandas as pd

from Database import DB_Code, DBFunctions, SetUpFile
from Database import Archive
from Database import Log
from Database import Statement


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
        self.InvestmentArchive = Archive.InvestmentArchive()
        self.Log = Log.Log()
        self.InvestmentLog = Log.Log.InvestmentLog()
        self.MoneyLog = Log.Log.Money()
        self.Statement = Statement.Statement()

    def ImportFromExcel(self):
        # source = 'UserTemplate.xlsx'
        target = 'Investment.xlsx'
        # shutil.copyfile(source,target)
        # os.system(target)

        sheet_name = 'Sheet1'

        path = target

        # Read the Excel file into a DataFrame
        df = pd.read_excel(path, sheet_name=sheet_name)

        from Database import User
        User = User.User()

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
                                         ProfitLoss=values[5], LogChanges=False, IgnoreMoney=True)

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
              ([Investment_ID] VARCHAR PRIMARY KEY,[Date_Added] DATE, [User_ID] VARCHAR,[Gold] REAL ,[Purity] REAL, [BoughtFor] REAL, [ProfitLoss] REAL DEFAULT 0.0,
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
        if ProfitLoss is None:
            ProfitLoss = 0.0
        if IgnoreMoney is False:
            from Database import User
            User = User.User()
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

    def getTable(self, StartDate=None, EndDate=None):
        self.__SetUpConnection()
        try:
            sql = "SELECT * FROM Investment WHERE User_ID = ?"
            if StartDate:
                sql += f" AND Date_Added >= '{StartDate}'"

            if EndDate:
                sql += f" AND Date_Added <= '{EndDate}'"
            sql += f" ORDER BY Date_Added DESC"

            print(sql)
            values = (self.Profile,)
            df = pd.read_sql(sql, self.conn, params=values)
            df = df.drop('User_ID', axis=1)
            df = df.drop('Purity', axis=1)
        except sqlite3.Error as error:
            print(error)
        finally:
            self.conn.close()
            # print(df)
            return df

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

    def updateProfitLoss(self, GoldRate, Investment_ID=None):
        """Run continuously to update profit/loss"""
        values = (GoldRate, self.Profile)
        self.__SetUpConnection()
        select = "SELECT round(((?-(BoughtFor/Gold))/(BoughtFor/Gold))*100,2) WHERE User_ID =? "
        if Investment_ID is not None:
            values = values + (Investment_ID,)
            select += "AND Investment_ID = ?"
        complete = "UPDATE Investment SET ProfitLoss =({0})".format(select)
        print(complete)
        self.c.execute(complete, values)
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
    def sellProfit(self, LogChanges=True, Rate=None, Date=None, StartDate=None, EndDate=None):
        # only apply rate to what is going to be sold.
        if Rate is not None:
            # if connected to a thread this might not work all the time.
            self.updateProfitLoss(Rate)

        sql = "SELECT * FROM Investment WHERE User_ID = ? AND ProfitLoss>0"
        if StartDate:
            sql += f" AND Date_Added >= '{StartDate}'"

        if EndDate:
            sql += f" AND Date_Added <= '{EndDate}'"

        sqlCount = "SELECT COUNT(*) FROM Investment WHERE User_ID = ? AND ProfitLoss>0"
        if StartDate:
            sqlCount += f" AND Date_Added >= '{StartDate}'"

        if EndDate:
            sqlCount += f" AND Date_Added <= '{EndDate}'"

        sqlProfitLoss = "SELECT SUM((ProfitLoss/100)*BoughtFor) FROM Investment WHERE User_ID=? AND ProfitLoss>0"
        if StartDate:
            sqlProfitLoss += f" AND Date_Added >= '{StartDate}'"

        if EndDate:
            sqlProfitLoss += f" AND Date_Added <= '{EndDate}'"

        sqlSumBoughtFor = "SELECT SUM(BoughtFor) FROM Investment WHERE User_ID=? AND ProfitLoss>0"
        if StartDate:
            sqlSumBoughtFor += f" AND Date_Added >= '{StartDate}'"

        if EndDate:
            sqlSumBoughtFor += f" AND Date_Added <= '{EndDate}'"

        sqlSelectStatement = "SELECT Investment_ID, User_ID , Gold, Purity, BoughtFor, ProfitLoss FROM Investment WHERE User_ID=? AND ProfitLoss>0"
        if StartDate:
            sqlSelectStatement += f" AND Date_Added >= '{StartDate}'"

        if EndDate:
            sqlSelectStatement += f" AND Date_Added <= '{EndDate}'"

        sqlDeleteStatement = "DELETE FROM Investment WHERE User_ID=? AND ProfitLoss>0"
        if StartDate:
            sqlDeleteStatement += f" AND Date_Added >= '{StartDate}'"

        if EndDate:
            sqlDeleteStatement += f" AND Date_Added <= '{EndDate}'"

        self.__SetUpConnection()
        self.c.execute(sql, (self.Profile,))
        Values = self.c.fetchall()
        self.c.execute(sqlCount, (self.Profile,))
        RecordsAffected = self.c.fetchone()[0]
        # calculate total profit
        # profitloss/100 * bought for
        self.c.execute(sqlProfitLoss,
                       (self.Profile,))
        TotalProfit = self.c.fetchone()[0]
        if TotalProfit is None:
            return
        self.c.execute(sqlSumBoughtFor,
                       (self.Profile,))
        TotalCost = self.c.fetchone()[0]
        from Database import User
        User = User.User()
        User.SelectProfile(self.Profile)
        User.addMoney(TotalProfit + TotalCost, LogChanges=False)
        print("Total Profit:" + str(TotalProfit))
        self.c.execute(
            sqlSelectStatement,
            (self.Profile,))
        values = self.c.fetchall()
        for i in range(len(values)):
            values[i] = values[i] + (Date,)
        print(values)
        self.c.executemany('''
                    INSERT INTO Statement(Investment_ID, User_ID , Gold, Purity, BoughtFor, ProfitLoss,Date_Added) 
                    VALUES (?,?,?,?,?,?,?)  
                  ''', values)
        self.c.execute(sqlDeleteStatement, (self.Profile,))
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
    def sellAll(self, LogChanges=True, Rate=None, Date=None, StartDate=None, EndDate=None):
        # only apply rate to what is going to be sold.
        if Rate is not None:
            # if connected to a thread this might not work all the time.

            # maybe use investment id to update specific records only.
            self.updateProfitLoss(Rate)
        self.__SetUpConnection()
        sql = "SELECT * FROM Investment WHERE User_ID = ?"
        if StartDate:
            sql += f" AND Date_Added >= '{StartDate}'"

        if EndDate:
            sql += f" AND Date_Added <= '{EndDate}'"

        sqlCount = "SELECT COUNT(*) FROM Investment WHERE User_ID = ?"
        if StartDate:
            sqlCount += f" AND Date_Added >= '{StartDate}'"

        if EndDate:
            sqlCount += f" AND Date_Added <= '{EndDate}'"

        sqlProfitLoss = "SELECT SUM((ProfitLoss/100)*BoughtFor) FROM Investment WHERE User_ID=?"
        if StartDate:
            sqlProfitLoss += f" AND Date_Added >= '{StartDate}'"

        if EndDate:
            sqlProfitLoss += f" AND Date_Added <= '{EndDate}'"

        sqlSumBoughtFor = "SELECT SUM(BoughtFor) FROM Investment WHERE User_ID=?"
        if StartDate:
            sqlSumBoughtFor += f" AND Date_Added >= '{StartDate}'"

        if EndDate:
            sqlSumBoughtFor += f" AND Date_Added <= '{EndDate}'"

        sqlSelectStatement = "SELECT Investment_ID, User_ID , Gold, Purity, BoughtFor, ProfitLoss FROM Investment WHERE User_ID=?"
        if StartDate:
            sqlSelectStatement += f" AND Date_Added >= '{StartDate}'"

        if EndDate:
            sqlSelectStatement += f" AND Date_Added <= '{EndDate}'"

        sqlDeleteStatement = "DELETE FROM Investment WHERE User_ID=?"
        if StartDate:
            sqlDeleteStatement += f" AND Date_Added >= '{StartDate}'"

        if EndDate:
            sqlDeleteStatement += f" AND Date_Added <= '{EndDate}'"

        self.c.execute(sql, (self.Profile,))
        Values = self.c.fetchall()
        self.c.execute(sqlCount, (self.Profile,))
        RecordsAffected = self.c.fetchone()[0]
        # calculate total profit
        # profitloss/100 * bought for
        self.c.execute(sqlProfitLoss,
                       (self.Profile,))
        TotalProfit = self.c.fetchone()[0]
        if TotalProfit is None:
            return
        self.c.execute(sqlSumBoughtFor,
                       (self.Profile,))
        TotalCost = self.c.fetchone()[0]
        from Database import User
        User = User.User()
        User.SelectProfile(self.Profile)
        User.addMoney(TotalProfit + TotalCost, LogChanges=False)
        print("Total Profit:" + str(TotalProfit))
        self.c.execute(
            sqlSelectStatement,
            (self.Profile,))
        values = self.c.fetchall()
        for i in range(len(values)):
            values[i] = values[i] + (Date,)
        print(values)
        self.c.executemany('''
                    INSERT INTO Statement(Investment_ID, User_ID , Gold, Purity, BoughtFor, ProfitLoss,Date_Added) 
                    VALUES (?,?,?,?,?,?,?)  
                  ''', values)
        self.c.execute(sqlDeleteStatement, (self.Profile,))
        self.conn.commit()
        if LogChanges is True:
            Transaction_ID = generateTransactionID()
            self.__LogSellAll(RecordsAffected, Values, Transaction_ID)
            print("hmmm")
            self.MoneyLog.insertIntoTable(self.Profile, DB_Code.ProfitLoss, TotalProfit, Transaction_ID=Transaction_ID,
                                          TradeCost=TotalCost)
        self.conn.close()

    # # add user here
    # def sellAll(self, LogChanges=True, Date=None, Rate=None):
    #     if Rate is not None:
    #         self.updateProfitLoss(Rate)
    #     self.__SetUpConnection()
    #     if Date is None:
    #         Date = datetime.now().date()
    #     self.c.execute('''SELECT MIN(Date_Added) FROM Investment WHERE User_ID= ?''', (self.Profile,))
    #     minimum_date = self.c.fetchone()[0]
    #     print(minimum_date)
    #     if minimum_date is not None and datetime.strptime(str(Date), '%Y-%m-%d').date() < datetime.strptime(
    #             minimum_date, '%Y-%m-%d').date():
    #         print("------------")
    #         print("invalid")
    #         print("------------")
    #         return
    #
    #     #
    #     #     Values = self.c.fetchall()
    #     #     if  > datetime.now().date():
    #     #         print("date is in future")
    #     #         return
    #
    #     self.c.execute('''SELECT * FROM Investment WHERE User_ID= ?''', (self.Profile,))
    #     Values = self.c.fetchall()
    #     self.c.execute('''SELECT COUNT(*) FROM Investment WHERE User_ID= ?''', (self.Profile,))
    #     RecordsAffected = self.c.fetchone()[0]
    #
    #     # calculate total profit
    #     # profitloss/100 * bought for
    #     self.c.execute('''SELECT SUM((ProfitLoss/100)*BoughtFor) FROM Investment WHERE (User_ID=? AND ProfitLoss>=0)''',
    #                    (self.Profile,))
    #     TotalPositiveProfit = self.c.fetchone()[0]
    #     self.c.execute(
    #         '''SELECT SUM((ProfitLoss/100)*BoughtFor) FROM Investment WHERE (User_ID=? AND ProfitLoss<0)''',
    #         (self.Profile,))
    #     TotalNegativeProfit = self.c.fetchone()[0]
    #     print("-" + str(TotalNegativeProfit))
    #     print("+" + str(TotalPositiveProfit))
    #
    #     self.c.execute('''SELECT SUM(BoughtFor) FROM Investment WHERE (User_ID=?)''',
    #                    (self.Profile,))
    #     TotalCost = self.c.fetchone()[0]
    #     if TotalCost is None:
    #         TotalCost = 0
    #
    #     print(TotalCost)
    #
    #     from Database import User
    #     User = User.User()
    #     User.SelectProfile(self.Profile)
    #     if TotalPositiveProfit is None:
    #         TotalPositiveProfit = 0
    #     if TotalNegativeProfit is None:
    #         TotalNegativeProfit = 0
    #         print(TotalPositiveProfit + TotalNegativeProfit)
    #     User.addMoney((TotalPositiveProfit + TotalNegativeProfit + TotalCost), LogChanges=False)
    #
    #     self.c.execute('''
    #                 INSERT INTO Statement(Investment_ID,User_ID,Gold,Purity,BoughtFor,ProfitLoss) SELECT Investment_ID,User_ID,Gold,Purity,BoughtFor,ProfitLoss FROM Investment WHERE User_ID= ?
    #               ''', (self.Profile,))
    #     self.c.execute('''
    #                 DELETE FROM Investment WHERE User_ID=?
    #               ''', (self.Profile,))
    #     self.conn.commit()
    #     self.conn.close()
    #     if RecordsAffected > 0 and LogChanges is True:
    #         Transaction_ID = generateTransactionID()
    #         self.__LogSellAll(RecordsAffected, Values, Transaction_ID)
    #         self.MoneyLog.insertIntoTable(self.Profile, DB_Code.ProfitLoss, (TotalPositiveProfit + TotalNegativeProfit),
    #                                       Transaction_ID=Transaction_ID, TradeCost=TotalCost)

    def __LogSellAll(self, RecordsAffected, Values, id):
        self.Log.insert(id, DB_Code.ISA)
        self.InvestmentLog.SellAllStatement(id, RecordsAffected, self.Profile)
        self.InvestmentArchive.Archive(Values)

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
            date = datetime.strptime(date, format_str)
            sum_of_values = self.c.fetchone()[0]
            dictionary[date] = sum_of_values
        print(dictionary)

        # close database connection
        self.conn.close()
        return dictionary

    def add_to_dict(self, dictionary, key, value):
        dictionary[key] = value
        return dictionary

    def convertToExcel(self):
        DBFunctions.convertToExcel("Investment", SetUpFile.DBName)

    def sell(self, uniqueID, Rate=None, Date=None):
        if len(uniqueID) == 0:
            return
        # instead of total sum, use profit
        self.TotalProfitLoss = 0
        self.TotalSum = 0
        print(len(uniqueID))
        from Database import User
        User = User.User()
        for id in uniqueID:
            self.sellIndividual(id, Rate=Rate, Date=Date)
        Transaction_ID = generateTransactionID()
        self.LogForDelete(Transaction_ID, len(uniqueID), self.Profile)
        # print(self.TotalSum)
        User.SelectProfile(self.Profile)
        self.MoneyLog.insertIntoTable(self.Profile, DB_Code.ProfitLoss, self.TotalProfitLoss,
                                      Transaction_ID=Transaction_ID,
                                      TradeCost=self.TotalSum)
        User.addMoney(self.TotalSum + self.TotalProfitLoss, LogChanges=False)

    def sellIndividual(self, id, Rate=None, Date=None):
        if Rate is not None:
            self.updateProfitLoss(Rate, Investment_ID=id)
        self.__SetUpConnection()
        try:
            self.c.execute("SELECT * FROM Investment WHERE Investment_ID = ?", (id,))
            Values = self.c.fetchone()
            self.c.execute("SELECT BoughtFor FROM Investment WHERE Investment_ID = ?", (id,))
            BoughtFor = self.c.fetchone()[0]
            self.c.execute("SELECT ((ProfitLoss/100)*BoughtFor) FROM Investment WHERE Investment_ID = ?", (id,))
            ProfitLoss = self.c.fetchone()[0]
            self.TotalProfitLoss += ProfitLoss
            self.TotalSum += BoughtFor
            print("---")
            print("---")
            a = [Values]
            self.InvestmentArchive.Archive(a)
            sql = "DELETE FROM Investment WHERE Investment_ID =?"
            self.c.execute(sql, (id,))
            self.conn.commit()
            self.Statement.setProfile(Values[2])
            print(Date)
            self.Statement.addIntoTable(Values[3], Values[4], Values[5], Values[6], Transaction_ID=Values[0],
                                        Date=Date.strftime("%Y-%m-%d"))
            print(Date)
        except sqlite3.Error as error:
            print(error)
        finally:
            self.conn.close()

    def getSumBoughtFor(self):
        self.__SetUpConnection()
        self.c.execute("SELECT SUM(BoughtFor) FROM Investment WHERE User_ID =?", (self.Profile,))
        Sum = self.c.fetchone()[0]
        self.conn.close()
        if Sum is None:
            Sum = 0
        return Sum

    def getTotalGold(self):
        self.__SetUpConnection()
        self.c.execute("SELECT SUM(Gold) FROM Investment WHERE User_ID =?", (self.Profile,))
        Sum = self.c.fetchone()[0]
        self.conn.close()
        if Sum is None:
            Sum = 0
        return Sum
