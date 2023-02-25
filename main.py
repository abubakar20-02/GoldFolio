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

    User.insertIntoTable("Muhammad", "Abubakar", 100000000)
    User.SelectProfile("ma")
    User.addMoney(1000)
    Investment.setProfile("ma")
    # Investment.insertIntoTable(123, 123, 15)
    # Investment.sellAll(Rate=10)
    # User.cashout(2760)
    # User.ImportFromExcel()
    # User.convertToExcel()
    Investment.ImportFromExcel()
    # Investment.convertToExcel()
    # MoneyLog.convertToExcel()
    MoneyLog.setProfile("ma")
    MoneyLog.dataforgraph()
    Investment.traverse_all_dates("BoughtFor")

# when deleting user app crashes
