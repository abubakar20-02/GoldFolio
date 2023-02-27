from datetime import datetime

import DBFunctions
import DB_Code

from Investment import Investment
from Log import Log
from Statement import Statement
from User import User


def strToDate(date_string):
    # date_string = "2022-03-05"
    date_format = "%Y-%m-%d"
    date_object = datetime.strptime(date_string, date_format)
    return date_object


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
    Investment.setProfile("ma")
    Investment.ImportFromExcel()
    Investment.sellAll(Rate=180)
    # Investment.insertIntoTable(100,1,100)
    # Investment.insertIntoTable(1000,1,1000)
    # Investment.sellAll(Rate=10)
    # Investment.insertIntoTable(123, 123, 15)
    # Investment.sellAll(Rate=10)
    # User.cashout(2760)
    # User.ImportFromExcel()
    # User.convertToExcel()
    # Investment.sellAll(Rate=10000)
    # Investment.convertToExcel()
    # MoneyLog.convertToExcel()
    MoneyLog.setProfile("ma")
    # MoneyLog.convertToExcel()
    # MoneyLog.dataforgraph(EndDate=strToDate("2023-02-24"))
    Statement.ImportFromExcel()
    Statement.trial1("Gold", Start=strToDate("2020-01-01"), End=strToDate("2025-12-12"))
    # Statement.traverse_all_dates("BoughtFor", Preset="Month")

# when deleting user app crashes
