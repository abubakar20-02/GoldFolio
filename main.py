import time

from User import User
from Investment import Investment
from Statement import Statement
from Log import Log

from Archive import UserArchive
from Archive import InvestmentArchive


def ClearArchive():
    global UserArchive, InvestmentArchive
    UserArchive = UserArchive()
    UserArchive.dropTable()
    InvestmentArchive = InvestmentArchive()
    InvestmentArchive.dropTable()


Log = Log()
Log.dropTable()
ClearArchive()

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

User.insertIntoTable("Muhammad", "Abubakar", 100)
User.updateRecord("ma", 20)
User.updateRecord("ma", 50)
#
Investment.setProfile("ma")

Investment.insertIntoTable(123, 123, 123)
Investment.insertIntoTable(12, 123, 23)
Investment.insertIntoTable(123, 3, 123)
User.deleteRecord("ma")
User.insertIntoTable("Ali", "Baba", 1)

Investment.setProfile("ab")

Investment.insertIntoTable(123, 123, 123)
Investment.insertIntoTable(12, 123, 23)
Investment.insertIntoTable(123, 3, 123)
User.insertIntoTable("m", "s", 90)
User.deleteRecord("ms")


def previousStage(num):
    for i in range(0, num):
        Log.previousStage()


previousStage(13)

# when deleting user app crashes
