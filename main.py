import time

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
User.ImportFromExcel()

timer = 1
User.insertIntoTable("Muhammad", "Abubakar", 100)
Investment.ImportFromExcel()
# time.sleep(timer)
# User.insertIntoTable("Hamza", "Rizwan",100)
# time.sleep(timer)
# User.updateRecord("ma", 20)
# time.sleep(timer)
# User.updateRecord("ma", 50)
# time.sleep(timer)
# Investment.setProfile("ma")
# #
# Investment.insertIntoTable(1, 123, 101)
# time.sleep(timer)
# Investment.setProfile("hr")
# Investment.insertIntoTable(2, 123, 98)
# time.sleep(timer)
# Investment.insertIntoTable(3, 3, 50)
# Investment.sellAll(Rate=50)


# a = 10
# while True:
#     a = a + 1
#     time.sleep(timer)
#     Investment.updateProfitLoss(a)


# Investment.setProfile("hr")
# Investment.insertIntoTable(123,123,123)
# Investment.setProfile("ma")
# Investment.sellAll(Rate=50)
# Investment.setProfile("hr")
# time.sleep(timer)
# Investment.sellAll(Rate=20)
# time.sleep(timer)
# # User.deleteRecord("ma")
# time.sleep(timer)
# User.insertIntoTable("Ali", "Baba", 1)
# time.sleep(timer)
#
# Investment.setProfile("ab")
# time.sleep(timer)
#
# Investment.insertIntoTable(1, 1, 1, Date="2020-01-21")
# time.sleep(timer)
# Investment.insertIntoTable(12, 123, 23)
# time.sleep(timer)
# Investment.insertIntoTable(123, 3, 123)
# time.sleep(timer)
#
# Investment.updateProfitLoss(1000)
# Investment.sellAll()
#
# Investment.updateProfitLoss(1.5)
# # Investment.sellAll()
# time.sleep(timer)
#
# # Investment.sellAll()
# time.sleep(timer)
# User.insertIntoTable("m", "s", 90)
# time.sleep(timer)
# User.deleteRecord("ms")
# time.sleep(timer)
#
# # method_name()
# User.insertIntoTable("sa", "as", 100)
# Investment.setProfile("sa")
# Investment.insertIntoTable(1, 1, 23)
# Investment.sellAll()


def previousStage(num):
    for i in range(0, num):
        Log.previousStage()


previousStage(0)

# when deleting user app crashes
