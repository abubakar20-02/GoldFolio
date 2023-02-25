import DBFunctions
import DB_Code

from Investment import Investment
from Log import Log
from Statement import Statement
from User import User

if __name__ == "__main__":
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

    User.insertIntoTable("Muhammad", "Abubakar", 1000)
    User.SelectProfile("ma")
    User.addMoney(1000)
    User.addMoney(5000)
    User.cashout(100)
    User.cashout(500)
    User.cashout(100)
    Investment.setProfile("ma")
    Investment.insertIntoTable(123, 123, 123)
    Investment.sellAll(Rate=10)
    User.ImportFromExcel()
    # User.convertToExcel()
    Investment.ImportFromExcel()
    # Investment.convertToExcel()
    # MoneyLog.convertToExcel()
    MoneyLog.setProfile("ma")
    MoneyLog.dataforgraph()

# when deleting user app crashes
