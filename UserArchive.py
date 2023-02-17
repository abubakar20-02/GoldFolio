import sqlite3
import SetUpFile


class UserArchive:
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
              CREATE TABLE IF NOT EXISTS ArchiveUser
              ([User_ID] VARCHAR PRIMARY KEY, [FirstName] TEXT , [LastName] TEXT, [Money] REAL,[deleted_at] TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
              ''')
        self.conn.commit()
        self.conn.close()

    def Archive(self, Values):
        self.SetUpConnection()
        try:

            self.c.executemany("INSERT INTO ArchiveUser(User_ID, FirstName, LastName, Money) VALUES(?,?,?,?)", Values)
            self.conn.commit()
        except sqlite3.Error as error:
            print(error)
        finally:
            self.conn.close()
