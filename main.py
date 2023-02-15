from User import User
from Investment import Investment
from ProfitLoss import Statement

# start temp db to store commands that are run. so we can backtrack if needed.
Statement = Statement()
Statement.deleteTable()
Statement.createTable()
Statement.showStatement()

User = User()
User.createTable()
User.insertIntoTable("Muhammad", "Abubakar", 100)
User.insertIntoTable("Kanishka", "Jay", 10)
User.insertIntoTable("Kabubakar", "J", 1)
User.deleteRecord("kj1")
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
# User.deleteRecord("ma")
# Investment.deleteRecord("ma")

# User.deleteRecord("ma")
# User.deleteRecord("kj")
# Investment.showTable()
Investment.updateProfitLoss(12)
Investment.setProfile("ma")
User.showTable()

Investment.setProfile("kj")
Investment.sellAll()
print("------------------")
# Investment.showProfit()
Investment.sellAll()
Statement.setProfile("kj")
Statement.showStatement()
print("------------------")
# Investment.showLoss()
