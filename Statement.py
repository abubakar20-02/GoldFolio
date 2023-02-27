import math
import sqlite3
import uuid
from datetime import datetime, timedelta
import calendar
from time import strftime

import pandas as pd

import DBFunctions
import SetUpFile


class Statement:
    def __init__(self):
        super().__init__()
        self.c = None
        self.conn = None
        self.Profile = None

    def setProfile(self, user):
        self.Profile = user

    # can't handle empty lines at the moment
    def ImportFromExcel(self):
        # source = 'UserTemplate.xlsx'
        target = 'Statement.xlsx'
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
        table_name = "Statement"
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
                    values[3]) and self.CorrectNumberFormat(values[4]) and self.CorrectNumberFormat(values[5])):
                continue

            # if it reaches here, then user is in the list, so we can set profile.
            self.setProfile(values[1])

            # self, InvestmentId, Date_added, UserID, Gold, Purity, BoughtFor

            # checks if time is none or date is empty.
            if isinstance(values[0], datetime) and values[0] is pd.NaT or self.isEmpty(values[0]):
                self.addIntoTable(values[2], values[3], values[4], values[5])
            else:
                if isinstance(values[0], datetime):
                    # if date is in the future then don't add it.
                    # if datetime.strptime(values[0].strftime("%Y-%m-%d"), '%Y-%m-%d').date() > datetime.now().date():
                    #     print("future")
                    #     continue
                    # convert date to Y-m-d format
                    self.addIntoTable(values[2], values[3], values[4], values[5], Date=values[0].strftime("%Y-%m-%d"))

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

    # __ makes the method private
    def __SetUpConnection(self):
        self.conn = sqlite3.connect(SetUpFile.DBName)
        self.c = self.conn.cursor()

    def createTable(self):
        self.__SetUpConnection()
        self.c.execute('''
              CREATE TABLE IF NOT EXISTS Statement
              ([Investment_ID] VARCHAR PRIMARY KEY, [Date_added] DATE DEFAULT CURRENT_DATE ,[User_ID] VARCHAR,[Gold] REAL ,[Purity] REAL, [BoughtFor] REAL, [ProfitLoss] REAL,
              FOREIGN KEY(User_ID) REFERENCES User(User_ID))
              ''')
        self.conn.commit()
        self.conn.close()

    def addIntoTable(self, Gold, Purity, BoughtFor, ProfitLoss, Transaction_ID=None, Date=None):
        """Takes in the investmentID , User ID, Gold in grams, Purity and the total price bought for"""
        self.__SetUpConnection()
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
                Transaction_ID = str(uuid.uuid4())
            try:
                self.c.execute('''
                      INSERT INTO Statement (Investment_ID,Date_Added, User_ID , Gold, Purity, BoughtFor, ProfitLoss)

                            VALUES
                            (?,?,?,?,?,?,?)
                      ''', (Transaction_ID, Date, self.Profile, Gold, Purity, BoughtFor, ProfitLoss))
            except sqlite3.Error as error:
                print(error)
                Error = True
        self.conn.commit()
        self.conn.close()

    def deleteTable(self):
        self.__SetUpConnection()
        # Disable foreign key constraints
        self.c.execute("PRAGMA foreign_keys = OFF")
        try:
            self.c.execute("DROP TABLE Statement")
            self.conn.commit()
        except sqlite3.Error as error:
            print(error)
        finally:
            # Enable foreign key constraints
            self.c.execute("PRAGMA foreign_keys = ON")
            self.conn.close()

    def insertIntoTable(self, InvestmentId, Date_added, UserID, Gold, Purity, BoughtFor):
        """Takes in the investmentID , User ID, Gold in grams, Purity and the total price bought for"""
        self.__SetUpConnection()
        try:
            self.c.execute('''
                  INSERT INTO Investment (Investment_ID,Date_added, User_ID , Gold, Purity, BoughtFor, ProfitLoss)

                        VALUES
                        (?,?,?,?,?,?)
                  ''', (InvestmentId, Date_added, UserID, Gold, Purity, BoughtFor, 0.00))
            self.conn.commit()
        except sqlite3.Error as error:
            print(error)
        finally:
            self.conn.close()

    def showStatement(self):
        self.__SetUpConnection()
        self.c.execute('''
                    SELECT * FROM Statement WHERE User_ID = ?
                  ''', (self.Profile,))
        self.conn.commit()
        df = pd.DataFrame(self.c.fetchall(),
                          columns=['Investment_ID', 'User_ID', 'Gold', 'Purity', 'BoughtFor', 'ProfitLoss'])
        print(df)
        self.conn.close()

    def getData(self, User_ID, *Investment_ID):
        """Takes in user id to show statement and it can also take investment id to get record for the investment id"""
        self.__SetUpConnection()
        Data = None
        self.c.execute("SELECT COUNT(*) FROM Statement WHERE User_ID = ?", (User_ID,))
        Count = self.c.fetchone()[0]
        print(Count)
        if Count > 0:
            if not Investment_ID:
                self.c.execute("SELECT * FROM Statement WHERE User_ID = ? LIMIT 1 OFFSET ?",
                               (User_ID, Count - 1,))
            else:
                self.c.execute(
                    "SELECT * FROM Statement WHERE Investment_ID = ? AND User_ID = ? LIMIT 1 OFFSET ?",
                    (Investment_ID, User_ID, Count - 1,))
            Data = self.c.fetchone()
            if not Investment_ID:
                # needs id to delete, its fine as id is primary key and unique.
                self.c.execute(
                    "DELETE FROM Statement WHERE Investment_ID IN (SELECT Investment_ID FROM Statement WHERE User_ID = ? LIMIT 1 OFFSET ?)",
                    (User_ID, Count - 1,))
            else:
                self.c.execute(
                    "DELETE FROM Statement WHERE (SELECT * FROM Statement WHERE User_ID = ? LIMIT 1 OFFSET ?)",
                    (User_ID, Count - 1,))

        self.conn.commit()
        self.conn.close()
        return Data

    def convertToExcel(self):
        DBFunctions.convertToExcel("Statement", SetUpFile.DBName)

    def traverse_all_dates(self, ColumnName, StartDate=None, EndDate=None, Preset=None, Mode=None):
        # connect to database
        dictionary = {}
        self.__SetUpConnection()
        # idk why substract 2

        if Preset == "Month":
            EndDate = datetime.now().date()
            StartDate = EndDate - timedelta(
                days=(calendar.monthrange(datetime.now().year, datetime.now().month)[1]) - 2)
        if Preset == "Week":
            EndDate = datetime.now().date()
            StartDate = EndDate - timedelta(days=5)
        if Preset == "2Week":
            EndDate = datetime.now().date()
            StartDate = EndDate - timedelta(days=12)

        sql = "SELECT SUM({0}) FROM Statement WHERE Date_Added = ?".format(ColumnName)

        sql1 = "SELECT DISTINCT Date_Added FROM Statement WHERE 1=1"

        if StartDate:
            # idk why I have to do this.
            StartDate = StartDate - timedelta(days=1)
            sql1 += f" AND Date_Added >= '{StartDate}'"

        if EndDate:
            sql1 += f" AND Date_Added <= '{EndDate}'"

        sql1 += f" ORDER BY Date_Added ASC"

        print(sql1)

        # execute SQL query to get all dates
        self.c.execute(sql1)
        if Mode is None:
            if StartDate and EndDate:
                date = StartDate
                while date <= EndDate:
                    dictionary[date] = 0
                    date += timedelta(days=1)

        dates = []
        date = StartDate
        while date <= EndDate:
            dates.append(date)
            date += timedelta(days=1)

        print(dates)
        # loop through dates and print the sum of values for each date
        sum = 0
        for date in dates:
            # format_str = '%Y-%m-%d'
            # date = datetime.strptime(date, format_str)
            self.c.execute(sql, (date,))
            sum_of_values = self.c.fetchone()[0]
            if sum_of_values is None:
                sum_of_values = 0
            sum += sum_of_values
            if Mode is None:
                dictionary[date] = sum_of_values
            else:
                dictionary[date] = sum

        # close database connection
        self.conn.close()
        return dictionary

    def trial(self, ColumnName, Start=None, End=None):
        self.__SetUpConnection()
        sql = (
            "SELECT strftime('%Y-%m', Date_Added) AS month, SUM({0}) AS total_value FROM Statement WHERE 1=1").format(
            ColumnName)
        if Start:
            # idk why I have to do this.
            sql += f" AND Date_Added >= '{Start.strftime('%Y-%m')}'"

        if End:
            sql += f" AND Date_Added <= '{End.strftime('%Y-%m')}'"

        sql += f"GROUP BY month"

        if Start and End:
            monthlydict = self.generate_monthly_dict(Start, End)

        print(sql)

        self.c.execute(sql)

        for rows in self.c.fetchall():
            month, sum = rows
            monthlydict[month] = sum

        print("----")
        print(monthlydict)
        print("----")

        self.conn.close()
        return monthlydict

    def trial1(self, ColumnName, Start=None, End=None):
        self.__SetUpConnection()
        sql = (
            "SELECT strftime('%Y', Date_Added) AS year, SUM({0}) AS total_value FROM Statement WHERE 1=1").format(
            ColumnName)
        if Start:
            # idk why I have to do this.
            sql += f" AND Date_Added >= '{Start.strftime('%Y-%m-%d')}'"

        if End:
            sql += f" AND Date_Added <= '{End.strftime('%Y-%m-%d')}'"

        sql += f"GROUP BY year"

        if Start and End:
            yearlydict = self.generate_yearly_dict(Start, End)

        print(sql)

        self.c.execute(sql)

        for rows in self.c.fetchall():
            year, sum = rows
            print(type(year))
            yearlydict[datetime.strptime(year, '%Y').year] = sum

        print("----")
        print(yearlydict)
        print("----")

        self.conn.close()
        return yearlydict

    def generate_monthly_dict(self, start_date, end_date):
        result = {}
        current_date = start_date.replace(day=1)
        while current_date <= end_date:
            result[current_date.strftime('%Y-%m')] = 0
            current_date += timedelta(days=32)
            current_date = current_date.replace(day=1)
        print(result)
        return result

    def generate_yearly_dict(self, start_date, end_date):
        result = {}
        for year in range(start_date.year, end_date.year + 1):
            result[year] = 0
        print(result)
        return result

    def add_to_dict(self, dictionary, key, value):
        dictionary[key] = value
        return dictionary
