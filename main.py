import DBFunctions

from Investment import Investment
from Log import Log
from Statement import Statement
from User import User

MoneyLog = Log.Money()

DBFunctions.ClearTables()

User = User()
Investment = Investment()
Statement = Statement()
# start temp db to store commands that are run. so we can backtrack if needed.
Statement.deleteTable()
Statement.createTable()
Investment.deleteTable()
Investment.createTable()
User.deleteTable(False)
User.createTable()


User.insertIntoTable("Muhammad","Abubakar",1000)
Investment.setProfile("ma")
Investment.insertIntoTable(123,123,123)
Investment.sellAll(Rate=10)
User.ImportFromExcel()
# User.convertToExcel()
Investment.ImportFromExcel()
# Investment.convertToExcel()
MoneyLog.convertToExcel()


# when deleting user app crashes
