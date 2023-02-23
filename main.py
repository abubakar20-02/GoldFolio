import sqlite3
import time

import SetUpFile
from User import User
from Investment import Investment
from Statement import Statement
from Log import Log

from Archive import UserArchive
from Archive import InvestmentArchive

UserArchive = UserArchive()
InvestmentArchive = InvestmentArchive()
Log = Log()


def ClearArchive():
    UserArchive.dropTable()
    InvestmentArchive.dropTable()


def method_name():
    Log.dropTable()
    ClearArchive()


def saveSnapshot():
    # take snapshot before importing files.
    conn = sqlite3.connect(SetUpFile.DBName)

    # Create a file object to store the snapshot
    snapshot_file = sqlite3.connect(SetUpFile.Snap_DB)

    # Take a snapshot of the database
    conn.backup(snapshot_file)

    # Close the file object and the database connection
    snapshot_file.close()
    conn.close()

    conn = sqlite3.connect(SetUpFile.DBArchiveName)

    # Create a file object to store the snapshot
    snapshot_file = sqlite3.connect(SetUpFile.Snap_Archive)

    # Take a snapshot of the database
    conn.backup(snapshot_file)

    # Close the file object and the database connection
    snapshot_file.close()
    conn.close()

    conn = sqlite3.connect(SetUpFile.DBLog)

    # Create a file object to store the snapshot
    snapshot_file = sqlite3.connect(SetUpFile.Snap_DBLog)

    # Take a snapshot of the database
    conn.backup(snapshot_file)

    # Close the file object and the database connection
    snapshot_file.close()
    conn.close()


method_name()

# start temp db to store commands that are run. so we can backtrack if needed.
Statement = Statement()
Statement.deleteTable()
Statement.createTable()
Statement.showStatement()

Investment = Investment()
Investment.deleteTable()
Investment.createTable()

User = User()
User.deleteTable(False)
User.createTable()
# User.ImportFromExcel()

timer = 1
User.insertIntoTable("Muhammad", "Abubakar", 201)
User.SelectProfile("ma")
User.addMoney(1000)
# User.cashout(301)
# Investment.ImportFromExcel()
# Statement.ImportFromExcel()

# time.sleep(timer)
# User.insertIntoTable("Hamza", "Rizwan", 100)
# time.sleep(timer)
# User.updateRecord("ma", 20)
# time.sleep(timer)
# User.updateRecord("ma", 50)
# time.sleep(timer)
Investment.setProfile("ma")
#
Investment.insertIntoTable(1, 123, 100)
Investment.insertIntoTable(1, 123, 100)
Investment.insertIntoTable(5, 123, 20)
Investment.sellAll(Rate=10)
time.sleep(timer)
User.insertIntoTable("Hamza", "Rizwan", 1000)
Investment.setProfile("hr")
Investment.insertIntoTable(10, 1, 10)
Investment.sellAll(Rate=10)

# saveSnapshot()


def previousStage(num):
    for i in range(0, num):
        Log.previousStage()


previousStage(1)

# when deleting user app crashes
