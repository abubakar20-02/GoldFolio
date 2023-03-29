import time
from datetime import datetime

from Database import DBFunctions
# when selling indv inv doesnt add money.
# selling one then sell multiple then try to reverse.

# when deleting data sometimes it went to 29 data instead of 33
# start ui and delete in first cycle.

from Database.Investment import Investment
from Database.Log import Log
from Database.Statement import Statement
from Database.User import User
from Database import DBFunctions


# when reversing sell profit there is issue.
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

    User.insertIntoTable("Muhammad", "Abubakar", 1000, "trial")
    User.UpdatePassword("ma","trial2")
    time.sleep(1)
    User.SelectProfile("ma")
    User.addMoney(1000)
    time.sleep(1)
    Investment.setProfile("ma")
    Investment.insertIntoTable(123, 123, 123)
    time.sleep(1)
    Investment.ImportFromExcel()
    time.sleep(1)
    Investment.PDF()
    User.insertIntoTable("Hamza", "Rizwan", 1000, "trial1")
    time.sleep(1)
    User.SelectProfile("hr")
    User.addMoney(100)
    time.sleep(1)
    Investment.setProfile("hr")
    Investment.insertIntoTable(123, 123, 123)
    time.sleep(1)
    Investment.insertIntoTable(123, 123, 123)
    time.sleep(1)
    Investment.insertIntoTable(123, 123, 123)
    time.sleep(1)
    User.SelectProfile("ma")
    User.addMoney(500)
    time.sleep(1)
    Investment.sellAll(Rate=10)
    time.sleep(1)
    Investment.setProfile("ma")
    Investment.sellAll(Rate=10)
    # Investment.sellAll(Rate=180)
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
    # Statement.ImportFromExcel()
    # Statement.trial("Gold", Start=strToDate("2022-01-01"), End=strToDate("2022-12-12"))
    # Statement.traverse_all_dates("BoughtFor", Preset="Month")
    # DBFunctions.previousStage(5)
    # Investment.insertIntoTable(123,123,123,ProfitLoss=123)

# when deleting user app crashes
