import sqlite3
import SetUpFile


class InvestmentArchive:
    def __init__(self):
        self.c = None
        self.conn = None
        self.__createTable()

    def SetUpConnection(self):
        self.conn = sqlite3.connect(SetUpFile.DBArchiveName)
        self.c = self.conn.cursor()

    def __createTable(self):
        self.SetUpConnection()
        self.c.execute('''
              CREATE TABLE IF NOT EXISTS ArchiveInvestment                                                         
              ([Investment_ID] VARCHAR PRIMARY KEY,[User_ID] VARCHAR, [Gold] Real , [Purity] Real, [BoughtFor] REAL,[ProfitLoss] Real,[deleted_at] TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
              ''')
        self.conn.commit()
        self.conn.close()

    def Archive(self, Values):
        self.SetUpConnection()
        try:

            self.c.executemany(
                "INSERT INTO ArchiveInvestment(Investment_ID,User_ID, Gold, Purity, BoughtFor,ProfitLoss) VALUES(?,?,?,?,?,?)",
                Values)
            self.conn.commit()
        except sqlite3.Error as error:
            print(error)
        finally:
            self.conn.close()

    def dropTable(self):
        self.SetUpConnection()
        try:
            self.c.execute("DROP TABLE ArchiveInvestment")
            self.conn.commit()
        except sqlite3.Error as error:
            print(error)
        finally:
            self.conn.close()

    def getData(self, *Investment_ID):
        self.SetUpConnection()
        self.c.execute("SELECT COUNT(*) FROM ArchiveInvestment")
        Count = self.c.fetchone()[0]
        print(Count)

        if not Investment_ID:
            self.c.execute("SELECT * FROM ArchiveInvestment LIMIT 1 OFFSET ?", (Count - 1,))
        else:
            self.c.execute("SELECT * FROM ArchiveInvestment WHERE Investment_ID = ? LIMIT 1 OFFSET ?", (Investment_ID, Count - 1,))
        Data = self.c.fetchone()
        if not Investment_ID:
            # needs id to delete, its fine as id is primary key and unique.
            self.c.execute(
                "DELETE FROM ArchiveInvestment WHERE Investment_ID IN (SELECT Investment_ID FROM ArchiveInvestment LIMIT 1 OFFSET ?)",
                (Count - 1,))
        else:
            self.c.execute(
                "DELETE FROM ArchiveUser WHERE (SELECT * FROM ArchiveInvestment WHERE User_ID = ? LIMIT 1 OFFSET ?)",
                (Investment_ID, Count - 1,))

        self.conn.commit()
        self.conn.close()
        return Data
