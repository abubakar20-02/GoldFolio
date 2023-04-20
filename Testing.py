import time
from Database import DBFunctions


class Testing:
    def __init__(self):
        from Database import Investment
        from Database import Log
        from Database import Statement
        from Database import User
        self.MoneyLog = Log.Log.Money()
        self.User = User.User()
        self.Investment = Investment.Investment()
        self.Statement = Statement.Statement()
        self.clearTables()

    def clearTables(self):
        DBFunctions.ClearTables()
        self.Statement.deleteTable()
        self.Investment.deleteTable()
        self.User.deleteTable()

    def TestUndoInsert(self):
        StartingMoney = 1000
        self.User.insertIntoTable("Muhammad", "Abubakar", StartingMoney, "123", "$")
        time.sleep(1)
        self.User.SelectProfile("ma")
        self.Investment.setProfile("ma")
        self.Investment.insertIntoTable(1, 1, 60)
        time.sleep(1)
        DBFunctions.previousStage("ma")
        print(self.User.getMoney())
        if self.User.getMoney() == StartingMoney:
            result = "Pass"
        else:
            result = "Fail"
        print(f"Undo insert: {result}")

    def TestUndoUpdate(self):
        StartingMoney = 1000
        Transaction_ID = "1"
        self.User.insertIntoTable("Muhammad", "Abubakar", StartingMoney, "123", "$")
        time.sleep(1)
        self.User.SelectProfile("ma")
        self.Investment.setProfile("ma")
        self.Investment.insertIntoTable(1, 1, 60, Transaction_ID=Transaction_ID)
        MoneyAfterBuyingInvestment = self.User.getMoney()
        time.sleep(1)
        self.Investment.updateRecord(Transaction_ID, 5, 12)
        time.sleep(1)
        DBFunctions.previousStage("ma")
        print(self.User.getMoney())
        if self.User.getMoney() == MoneyAfterBuyingInvestment and self.Investment.getSUM("Gold") == 1:
            result = "Pass"
        else:
            result = "Fail"
        print(f"Undo update: {result}")

    def TestUndoDelete(self):
        StartingMoney = 1000
        self.User.insertIntoTable("Muhammad", "Abubakar", StartingMoney, "123", "$")
        time.sleep(1)
        self.User.SelectProfile("ma")
        self.Investment.setProfile("ma")
        self.Investment.insertIntoTable(1, 1, 60)
        time.sleep(1)
        self.Investment.insertIntoTable(1, 1, 60)
        time.sleep(1)
        self.Investment.insertIntoTable(1, 1, 60)
        time.sleep(1)
        MoneyAfterBuyingInvestments = self.User.getMoney()
        time.sleep(1)
        self.Investment.sellAll(Rate=70)
        time.sleep(1)
        DBFunctions.previousStage("ma")
        print(self.User.getMoney())
        if self.User.getMoney() == MoneyAfterBuyingInvestments:
            result = "Pass"
        else:
            result = "Fail"
        print(f"Undo delete: {result}")

    # def BuyInvestmentMoreThanMoney(self):
    #     StartingMoney = 1000
    #     self.User.insertIntoTable("Muhammad", "Abubakar", StartingMoney, "123", "$")
    #     time.sleep(1)
    #     self.User.SelectProfile("ma")
    #     self.Investment.setProfile("ma")
    #     self.Investment.insertIntoTable(1, 1, 1100)
    #     time.sleep(1)
    #     print(self.User.getMoney())
    #     if self.User.getMoney() == StartingMoney:
    #         result = "Pass"
    #     else:
    #         result = "Fail"
    #     print(f"Buying investment more than money in hand: {result}")


if __name__ == "__main__":
    Test = Testing()

    Test.TestUndoInsert()

    Test.clearTables()

    Test.TestUndoUpdate()

    Test.clearTables()

    Test.TestUndoDelete()

