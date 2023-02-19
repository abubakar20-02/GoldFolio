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
              ([ActionType] TEXT,[User_ID] VARCHAR , [FirstName] TEXT , [LastName] TEXT, [Money] REAL,[time_stamp] TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
              ''')
        self.conn.commit()
        self.conn.close()

    def Archive(self, Action, Values):
        Values[0] = (Action,) + Values[0]
        self.SetUpConnection()
        try:
            self.c.executemany(
                "INSERT INTO ArchiveUser(ActionType,User_ID, FirstName, LastName, Money) VALUES(?,?,?,?,?)",
                Values)

            self.conn.commit()
        except sqlite3.Error as error:
            print(error)
        finally:
            self.conn.close()

    def dropTable(self):
        self.SetUpConnection()
        try:
            self.c.execute("DROP TABLE ArchiveUser")
            self.conn.commit()
        except sqlite3.Error as error:
            print(error)
        finally:
            self.conn.close()

    def getData(self, *User_ID):
        self.SetUpConnection()
        Data = None
        self.c.execute("SELECT COUNT(*) FROM ArchiveUser")
        Count = self.c.fetchone()[0]
        print(Count)

        if Count > 0:
            if not User_ID:
                self.c.execute("SELECT * FROM ArchiveUser LIMIT 1 OFFSET ?", (Count - 1,))
            else:
                self.c.execute("SELECT * FROM ArchiveUser WHERE User_ID = ? LIMIT 1 OFFSET ?", (User_ID, Count - 1,))
            Data = self.c.fetchone()
            if not User_ID:
                # needs id to delete, its fine as id is primary key and unique.
                self.c.execute(
                    "DELETE FROM ArchiveUser WHERE User_ID IN (SELECT User_ID FROM ArchiveUser LIMIT 1 OFFSET ?)",
                    (Count - 1,))
            else:
                self.c.execute(
                    "DELETE FROM ArchiveUser WHERE (SELECT * FROM ArchiveUser WHERE User_ID = ? LIMIT 1 OFFSET ?)",
                    (User_ID, Count - 1,))

        self.conn.commit()
        self.conn.close()
        return Data
        # return Data
