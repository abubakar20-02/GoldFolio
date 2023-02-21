import sqlite3
import pandas as pd
import SetUpFile


class Statement:
    def __init__(self):
        super().__init__()
        self.c = None
        self.conn = None
        self.Profile = None

    def setProfile(self, user):
        self.Profile = user

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
