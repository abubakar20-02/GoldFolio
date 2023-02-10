from User import User
from Investment import Investment
User = User()
User.deleteTable()
User.createTable()
User.insertIntoTable("Muhammad" , "Abubakar" , 100, 100)
User.insertIntoTable("Kanishka", "Jay", 10, 10)
User.insertIntoTable("Kabubakar", "J" , 1, 1)
User.showTable()

Investment = Investment()
Investment.deleteTable()
Investment.createTable()
Investment.insertIntoTable("1","ma",123,21,123)
Investment.insertIntoTable("2", "ma" , 21,1,1)
Investment.insertIntoTable("3", "ma",1000,21,20)
Investment.insertIntoTable("4","ma",1,21,12)
# Investment.deleteRecord("ma")

# User.deleteRecord("ma")
# User.deleteRecord("kj")
# Investment.showTable()
Investment.showProfitLoss(12)
User.showTable()

