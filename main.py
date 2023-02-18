from User import User
from Investment import Investment
from ProfitLoss import Statement
from Log import Log
from InvestmentLog import InvestmentLog
from UserLog import UserLog

from UserArchive import UserArchive
from InvestmentArchive import InvestmentArchive


def ClearArchive():
    global UserArchive, InvestmentArchive
    UserArchive = UserArchive()
    UserArchive.dropTable()
    InvestmentArchive = InvestmentArchive()
    InvestmentArchive.dropTable()


def ClearLog():
    global Log, InvestmentLog, UserLog
    Log = Log()
    InvestmentLog = InvestmentLog()
    UserLog = UserLog()
    Log.dropTable()
    InvestmentLog.dropTable()
    UserLog.dropTable()


ClearArchive()
ClearLog()

# start temp db to store commands that are run. so we can backtrack if needed.
Statement = Statement()
Statement.deleteTable()
Statement.createTable()
Statement.showStatement()

User = User()
User.deleteTable()
User.createTable()
User.insertIntoTable("Muhammad", "Abubakar", 100)
User.insertIntoTable("Kanishka", "Jay", 10)
User.insertIntoTable("Kabubakar", "J", 1)
User.updateRecord("ma",1)
User.deleteRecord("kj1")
import time
time.sleep(1)
User.deleteRecord("ma")
User.showTable()

Investment = Investment()
Investment.deleteTable()
Investment.createTable()

# code to show help
# print(Investment.insertIntoTable.__doc__)
Investment.setProfile("ma")
Investment.insertIntoTable(123, 21, 123)
Investment.insertIntoTable(21, 1, 1)
Investment.insertIntoTable(1000, 21, 20)
Investment.insertIntoTable(1, 21, 12)
Investment.insertIntoTable(1, 21, 21)
Investment.setProfile("kj")
Investment.insertIntoTable(123, 21, 21)
Investment.insertIntoTable(1, 21, 40)

# import time
# time.sleep(3)
# User.deleteRecord("ma")
# User.deleteRecord("ma")
# Investment.deleteRecord("ma")

# User.deleteRecord("ma")
# User.deleteRecord("kj")
# Investment.showTable()
Investment.updateProfitLoss(12)
Investment.setProfile("ma")
User.showTable()

Investment.setProfile("ma")
Investment.sellAll()
print("------------------")
# Investment.showProfit()
Investment.sellAll()
Statement.setProfile("kj")
Statement.showStatement()
print("------------------")


def previousStage(num):
    for i in range(0, num):
        Log.previousStage()


# previousStage(14)

# Investment.showLoss()
