import sqlite3
import uuid

import SetUpFile


def generateTransactionID():
    return str(uuid.uuid4())


class UserArchive:
    def __init__(self):
        self.c = None
        self.conn = None
        self.__createTable()

    def SetUpConnection(self):
        """Get the setup connection."""
        self.conn = sqlite3.connect(SetUpFile.DBArchiveName)
        self.c = self.conn.cursor()

    def __createTable(self):
        self.SetUpConnection()
        self.c.execute('''
              CREATE TABLE IF NOT EXISTS ArchiveUser
              ([Transaction_ID] VARCHAR PRIMARY KEY,[ActionType] TEXT,[User_ID] VARCHAR , [FirstName] TEXT , [LastName] TEXT, [Money] REAL,[time_stamp] TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
              ''')
        self.conn.commit()
        self.conn.close()

    def Archive(self, Action, Values):
        """Take the action type and the record values in the form of UserArchive tuple."""
        Values[0] = (generateTransactionID(), Action,) + Values[0]
        self.SetUpConnection()
        try:
            self.c.executemany(
                "INSERT INTO ArchiveUser(Transaction_ID,ActionType,User_ID, FirstName, LastName, Money) VALUES(?,?,?,?,?,?)",
                Values)

            self.conn.commit()
        except sqlite3.Error as error:
            print(error)
        finally:
            self.conn.close()

    def dropTable(self):
        """Delete all data in the archive."""
        self.SetUpConnection()
        try:
            self.c.execute("DELETE FROM ArchiveUser")
            self.conn.commit()
        except sqlite3.Error as error:
            print(error)
        finally:
            self.conn.close()

    def getData(self, User_ID=None):
        """Function to get record data, if no user id specified then returns the latest record otherwise it returns
        the record with the corresponding user id. """
        self.SetUpConnection()

        if User_ID is None:
            self.c.execute("SELECT COUNT(*) FROM ArchiveUser")
            Count = self.c.fetchone()[0]
        else:
            self.c.execute("SELECT COUNT(*) FROM ArchiveUser WHERE User_ID = ?", (User_ID,))
            Count = self.c.fetchone()[0]
        print(Count)

        # if User_ID is None:
        #     self.c.execute("SELECT * FROM ArchiveUser LIMIT 1 OFFSET ?", (Count - 1,))
        # else:
        #     self.c.execute("SELECT * FROM ArchiveUser WHERE User_ID = ? LIMIT 1 OFFSET ?", (User_ID, Count - 1,))
        #     print(self.c.fetchone())

        # self.c.execute("SELECT * FROM ArchiveUser WHERE time_stamp = (SELECT MAX(time_stamp) FROM ArchiveUser)")
        self.c.execute("SELECT * FROM ArchiveUser WHERE User_ID =? ORDER BY time_stamp DESC LIMIT 1", (User_ID,))
        Data = self.c.fetchone()
        print("____________________________")
        print(Data)
        print("____________________________")
        #     DESC, ROWID
        # ASC
        self.c.execute(
            "DELETE FROM ArchiveUser WHERE Transaction_ID = (SELECT Transaction_ID FROM ArchiveUser WHERE User_ID =? ORDER BY time_stamp DESC LIMIT 1)",
            (User_ID,))

        self.conn.commit()
        self.conn.close()
        return Data


class InvestmentArchive:
    def __init__(self):
        self.c = None
        self.conn = None
        self.__createTable()

    def __SetUpConnection(self):
        self.conn = sqlite3.connect(SetUpFile.DBArchiveName)
        self.c = self.conn.cursor()

    def __createTable(self):
        self.__SetUpConnection()
        self.c.execute('''
              CREATE TABLE IF NOT EXISTS ArchiveInvestment                                                         
              ([Investment_ID] VARCHAR ,[Date_added] DATE,[User_ID] VARCHAR, [Gold] Real , [Purity] Real, [BoughtFor] REAL,[ProfitLoss] Real,[deleted_at] TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
              ''')
        self.conn.commit()
        self.conn.close()

    def Archive(self, Values):
        """Takes value of investment to archive."""
        self.__SetUpConnection()
        try:
            self.c.executemany(
                "INSERT INTO ArchiveInvestment(Investment_ID,Date_added,User_ID, Gold, Purity, BoughtFor,ProfitLoss) VALUES(?,?,?,?,?,?,?)",
                Values)
            self.conn.commit()
        except sqlite3.Error as error:
            print(error)
        finally:
            self.conn.close()

    def dropTable(self):
        self.__SetUpConnection()
        try:
            print("Archive Investment deleted")
            self.c.execute("DELETE FROM ArchiveInvestment")
            self.conn.commit()
        except sqlite3.Error as error:
            print(error)
        finally:
            self.conn.close()

    def getData(self, User_ID, Investment_ID=None):
        """Takes user id to get archive investment for the user and investment id can also be used to get specific
        record data. """
        self.__SetUpConnection()


        self.c.execute("SELECT * FROM ArchiveInvestment WHERE User_ID =? ORDER BY deleted_at DESC LIMIT 1", (User_ID,))
        Data = self.c.fetchone()
        print("____________________________")
        print(Data)
        print("____________________________")
        #     DESC, ROWID
        # ASC
        self.c.execute(
            "DELETE FROM ArchiveInvestment WHERE Investment_ID = (SELECT Investment_ID FROM ArchiveInvestment WHERE User_ID =? ORDER BY deleted_at DESC LIMIT 1)",
            (User_ID,))


        self.conn.commit()
        self.conn.close()
        return Data


