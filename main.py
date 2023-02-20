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

timer = 2
User.insertIntoTable("Muhammad", "Abubakar", 100)
time.sleep(timer)
User.updateRecord("ma", 20)
time.sleep(timer)
User.updateRecord("ma", 50)
time.sleep(timer)
Investment.setProfile("ma")

Investment.insertIntoTable(123, 123, 123)
time.sleep(timer)
Investment.insertIntoTable(12, 123, 23)
time.sleep(timer)
Investment.insertIntoTable(123, 3, 123)
time.sleep(timer)
User.deleteRecord("ma")
time.sleep(timer)
User.insertIntoTable("Ali", "Baba", 1)
time.sleep(timer)

Investment.setProfile("ab")
time.sleep(timer)

Investment.insertIntoTable(123, 123, 150)
time.sleep(timer)
Investment.insertIntoTable(12, 123, 23)
time.sleep(timer)
Investment.insertIntoTable(123, 3, 123)
time.sleep(timer)

Investment.updateProfitLoss(1.5)
time.sleep(timer)

Investment.sellProfit()
time.sleep(timer)
User.insertIntoTable("m", "s", 90)
time.sleep(timer)
User.deleteRecord("ms")
time.sleep(timer)



def previousStage(num):
    for i in range(0, num):
        Log.previousStage()


previousStage(12)

# when deleting user app crashes
