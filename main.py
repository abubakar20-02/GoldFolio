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
Investment.createTable()

User = User()
User.deleteTable(False)
User.createTable()
User.insertIntoTable("Muhammad", "Abubakar", 100)
User.insertIntoTable("Muhammad", "Abu", 69)
User.updateRecord("ma", 1)
User.updateRecord("ma", 2)
# User.deleteRecord("ma")
User.insertIntoTable("Mu", "Abu", 9)

Investment.setProfile("ma")
Investment.insertIntoTable(1,21,100)
Investment.setProfile("ma1")
Investment.insertIntoTable(2,21,100)
Investment.setProfile("ma")
Investment.insertIntoTable(3,21,100)
Investment.updateProfitLoss(10)
User.deleteRecord("ma1")
Investment.updateProfitLoss(2400)
#
User.insertIntoTable("Kanishka", "Jay", 10)
User.insertIntoTable("Kabubakar", "J", 1)
# User.updateRecord("ma", 1)
# look into this
User.deleteRecord("kj1")
User.deleteRecord("ma")
# import time
#
# time.sleep(1)
# # User.deleteRecord("ma")
# User.showTable()
#
# Investment = Investment()
# Investment.deleteTable()
# Investment.createTable()

# # code to show help
# # print(Investment.insertIntoTable.__doc__)
# Investment.setProfile("ma")
# Investment.insertIntoTable(123, 21, 123)
# Investment.insertIntoTable(21, 1, 1)
# Investment.insertIntoTable(31, 1, 1)
# # Investment.insertIntoTable(1000, 21, 20)
# # Investment.insertIntoTable(1, 21, 12)
# # Investment.insertIntoTable(1, 21, 21)
# Investment.setProfile("kj")
# Investment.insertIntoTable(123, 21, 21)
# Investment.insertIntoTable(1, 21, 40)
# User.deleteRecord("ma")

# # User.deleteRecord("ma")
# # User.deleteRecord("ma")
# # Investment.deleteRecord("ma")
#
# # User.deleteRecord("ma")
# # User.deleteRecord("kj")
# # Investment.showTable()
# Investment.updateProfitLoss(12)
# Investment.setProfile("ma")
# User.showTable()
#
# Investment.setProfile("ma")
# Investment.sellAll()
# # Investment.showProfit()
# Investment.sellAll()
# Statement.setProfile("kj")
# Statement.showStatement()


def previousStage(num):
    for i in range(0, num):
        Log.previousStage()


previousStage(15)

