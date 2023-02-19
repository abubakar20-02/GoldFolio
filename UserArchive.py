import sqlite3
import SetUpFile


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
              ([ActionType] TEXT,[User_ID] VARCHAR , [FirstName] TEXT , [LastName] TEXT, [Money] REAL,[time_stamp] TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
              ''')
        self.conn.commit()
        self.conn.close()

    def Archive(self, Action, Values):
        """Take the action type and the record values in the form of UserArchive tuple."""
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
        """Delete all data in the archive."""
        self.SetUpConnection()
        try:
            self.c.execute("DELETE FROM ArchiveUser")
            self.conn.commit()
        except sqlite3.Error as error:
            print(error)
        finally:
            self.conn.close()

    def getData(self, *User_ID):
        """Function to get record data, if no user id specified then returns the latest record otherwise it returns
        the record with the corresponding user id. """
        self.SetUpConnection()

        self.c.execute("SELECT COUNT(*) FROM ArchiveUser")
        Count = self.c.fetchone()[0]

        if not User_ID:
            self.c.execute("SELECT * FROM ArchiveUser LIMIT 1 OFFSET ?", (Count - 1,))
        else:
            self.c.execute("SELECT * FROM ArchiveUser WHERE User_ID = ? LIMIT 1 OFFSET ?", (User_ID, Count - 1,))

        Data = self.c.fetchone()

        if not User_ID:
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
